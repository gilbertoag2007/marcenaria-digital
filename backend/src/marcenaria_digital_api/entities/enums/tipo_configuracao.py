from enum import StrEnum


class TipoConfiguracao(StrEnum):
    """Identifica os tipos de detalhe de uma configuração."""

    COMPARTIMENTO = "COMPARTIMENTO"
    PORTA = "PORTA"
