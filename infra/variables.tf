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

# Productor que consume Documents (Profile). El source va en variable
# para dejar el pattern legible; los detail-type van en lista aparte.
variable "profile_source" {
  description = "Source de EventBridge del productor Profile."
  type        = string
  default     = "kenko.profile"
}

variable "profile_detail_types" {
  description = "Lista de detail-type de Profile que enruta la regla. Agregar eventos futuros (p. ej. ProfileUpdated) aquí, sin crear otra cola."
  type        = list(string)
  default     = ["ProfileCreated"]
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
