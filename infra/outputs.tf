# Salidas de la mensajería de documents.

output "queue_url" {
  description = "URL de la cola de Notifications para documents."
  value       = aws_sqs_queue.notifications.url
}

output "queue_arn" {
  description = "ARN de la cola de Notifications para documents."
  value       = aws_sqs_queue.notifications.arn
}

output "dlq_url" {
  description = "URL de la DLQ de Notifications para documents."
  value       = aws_sqs_queue.notifications_dlq.url
}

output "dlq_arn" {
  description = "ARN de la DLQ de Notifications para documents."
  value       = aws_sqs_queue.notifications_dlq.arn
}

output "rule_arn" {
  description = "ARN de la regla documents-to-notifications."
  value       = aws_cloudwatch_event_rule.documents_to_notifications.arn
}
