"""Write the API contract snapshot: python -m spakr.api.snapshot

The snapshot (tests/api_contract.snapshot) holds API_VERSION and the generated
OpenAPI description. Run this after changing the API and bumping API_VERSION.
"""

import json
from pathlib import Path

from spakr.api import API_VERSION, create_app

SNAPSHOT = Path(__file__).resolve().parents[3] / "tests" / "api_contract.snapshot"


def current_contract() -> dict:
    app = create_app(config={})
    with app.app_context():
        spec = app.extensions["spakr_spec"].spec
    return {"api_version": API_VERSION, "openapi": json.loads(json.dumps(spec))}


def render(contract: dict) -> str:
    return json.dumps(contract, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    SNAPSHOT.write_text(render(current_contract()))
    print(f"wrote {SNAPSHOT}")
