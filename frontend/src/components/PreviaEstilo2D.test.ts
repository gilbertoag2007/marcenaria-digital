import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import type {
  AcabamentoExterno,
  CompartimentoConfiguracao,
} from "../types/configuracao";
import PreviaEstilo2D from "./PreviaEstilo2D.vue";

const acabamentos: AcabamentoExterno[] = [
  {
    id: 1,
    posicao: "SUPERIOR",
    estilo_acabamento: "EXTERNO",
    extensao_cm: 5,
    espessura: "15 mm",
    corte_extremidade_1: "reto",
    corte_extremidade_2: "reto",
  },
  {
    id: 2,
    posicao: "INFERIOR",
    estilo_acabamento: "INTERNO",
    extensao_cm: 5,
    espessura: "15 mm",
    corte_extremidade_1: "reto",
    corte_extremidade_2: "reto",
  },
];

const compartimentos: CompartimentoConfiguracao[] = [
  {
    id: 1,
    percentual_ocupacao_vertical: 50,
    percentual_ocupacao_horizontal: 100,
    em_cima_de_id: null,
    embaixo_de_id: null,
    a_direita_de_id: null,
    a_esquerda_de_id: null,
  },
  {
    id: 2,
    percentual_ocupacao_vertical: 50,
    percentual_ocupacao_horizontal: 100,
    em_cima_de_id: null,
    embaixo_de_id: 1,
    a_direita_de_id: null,
    a_esquerda_de_id: null,
  },
];

describe("PreviaEstilo2D", () => {
  it("mantém visíveis as divisões dos compartimentos sob uma porta externa", () => {
    const wrapper = mount(PreviaEstilo2D, {
      props: { acabamentos: [], compartimentos, descricao: "Prévia interna" },
    });

    expect(wrapper.findAll("rect.compartimento")).toHaveLength(2);
    expect(wrapper.find("rect.porta-externa").exists()).toBe(false);
  });

  it("desenha os acabamentos superiores e inferiores no contorno interno", () => {
    const wrapper = mount(PreviaEstilo2D, {
      props: { acabamentos, compartimentos, descricao: "Prévia interna" },
    });
    const acabamentosDesenhados = wrapper.findAll("rect.acabamento-externo");

    expect(acabamentosDesenhados).toHaveLength(2);
    expect(
      acabamentosDesenhados.map((acabamento) =>
        acabamento.attributes("data-posicao"),
      ),
    ).toEqual(["SUPERIOR", "INFERIOR"]);
    expect(Number(acabamentosDesenhados[0].attributes("y"))).toBe(2);
    expect(Number(acabamentosDesenhados[1].attributes("y"))).toBe(86);
    expect(Number(wrapper.find("rect.compartimento").attributes("y"))).toBe(14);
    expect(Number(wrapper.find("rect.compartimento").attributes("height"))).toBe(36);
  });
});
