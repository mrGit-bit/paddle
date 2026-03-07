import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_workspace_port_8000_defaults_to_public_visibility():
    settings_path = REPO_ROOT / ".vscode" / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))

    port_attrs = settings.get("remote.portsAttributes", {}).get("8000", {})

    assert port_attrs.get("label") == "Django dev server"
    assert port_attrs.get("protocol") == "http"
    assert port_attrs.get("onAutoForward") == "notify"
    assert port_attrs.get("visibility") == "public"


def test_devcontainer_port_8000_defaults_to_public_visibility():
    devcontainer_path = REPO_ROOT / ".devcontainer" / "devcontainer.json"
    devcontainer = json.loads(devcontainer_path.read_text(encoding="utf-8"))

    assert 8000 in devcontainer.get("forwardPorts", [])

    port_attrs = devcontainer.get("portsAttributes", {}).get("8000", {})

    assert port_attrs.get("label") == "Django dev server"
    assert port_attrs.get("protocol") == "http"
    assert port_attrs.get("onAutoForward") == "notify"
    assert port_attrs.get("visibility") == "public"
