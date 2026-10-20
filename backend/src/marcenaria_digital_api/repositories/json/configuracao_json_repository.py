import json
import os
import tempfile
import threading
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import ClassVar, Iterator, Literal

if os.name == "nt":
    import msvcrt
else:
    import fcntl

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_serializer

from marcenaria_digital_api.entities.configuracao import (
    AcabamentoExterno,
    CompartimentoConfiguracao,
    Configuracao,
    ConfiguracaoArmario,
    Limites,
    PortaConfiguracao,
)
from marcenaria_digital_api.entities.configuracao.validacao import validar_configuracao
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
from marcenaria_digital_api.entities.exceptions import (
    ConfiguracaoDuplicadaError,
    ConfiguracaoInvalidaError,
    FalhaPersistenciaError,
)


class _LimitesJson(BaseModel):
    """Representa os limites dimensionais no arquivo JSON versionado."""

    model_config = ConfigDict(extra="forbid")

    altura_minima_cm: Decimal = Field(gt=0)
    altura_maxima_cm: Decimal = Field(gt=0)
    largura_minima_cm: Decimal = Field(gt=0)
    largura_maxima_cm: Decimal = Field(gt=0)
    profundidade_minima_cm: Decimal = Field(gt=0)
    profundidade_maxima_cm: Decimal = Field(gt=0)
    espessura_minima_cm: Decimal = Field(gt=0)
    espessura_maxima_cm: Decimal = Field(gt=0)

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
        """Serializa medidas decimais como números no arquivo JSON."""
        return float(valor)

    def para_entidade(self) -> Limites:
        """Converte o registro persistido em objeto de valor."""
        return Limites(**self.model_dump())

    @classmethod
    def da_entidade(cls, limites: Limites) -> "_LimitesJson":
        """Cria um registro persistível a partir do objeto de valor."""
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


class _AcabamentoExternoJson(BaseModel):
    """Representa um acabamento externo no arquivo JSON versionado."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0, strict=True)
    tipo_acabamento: Posicao
    estilo_acabamento: EstiloAcabamento
    extensao_cm: float = Field(gt=0, strict=True)
    espessura: Espessura
    corte_extremidade_1: Corte
    corte_extremidade_2: Corte

    def para_entidade(self) -> AcabamentoExterno:
        """Converte o registro persistido em entidade."""
        return AcabamentoExterno(
            id=self.id,
            posicao=self.tipo_acabamento,
            estilo_acabamento=self.estilo_acabamento,
            extensao_cm=self.extensao_cm,
            espessura=self.espessura,
            corte_extremidade_1=self.corte_extremidade_1,
            corte_extremidade_2=self.corte_extremidade_2,
        )

    @classmethod
    def da_entidade(cls, acabamento: AcabamentoExterno) -> "_AcabamentoExternoJson":
        """Cria um registro persistível a partir de uma entidade."""
        return cls(
            id=acabamento.id,
            tipo_acabamento=acabamento.posicao,
            estilo_acabamento=acabamento.estilo_acabamento,
            extensao_cm=acabamento.extensao_cm,
            espessura=acabamento.espessura,
            corte_extremidade_1=acabamento.corte_extremidade_1,
            corte_extremidade_2=acabamento.corte_extremidade_2,
        )


class _CompartimentoConfiguracaoJson(BaseModel):
    """Representa um compartimento no arquivo JSON versionado."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0, strict=True)
    percentual_ocupacao_vertical: float = Field(gt=0, le=100, strict=True)
    percentual_ocupacao_horizontal: float = Field(gt=0, le=100, strict=True)
    em_cima_de_id: int | None = Field(default=None, gt=0, strict=True)
    embaixo_de_id: int | None = Field(default=None, gt=0, strict=True)
    a_direita_de_id: int | None = Field(default=None, gt=0, strict=True)
    a_esquerda_de_id: int | None = Field(default=None, gt=0, strict=True)

    def para_entidade(self) -> CompartimentoConfiguracao:
        """Converte o registro persistido em entidade de compartimento."""
        return CompartimentoConfiguracao(**self.model_dump())

    @classmethod
    def da_entidade(
        cls, compartimento: CompartimentoConfiguracao
    ) -> "_CompartimentoConfiguracaoJson":
        """Cria um registro persistível a partir de um compartimento."""
        return cls(
            id=compartimento.id,
            percentual_ocupacao_vertical=compartimento.percentual_ocupacao_vertical,
            percentual_ocupacao_horizontal=compartimento.percentual_ocupacao_horizontal,
            em_cima_de_id=compartimento.em_cima_de_id,
            embaixo_de_id=compartimento.embaixo_de_id,
            a_direita_de_id=compartimento.a_direita_de_id,
            a_esquerda_de_id=compartimento.a_esquerda_de_id,
        )


class _PortaConfiguracaoJson(_CompartimentoConfiguracaoJson):
    """Representa uma porta no arquivo JSON versionado."""

    abertura: AberturaPorta

    def para_entidade(self) -> PortaConfiguracao:
        """Converte o registro persistido em entidade de porta."""
        return PortaConfiguracao(**self.model_dump())

    @classmethod
    def da_entidade(cls, porta: PortaConfiguracao) -> "_PortaConfiguracaoJson":
        """Cria um registro persistível a partir de uma porta."""
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


class _ConfiguracaoJson(BaseModel):
    """Representa uma configuração no arquivo JSON versionado."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0, strict=True)
    tipo: TipoMovel
    estilo: EstiloMovel
    limites: _LimitesJson
    ativo: bool = Field(strict=True)
    direcao_vertical: DirecaoVertical
    direcao_horizontal: DirecaoHorizontal
    acabamentos: list[_AcabamentoExternoJson] = Field(default_factory=list)
    compartimentos: list[_CompartimentoConfiguracaoJson] = Field(min_length=1)
    portas: list[_PortaConfiguracaoJson] = Field(default_factory=list)

    def para_entidade(self) -> Configuracao:
        """Converte o registro persistido em entidade."""
        if self.tipo is not TipoMovel.ARMARIO:
            raise ValueError(f"tipo de configuração não suportado: {self.tipo}")
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

    @classmethod
    def da_entidade(cls, configuracao: Configuracao) -> "_ConfiguracaoJson":
        """Cria um registro persistível a partir de uma entidade."""
        if not isinstance(configuracao, ConfiguracaoArmario):
            raise ValueError("somente configurações de armário podem ser persistidas")
        return cls(
            id=configuracao.id,
            tipo=configuracao.tipo,
            estilo=configuracao.estilo_armario,
            limites=_LimitesJson.da_entidade(configuracao.limites),
            ativo=configuracao.ativo,
            direcao_vertical=configuracao.direcao_vertical,
            direcao_horizontal=configuracao.direcao_horizontal,
            acabamentos=[
                _AcabamentoExternoJson.da_entidade(acabamento)
                for acabamento in configuracao.acabamentos
            ],
            compartimentos=[
                _CompartimentoConfiguracaoJson.da_entidade(compartimento)
                for compartimento in configuracao.compartimentos
            ],
            portas=[
                _PortaConfiguracaoJson.da_entidade(porta)
                for porta in configuracao.portas
            ],
        )


class _ArquivoConfiguracoes(BaseModel):
    """Valida a estrutura raiz do arquivo de configurações."""

    model_config = ConfigDict(extra="forbid")

    versao: Literal[1]
    configuracoes: list[_ConfiguracaoJson] = Field(default_factory=list)


class ConfiguracaoJsonRepository:
    """Repositório JSON versionado, com atualização atômica e sincronizada."""

    _locks: ClassVar[dict[Path, threading.RLock]] = {}
    _locks_guard: ClassVar[threading.Lock] = threading.Lock()

    def __init__(self, caminho: str | Path | None = None) -> None:
        """Inicializa o repositório para o caminho informado ou padrão."""
        self.caminho = Path(caminho) if caminho else Path(__file__).with_name("configuracoes.json")
        self.caminho = self.caminho.resolve()
        with self._locks_guard:
            self._lock = self._locks.setdefault(self.caminho, threading.RLock())

    def adicionar(self, configuracao: Configuracao) -> Configuracao:
        """Valida e adiciona uma configuração ao arquivo JSON."""
        validar_configuracao(configuracao)
        with self._lock:
            with self._bloqueio_entre_processos():
                arquivo = self._ler()
                if any(item.id == configuracao.id for item in arquivo.configuracoes):
                    raise ConfiguracaoDuplicadaError(configuracao.id)

                arquivo.configuracoes.append(_ConfiguracaoJson.da_entidade(configuracao))
                self._gravar(arquivo)
        return configuracao

    def obter_por_id(self, configuracao_id: int) -> Configuracao | None:
        """Obtém uma configuração pelo identificador, quando existente."""
        with self._lock:
            with self._bloqueio_entre_processos():
                arquivo = self._ler()
                for item in arquivo.configuracoes:
                    if item.id == configuracao_id:
                        return item.para_entidade()
        return None

    def listar_ativas(self) -> list[Configuracao]:
        """Lista as configurações ativas preservando a ordem do arquivo JSON."""
        with self._lock:
            with self._bloqueio_entre_processos():
                arquivo = self._ler()
                return [
                    item.para_entidade()
                    for item in arquivo.configuracoes
                    if item.ativo
                ]

    @contextmanager
    def _bloqueio_entre_processos(self) -> Iterator[None]:
        """Serializa o ciclo completo de leitura e gravação entre workers."""
        caminho_lock = self.caminho.with_name(f"{self.caminho.name}.lock")
        try:
            caminho_lock.parent.mkdir(parents=True, exist_ok=True)
            with caminho_lock.open("a+b") as arquivo_lock:
                arquivo_lock.seek(0, os.SEEK_END)
                if arquivo_lock.tell() == 0:
                    arquivo_lock.write(b"\0")
                    arquivo_lock.flush()
                arquivo_lock.seek(0)
                if os.name == "nt":
                    msvcrt.locking(arquivo_lock.fileno(), msvcrt.LK_LOCK, 1)
                else:
                    fcntl.flock(arquivo_lock.fileno(), fcntl.LOCK_EX)
                try:
                    yield
                finally:
                    arquivo_lock.seek(0)
                    if os.name == "nt":
                        msvcrt.locking(arquivo_lock.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        fcntl.flock(arquivo_lock.fileno(), fcntl.LOCK_UN)
        except FalhaPersistenciaError:
            raise
        except OSError as erro:
            raise FalhaPersistenciaError(
                "Não foi possível bloquear o arquivo de configurações."
            ) from erro

    def _ler(self) -> _ArquivoConfiguracoes:
        try:
            conteudo = self.caminho.read_text(encoding="utf-8")
            arquivo = _ArquivoConfiguracoes.model_validate_json(conteudo)
            ids: set[int] = set()
            for item in arquivo.configuracoes:
                if item.id in ids:
                    raise ValueError(f"id de configuração duplicado: {item.id}")
                ids.add(item.id)
                validar_configuracao(item.para_entidade())
            return arquivo
        except (OSError, UnicodeError, ValidationError, ValueError, ConfiguracaoInvalidaError) as erro:
            raise FalhaPersistenciaError("Não foi possível ler o arquivo de configurações.") from erro

    def _gravar(self, arquivo: _ArquivoConfiguracoes) -> None:
        temporario: Path | None = None
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
            serializado = json.dumps(
                arquivo.model_dump(mode="json"),
                ensure_ascii=False,
                indent=2,
            ) + "\n"
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                prefix=f".{self.caminho.name}.",
                suffix=".tmp",
                dir=self.caminho.parent,
                delete=False,
            ) as arquivo_temporario:
                temporario = Path(arquivo_temporario.name)
                arquivo_temporario.write(serializado)
                arquivo_temporario.flush()
                os.fsync(arquivo_temporario.fileno())
            os.replace(temporario, self.caminho)
            temporario = None
        except OSError as erro:
            raise FalhaPersistenciaError("Não foi possível gravar o arquivo de configurações.") from erro
        finally:
            if temporario is not None:
                try:
                    temporario.unlink(missing_ok=True)
                except OSError:
                    pass
