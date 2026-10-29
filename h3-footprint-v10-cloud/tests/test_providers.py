from __future__ import annotations

import io
import json
import os
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import providers


class FakeResponse:
    def __init__(self, body: bytes, status: int = 200, headers: dict[str, str] | None = None):
        self._body = body
        self.status = status
        self.headers = headers or {}
        self.read_limit = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit: int = -1) -> bytes:
        self.read_limit = limit
        return self._body[:limit]


def openai_response(content: str = "H3_PROVIDER_SMOKE_OK", status: int = 200,
                    extra: dict | None = None) -> FakeResponse:
    item = {
        "id": "req-test-123",
        "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7},
    }
    if extra:
        item.update(extra)
    return FakeResponse(
        json.dumps(item).encode(),
        status=status,
        headers={"x-request-id": "req-header-123", "x-ratelimit-remaining-requests": "5",
                 "set-cookie": "not-allowed-to-escape"},
    )


class ProviderAdapterTests(unittest.TestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {
            "NVIDIA_NIM_API_KEY": "SENSITIVE-TEST-KEY-DO-NOT-LOG",
            "TOKENHARBOR_API_KEY": "SENSITIVE-TEST-KEY-DO-NOT-LOG",
        }, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_all_routes_have_explicit_unique_ids_and_key_names(self):
        self.assertEqual(set(providers.ROUTES), {"deepseek", "glm", "mimo"})
        self.assertEqual(providers.ROUTES["deepseek"].key_env, "NVIDIA_NIM_API_KEY")
        self.assertEqual(providers.ROUTES["glm"].key_env, "NVIDIA_NIM_API_KEY")
        self.assertEqual(providers.ROUTES["mimo"].key_env, "TOKENHARBOR_API_KEY")
        self.assertTrue(all(route.api_url.startswith("https://") for route in providers.ROUTES.values()))

    def test_success_sends_openai_compatible_body_and_returns_redacted_metadata(self):
        response = openai_response()
        seen = {}

        def opener(request, timeout):
            seen["url"] = request.full_url
            seen["authorization"] = request.get_header("Authorization")
            seen["timeout"] = timeout
            seen["body"] = json.loads(request.data.decode())
            return response

        result = providers.call_chat("deepseek", "Reply with the token.", max_tokens=24,
                                     timeout=12, opener=opener)
        self.assertEqual(result["http_status"], 200)
        self.assertEqual(result["content"], "H3_PROVIDER_SMOKE_OK")
        self.assertEqual(result["provider_request_id"], "req-test-123")
        self.assertEqual(result["safe_rate_headers"]["x-ratelimit-remaining-requests"], "5")
        self.assertNotIn("set-cookie", result["safe_rate_headers"])
        self.assertEqual(seen["authorization"], "Bearer SENSITIVE-TEST-KEY-DO-NOT-LOG")
        self.assertEqual(seen["body"]["model"], providers.ROUTES["deepseek"].api_model)
        self.assertEqual(seen["body"]["max_tokens"], 24)
        self.assertEqual(seen["body"]["stream"], False)
        self.assertNotIn("SENSITIVE-TEST-KEY-DO-NOT-LOG", json.dumps(result))

    def test_missing_key_fails_closed_without_network_call(self):
        with mock.patch.dict(os.environ, {"NVIDIA_NIM_API_KEY": ""}, clear=False):
            with self.assertRaises(providers.ProviderError) as ctx:
                providers.call_chat("deepseek", "ping", opener=lambda *a, **k: self.fail("network called"))
        self.assertIn("missing environment variable", str(ctx.exception))
        self.assertNotIn("SENSITIVE-TEST-KEY-DO-NOT-LOG", str(ctx.exception))

    def test_unknown_route_and_invalid_parameters_are_rejected_before_network(self):
        opener = lambda *a, **k: self.fail("network called")
        with self.assertRaises(ValueError):
            providers.call_chat("unknown", "ping", opener=opener)
        with self.assertRaises(ValueError):
            providers.call_chat("deepseek", "", opener=opener)
        with self.assertRaises(ValueError):
            providers.call_chat("deepseek", "ping", max_tokens=0, opener=opener)
        with self.assertRaises(ValueError):
            providers.call_chat("deepseek", "ping", temperature=2.1, opener=opener)

    def test_http_error_never_exposes_response_body_or_key(self):
        secret_body = b"private provider error body"
        error = urllib.error.HTTPError(
            "https://example.invalid", 429, "Rate limited",
            {"Retry-After": "30"}, io.BytesIO(secret_body)
        )
        with self.assertRaises(providers.ProviderError) as ctx:
            providers.call_chat("mimo", "ping", opener=lambda *a, **k: (_ for _ in ()).throw(error))
        self.assertEqual(ctx.exception.status, 429)
        self.assertEqual(ctx.exception.retry_after, "30")
        self.assertNotIn("private provider error body", str(ctx.exception))
        self.assertNotIn("SENSITIVE-TEST-KEY-DO-NOT-LOG", str(ctx.exception))

    def test_http_non_success_status_is_redacted(self):
        with self.assertRaises(providers.ProviderError) as ctx:
            providers.call_chat("glm", "ping", opener=lambda *a, **k: openai_response(status=503))
        self.assertEqual(ctx.exception.status, 503)
        self.assertIn("non_success_http_status", str(ctx.exception))

    def test_response_size_limit_is_enforced(self):
        oversized = FakeResponse(b"x" * (providers.MAX_RESPONSE_BYTES + 1))
        with self.assertRaises(providers.ProviderError) as ctx:
            providers.call_chat("deepseek", "ping", opener=lambda *a, **k: oversized)
        self.assertIn("response_too_large", str(ctx.exception))

    def test_invalid_response_shape_is_redacted(self):
        bad = FakeResponse(b'{"error":"private response details"}')
        with self.assertRaises(providers.ProviderError) as ctx:
            providers.call_chat("glm", "ping", opener=lambda *a, **k: bad)
        self.assertIn("invalid_openai_compatible_response", str(ctx.exception))
        self.assertNotIn("private response details", str(ctx.exception))

    def test_network_error_does_not_leak_exception_url_or_message(self):
        def fail(*args, **kwargs):
            raise urllib.error.URLError("private-url-and-secret")
        with self.assertRaises(providers.ProviderError) as ctx:
            providers.call_chat("mimo", "ping", opener=fail)
        self.assertIn("URLError", str(ctx.exception))
        self.assertNotIn("private-url-and-secret", str(ctx.exception))
        self.assertNotIn("SENSITIVE-TEST-KEY-DO-NOT-LOG", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
