"""Client helpers for the Apprise Notify integration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

APPRISE_DATA_KEYS = (
    "type",
    "format",
    "attachment",
    "attach",
    "attachments",
    "tag",
    "tags",
)


class AppriseApiError(RuntimeError):
    """Raised when Apprise API rejects or cannot process a notification."""


@dataclass(frozen=True)
class AppriseApiClient:
    """Small synchronous client for the Apprise API notify endpoint."""

    url: str
    timeout: int = 10

    def notify(self, payload: dict[str, Any]) -> None:
        """Send a notification payload to Apprise API."""
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            self.url,
            data=body,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                response_body = response.read().decode("utf-8")

        except HTTPError as err:
            error_body = err.read().decode("utf-8", errors="replace")
            raise AppriseApiError(
                f"Apprise API returned HTTP {err.code}: {error_body or err.reason}"
            ) from err

        except URLError as err:
            raise AppriseApiError(f"Could not reach Apprise API: {err.reason}") from err

        if not response_body:
            return

        try:
            parsed = json.loads(response_body)
        except json.JSONDecodeError:
            return

        if parsed.get("error"):
            raise AppriseApiError(f"Apprise API returned an error: {parsed['error']}")


def build_payload(
    message: str,
    title: str,
    data: dict[str, Any] | None = None,
    target: list[str] | str | None = None,
) -> dict[str, Any]:
    """Build an Apprise API payload from Home Assistant notify inputs."""
    payload: dict[str, Any] = {
        "body": message,
        "title": title,
    }
    data = data or {}

    for key in APPRISE_DATA_KEYS:
        value = data.get(key)
        if value is not None:
            payload[key] = value

    if target and "tag" not in payload and "tags" not in payload:
        payload["tag"] = target

    return payload
