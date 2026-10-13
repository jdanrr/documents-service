# Infra de mensajería — kenko.documents (Terraform)

Crea **solo** la mensajería de Documents: regla de EventBridge, cola SQS de Notifications y su DLQ. El bus `kenko-{env}-bus` es compartido y lo creó Authentication; aquí solo se referencia. No toca el código FastAPI/hexagonal.

## Qué crea

- Regla `documents-to-notifications` en el bus compartido (pattern: `AuthorizationIssued`, `CertificateGenerated`, `MedicalHistoryPdfGenerated` con `source: kenko.documents`).
- Cola `kenko-{env}-notifications-documents` (target de la regla) con `redrive_policy` a su DLQ (`maxReceiveCount = 3`).
- DLQ `kenko-{env}-notifications-documents-dlq`.
- `aws_sqs_queue_policy` mínima: `sqs:SendMessage` solo para `events.amazonaws.com` condicionado al ARN de la regla.
- `DocumentsUpdated` **no** tiene regla ni cola (auditoría, queda en el bus).

## Cómo ejecutar

```bash
cd documents-service/infra

terraform init
terraform fmt -check -recursive
terraform validate

# Por entorno (plan de lectura, sin aplicar):
terraform plan -var-file=envs/dev.tfvars
terraform plan -var-file=envs/prod.tfvars
```

No ejecutar `apply`/`destroy` sin coordinar con el equipo (el bus compartido ya debe existir).

## Tabla evento → regla → cola → DLQ

| Evento (detail-type) | Regla | Cola | DLQ |
|---|---|---|---|
| `AuthorizationIssued` | `documents-to-notifications` | `kenko-{env}-notifications-documents` | `kenko-{env}-notifications-documents-dlq` |
| `CertificateGenerated` | `documents-to-notifications` | `kenko-{env}-notifications-documents` | `kenko-{env}-notifications-documents-dlq` |
| `MedicalHistoryPdfGenerated` | `documents-to-notifications` | `kenko-{env}-notifications-documents` | `kenko-{env}-notifications-documents-dlq` |
| `DocumentsUpdated` | — (sin regla, auditoría) | — | — |
