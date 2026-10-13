# Variables de la mensajería de documents. Nombres en inglés, comentarios en español.

variable "project" {
  description = "Nombre del proyecto (prefijo de todos los recursos)."
  type        = string
  default     = "kenko"
}

variable "environment" {
  description = "Entorno de despliegue: dev o prod."
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "environment debe ser \"dev\" o \"prod\"."
  }
}

variable "aws_region" {
  description = "Región AWS donde viven el bus, la regla y las colas."
  type        = string
  default     = "us-east-1"
}

# Parámetros SQS expuestos como variables con valores razonables por defecto.
variable "max_receive_count" {
  description = "Intentos de entrega antes de mover el mensaje a la DLQ."
  type        = number
  default     = 3
}

variable "visibility_timeout_seconds" {
  description = "Tiempo de invisibilidad de la cola principal."
  type        = number
  default     = 30
}

variable "message_retention_seconds" {
  description = "Retención de la cola principal (4 días)."
  type        = number
  default     = 345600
}

variable "dlq_message_retention_seconds" {
  description = "Retención de la DLQ (14 días)."
  type        = number
  default     = 1209600
}
