from marcenaria_digital_api.entities.configuracao import Configuracao
from marcenaria_digital_api.entities.configuracao.validacao import (
    validar_configuracao as validar_invariantes_configuracao,
)


def validar_configuracao(configuracao: Configuracao) -> None:
    """Valida as regras e relações espaciais de uma configuração."""
    validar_invariantes_configuracao(configuracao)

