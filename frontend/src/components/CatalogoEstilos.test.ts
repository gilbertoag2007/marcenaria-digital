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
    estilo: id === 1 ? "MULTIUSO" : "GUARDA_ROUPA",
    altura_minima_cm: 100,
    altura_maxima_cm: 240,
    largura_minima_cm: 100,
    largura_maxima_cm: 200,
    profundidade_minima_cm: 40,
    profundidade_maxima_cm: 50,
    ativo: true,
    detalhes: [
      {
        id: 10,
        tipo: "COMPARTIMENTO",
        percentual_ocupacao_vertical: 100,
        percentual_ocupacao_horizontal: 100,
        em_cima_de_id: null,
        embaixo_de_id: null,
        a_direita_de_id: null,
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

    expect(wrapper.findAll("svg.previa")).toHaveLength(2);
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
