from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import provider_smoke
from providers import ProviderError, ROUTES


def successful_response(route_id: str) -> dict:
    route = ROUTES[route_id]
    return {
        "route_id": route_id,
        "original_alias": route.original_alias,
        "provider": route.provider,
        "api_url": route.api_url,
        "api_model": route.api_model,
        "http_status": 200,
        "provider_request_id": "req-test-safe",
        "finish_reason": "stop",
        "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7},
        "safe_rate_headers": {"x-ratelimit-remaining-requests": "5"},
        "elapsed_seconds": 0.01,
        "content": provider_smoke.EXPECTED,
    }


class ProviderSmokeTests(unittest.TestCase):
    def test_missing_token_harbor_key_counts_no_request_and_never_calls_network(self):
        with mock.patch.dict(os.environ, {"TOKENHARBOR_API_KEY": ""}, clear=True):
            with mock.patch("providers.urllib.request.urlopen", side_effect=AssertionError("network must not be called")) as urlopen:
                report = provider_smoke.run(["deepseek", "mimo"], timeout=2.0)
        urlopen.assert_not_called()
        self.assertEqual(report["outcome"], "BLOCKED")
        self.assertEqual(report["route_count"], 2)
        self.assertEqual(report["request_attempt_count"], 0)
        self.assertEqual(report["http_response_count"], 0)
        self.assertTrue(all(item["request_attempted"] is False for item in report["results"]))
        self.assertTrue(all(item["status"] == "BLOCKED" for item in report["results"]))
        self.assertNotIn("TOKENHARBOR_API_KEY=", json.dumps(report))

    def test_missing_nvidia_key_does_not_count_a_request(self):
        with mock.patch.dict(os.environ, {"NVIDIA_NIM_API_KEY": ""}, clear=True):
            with mock.patch("providers.urllib.request.urlopen", side_effect=AssertionError("network must not be called")) as urlopen:
                report = provider_smoke.run(["glm"], timeout=2.0)
        urlopen.assert_not_called()
        self.assertEqual(report["route_count"], 1)
        self.assertEqual(report["request_attempt_count"], 0)
        self.assertEqual(report["results"][0]["request_attempted"], False)
        self.assertEqual(report["results"][0]["http_response_received"], False)

    def test_configured_route_is_counted_as_attempted_even_when_network_fails(self):
        with mock.patch.dict(os.environ, {"TOKENHARBOR_API_KEY": "TEST-SECRET"}, clear=True):
            with mock.patch.object(
                provider_smoke,
                "call_chat",
                side_effect=ProviderError("deepseek", None, "URLError"),
            ):
                report = provider_smoke.run(["deepseek"], timeout=2.0)
        self.assertEqual(report["route_count"], 1)
        self.assertEqual(report["request_attempt_count"], 1)
        self.assertEqual(report["http_response_count"], 0)
        self.assertTrue(report["results"][0]["request_attempted"])
        self.assertFalse(report["results"][0]["http_response_received"])
        self.assertNotIn("TEST-SECRET", json.dumps(report))

    def test_http_failure_distinguishes_attempt_from_received_response(self):
        with mock.patch.dict(os.environ, {"NVIDIA_NIM_API_KEY": "TEST-SECRET"}, clear=True):
            with mock.patch.object(
                provider_smoke,
                "call_chat",
                side_effect=ProviderError("glm", 429, "http_error", "30"),
            ):
                report = provider_smoke.run(["glm"], timeout=2.0)
        self.assertEqual(report["request_attempt_count"], 1)
        self.assertEqual(report["http_response_count"], 1)
        item = report["results"][0]
        self.assertTrue(item["request_attempted"])
        self.assertTrue(item["http_response_received"])
        self.assertEqual(item["http_status"], 429)
        self.assertNotIn("TEST-SECRET", json.dumps(report))

    def test_nonempty_smoke_response_is_redacted_and_counted_once(self):
        with mock.patch.dict(os.environ, {"TOKENHARBOR_API_KEY": "TEST-SECRET"}, clear=True):
            with mock.patch.object(provider_smoke, "call_chat", return_value=successful_response("deepseek")) as call:
                report = provider_smoke.run(["deepseek"], timeout=2.0)
        call.assert_called_once()
        self.assertEqual(report["outcome"], "PASS")
        self.assertEqual(report["route_count"], 1)
        self.assertEqual(report["request_attempt_count"], 1)
        self.assertEqual(report["http_response_count"], 1)
        item = report["results"][0]
        self.assertEqual(item["response_characters"], len(provider_smoke.EXPECTED))
        self.assertEqual(item["exact_token_match"], True)
        self.assertFalse(item["raw_response_stored"])
        self.assertNotIn(provider_smoke.EXPECTED, json.dumps(report))
        self.assertNotIn("TEST-SECRET", json.dumps(report))

    def test_unknown_route_rejected_without_calling_provider(self):
        with mock.patch.object(provider_smoke, "call_chat", side_effect=AssertionError("must not be called")) as call:
            with self.assertRaisesRegex(ValueError, "unknown route"):
                provider_smoke.run(["no-such-route"], timeout=2.0)
        call.assert_not_called()


if __name__ == "__main__":
    unittest.main()
