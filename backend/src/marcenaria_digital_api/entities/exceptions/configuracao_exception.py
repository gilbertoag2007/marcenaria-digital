from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErroValidacao:
    """Descreve uma inconsistência encontrada em um campo."""

    campo: str
    mensagem: str


class ConfiguracaoInvalidaError(ValueError):
    """Indica que uma configuração viola regras do negócio."""

    def __init__(self, detalhes: list[ErroValidacao]) -> None:
        self.detalhes = detalhes
        super().__init__("A configuração informada é inválida.")


class ConfiguracaoDuplicadaError(ValueError):
    """Indica que já existe uma configuração com o identificador informado."""

    def __init__(self, configuracao_id: int) -> None:
        self.configuracao_id = configuracao_id
        super().__init__(f"Já existe uma configuração com o id {configuracao_id}.")


class FalhaPersistenciaError(RuntimeError):
    """Falha técnica ao ler ou gravar a fonte de dados."""
