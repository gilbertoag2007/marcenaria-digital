import { describe, expect, it } from "vitest";

import type {
  CompartimentoConfiguracao,
  PortaConfiguracao,
} from "../types/configuracao";
import { calcularLayoutPortasPrevia, calcularLayoutPrevia } from "./layoutPrevia";

type RelacoesCompartimento = Partial<
  Pick<
    CompartimentoConfiguracao,
    | "em_cima_de_id"
    | "embaixo_de_id"
    | "a_direita_de_id"
    | "a_esquerda_de_id"
  >
>;

/** Cria um compartimento válido para os cenários da prévia. */
function compartimento(
  id: number,
  horizontal: number,
  vertical: number,
  relacoes: RelacoesCompartimento = {},
): CompartimentoConfiguracao {
  return {
    id,
    percentual_ocupacao_horizontal: horizontal,
    percentual_ocupacao_vertical: vertical,
    em_cima_de_id: null,
    embaixo_de_id: null,
    a_direita_de_id: null,
    a_esquerda_de_id: null,
    ...relacoes,
  };
}

describe("calcularLayoutPrevia", () => {
  it("posiciona compartimentos à direita e abaixo de suas referências", () => {
    const resultado = calcularLayoutPrevia([
      compartimento(1, 50, 30),
      compartimento(2, 50, 30, { a_direita_de_id: 1 }),
      compartimento(3, 100, 70, { embaixo_de_id: 1 }),
    ]);
    const porId = new Map(resultado.map((item) => [item.id, item]));

    expect(porId.get(2)!.x).toBeGreaterThan(porId.get(1)!.x);
    expect(porId.get(3)!.y).toBeGreaterThan(porId.get(1)!.y);
  });

  it("normaliza todos os retângulos dentro do viewBox", () => {
    const resultado = calcularLayoutPrevia([
      compartimento(1, 33, 30, { a_esquerda_de_id: 2 }),
      compartimento(2, 33, 30, { a_direita_de_id: 1 }),
    ]);

    for (const item of resultado) {
      expect(item.x).toBeGreaterThanOrEqual(0);
      expect(item.y).toBeGreaterThanOrEqual(0);
      expect(item.x + item.largura).toBeLessThanOrEqual(100);
      expect(item.y + item.altura).toBeLessThanOrEqual(100);
    }
  });

  it("preenche a largura em faixas com quantidades diferentes de compartimentos", () => {
    const resultado = calcularLayoutPrevia([
      compartimento(1, 33.33, 30, { a_esquerda_de_id: 2 }),
      compartimento(2, 33.33, 30, { a_direita_de_id: 1, a_esquerda_de_id: 3 }),
      compartimento(3, 33.33, 30, { a_direita_de_id: 2 }),
      compartimento(4, 20, 70, { embaixo_de_id: 1, a_esquerda_de_id: 5 }),
      compartimento(5, 20, 70, { embaixo_de_id: 1, a_direita_de_id: 4, a_esquerda_de_id: 6 }),
      compartimento(6, 20, 70, { embaixo_de_id: 2, a_direita_de_id: 5, a_esquerda_de_id: 7 }),
      compartimento(7, 20, 70, { embaixo_de_id: 3, a_direita_de_id: 6, a_esquerda_de_id: 8 }),
      compartimento(8, 20, 70, { embaixo_de_id: 3, a_direita_de_id: 7 }),
    ]);

    const faixaSuperior = resultado.filter((item) => item.id <= 3);
    const faixaInferior = resultado.filter((item) => item.id >= 4);

    /** Calcula a extensão horizontal ocupada por uma faixa da prévia. */
    const larguraTotal = (faixa: typeof resultado): number => {
      const esquerda = Math.min(...faixa.map((item) => item.x));
      const direita = Math.max(
        ...faixa.map((item) => item.x + item.largura),
      );
      return direita - esquerda;
    };

    for (const faixa of [faixaSuperior, faixaInferior]) {
      expect(Math.min(...faixa.map((item) => item.x))).toBeCloseTo(0);
      expect(
        Math.max(...faixa.map((item) => item.x + item.largura)),
      ).toBeCloseTo(100);
    }
    expect(larguraTotal(faixaSuperior)).toBeCloseTo(
      larguraTotal(faixaInferior),
    );
  });
});

describe("calcularLayoutPortasPrevia", () => {
  it("representa cada porta uma vez", () => {
    const portaEsquerda: PortaConfiguracao = {
      ...compartimento(2, 50, 100, { a_esquerda_de_id: 3 }),
      abertura: "ABERTURA VERTICAL PARA DIREITA",
    };
    const portaDireita: PortaConfiguracao = {
      ...compartimento(3, 50, 100, { a_direita_de_id: 2 }),
      abertura: "ABERTURA VERTICAL PARA ESQUERDA",
    };

    const resultado = calcularLayoutPortasPrevia([portaEsquerda, portaDireita]);

    expect(resultado).toHaveLength(2);
    expect(resultado[0].id).toBe("2");
    expect(resultado[1].x).toBeCloseTo(50);
  });
});
