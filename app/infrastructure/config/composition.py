"""Composition root: único lugar donde se cablean dependencias para Depends.

Los routers solo piden casos de uso; aquí se construyen con sus adaptadores.
"""

from functools import lru_cache

from app.application.use_cases.add_history_record import AddMedicalHistoryRecordUseCaseImpl
from app.application.use_cases.export_history_pdf import (
    ExportMedicalHistoryPdfUseCaseImpl,
)
from app.application.use_cases.generate_certificate import (
    GenerateAffiliationCertificateUseCaseImpl,
)
from app.application.use_cases.issue_authorization import IssueAuthorizationUseCaseImpl
from app.application.use_cases.mark_authorization import (
    MarkAuthorizationDeliveredUseCaseImpl,
    MarkAuthorizationDeliveryFailedUseCaseImpl,
)
from app.application.use_cases.mark_certificate import (
    MarkCertificateDeliveredUseCaseImpl,
    MarkCertificateDeliveryFailedUseCaseImpl,
)
from app.application.use_cases.queries import (
    GetAffiliationCertificateUseCaseImpl,
    GetAuthorizationUseCaseImpl,
    ListMedicalHistoryRecordsUseCaseImpl,
)
from app.application.use_cases.update_history_record import (
    UpdateMedicalHistoryRecordUseCaseImpl,
)
from app.infrastructure.config.settings import Settings
from app.infrastructure.messaging.publishers.eventbridge_publisher import (
    EventBridgePublisher,
)
from app.infrastructure.pdf.pdf_generator import StubPdfGenerator
from app.infrastructure.persistence.in_memory_repositories import (
    InMemoryAuthorizationRepository,
    InMemoryCertificateRepository,
    InMemoryMedicalHistoryExportRepository,
    InMemoryMedicalHistoryRecordRepository,
)


def get_db():
    """Sesión SQL por request (una por request, vía Depends).

    TODO: inicializar database.init_database(settings.database_url) al arrancar
    TODO: y retornar la sesión: from app.infrastructure.persistence.database import get_db.
    """
    # TODO: yield from get_db_session() con Depends centralizado aquí.
    raise NotImplementedError


# TODO: providers SqlAlchemy*Repository(session=Depends(get_db)) para prod,
# TODO: manteniendo los InMemory para tests y desarrollo sin BD.
from app.infrastructure.storage.document_storage import S3DocumentStorage
from app.infrastructure.system.clock_ids import RandomIdGenerator, SystemClock


def _clock() -> SystemClock:
    """Reloj del sistema (UTC)."""
    return SystemClock()


def _ids() -> RandomIdGenerator:
    """Generador aleatorio de identificadores."""
    return RandomIdGenerator()


@lru_cache
def get_settings() -> Settings:
    """Retorna los settings (cacheados)."""
    # TODO: validar que EVENT_BUS_NAME corresponda al env (dev/prod).
    return Settings()


# TODO: en producción los repositorios deberían ser singletons compartidos;
# TODO: por ahora se instancian aquí como esqueletos en memoria.


def get_event_publisher() -> EventBridgePublisher:
    """Proveedor del adaptador de publicación."""
    return EventBridgePublisher(get_settings())


def get_issue_authorization_use_case() -> IssueAuthorizationUseCaseImpl:
    """Cablea emitir autorización: repo + publisher + reloj + ids."""
    # TODO: reutilizar instancias singleton en vez de crear cada vez.
    return IssueAuthorizationUseCaseImpl(
        InMemoryAuthorizationRepository(), get_event_publisher(), _clock(), _ids()
    )


def get_generate_certificate_use_case() -> GenerateAffiliationCertificateUseCaseImpl:
    """Cablea generar certificado: repo + publisher + reloj + ids."""
    return GenerateAffiliationCertificateUseCaseImpl(
        InMemoryCertificateRepository(), get_event_publisher(), _clock(), _ids()
    )


def get_add_history_record_use_case() -> AddMedicalHistoryRecordUseCaseImpl:
    """Cablea agregar registro: repo + publisher + reloj + ids."""
    return AddMedicalHistoryRecordUseCaseImpl(
        InMemoryMedicalHistoryRecordRepository(), get_event_publisher(), _clock(), _ids()
    )


def get_update_history_record_use_case() -> UpdateMedicalHistoryRecordUseCaseImpl:
    """Cablea actualizar registro: repo + publisher + reloj."""
    return UpdateMedicalHistoryRecordUseCaseImpl(
        InMemoryMedicalHistoryRecordRepository(), get_event_publisher(), _clock()
    )


def get_export_history_pdf_use_case() -> ExportMedicalHistoryPdfUseCaseImpl:
    """Cablea exportar PDF: repos + pdf + storage + publisher + reloj + ids."""
    return ExportMedicalHistoryPdfUseCaseImpl(
        InMemoryMedicalHistoryRecordRepository(),
        InMemoryMedicalHistoryExportRepository(),
        StubPdfGenerator(),
        S3DocumentStorage(get_settings()),
        get_event_publisher(),
        _clock(),
        _ids(),
    )


def get_mark_authorization_delivered_use_case() -> MarkAuthorizationDeliveredUseCaseImpl:
    """Cablea marcar autorización enviada (sin eventos)."""
    return MarkAuthorizationDeliveredUseCaseImpl(InMemoryAuthorizationRepository())


def get_mark_authorization_failed_use_case() -> MarkAuthorizationDeliveryFailedUseCaseImpl:
    """Cablea marcar autorización fallida (sin eventos)."""
    return MarkAuthorizationDeliveryFailedUseCaseImpl(InMemoryAuthorizationRepository())


def get_mark_certificate_delivered_use_case() -> MarkCertificateDeliveredUseCaseImpl:
    """Cablea marcar certificado enviado (sin eventos)."""
    return MarkCertificateDeliveredUseCaseImpl(InMemoryCertificateRepository())


def get_mark_certificate_failed_use_case() -> MarkCertificateDeliveryFailedUseCaseImpl:
    """Cablea marcar certificado fallido (sin eventos)."""
    return MarkCertificateDeliveryFailedUseCaseImpl(InMemoryCertificateRepository())


def get_authorization_use_case() -> GetAuthorizationUseCaseImpl:
    """Cablea consultar autorización."""
    return GetAuthorizationUseCaseImpl(InMemoryAuthorizationRepository())


def get_certificate_use_case() -> GetAffiliationCertificateUseCaseImpl:
    """Cablea consultar certificado."""
    return GetAffiliationCertificateUseCaseImpl(InMemoryCertificateRepository())


def get_history_records_use_case() -> ListMedicalHistoryRecordsUseCaseImpl:
    """Cablea listar historial."""
    return ListMedicalHistoryRecordsUseCaseImpl(InMemoryMedicalHistoryRecordRepository())


# TODO: eliminar cuando se implementen los routers (nombre antiguo del export).
get_generate_history_pdf_use_case = get_export_history_pdf_use_case
