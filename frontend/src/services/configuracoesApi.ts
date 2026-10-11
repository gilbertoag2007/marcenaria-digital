import type { Configuracao } from "../types/configuracao";

const BASE_API = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

export async function listarConfiguracoesAtivas(): Promise<Configuracao[]> {
  const resposta = await fetch(`${BASE_API}/configuracoes`, {
    headers: { Accept: "application/json" },
  });
  if (!resposta.ok) {
    throw new Error("Falha ao carregar o catálogo de configurações.");
  }
  return (await resposta.json()) as Configuracao[];
}
