"""Siembra un titular de prueba en profile_snapshots (solo desarrollo local).

Uso: DATABASE_URL=... .venv/bin/python scripts/seed_profile.py [user_id]
El user_id debe coincidir con el claim userId de tu token de prueba.
"""

import os
import sys
from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.infrastructure.persistence.models import ProfileSnapshotModel

DEFAULT_USER_ID = "0192b3c4-7d8e-7f10-a2b3-4c5d6e7f8000"


def main(user_id: str) -> None:
    """Inserta o actualiza el titular de prueba."""
    url = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://kenko:kenko@localhost:5432/kenko_documents"
    )
    engine = create_engine(url)
    snapshot = ProfileSnapshotModel(
        user_id=user_id,
        document_type="CC",
        document_number="1020304050",
        first_name="Maria Fernanda",
        last_name="Gomez Rojas",
        affiliation_start_date=datetime(2020, 3, 1, tzinfo=timezone.utc),
    )
    with Session(engine) as session:
        session.merge(snapshot)
        session.commit()
    print(f"Titular de prueba listo: user_id={user_id}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USER_ID)
