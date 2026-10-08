import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from marcenaria_digital_api.entities.exceptions import (
    ConfiguracaoDuplicadaError,
    FalhaPersistenciaError,
)
from marcenaria_digital_api.repositories.json import ConfiguracaoJsonRepository
from marcenaria_digital_api.routes.schemas import ConfiguracaoInput


def test_adiciona_e_recupera_sem_perda_de_dados(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    repositorio = ConfiguracaoJsonRepository(arquivo_configuracoes)
    entidade = ConfiguracaoInput.model_validate(payload_valido).para_entidade()

    repositorio.adicionar(entidade)

    assert repositorio.obter_por_id(entidade.id) == entidade
    persistido = json.loads(arquivo_configuracoes.read_text(encoding="utf-8"))
    assert persistido["versao"] == 1
    assert persistido["configuracoes"][0] == payload_valido
    assert isinstance(persistido["configuracoes"][0]["altura_minima_cm"], float)


def test_nao_duplica_id(arquivo_configuracoes: Path, payload_valido: dict) -> None:
    repositorio = ConfiguracaoJsonRepository(arquivo_configuracoes)
    entidade = ConfiguracaoInput.model_validate(payload_valido).para_entidade()
    repositorio.adicionar(entidade)

    with pytest.raises(ConfiguracaoDuplicadaError):
        repositorio.adicionar(entidade)

    assert len(json.loads(arquivo_configuracoes.read_text())["configuracoes"]) == 1


def test_preserva_original_quando_substituicao_falha(
    arquivo_configuracoes: Path, payload_valido: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    repositorio = ConfiguracaoJsonRepository(arquivo_configuracoes)
    original = arquivo_configuracoes.read_text(encoding="utf-8")

    def falhar_substituicao(_origem: Path, _destino: Path) -> None:
        raise OSError("falha simulada que não pode vazar para a API")

    monkeypatch.setattr(
        "marcenaria_digital_api.repositories.json.configuracao_json_repository.os.replace",
        falhar_substituicao,
    )

    with pytest.raises(FalhaPersistenciaError):
        repositorio.adicionar(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert arquivo_configuracoes.read_text(encoding="utf-8") == original
    json.loads(original)


def test_rejeita_arquivo_invalido(arquivo_configuracoes: Path) -> None:
    arquivo_configuracoes.write_text('{"versao": 2}', encoding="utf-8")
    repositorio = ConfiguracaoJsonRepository(arquivo_configuracoes)

    with pytest.raises(FalhaPersistenciaError):
        repositorio.obter_por_id(1)


def test_gravacoes_concorrentes_nao_perdem_atualizacoes(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    repositorio = ConfiguracaoJsonRepository(arquivo_configuracoes)

    def adicionar(configuracao_id: int) -> None:
        payload = {**payload_valido, "id": configuracao_id}
        repositorio.adicionar(ConfiguracaoInput.model_validate(payload).para_entidade())

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(adicionar, range(1, 21)))

    dados = json.loads(arquivo_configuracoes.read_text(encoding="utf-8"))
    assert {item["id"] for item in dados["configuracoes"]} == set(range(1, 21))
