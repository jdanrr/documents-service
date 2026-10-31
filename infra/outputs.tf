# Salidas de la mensajería de documents.

output "queue_url" {
  description = "URL de la cola de Documents para eventos de Profile."
  value       = aws_sqs_queue.documents_profile.url
}

output "queue_arn" {
  description = "ARN de la cola de Documents para eventos de Profile."
  value       = aws_sqs_queue.documents_profile.arn
}

output "dlq_url" {
  description = "URL de la DLQ de Documents para eventos de Profile."
  value       = aws_sqs_queue.documents_profile_dlq.url
}

output "dlq_arn" {
  description = "ARN de la DLQ de Documents para eventos de Profile."
  value       = aws_sqs_queue.documents_profile_dlq.arn
}

output "rule_arn" {
  description = "ARN de la regla profile-to-documents."
  value       = aws_cloudwatch_event_rule.profile_to_documents.arn
}

output "bucket_name" {
  description = "Nombre del bucket S3 de PDFs (DOCUMENTS_BUCKET_NAME)."
  value       = aws_s3_bucket.documents_files.id
}

output "bucket_arn" {
  description = "ARN del bucket S3 de PDFs."
  value       = aws_s3_bucket.documents_files.arn
}

output "policy_arn" {
  description = "ARN de la policy de IAM del servicio Documents."
  value       = aws_iam_policy.documents_service.arn
}
