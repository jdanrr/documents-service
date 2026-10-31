# Infra de Documents — kenko.documents (Terraform)

Crea **solo** lo propio de Documents: bucket S3 de PDFs, consumo desde Profile (regla de EventBridge, cola SQS y su DLQ) y la policy de IAM del servicio. El bus `kenko-{env}-bus` es compartido y ya existe; aquí solo se referencia. No toca el código FastAPI/hexagonal.

## Qué crea

- Bucket `kenko-{env}-documents-files`: privado (bloqueo total de acceso público), cifrado SSE-S3 (`AES256`), ACLs desactivadas (`BucketOwnerEnforced`), policy que rechaza peticiones sin TLS, versionado desactivado y limpieza de cargas multipart incompletas a los 7 días. Sin expiración de objetos: la base de datos los referencia.
- Regla `kenko-{env}-profile-to-documents` en el bus compartido (pattern: `source: kenko.profile`, `detail-type` desde la variable `profile_detail_types`, por defecto `["ProfileCreated"]`).
- Cola `kenko-{env}-documents-profile` (target de la regla) con `redrive_policy` a su DLQ (`maxReceiveCount = 3`).
- DLQ `kenko-{env}-documents-profile-dlq`.
- `aws_sqs_queue_policy` mínima: `sqs:SendMessage` solo para `events.amazonaws.com` condicionado al ARN de la regla.
- Sin `input_path`: el mensaje SQS conserva el evento completo (misma convención que `notifications-service`).
- Policy de IAM `kenko-{env}-documents-service` (administrada, **sin adjuntar a ningún rol**): `s3:PutObject`/`s3:GetObject` sobre el bucket, consumo SQS solo de la cola propia y `events:PutEvents` solo sobre el bus compartido.

## Estructura de claves del bucket (la define la aplicación, no Terraform)

```
authorizations/<userId>/<authorizationId>/<timestamp>-<STATUS>.pdf
certificates/<userId>/<certificateId>.pdf
exports/<userId>/<pdfId>.pdf
```

## Variables de entorno de la aplicación (salen de los outputs)

| Variable de entorno    | Output de Terraform |
|---|---|
| `DOCUMENTS_BUCKET_NAME` | `bucket_name` |
| `QUEUE_PROFILE_URL`     | `queue_url` |

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

No ejecutar `apply`/`destroy` sin confirmación explícita (el bus compartido ya debe existir). El `plan` debe mostrar solo recursos nuevos (`+`).

## Tabla evento → regla → cola → DLQ

| Evento (detail-type) | Regla | Cola | DLQ |
|---|---|---|---|
| `ProfileCreated` | `kenko-{env}-profile-to-documents` | `kenko-{env}-documents-profile` | `kenko-{env}-documents-profile-dlq` |
| `ProfileUpdated` (futuro, agregar en `profile_detail_types`) | `kenko-{env}-profile-to-documents` | `kenko-{env}-documents-profile` | `kenko-{env}-documents-profile-dlq` |

## Lo que NO crea este Terraform

- El bus de eventos (ya existe).
- La cola, DLQ y regla de Notifications para los eventos de Documents (`kenko-{env}-notifications-documents` y su regla): las crea Notifications en su propio Terraform, junto con su permiso de lectura sobre este bucket (pendiente de confirmar con ese equipo).
- Roles de IAM ni adjuntos de la policy, objetos dentro del bucket, ni regla para `DocumentsUpdated` (nadie lo consume).
