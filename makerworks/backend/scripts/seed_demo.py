import secrets

from sqlalchemy.orm import Session

from app.db import engine
from app.models import APIKey, Theme


def main() -> None:
    with Session(engine) as session:
        if not session.query(APIKey).first():
            key = APIKey(name="demo", key=secrets.token_hex(32))
            session.add(key)
        if not session.query(Theme).filter_by(org="demo").first():
            theme = Theme(org="demo", tokens={"primary": "#00ff00"})
            session.add(theme)
        session.commit()
        print("Seeded demo data")


if __name__ == "__main__":
    main()
