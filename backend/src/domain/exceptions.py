"""Domain exceptions for prl-documenta."""


class PrlError(Exception):
    """Base exception for all domain errors."""


class InvalidExpiryDate(PrlError):
    """Raised when fecha_caducidad is not strictly after fecha_validez."""


class InvalidDocumentFormat(PrlError):
    """Raised when the document format is not in the allowed set."""


class MissingRequiredField(PrlError):
    """Raised when a required field is missing."""


class InvalidDocumentCategory(PrlError):
    """Raised when the document category is not in the allowed set."""


class DocumentNotFound(PrlError):
    """Raised when a document is not found or has been deleted."""


class UserAlreadyExists(PrlError):
    """Email ya registrado."""


class InvalidCredentials(PrlError):
    """Credenciales incorrectas o token inválido/expirado."""


class InactiveUser(PrlError):
    """Usuario con is_active=False."""


class InsufficientPermissions(PrlError):
    """El usuario no tiene permisos para esta operación."""
