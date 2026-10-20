# Regla profile-to-documents en el bus compartido y su target a la cola SQS.
# Sin input_path: EventBridge entrega el evento completo para conservar
# source y detail-type (misma convención que notifications-service).

resource "aws_cloudwatch_event_rule" "profile_to_documents" {
  name           = local.rule_name
  description    = "Enruta eventos de kenko.profile hacia la cola de Documents."
  event_bus_name = data.aws_cloudwatch_event_bus.shared.name

  event_pattern = jsonencode({
    source      = [var.profile_source]
    detail-type = var.profile_detail_types
  })

  tags = local.common_tags
}

resource "aws_cloudwatch_event_target" "documents_profile_queue" {
  rule           = aws_cloudwatch_event_rule.profile_to_documents.name
  event_bus_name = data.aws_cloudwatch_event_bus.shared.name
  target_id      = "documents-profile-queue"
  arn            = aws_sqs_queue.documents_profile.arn
}
