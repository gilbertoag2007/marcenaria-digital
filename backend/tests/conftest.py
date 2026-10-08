import json
from pathlib import Path

import pytest


@pytest.fixture
def arquivo_configuracoes(tmp_path: Path) -> Path:
    caminho = tmp_path / "configuracoes.json"
    caminho.write_text(
        json.dumps({"versao": 1, "configuracoes": []}, ensure_ascii=False),
        encoding="utf-8",
    )
    return caminho


@pytest.fixture
def payload_valido() -> dict:
    return {
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
