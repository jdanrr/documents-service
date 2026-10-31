# Policy administrada del servicio Documents. No se adjunta a ningún rol
# porque aún no se sabe dónde correrá el servicio.

resource "aws_iam_policy" "documents_service" {
  name        = local.policy_name
  description = "Permisos mínimos del servicio Documents: PDFs en S3, cola de Profile y publicación en el bus."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "PdfsBucketAccess"
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject"]
        Resource = "${aws_s3_bucket.documents_files.arn}/*"
      },
      {
        Sid    = "ProfileQueueConsume"
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
        ]
        Resource = aws_sqs_queue.documents_profile.arn
      },
      {
        Sid      = "PublishToBus"
        Effect   = "Allow"
        Action   = "events:PutEvents"
        Resource = data.aws_cloudwatch_event_bus.shared.arn
      },
    ]
  })

  tags = local.common_tags
}
