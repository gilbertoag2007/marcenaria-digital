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
    Configuracao,
    DetalheConfiguracao,
)
from marcenaria_digital_api.entities.configuracao.validacao import validar_configuracao
from marcenaria_digital_api.entities.enums import (
    EstiloMovel,
    TipoConfiguracao,
    TipoMovel,
)
from marcenaria_digital_api.entities.exceptions import (
    ConfiguracaoDuplicadaError,
    ConfiguracaoInvalidaError,
    FalhaPersistenciaError,
)


class _DetalheConfiguracaoJson(BaseModel):
    """Representa um detalhe no arquivo JSON versionado."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0, strict=True)
    tipo: TipoConfiguracao
    percentual_ocupacao_vertical: float = Field(gt=0, le=100, strict=True)
    percentual_ocupacao_horizontal: float = Field(gt=0, le=100, strict=True)
    em_cima_de_id: int | None = Field(default=None, gt=0, strict=True)
    embaixo_de_id: int | None = Field(default=None, gt=0, strict=True)
    a_direita_de_id: int | None = Field(default=None, gt=0, strict=True)
    a_esquerda_de_id: int | None = Field(default=None, gt=0, strict=True)

    def para_entidade(self) -> DetalheConfiguracao:
        """Converte o registro persistido em entidade."""
        return DetalheConfiguracao(**self.model_dump())

    @classmethod
    def da_entidade(cls, detalhe: DetalheConfiguracao) -> "_DetalheConfiguracaoJson":
        """Cria um registro persistível a partir de uma entidade."""
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


class _ConfiguracaoJson(BaseModel):
    """Representa uma configuração no arquivo JSON versionado."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0, strict=True)
    tipo: TipoMovel
    estilo: EstiloMovel
    altura_minima_cm: Decimal = Field(gt=0)
    altura_maxima_cm: Decimal = Field(gt=0)
    largura_minima_cm: Decimal = Field(gt=0)
    largura_maxima_cm: Decimal = Field(gt=0)
    profundidade_minima_cm: Decimal = Field(gt=0)
    profundidade_maxima_cm: Decimal = Field(gt=0)
    ativo: bool = Field(strict=True)
    detalhes: list[_DetalheConfiguracaoJson] = Field(min_length=1)

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
        """Serializa medidas decimais como números no arquivo JSON."""
        return float(valor)

    def para_entidade(self) -> Configuracao:
        """Converte o registro persistido em entidade."""
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

    @classmethod
    def da_entidade(cls, configuracao: Configuracao) -> "_ConfiguracaoJson":
        """Cria um registro persistível a partir de uma entidade."""
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
                _DetalheConfiguracaoJson.da_entidade(detalhe)
                for detalhe in configuracao.detalhes
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
