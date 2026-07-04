"""Repository metadata tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "apprise_notify"


def test_hacs_manifest_names_integration() -> None:
    """Validate the root HACS manifest expected by HACS custom repositories."""
    hacs = json.loads((ROOT / "hacs.json").read_text())

    assert hacs["name"] == "Apprise Notify"
    assert hacs["render_readme"] is True


def test_custom_component_manifest_is_hacs_compatible() -> None:
    """Validate the integration manifest fields required for HACS integrations."""
    manifest_path = ROOT / "custom_components" / DOMAIN / "manifest.json"
    manifest = json.loads(manifest_path.read_text())

    assert manifest["domain"] == DOMAIN
    assert manifest["name"] == "Apprise Notify"
    assert manifest["documentation"].startswith("https://github.com/ikarpovich/")
    assert manifest["issue_tracker"].endswith("/issues")
    assert manifest["codeowners"] == ["@ikarpovich"]
    assert manifest["version"] == "0.0.0"


def test_brand_icon_is_present_for_hacs() -> None:
    """HACS integrations need local brand assets or a brands repository entry."""
    icon = ROOT / "custom_components" / DOMAIN / "brand" / "icon.png"

    assert icon.is_file()
    assert icon.read_bytes().startswith(b"\x89PNG")


def test_only_one_custom_component_is_present() -> None:
    """HACS manages one integration directory per integration repository."""
    components = [path.name for path in (ROOT / "custom_components").iterdir() if path.is_dir()]

    assert components == [DOMAIN]
