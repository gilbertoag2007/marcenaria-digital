import { describe, expect, it } from "vitest";

import type { DetalheConfiguracao } from "../types/configuracao";
import { calcularLayoutPrevia } from "./layoutPrevia";

/** Cria um detalhe válido para os cenários de cálculo da prévia. */
function detalhe(
  id: number,
  horizontal: number,
  vertical: number,
  relacoes: Partial<DetalheConfiguracao> = {},
): DetalheConfiguracao {
  return {
    id,
    tipo: "COMPARTIMENTO",
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
  it("posiciona detalhes à direita e abaixo de suas referências", () => {
    const resultado = calcularLayoutPrevia([
      detalhe(1, 50, 30),
      detalhe(2, 50, 30, { a_direita_de_id: 1 }),
      detalhe(3, 100, 70, { embaixo_de_id: 1 }),
    ]);
    const porId = new Map(resultado.map((item) => [item.id, item]));

    expect(porId.get(2)!.x).toBeGreaterThan(porId.get(1)!.x);
    expect(porId.get(3)!.y).toBeGreaterThan(porId.get(1)!.y);
  });

  it("normaliza todos os retângulos dentro do viewBox", () => {
    const resultado = calcularLayoutPrevia([
      detalhe(1, 33, 30, { a_esquerda_de_id: 2 }),
      detalhe(2, 33, 30, { a_direita_de_id: 1 }),
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
      detalhe(1, 33.33, 30, { a_esquerda_de_id: 2 }),
      detalhe(2, 33.33, 30, { a_direita_de_id: 1, a_esquerda_de_id: 3 }),
      detalhe(3, 33.33, 30, { a_direita_de_id: 2 }),
      detalhe(4, 20, 70, { embaixo_de_id: 1, a_esquerda_de_id: 5 }),
      detalhe(5, 20, 70, { embaixo_de_id: 1, a_direita_de_id: 4, a_esquerda_de_id: 6 }),
      detalhe(6, 20, 70, { embaixo_de_id: 2, a_direita_de_id: 5, a_esquerda_de_id: 7 }),
      detalhe(7, 20, 70, { embaixo_de_id: 3, a_direita_de_id: 6, a_esquerda_de_id: 8 }),
      detalhe(8, 20, 70, { embaixo_de_id: 3, a_direita_de_id: 7 }),
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
