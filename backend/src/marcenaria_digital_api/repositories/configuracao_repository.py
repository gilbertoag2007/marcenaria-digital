from typing import Protocol

from marcenaria_digital_api.entities.configuracao import Configuracao


class ConfiguracaoRepository(Protocol):
    """Define as operações de persistência de configurações."""

    def adicionar(self, configuracao: Configuracao) -> Configuracao:
        """Persiste e devolve uma configuração."""
        ...

    def obter_por_id(self, configuracao_id: int) -> Configuracao | None:
        """Obtém uma configuração pelo identificador, quando existente."""
        ...

    def listar_ativas(self) -> list[Configuracao]:
        """Lista as configurações ativas na ordem da fonte de dados."""
        ...
