"""Ejemplo de test de aplicación (caso de uso con fakes en memoria)."""

import pytest

from app.application.use_cases.issue_authorization import IssueAuthorizationUseCaseImpl
from tests.fakes.event_publisher import FakeEventPublisher
from tests.fakes.repositories import InMemoryAuthorizationRepository

pytestmark = pytest.mark.unit


def test_issue_authorization_use_case_wires_ports():
    """Ejemplo trivial que pasa: el caso de uso se cablea con sus puertos."""
    # TODO: ejecutar execute() y verificar repo + evento AuthorizationIssued + DocumentsUpdated.
    use_case = IssueAuthorizationUseCaseImpl(InMemoryAuthorizationRepository(), FakeEventPublisher())
    assert use_case is not None
