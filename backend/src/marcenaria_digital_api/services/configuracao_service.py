from marcenaria_digital_api.entities.configuracao import Configuracao
from marcenaria_digital_api.entities.enums import EstiloMovel
from marcenaria_digital_api.entities.exceptions import ConfiguracaoNaoEncontradaError
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

    def listar_ativas(self) -> list[Configuracao]:
        """Lista as configurações ativas disponíveis no catálogo."""
        return self._repositorio.listar_ativas()

    def obter_ativa_por_id(self, configuracao_id: int) -> Configuracao:
        """Recupera uma configuração ativa ou informa sua indisponibilidade."""
        configuracao = self._repositorio.obter_por_id(configuracao_id)
        if configuracao is None or not configuracao.ativo:
            raise ConfiguracaoNaoEncontradaError(configuracao_id)
        return configuracao

    def listar_estilos_ativos(self) -> list[EstiloMovel]:
        """Lista estilos ativos sem duplicidade e na ordem do catálogo."""
        estilos: list[EstiloMovel] = []
        vistos: set[EstiloMovel] = set()
        for configuracao in self._repositorio.listar_ativas():
            if configuracao.estilo not in vistos:
                vistos.add(configuracao.estilo)
                estilos.append(configuracao.estilo)
        return estilos
