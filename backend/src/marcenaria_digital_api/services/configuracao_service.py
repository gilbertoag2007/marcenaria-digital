from marcenaria_digital_api.entities.configuracao import Configuracao
from marcenaria_digital_api.repositories import ConfiguracaoRepository
from marcenaria_digital_api.services.validacao_service import validar_configuracao


class ConfiguracaoService:
    """Coordena os fluxos relacionados às configurações."""

    def __init__(self, repositorio: ConfiguracaoRepository) -> None:
        self._repositorio = repositorio

    def criar(self, configuracao: Configuracao) -> Configuracao:
        """Valida e persiste uma nova configuração."""
        validar_configuracao(configuracao)
        return self._repositorio.adicionar(configuracao)

    def obter_por_id(self, configuracao_id: int) -> Configuracao | None:
        """Recupera uma configuração pelo identificador."""
        return self._repositorio.obter_por_id(configuracao_id)
