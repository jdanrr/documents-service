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
