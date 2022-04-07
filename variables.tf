variable "ami" {
  type        = string
  default     = "ami-0c02fb55956c7d316" # amazon linux 2community image
  description = "AMI code for the Airflow server"
}

variable "instance_type" {
  type        = string
  default     = "t3.large"
  description = "Instance type for the Airflow server"
}

variable "key" {
  type        = string
  default     = "key-pair2"
  description = "AWS SSH Key Pair name"
}

variable "db_password" {
  type        = string
  default     = "joaoluis"
  description = "Password for the PostgreSQL instance"
}
variable "fernet_key" {
  type        = string
  default     = "yt5yQeHsQSpGahuiU6oNh2uI0XeX_-oxrQhdKO5zUkU="
  description = "Key for encrypting data in the database - see Airflow docs"
}
