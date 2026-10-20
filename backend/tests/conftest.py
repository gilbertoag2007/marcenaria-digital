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
            },
            {
                "id": 2,
                "tipo_acabamento": "INFERIOR",
                "estilo_acabamento": "INTERNO",
                "extensao_cm": 8.0,
                "espessura": "18 mm",
                "corte_extremidade_1": "reto",
                "corte_extremidade_2": "reto",
            },
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
            {
                "id": 20,
                "percentual_ocupacao_vertical": 50.0,
                "percentual_ocupacao_horizontal": 100.0,
                "em_cima_de_id": None,
                "embaixo_de_id": 10,
                "a_direita_de_id": None,
                "a_esquerda_de_id": None,
            },
        ],
        "portas": [
            {
                "id": 30,
                "percentual_ocupacao_vertical": 100.0,
                "percentual_ocupacao_horizontal": 100.0,
                "abertura": "ABERTURA VERTICAL PARA DIREITA",
                "em_cima_de_id": None,
                "embaixo_de_id": None,
                "a_direita_de_id": None,
                "a_esquerda_de_id": None,
            },
        ],
    }
