import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import type { DetalheConfiguracao } from "../types/configuracao";
import PreviaEstilo2D from "./PreviaEstilo2D.vue";

const detalhes: DetalheConfiguracao[] = [
  {
    id: 1,
    tipo: "COMPARTIMENTO",
    percentual_ocupacao_vertical: 50,
    percentual_ocupacao_horizontal: 100,
    quantidade_portas: 1,
    abertura_porta: "ABERTURA VERTICAL PARA DIREITA",
    em_cima_de_id: null,
    embaixo_de_id: null,
    a_direita_de_id: null,
    a_esquerda_de_id: null,
  },
  {
    id: 2,
    tipo: "COMPARTIMENTO",
    percentual_ocupacao_vertical: 50,
    percentual_ocupacao_horizontal: 100,
    quantidade_portas: 0,
    abertura_porta: null,
    em_cima_de_id: null,
    embaixo_de_id: 1,
    a_direita_de_id: null,
    a_esquerda_de_id: null,
  },
  {
    id: 3,
    tipo: "PORTA",
    percentual_ocupacao_vertical: 100,
    percentual_ocupacao_horizontal: 100,
    quantidade_portas: null,
    abertura_porta: null,
    em_cima_de_id: null,
    embaixo_de_id: null,
    a_direita_de_id: null,
    a_esquerda_de_id: null,
  },
];

describe("PreviaEstilo2D", () => {
  it("mantém visíveis as divisões dos compartimentos sob uma porta externa", () => {
    const wrapper = mount(PreviaEstilo2D, {
      props: { detalhes, descricao: "Prévia interna" },
    });

    expect(wrapper.findAll("rect.detalhe--compartimento")).toHaveLength(2);
    expect(wrapper.find("rect.detalhe--porta").exists()).toBe(false);
  });
});
