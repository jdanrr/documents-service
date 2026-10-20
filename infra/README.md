# Infra de mensajería — kenko.documents (Terraform)

Crea **solo** el consumo de Documents desde Profile: regla de EventBridge, cola SQS y su DLQ. El bus `kenko-{env}-bus` es compartido y ya existe; aquí solo se referencia. No toca el código FastAPI/hexagonal.

## Qué crea

- Regla `kenko-{env}-profile-to-documents` en el bus compartido (pattern: `source: kenko.profile`, `detail-type` desde la variable `profile_detail_types`, por defecto `["ProfileCreated"]`).
- Cola `kenko-{env}-documents-profile` (target de la regla) con `redrive_policy` a su DLQ (`maxReceiveCount = 3`).
- DLQ `kenko-{env}-documents-profile-dlq`.
- `aws_sqs_queue_policy` mínima: `sqs:SendMessage` solo para `events.amazonaws.com` condicionado al ARN de la regla.
- Sin `input_path`: el mensaje SQS conserva el evento completo (misma convención que `notifications-service`).

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

No ejecutar `apply`/`destroy` sin confirmación explícita (el bus compartido ya debe existir).

## Tabla evento → regla → cola → DLQ

| Evento (detail-type) | Regla | Cola | DLQ |
|---|---|---|---|
| `ProfileCreated` | `kenko-{env}-profile-to-documents` | `kenko-{env}-documents-profile` | `kenko-{env}-documents-profile-dlq` |
| `ProfileUpdated` (futuro, agregar en `profile_detail_types`) | `kenko-{env}-profile-to-documents` | `kenko-{env}-documents-profile` | `kenko-{env}-documents-profile-dlq` |
