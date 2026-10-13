# Regla documents-to-notifications en el bus compartido y su target a la cola SQS.

resource "aws_cloudwatch_event_rule" "documents_to_notifications" {
  name           = local.rule_name
  description    = "Enruta eventos de kenko.documents hacia la cola de Notifications."
  event_bus_name = data.aws_cloudwatch_event_bus.shared.name

  event_pattern = jsonencode({
    source      = ["kenko.documents"]
    detail-type = ["AuthorizationIssued", "CertificateGenerated", "MedicalHistoryPdfGenerated"]
    # NOTA: DocumentsUpdated NO va en el pattern porque no tiene consumidor
    # operativo por ahora (auditoría; queda publicado en el bus sin regla a SQS).
    # "DocumentsUpdated"
  })

  tags = local.common_tags
}

resource "aws_cloudwatch_event_target" "notifications_queue" {
  rule           = aws_cloudwatch_event_rule.documents_to_notifications.name
  event_bus_name = data.aws_cloudwatch_event_bus.shared.name
  target_id      = "notifications-documents-queue"
  arn            = aws_sqs_queue.notifications.arn
}
