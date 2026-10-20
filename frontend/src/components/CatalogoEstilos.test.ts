import { flushPromises, mount } from "@vue/test-utils";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { listarConfiguracoesAtivas } from "../services/configuracoesApi";
import type { Configuracao } from "../types/configuracao";
import CatalogoEstilos from "./CatalogoEstilos.vue";

vi.mock("../services/configuracoesApi", () => ({
  listarConfiguracoesAtivas: vi.fn(),
}));

const listarMock = vi.mocked(listarConfiguracoesAtivas);

/** Cria uma configuração válida para os cenários do catálogo. */
function configuracao(id: number): Configuracao {
  return {
    id,
    tipo: "ARMARIO",
    estilo_armario: id === 1 ? "MULTIUSO" : "GUARDA_ROUPA",
    limites: {
      altura_minima_cm: 100,
      altura_maxima_cm: 240,
      largura_minima_cm: 100,
      largura_maxima_cm: 200,
      profundidade_minima_cm: 40,
      profundidade_maxima_cm: 50,
      espessura_minima_cm: 0.6,
      espessura_maxima_cm: 1.8,
    },
    ativo: true,
    direcao_vertical: "cima_baixo",
    direcao_horizontal: "esquerda_direita",
    acabamentos: [
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
        extensao_cm: 8,
        espessura: "18 mm",
        corte_extremidade_1: "reto",
        corte_extremidade_2: "reto",
      },
    ],
    compartimentos: [
      {
        id: 10,
        percentual_ocupacao_vertical: 100,
        percentual_ocupacao_horizontal: 100,
        em_cima_de_id: null,
        embaixo_de_id: null,
        a_direita_de_id: null,
        a_esquerda_de_id: null,
      },
    ],
    portas: [
      {
        id: 20,
        percentual_ocupacao_vertical: 100,
        percentual_ocupacao_horizontal: 50,
        abertura: "ABERTURA VERTICAL PARA DIREITA",
        em_cima_de_id: null,
        embaixo_de_id: null,
        a_direita_de_id: null,
        a_esquerda_de_id: 30,
      },
      {
        id: 30,
        percentual_ocupacao_vertical: 100,
        percentual_ocupacao_horizontal: 50,
        abertura: "ABERTURA VERTICAL PARA ESQUERDA",
        em_cima_de_id: null,
        embaixo_de_id: null,
        a_direita_de_id: 20,
        a_esquerda_de_id: null,
      },
    ],
  };
}

describe("CatalogoEstilos", () => {
  beforeEach(() => {
    listarMock.mockReset();
  });

  it("exibe prévias SVG e mantém uma única seleção", async () => {
    listarMock.mockResolvedValue([configuracao(1), configuracao(2)]);
    const wrapper = mount(CatalogoEstilos);
    await flushPromises();

    expect(wrapper.findAll("svg.previa--interna")).toHaveLength(2);
    expect(wrapper.findAll("svg.previa--externa")).toHaveLength(2);
    expect(wrapper.findAll("rect.porta-externa")).toHaveLength(4);
    expect(wrapper.text()).toContain("Layout Externo");
    expect(wrapper.text()).toContain("0,6–1,8 cm");
    expect(wrapper.findAll("thead th").map((celula) => celula.text())).toEqual([
      "Layout Interno",
      "Layout Externo",
      "Tipo de móvel",
      "Estilo",
      "Limites",
      "Acabamentos",
      "Portas",
      "Compartimentos",
      "Status",
      "Ações",
    ]);

    const celulas = wrapper.find("tbody tr").findAll("td");
    const acabamentosInternos = celulas[0].findAll("rect.acabamento-externo");
    expect(
      acabamentosInternos.map((acabamento) =>
        acabamento.attributes("data-posicao"),
      ),
    ).toEqual(["SUPERIOR", "INFERIOR"]);
    expect(celulas[5].attributes("data-label")).toBe("Acabamentos");
    expect(celulas[5].text()).toBe("2");
    expect(celulas[5].text()).not.toContain("Superior");
    expect(celulas[5].text()).not.toContain("Inferior");
    expect(celulas[6].attributes("data-label")).toBe("Portas");
    expect(celulas[6].text()).toBe("2");
    expect(celulas[7].attributes("data-label")).toBe("Compartimentos");
    expect(celulas[7].text()).toBe("1");

    const botoes = wrapper.findAll("button.botao-selecao");
    await botoes[0].trigger("click");
    expect(botoes[0].attributes("aria-pressed")).toBe("true");
    await botoes[1].trigger("click");
    expect(botoes[0].attributes("aria-pressed")).toBe("false");
    expect(botoes[1].attributes("aria-pressed")).toBe("true");
  });

  it("apresenta o estado vazio", async () => {
    listarMock.mockResolvedValue([]);
    const wrapper = mount(CatalogoEstilos);
    await flushPromises();

    expect(wrapper.text()).toContain("Nenhum estilo disponível");
  });

  it("apresenta erro e permite tentar novamente", async () => {
    listarMock
      .mockRejectedValueOnce(new Error("indisponível"))
      .mockResolvedValueOnce([configuracao(1)]);
    const wrapper = mount(CatalogoEstilos);
    await flushPromises();

    expect(wrapper.get('[role="alert"]').text()).toContain(
      "não pôde ser carregado",
    );
    await wrapper.get("button.botao-secundario").trigger("click");
    await flushPromises();
    expect(wrapper.findAll("button.botao-selecao")).toHaveLength(1);
  });

  it("filtra as configurações usando dados recebidos da API", async () => {
    listarMock.mockResolvedValue([configuracao(1), configuracao(2)]);
    const wrapper = mount(CatalogoEstilos);
    await flushPromises();

    await wrapper.get('input[type="search"]').setValue("guarda");

    expect(wrapper.findAll("tbody tr")).toHaveLength(1);
    expect(wrapper.text()).toContain("Guarda-roupa");
    expect(wrapper.text()).not.toContain("Armário multiuso");
  });
});
