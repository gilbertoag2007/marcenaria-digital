import { afterEach, describe, expect, it, vi } from "vitest";

import { listarConfiguracoesAtivas } from "./configuracoesApi";

describe("listarConfiguracoesAtivas", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("converte os nomes HTTP para os nomes das entidades do domínio", async () => {
    const json = vi.fn().mockResolvedValue([
      {
        id: 1,
        tipo: "ARMARIO",
        estilo: "MULTIUSO",
        limites: {
          altura_minima_cm: 40,
          altura_maxima_cm: 220,
          largura_minima_cm: 30,
          largura_maxima_cm: 180,
          profundidade_minima_cm: 20,
          profundidade_maxima_cm: 80,
          espessura_minima_cm: 0.6,
          espessura_maxima_cm: 1.8,
        },
        ativo: true,
        direcao_vertical: "cima_baixo",
        direcao_horizontal: "esquerda_direita",
        acabamentos: [
          {
            id: 2,
            tipo_acabamento: "SUPERIOR",
            estilo_acabamento: "EXTERNO",
            extensao_cm: 5,
            espessura: "15 mm",
            corte_extremidade_1: "reto",
            corte_extremidade_2: "meia esquadria",
          },
        ],
        compartimentos: [],
        portas: [],
      },
    ]);
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json }),
    );

    const configuracoes = await listarConfiguracoesAtivas();

    expect(configuracoes[0].estilo_armario).toBe("MULTIUSO");
    expect(configuracoes[0].acabamentos[0].posicao).toBe("SUPERIOR");
    expect(configuracoes[0].acabamentos[0]).not.toHaveProperty(
      "tipo_acabamento",
    );
  });

  it("informa falha quando a API responde com erro", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));

    await expect(listarConfiguracoesAtivas()).rejects.toThrow(
      "Falha ao carregar o catálogo de configurações.",
    );
  });
});
