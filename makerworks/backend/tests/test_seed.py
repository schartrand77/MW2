import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from seed_demo import main  # type: ignore
from app.db import engine
from app.models import APIKey
from sqlalchemy.orm import Session


def test_seed_demo_creates_key():
    main()
    with Session(engine) as session:
        assert session.query(APIKey).first() is not None
