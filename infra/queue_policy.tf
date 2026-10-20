# Permiso mínimo: solo EventBridge (esta regla) puede enviar a la cola.

resource "aws_sqs_queue_policy" "documents_profile" {
  queue_url = aws_sqs_queue.documents_profile.url

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowEventBridgeSendMessage"
        Effect    = "Allow"
        Principal = { Service = "events.amazonaws.com" }
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.documents_profile.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_cloudwatch_event_rule.profile_to_documents.arn
          }
        }
      }
    ]
  })
}
