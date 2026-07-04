"""Tests for Apprise API client helpers."""

from __future__ import annotations

from custom_components.apprise_notify.client import build_payload


def test_build_payload_maps_basic_notify_fields() -> None:
    """Build a minimal Apprise API payload from HA notify inputs."""
    payload = build_payload("Door opened", "Home Assistant")

    assert payload == {"body": "Door opened", "title": "Home Assistant"}


def test_build_payload_preserves_rich_apprise_data() -> None:
    """Pass rich Apprise fields through from notify data."""
    payload = build_payload(
        "**Door opened**",
        "Front door",
        data={
            "type": "warning",
            "format": "markdown",
            "attachment": "https://example.test/snapshot.jpg",
            "unused": "ignored",
        },
    )

    assert payload == {
        "body": "**Door opened**",
        "title": "Front door",
        "type": "warning",
        "format": "markdown",
        "attachment": "https://example.test/snapshot.jpg",
    }


def test_build_payload_uses_target_as_tag_when_tag_is_absent() -> None:
    """Map HA notify target to Apprise tag filtering."""
    payload = build_payload("Message", "Title", target=["matrix"])

    assert payload["tag"] == ["matrix"]


def test_build_payload_prefers_explicit_data_tags_over_target() -> None:
    """Do not override explicit Apprise tags with HA targets."""
    payload = build_payload("Message", "Title", data={"tags": "urgent"}, target=["matrix"])

    assert payload["tags"] == "urgent"
    assert "tag" not in payload
