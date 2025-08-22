from pathlib import Path
import json
import sys

# Ensure backend app is on path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app  # type: ignore


def main() -> None:
    openapi = app.openapi()
    root = Path(__file__).resolve().parents[2]
    out = root / "shared" / "openapi.json"
    out.write_text(json.dumps(openapi, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
