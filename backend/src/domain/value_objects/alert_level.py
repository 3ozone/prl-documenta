from enum import Enum


class AlertLevel(str, Enum):
    OK = "ok"
    AVISO = "aviso"
    ALERTA = "alerta"
    ALERTA_CRITICA = "alerta_critica"
    CADUCADA = "caducada"
