"""Integración SQL: round-trip de certificado y snapshot (PostgreSQL real)."""

import os
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain.entities import AffiliationCertificate, ProfileSnapshot
from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models import (
    AffiliationCertificateModel,
    ProfileSnapshotModel,
)
from app.infrastructure.persistence.sqlalchemy_repositories import (
    SqlAlchemyCertificateRepository,
    SqlAlchemyProfileSnapshotRepository,
)

pytestmark = pytest.mark.integration

DATABASE_URL = os.getenv("DATABASE_URL")

requires_db = pytest.mark.skipif(
    DATABASE_URL is None, reason="Requiere DATABASE_URL al PostgreSQL del compose."
)

AFFILIATION_START = datetime(2020, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
ISSUED_AT = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)


@requires_db
async def test_certificate_round_trip():
    """Guardar y leer un certificado conserva foto fija y file_key."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            repo = SqlAlchemyCertificateRepository(session)
            saved = await repo.save(
                AffiliationCertificate(
                    cert_id="cert-int-1",
                    user_id="user-int-1",
                    affiliation_start_date=AFFILIATION_START,
                    issued_at=ISSUED_AT,
                    file_key="certificates/user-int-1/cert-int-1.pdf",
                )
            )
            assert saved.file_key == "certificates/user-int-1/cert-int-1.pdf"
            found = await repo.get_by_id("cert-int-1")
            assert found is not None
            assert found.affiliation_start_date == AFFILIATION_START
            assert found.issued_at == ISSUED_AT
            listed = await repo.list_by_user_id("user-int-1")
            assert [c.cert_id for c in listed] == ["cert-int-1"]
    finally:
        with Session(engine) as session:
            session.query(AffiliationCertificateModel).filter_by(
                user_id="user-int-1"
            ).delete()
            session.commit()
        engine.dispose()


@requires_db
async def test_snapshot_round_trip_and_missing():
    """Guardar y leer un snapshot; usuario ausente retorna None."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            session.merge(
                ProfileSnapshotModel(
                    user_id="user-int-2",
                    document_type="CC",
                    document_number="1020304050",
                    first_name="Maria Fernanda",
                    last_name="Gomez Rojas",
                    affiliation_start_date=AFFILIATION_START,
                )
            )
            session.commit()
            repo = SqlAlchemyProfileSnapshotRepository(session)
            found = await repo.get_by_user_id("user-int-2")
            assert isinstance(found, ProfileSnapshot)
            assert found.full_name == "Maria Fernanda Gomez Rojas"
            assert await repo.get_by_user_id("user-int-inexistente") is None
    finally:
        with Session(engine) as session:
            session.query(ProfileSnapshotModel).filter_by(
                user_id="user-int-2"
            ).delete()
            session.commit()
        engine.dispose()
