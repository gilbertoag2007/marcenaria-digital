import type {
  Configuracao,
  ConfiguracaoRespostaApi,
} from "../types/configuracao";

const BASE_API = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

export async function listarConfiguracoesAtivas(): Promise<Configuracao[]> {
  const resposta = await fetch(`${BASE_API}/configuracoes`, {
    headers: { Accept: "application/json" },
  });
  if (!resposta.ok) {
    throw new Error("Falha ao carregar o catálogo de configurações.");
  }
  const configuracoes = (await resposta.json()) as ConfiguracaoRespostaApi[];
  return configuracoes.map(paraConfiguracao);
}

/** Converte os nomes do contrato HTTP para os nomes do domínio frontend. */
function paraConfiguracao(
  resposta: ConfiguracaoRespostaApi,
): Configuracao {
  const { estilo, acabamentos, ...dados } = resposta;
  return {
    ...dados,
    estilo_armario: estilo,
    acabamentos: acabamentos.map(({ tipo_acabamento, ...acabamento }) => ({
      ...acabamento,
      posicao: tipo_acabamento,
    })),
  };
}
