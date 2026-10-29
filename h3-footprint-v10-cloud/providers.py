"""Direct, key-based API adapters for the H3 cloud prototype.

No model output is executed here. Provider responses are treated as plain text.
This module exists to smoke-test alternate serving routes before any predeclared
model-generation work is considered. It is not permission to generate candidates.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Callable

MAX_RESPONSE_BYTES = 2_000_000


@dataclass(frozen=True)
class Route:
    route_id: str
    original_alias: str
    provider: str
    api_url: str
    api_model: str
    key_env: str


ROUTES: dict[str, Route] = {
    "deepseek": Route(
        route_id="deepseek",
        original_alias="opencode/deepseek-v4.1-flash-free",
        provider="token-harbor",
        api_url="https://tokenharbor.ai/v1/chat/completions",
        api_model="deepseek-v4.1-flash:free",
        key_env="TOKENHARBOR_API_KEY",
    ),
    "glm": Route(
        route_id="glm",
        original_alias="opencode/glm-5.3-flash-free",
        provider="nvidia-nim",
        api_url="https://integrate.api.nvidia.com/v1/chat/completions",
        api_model="z-ai/glm-5.3-flash",
        key_env="NVIDIA_NIM_API_KEY",
    ),
    "mimo": Route(
        route_id="mimo",
        original_alias="opencode/mimo-v2.6-flash-free",
        provider="token-harbor",
        api_url="https://tokenharbor.ai/v1/chat/completions",
        api_model="mimo-v2.6-flash:free",
        key_env="TOKENHARBOR_API_KEY",
    ),
}

SAFE_HEADER_NAMES = (
    "x-request-id",
    "request-id",
    "x-ratelimit-limit-requests",
    "x-ratelimit-remaining-requests",
    "x-ratelimit-limit-tokens",
    "x-ratelimit-remaining-tokens",
    "retry-after",
)


class ProviderError(RuntimeError):
    """Redacted provider failure; never contains credentials or raw response bodies."""

    def __init__(
        self,
        route_id: str,
        status: int | None,
        category: str,
        retry_after: str | None = None,
        *,
        request_attempted: bool | None = None,
        http_response_received: bool | None = None,
    ):
        self.route_id = route_id
        self.status = status
        self.category = category
        self.retry_after = retry_after
        self.request_attempted = (status is not None) if request_attempted is None else request_attempted
        self.http_response_received = (status is not None) if http_response_received is None else http_response_received
        status_text = "network" if status is None else str(status)
        suffix = f", retry_after={retry_after}" if retry_after else ""
        super().__init__(f"{route_id}: {category} (HTTP {status_text}{suffix})")


def _safe_headers(headers: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in SAFE_HEADER_NAMES:
        value = headers.get(name) if headers is not None else None
        if value is not None:
            result[name] = str(value)[:128]
    return result


def call_chat(
    route_id: str,
    prompt: str,
    *,
    max_tokens: int = 64,
    temperature: float = 0.0,
    timeout: float = 90.0,
    opener: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Call one explicitly selected route; credentials never enter return values."""
    if route_id not in ROUTES:
        raise ValueError(f"unknown route_id: {route_id}")
    route = ROUTES[route_id]
    api_key = os.environ.get(route.key_env, "").strip()
    if not api_key:
        raise ProviderError(
            route_id, None, f"missing environment variable {route.key_env}",
            request_attempted=False, http_response_received=False,
        )
    if not prompt or not isinstance(prompt, str):
        raise ValueError("prompt must be a non-empty string")
    if not 1 <= max_tokens <= 4096:
        raise ValueError("max_tokens must be between 1 and 4096")
    if not 0.0 <= temperature <= 2.0:
        raise ValueError("temperature must be between 0 and 2")

    payload = {
        "model": route.api_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    request = urllib.request.Request(
        route.api_url,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "h3-footprint-v10-provider-smoke/1",
        },
        method="POST",
    )
    open_url = opener or urllib.request.urlopen
    started = time.monotonic()
    try:
        with open_url(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            headers = _safe_headers(response.headers)
            status = int(response.status)
    except urllib.error.HTTPError as exc:
        raise ProviderError(
            route_id, int(exc.code), "http_error",
            exc.headers.get("Retry-After") if exc.headers else None,
            request_attempted=True, http_response_received=True,
        ) from None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # Do not surface URLs with credentials, full exception strings, or bodies.
        raise ProviderError(
            route_id, None, type(exc).__name__,
            request_attempted=True, http_response_received=False,
        ) from None

    if status < 200 or status >= 300:
        raise ProviderError(
            route_id, status, "non_success_http_status",
            headers.get("retry-after"),
            request_attempted=True, http_response_received=True,
        )
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ProviderError(
            route_id, status, "response_too_large",
            request_attempted=True, http_response_received=True,
        )
    try:
        envelope = json.loads(raw.decode("utf-8"))
        content = envelope["choices"][0]["message"]["content"]
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError):
        raise ProviderError(
            route_id, status, "invalid_openai_compatible_response",
            request_attempted=True, http_response_received=True,
        ) from None
    if not isinstance(content, str):
        raise ProviderError(
            route_id, status, "response_content_not_text",
            request_attempted=True, http_response_received=True,
        )

    return {
        "route_id": route.route_id,
        "original_alias": route.original_alias,
        "provider": route.provider,
        "api_url": route.api_url,
        "api_model": route.api_model,
        "http_status": status,
        "request_attempted": True,
        "http_response_received": True,
        "provider_request_id": str(envelope.get("id", ""))[:200] or None,
        "finish_reason": str(envelope.get("choices", [{}])[0].get("finish_reason", ""))[:80] or None,
        "usage": envelope.get("usage") if isinstance(envelope.get("usage"), dict) else None,
        "safe_rate_headers": headers,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "content": content,
    }
