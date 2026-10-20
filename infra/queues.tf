# Cola SQS de Documents para eventos de Profile y su DLQ, con redrive_policy hacia la DLQ.

resource "aws_sqs_queue" "documents_profile_dlq" {
  name                      = local.dlq_name
  message_retention_seconds = var.dlq_message_retention_seconds
  sqs_managed_sse_enabled   = true

  tags = local.common_tags
}

resource "aws_sqs_queue" "documents_profile" {
  name                       = local.queue_name
  visibility_timeout_seconds = var.visibility_timeout_seconds
  message_retention_seconds  = var.message_retention_seconds
  sqs_managed_sse_enabled    = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.documents_profile_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })

  tags = local.common_tags
}
