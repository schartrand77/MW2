from sqlalchemy import create_engine, inspect

from app.models import Base


def test_models_create():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    insp = inspect(engine)
    tables = set(insp.get_table_names())
    # Spot check a few tables
    assert {"users", "products", "orders"}.issubset(tables)
