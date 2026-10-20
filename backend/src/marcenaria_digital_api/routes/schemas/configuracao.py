from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from marcenaria_digital_api.entities.configuracao import (
    AcabamentoExterno,
    CompartimentoConfiguracao,
    Configuracao,
    ConfiguracaoArmario,
    Limites,
    PortaConfiguracao,
)
from marcenaria_digital_api.entities.enums import (
    AberturaPorta,
    Corte,
    DirecaoHorizontal,
    DirecaoVertical,
    Espessura,
    EstiloAcabamento,
    EstiloMovel,
    Posicao,
    TipoMovel,
)


class LimitesInput(BaseModel):
    """Valida os limites dimensionais de uma configuração."""

    model_config = ConfigDict(extra="forbid")

    altura_minima_cm: Decimal = Field(gt=0, description="Altura mínima, em centímetros.")
    altura_maxima_cm: Decimal = Field(gt=0, description="Altura máxima, em centímetros.")
    largura_minima_cm: Decimal = Field(gt=0, description="Largura mínima, em centímetros.")
    largura_maxima_cm: Decimal = Field(gt=0, description="Largura máxima, em centímetros.")
    profundidade_minima_cm: Decimal = Field(
        gt=0, description="Profundidade mínima, em centímetros."
    )
    profundidade_maxima_cm: Decimal = Field(
        gt=0, description="Profundidade máxima, em centímetros."
    )
    espessura_minima_cm: Decimal = Field(
        gt=0, description="Espessura mínima, em centímetros."
    )
    espessura_maxima_cm: Decimal = Field(
        gt=0, description="Espessura máxima, em centímetros."
    )

    def para_entidade(self) -> Limites:
        """Converte o schema em objeto de valor de limites."""
        return Limites(**self.model_dump())


class AcabamentoExternoInput(BaseModel):
    """Valida os dados de entrada de um acabamento externo."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(
        gt=0,
        strict=True,
        description="Identificador positivo e único do acabamento na configuração.",
        examples=[1],
    )
    tipo_acabamento: Posicao = Field(
        description="Posição do móvel que recebe o acabamento.",
        examples=["SUPERIOR"],
    )
    estilo_acabamento: EstiloAcabamento = Field(
        description="Estilo de instalação do acabamento.",
        examples=["EXTERNO"],
    )
    extensao_cm: float = Field(
        gt=0,
        strict=True,
        description=(
            "Extensão do acabamento em centímetros, interpretada como largura "
            "ou altura conforme a posição."
        ),
        examples=[5.0],
    )
    espessura: Espessura = Field(
        description="Espessura do material do acabamento.",
        examples=["15 mm"],
    )
    corte_extremidade_1: Corte = Field(
        description="Tipo de corte na primeira extremidade do acabamento.",
        examples=["reto"],
    )
    corte_extremidade_2: Corte = Field(
        description="Tipo de corte na segunda extremidade do acabamento.",
        examples=["reto"],
    )

    def para_entidade(self) -> AcabamentoExterno:
        """Converte o schema em entidade de acabamento externo."""
        return AcabamentoExterno(
            id=self.id,
            posicao=self.tipo_acabamento,
            estilo_acabamento=self.estilo_acabamento,
            extensao_cm=self.extensao_cm,
            espessura=self.espessura,
            corte_extremidade_1=self.corte_extremidade_1,
            corte_extremidade_2=self.corte_extremidade_2,
        )


class CompartimentoConfiguracaoInput(BaseModel):
    """Valida os dados de entrada de um compartimento da configuração."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "id": 10,
                    "percentual_ocupacao_vertical": 50.0,
                    "percentual_ocupacao_horizontal": 100.0,
                    "em_cima_de_id": 20,
                    "embaixo_de_id": None,
                    "a_direita_de_id": None,
                    "a_esquerda_de_id": None,
                }
            ]
        },
    )

    id: int = Field(
        gt=0,
        strict=True,
        description="Identificador positivo e único do compartimento na configuração.",
        examples=[10],
    )
    percentual_ocupacao_vertical: float = Field(
        gt=0,
        le=100,
        strict=True,
        description=(
            "Percentual da dimensão vertical da configuração ocupado pelo "
            "compartimento, maior que 0 e menor ou igual a 100."
        ),
        examples=[50.0],
    )
    percentual_ocupacao_horizontal: float = Field(
        gt=0,
        le=100,
        strict=True,
        description=(
            "Percentual da dimensão horizontal da configuração ocupado pelo "
            "compartimento, maior que 0 e menor ou igual a 100."
        ),
        examples=[100.0],
    )
    em_cima_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do compartimento abaixo deste no eixo vertical, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[20],
    )
    embaixo_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do compartimento acima deste no eixo vertical, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[10],
    )
    a_direita_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do compartimento localizado à esquerda deste, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[30],
    )
    a_esquerda_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do compartimento localizado à direita deste, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[40],
    )

    def para_entidade(self) -> CompartimentoConfiguracao:
        """Converte o schema em entidade de compartimento."""
        return CompartimentoConfiguracao(**self.model_dump())


class PortaConfiguracaoInput(CompartimentoConfiguracaoInput):
    """Valida os dados de entrada de uma porta da configuração."""

    abertura: AberturaPorta = Field(
        description="Direção de abertura da porta.",
        examples=["ABERTURA VERTICAL PARA DIREITA"],
    )

    def para_entidade(self) -> PortaConfiguracao:
        """Converte o schema em entidade de porta."""
        return PortaConfiguracao(**self.model_dump())


class ConfiguracaoInput(BaseModel):
    """Valida os dados de entrada de uma configuração."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "tipo": "ARMARIO",
                    "estilo": "MULTIUSO",
                    "limites": {
                        "altura_minima_cm": 40.5,
                        "altura_maxima_cm": 220.5,
                        "largura_minima_cm": 30.5,
                        "largura_maxima_cm": 180.5,
                        "profundidade_minima_cm": 20.5,
                        "profundidade_maxima_cm": 80.5,
                        "espessura_minima_cm": 0.6,
                        "espessura_maxima_cm": 1.8,
                    },
                    "ativo": True,
                    "direcao_vertical": "cima_baixo",
                    "direcao_horizontal": "esquerda_direita",
                    "acabamentos": [
                        {
                            "id": 1,
                            "tipo_acabamento": "SUPERIOR",
                            "estilo_acabamento": "EXTERNO",
                            "extensao_cm": 5.0,
                            "espessura": "15 mm",
                            "corte_extremidade_1": "reto",
                            "corte_extremidade_2": "reto",
                        }
                    ],
                    "compartimentos": [
                        {
                            "id": 10,
                            "percentual_ocupacao_vertical": 50.0,
                            "percentual_ocupacao_horizontal": 100.0,
                            "em_cima_de_id": 20,
                            "embaixo_de_id": None,
                            "a_direita_de_id": None,
                            "a_esquerda_de_id": None,
                        },
                    ],
                    "portas": [
                        {
                            "id": 20,
                            "percentual_ocupacao_vertical": 50.0,
                            "percentual_ocupacao_horizontal": 100.0,
                            "abertura": "ABERTURA VERTICAL PARA DIREITA",
                            "em_cima_de_id": None,
                            "embaixo_de_id": 10,
                            "a_direita_de_id": None,
                            "a_esquerda_de_id": None,
                        },
                    ],
                }
            ]
        },
    )

    id: int = Field(
        gt=0,
        strict=True,
        description="Identificador positivo e único da configuração no catálogo.",
        examples=[1],
    )
    tipo: Literal[TipoMovel.ARMARIO] = Field(
        description="Tipo de móvel ao qual a configuração se aplica.",
        examples=["ARMARIO"],
    )
    estilo: EstiloMovel = Field(
        description="Estilo de armário definido pela configuração.",
        examples=["MULTIUSO"],
    )
    limites: LimitesInput = Field(
        description="Limites dimensionais permitidos para o móvel.",
    )
    ativo: bool = Field(
        strict=True,
        description="Indica se a configuração está ativa para utilização.",
        examples=[True],
    )
    direcao_vertical: DirecaoVertical = Field(
        description="Direção vertical de organização dos compartimentos.",
        examples=["cima_baixo"],
    )
    direcao_horizontal: DirecaoHorizontal = Field(
        description="Direção horizontal de organização dos compartimentos.",
        examples=["esquerda_direita"],
    )
    acabamentos: list[AcabamentoExternoInput] = Field(
        default_factory=list,
        description=(
            "Acabamentos externos previstos pela configuração; uma lista vazia "
            "ou a omissão do campo indica que não há acabamento superior nem inferior."
        ),
    )
    compartimentos: list[CompartimentoConfiguracaoInput] = Field(
        min_length=1,
        description=(
            "Compartimentos que compõem a configuração e definem seus elementos, "
            "percentuais de ocupação e relações espaciais."
        ),
    )
    portas: list[PortaConfiguracaoInput] = Field(
        default_factory=list,
        description="Portas previstas pela configuração.",
    )

    def para_entidade(self) -> ConfiguracaoArmario:
        """Converte o schema em entidade de configuração de armário."""
        return ConfiguracaoArmario(
            id=self.id,
            limites=self.limites.para_entidade(),
            ativo=self.ativo,
            direcao_vertical=self.direcao_vertical,
            direcao_horizontal=self.direcao_horizontal,
            estilo_armario=self.estilo,
            acabamentos=[
                acabamento.para_entidade() for acabamento in self.acabamentos
            ],
            compartimentos=[
                compartimento.para_entidade()
                for compartimento in self.compartimentos
            ],
            portas=[porta.para_entidade() for porta in self.portas],
        )


class AcabamentoExternoOutput(BaseModel):
    """Representa um acabamento externo na resposta da API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    tipo_acabamento: Posicao
    estilo_acabamento: EstiloAcabamento
    extensao_cm: float
    espessura: Espessura
    corte_extremidade_1: Corte
    corte_extremidade_2: Corte

    @classmethod
    def da_entidade(cls, acabamento: AcabamentoExterno) -> "AcabamentoExternoOutput":
        """Cria o schema de saída a partir de um acabamento externo."""
        return cls(
            id=acabamento.id,
            tipo_acabamento=acabamento.posicao,
            estilo_acabamento=acabamento.estilo_acabamento,
            extensao_cm=acabamento.extensao_cm,
            espessura=acabamento.espessura,
            corte_extremidade_1=acabamento.corte_extremidade_1,
            corte_extremidade_2=acabamento.corte_extremidade_2,
        )


class LimitesOutput(BaseModel):
    """Representa os limites dimensionais na resposta da API."""

    model_config = ConfigDict(extra="forbid")

    altura_minima_cm: Decimal
    altura_maxima_cm: Decimal
    largura_minima_cm: Decimal
    largura_maxima_cm: Decimal
    profundidade_minima_cm: Decimal
    profundidade_maxima_cm: Decimal
    espessura_minima_cm: Decimal
    espessura_maxima_cm: Decimal

    @field_serializer(
        "altura_minima_cm",
        "altura_maxima_cm",
        "largura_minima_cm",
        "largura_maxima_cm",
        "profundidade_minima_cm",
        "profundidade_maxima_cm",
        "espessura_minima_cm",
        "espessura_maxima_cm",
        when_used="json",
    )
    def serializar_medida_decimal(self, valor: Decimal) -> float:
        """Serializa medidas decimais como números no contrato JSON."""
        return float(valor)

    @classmethod
    def da_entidade(cls, limites: Limites) -> "LimitesOutput":
        """Cria o schema de saída a partir do objeto de valor."""
        return cls(
            altura_minima_cm=limites.altura_minima_cm,
            altura_maxima_cm=limites.altura_maxima_cm,
            largura_minima_cm=limites.largura_minima_cm,
            largura_maxima_cm=limites.largura_maxima_cm,
            profundidade_minima_cm=limites.profundidade_minima_cm,
            profundidade_maxima_cm=limites.profundidade_maxima_cm,
            espessura_minima_cm=limites.espessura_minima_cm,
            espessura_maxima_cm=limites.espessura_maxima_cm,
        )


class CompartimentoConfiguracaoOutput(BaseModel):
    """Representa um compartimento da configuração na resposta da API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    percentual_ocupacao_vertical: float
    percentual_ocupacao_horizontal: float
    em_cima_de_id: int | None = None
    embaixo_de_id: int | None = None
    a_direita_de_id: int | None = None
    a_esquerda_de_id: int | None = None

    @classmethod
    def da_entidade(
        cls, compartimento: CompartimentoConfiguracao
    ) -> "CompartimentoConfiguracaoOutput":
        """Cria o schema de saída a partir de uma entidade de compartimento."""
        return cls(
            id=compartimento.id,
            percentual_ocupacao_vertical=compartimento.percentual_ocupacao_vertical,
            percentual_ocupacao_horizontal=compartimento.percentual_ocupacao_horizontal,
            em_cima_de_id=compartimento.em_cima_de_id,
            embaixo_de_id=compartimento.embaixo_de_id,
            a_direita_de_id=compartimento.a_direita_de_id,
            a_esquerda_de_id=compartimento.a_esquerda_de_id,
        )


class PortaConfiguracaoOutput(CompartimentoConfiguracaoOutput):
    """Representa uma porta da configuração na resposta da API."""

    abertura: AberturaPorta

    @classmethod
    def da_entidade(cls, porta: PortaConfiguracao) -> "PortaConfiguracaoOutput":
        """Cria o schema de saída a partir de uma entidade de porta."""
        return cls(
            id=porta.id,
            percentual_ocupacao_vertical=porta.percentual_ocupacao_vertical,
            percentual_ocupacao_horizontal=porta.percentual_ocupacao_horizontal,
            abertura=porta.abertura,
            em_cima_de_id=porta.em_cima_de_id,
            embaixo_de_id=porta.embaixo_de_id,
            a_direita_de_id=porta.a_direita_de_id,
            a_esquerda_de_id=porta.a_esquerda_de_id,
        )


class ConfiguracaoOutput(BaseModel):
    """Representa uma configuração na resposta da API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    tipo: TipoMovel
    estilo: EstiloMovel
    limites: LimitesOutput
    ativo: bool
    direcao_vertical: DirecaoVertical
    direcao_horizontal: DirecaoHorizontal
    acabamentos: list[AcabamentoExternoOutput]
    compartimentos: list[CompartimentoConfiguracaoOutput]
    portas: list[PortaConfiguracaoOutput]

    @classmethod
    def da_entidade(
        cls, configuracao: ConfiguracaoArmario
    ) -> "ConfiguracaoOutput":
        """Cria o schema de saída a partir de uma configuração de armário."""
        return cls(
            id=configuracao.id,
            tipo=configuracao.tipo,
            estilo=configuracao.estilo_armario,
            limites=LimitesOutput.da_entidade(configuracao.limites),
            ativo=configuracao.ativo,
            direcao_vertical=configuracao.direcao_vertical,
            direcao_horizontal=configuracao.direcao_horizontal,
            acabamentos=[
                AcabamentoExternoOutput.da_entidade(acabamento)
                for acabamento in configuracao.acabamentos
            ],
            compartimentos=[
                CompartimentoConfiguracaoOutput.da_entidade(compartimento)
                for compartimento in configuracao.compartimentos
            ],
            portas=[
                PortaConfiguracaoOutput.da_entidade(porta)
                for porta in configuracao.portas
            ],
        )
