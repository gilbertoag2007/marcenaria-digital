from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from marcenaria_digital_api.entities.configuracao import (
    Configuracao,
    DetalheConfiguracao,
)
from marcenaria_digital_api.entities.enums import (
    EstiloMovel,
    TipoConfiguracao,
    TipoMovel,
)


class DetalheConfiguracaoInput(BaseModel):
    """Valida os dados de entrada de um detalhe de configuração."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "id": 10,
                    "tipo": "COMPARTIMENTO",
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
        description="Identificador positivo e único do detalhe dentro da configuração.",
        examples=[10],
    )
    tipo: TipoConfiguracao = Field(
        description="Tipo de elemento representado pelo detalhe.",
        examples=["COMPARTIMENTO"],
    )
    percentual_ocupacao_vertical: float = Field(
        gt=0,
        le=100,
        strict=True,
        description=(
            "Percentual da dimensão vertical da configuração ocupado pelo "
            "detalhe, maior que 0 e menor ou igual a 100."
        ),
        examples=[50.0],
    )
    percentual_ocupacao_horizontal: float = Field(
        gt=0,
        le=100,
        strict=True,
        description=(
            "Percentual da dimensão horizontal da configuração ocupado pelo "
            "detalhe, maior que 0 e menor ou igual a 100."
        ),
        examples=[100.0],
    )
    em_cima_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do detalhe abaixo deste no eixo vertical, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[20],
    )
    embaixo_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do detalhe acima deste no eixo vertical, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[10],
    )
    a_direita_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do detalhe localizado à esquerda deste, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[30],
    )
    a_esquerda_de_id: int | None = Field(
        default=None,
        gt=0,
        strict=True,
        description=(
            "Identificador do detalhe localizado à direita deste, ou nulo quando "
            "a relação não se aplica."
        ),
        examples=[40],
    )

    def para_entidade(self) -> DetalheConfiguracao:
        """Converte o schema em entidade de detalhe."""
        return DetalheConfiguracao(**self.model_dump())


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
                    "altura_minima_cm": 40.5,
                    "altura_maxima_cm": 220.5,
                    "largura_minima_cm": 30.5,
                    "largura_maxima_cm": 180.5,
                    "profundidade_minima_cm": 20.5,
                    "profundidade_maxima_cm": 80.5,
                    "ativo": True,
                    "detalhes": [
                        {
                            "id": 10,
                            "tipo": "COMPARTIMENTO",
                            "percentual_ocupacao_vertical": 50.0,
                            "percentual_ocupacao_horizontal": 100.0,
                            "em_cima_de_id": 20,
                            "embaixo_de_id": None,
                            "a_direita_de_id": None,
                            "a_esquerda_de_id": None,
                        },
                        {
                            "id": 20,
                            "tipo": "PORTA",
                            "percentual_ocupacao_vertical": 50.0,
                            "percentual_ocupacao_horizontal": 100.0,
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
    tipo: TipoMovel = Field(
        description="Tipo de móvel ao qual a configuração se aplica.",
        examples=["ARMARIO"],
    )
    estilo: EstiloMovel = Field(
        description="Estilo de armário definido pela configuração.",
        examples=["MULTIUSO"],
    )
    altura_minima_cm: Decimal = Field(
        gt=0,
        description="Altura mínima permitida para o móvel, em centímetros.",
        examples=[40.5],
    )
    altura_maxima_cm: Decimal = Field(
        gt=0,
        description="Altura máxima permitida para o móvel, em centímetros.",
        examples=[220.5],
    )
    largura_minima_cm: Decimal = Field(
        gt=0,
        description="Largura mínima permitida para o móvel, em centímetros.",
        examples=[30.5],
    )
    largura_maxima_cm: Decimal = Field(
        gt=0,
        description="Largura máxima permitida para o móvel, em centímetros.",
        examples=[180.5],
    )
    profundidade_minima_cm: Decimal = Field(
        gt=0,
        description="Profundidade mínima permitida para o móvel, em centímetros.",
        examples=[20.5],
    )
    profundidade_maxima_cm: Decimal = Field(
        gt=0,
        description="Profundidade máxima permitida para o móvel, em centímetros.",
        examples=[80.5],
    )
    ativo: bool = Field(
        strict=True,
        description="Indica se a configuração está ativa para utilização.",
        examples=[True],
    )
    detalhes: list[DetalheConfiguracaoInput] = Field(
        min_length=1,
        description=(
            "Detalhes que compõem a configuração e definem seus elementos, "
            "percentuais de ocupação e relações espaciais."
        ),
    )

    def para_entidade(self) -> Configuracao:
        """Converte o schema em entidade de configuração."""
        return Configuracao(
            id=self.id,
            tipo=self.tipo,
            estilo=self.estilo,
            altura_minima_cm=self.altura_minima_cm,
            altura_maxima_cm=self.altura_maxima_cm,
            largura_minima_cm=self.largura_minima_cm,
            largura_maxima_cm=self.largura_maxima_cm,
            profundidade_minima_cm=self.profundidade_minima_cm,
            profundidade_maxima_cm=self.profundidade_maxima_cm,
            ativo=self.ativo,
            detalhes=[detalhe.para_entidade() for detalhe in self.detalhes],
        )


class DetalheConfiguracaoOutput(BaseModel):
    """Representa um detalhe de configuração na resposta da API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    tipo: TipoConfiguracao
    percentual_ocupacao_vertical: float
    percentual_ocupacao_horizontal: float
    em_cima_de_id: int | None = None
    embaixo_de_id: int | None = None
    a_direita_de_id: int | None = None
    a_esquerda_de_id: int | None = None

    @classmethod
    def da_entidade(cls, detalhe: DetalheConfiguracao) -> "DetalheConfiguracaoOutput":
        """Cria o schema de saída a partir de uma entidade de detalhe."""
        return cls(
            id=detalhe.id,
            tipo=detalhe.tipo,
            percentual_ocupacao_vertical=detalhe.percentual_ocupacao_vertical,
            percentual_ocupacao_horizontal=detalhe.percentual_ocupacao_horizontal,
            em_cima_de_id=detalhe.em_cima_de_id,
            embaixo_de_id=detalhe.embaixo_de_id,
            a_direita_de_id=detalhe.a_direita_de_id,
            a_esquerda_de_id=detalhe.a_esquerda_de_id,
        )


class ConfiguracaoOutput(BaseModel):
    """Representa uma configuração na resposta da API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    tipo: TipoMovel
    estilo: EstiloMovel
    altura_minima_cm: Decimal
    altura_maxima_cm: Decimal
    largura_minima_cm: Decimal
    largura_maxima_cm: Decimal
    profundidade_minima_cm: Decimal
    profundidade_maxima_cm: Decimal
    ativo: bool
    detalhes: list[DetalheConfiguracaoOutput]

    @field_serializer(
        "altura_minima_cm",
        "altura_maxima_cm",
        "largura_minima_cm",
        "largura_maxima_cm",
        "profundidade_minima_cm",
        "profundidade_maxima_cm",
        when_used="json",
    )
    def serializar_medida_decimal(self, valor: Decimal) -> float:
        """Serializa medidas decimais como números no contrato JSON."""
        return float(valor)

    @classmethod
    def da_entidade(cls, configuracao: Configuracao) -> "ConfiguracaoOutput":
        """Cria o schema de saída a partir de uma configuração."""
        return cls(
            id=configuracao.id,
            tipo=configuracao.tipo,
            estilo=configuracao.estilo,
            altura_minima_cm=configuracao.altura_minima_cm,
            altura_maxima_cm=configuracao.altura_maxima_cm,
            largura_minima_cm=configuracao.largura_minima_cm,
            largura_maxima_cm=configuracao.largura_maxima_cm,
            profundidade_minima_cm=configuracao.profundidade_minima_cm,
            profundidade_maxima_cm=configuracao.profundidade_maxima_cm,
            ativo=configuracao.ativo,
            detalhes=[
                DetalheConfiguracaoOutput.da_entidade(detalhe)
                for detalhe in configuracao.detalhes
            ],
        )
