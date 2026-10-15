<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { listarConfiguracoesAtivas } from "../services/configuracoesApi";
import type { Configuracao, EstiloMovel } from "../types/configuracao";
import PreviaEstilo2D from "./PreviaEstilo2D.vue";
import PreviaPortas2D from "./PreviaPortas2D.vue";

const ROTULOS_ESTILO: Record<EstiloMovel, string> = {
  MULTIUSO: "Armário multiuso",
  GUARDA_ROUPA: "Guarda-roupa",
  ARMARIO_AEREO: "Armário aéreo",
};

const configuracoes = ref<Configuracao[]>([]);
const configuracaoSelecionadaId = ref<number | null>(null);
const carregando = ref(true);
const mensagemErro = ref<string | null>(null);
const termoBusca = ref("");
const ordem = ref<"original" | "estilo">("original");

const configuracoesAtivas = computed(() =>
  configuracoes.value.filter((configuracao) => configuracao.ativo),
);

const configuracoesVisiveis = computed(() => {
  const termo = termoBusca.value.trim().toLocaleLowerCase("pt-BR");
  const filtradas = configuracoesAtivas.value.filter((configuracao) => {
    const conteudo = `${configuracao.id} ${ROTULOS_ESTILO[configuracao.estilo]} ${configuracao.tipo}`;
    return conteudo.toLocaleLowerCase("pt-BR").includes(termo);
  });

  if (ordem.value === "estilo") {
    return [...filtradas].sort((a, b) =>
      ROTULOS_ESTILO[a.estilo].localeCompare(ROTULOS_ESTILO[b.estilo], "pt-BR"),
    );
  }
  return filtradas;
});

/** Carrega da API as configurações ativas que compõem o catálogo. */
async function carregarCatalogo(): Promise<void> {
  carregando.value = true;
  mensagemErro.value = null;
  try {
    configuracoes.value = await listarConfiguracoesAtivas();
  } catch {
    configuracoes.value = [];
    mensagemErro.value =
      "Não foi possível carregar as configurações. Verifique a conexão e tente novamente.";
  } finally {
    carregando.value = false;
  }
}

/** Mantém no estado transitório somente o identificador da opção escolhida. */
function selecionar(configuracaoId: number): void {
  configuracaoSelecionadaId.value = configuracaoId;
}

/** Formata uma medida do backend segundo a convenção brasileira. */
function formatarMedida(valor: number): string {
  return new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 2 }).format(valor);
}

/** Resume um intervalo dimensional em centímetros. */
function formatarIntervalo(minimo: number, maximo: number): string {
  return `${formatarMedida(minimo)}–${formatarMedida(maximo)} cm`;
}

/** Soma as portas informadas pelos detalhes de uma configuração. */
function contarPortas(configuracao: Configuracao): number {
  return configuracao.detalhes.reduce(
    (total, detalhe) => total + (detalhe.quantidade_portas ?? 0),
    0,
  );
}

/** Conta os compartimentos informados nos detalhes de uma configuração. */
function contarCompartimentos(configuracao: Configuracao): number {
  return configuracao.detalhes.filter(
    (detalhe) => detalhe.tipo === "COMPARTIMENTO",
  ).length;
}

onMounted(carregarCatalogo);
</script>

<template>
  <section class="catalogo" aria-labelledby="titulo-catalogo">
    <div class="catalogo__barra">
      <h2 id="titulo-catalogo">
        Todas as configurações
        <span v-if="!carregando && !mensagemErro">{{ configuracoesAtivas.length }}</span>
      </h2>

      <div v-if="!carregando && !mensagemErro && configuracoesAtivas.length" class="ferramentas">
        <label class="busca">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="6" />
            <path d="m16 16 4 4" />
          </svg>
          <span class="somente-leitor">Buscar configuração</span>
          <input v-model="termoBusca" type="search" placeholder="Buscar configuração..." />
        </label>

        <label class="ordenacao">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M8 6h11M8 12h8M8 18h5M4 4v16" />
          </svg>
          <span class="somente-leitor">Ordenar configurações</span>
          <select v-model="ordem">
            <option value="original">Ordem do catálogo</option>
            <option value="estilo">Nome do estilo</option>
          </select>
        </label>
      </div>
    </div>

    <div v-if="carregando" class="estado" role="status">
      <span class="carregador" aria-hidden="true"></span>
      <strong>Carregando configurações</strong>
      <span>Aguarde enquanto consultamos o catálogo.</span>
    </div>

    <div v-else-if="mensagemErro" class="estado estado--erro" role="alert">
      <span class="estado__icone" aria-hidden="true">!</span>
      <strong>O catálogo não pôde ser carregado.</strong>
      <span>{{ mensagemErro }}</span>
      <button class="botao-secundario" type="button" @click="carregarCatalogo">Tentar novamente</button>
    </div>

    <div v-else-if="configuracoesAtivas.length === 0" class="estado">
      <span class="estado__icone" aria-hidden="true">0</span>
      <strong>Nenhum estilo disponível.</strong>
      <span>Não há configurações ativas no catálogo neste momento.</span>
    </div>

    <template v-else>
      <div class="tabela-wrapper">
        <table>
          <thead>
            <tr>
              <th>Layout Interno</th>
              <th>Layout Externo</th>
              <th>Tipo de móvel</th>
              <th>Estilo</th>
              <th>Faixas dimensionais</th>
              <th>Elementos</th>
              <th>Status</th>
              <th><span class="somente-leitor">Ações</span></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="configuracao in configuracoesVisiveis"
              :key="configuracao.id"
              :class="{ 'linha--selecionada': configuracaoSelecionadaId === configuracao.id }"
            >
              <td data-label="Layout Interno">
                <div class="miniatura">
                  <PreviaEstilo2D
                    :detalhes="configuracao.detalhes"
                    :descricao="`Prévia da configuração ${configuracao.id}: ${ROTULOS_ESTILO[configuracao.estilo]}`"
                  />
                  <span>#{{ configuracao.id }}</span>
                </div>
              </td>
              <td data-label="Layout Externo">
                <div class="miniatura">
                  <PreviaPortas2D
                    :detalhes="configuracao.detalhes"
                    :descricao="`Prévia externa da configuração ${configuracao.id}: ${ROTULOS_ESTILO[configuracao.estilo]}`"
                  />
                </div>
              </td>
              <td data-label="Tipo de móvel">{{ configuracao.tipo }}</td>
              <td data-label="Estilo"><strong class="estilo">{{ ROTULOS_ESTILO[configuracao.estilo] }}</strong></td>
              <td data-label="Faixas dimensionais">
                <dl class="dimensoes">
                  <div>
                    <dt>A</dt>
                    <dd>{{ formatarIntervalo(configuracao.altura_minima_cm, configuracao.altura_maxima_cm) }}</dd>
                  </div>
                  <div>
                    <dt>L</dt>
                    <dd>{{ formatarIntervalo(configuracao.largura_minima_cm, configuracao.largura_maxima_cm) }}</dd>
                  </div>
                  <div>
                    <dt>P</dt>
                    <dd>{{ formatarIntervalo(configuracao.profundidade_minima_cm, configuracao.profundidade_maxima_cm) }}</dd>
                  </div>
                </dl>
              </td>
              <td data-label="Elementos">
                {{ contarCompartimentos(configuracao) }}
                {{ contarCompartimentos(configuracao) === 1 ? "compartimento" : "compartimentos" }}
                <br />
                {{ contarPortas(configuracao) }}
                {{ contarPortas(configuracao) === 1 ? "porta" : "portas" }}
              </td>
              <td data-label="Status"><span class="status"><i aria-hidden="true"></i>Disponível</span></td>
              <td data-label="Ações" class="acoes">
                <button
                  class="botao-selecao"
                  type="button"
                  :aria-pressed="configuracaoSelecionadaId === configuracao.id"
                  :aria-label="`${configuracaoSelecionadaId === configuracao.id ? 'Configuração selecionada' : 'Selecionar configuração'} ${configuracao.id}`"
                  @click="selecionar(configuracao.id)"
                >
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <circle cx="12" cy="12" r="8" />
                    <path v-if="configuracaoSelecionadaId === configuracao.id" d="m8.5 12 2.3 2.3 4.8-5" />
                    <circle v-else cx="12" cy="12" r="2.5" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="configuracoesVisiveis.length === 0" class="sem-resultados" role="status">
          Nenhuma configuração corresponde à busca.
        </div>
      </div>

      <footer class="catalogo__rodape">
        <span>
          Mostrando {{ configuracoesVisiveis.length }} de {{ configuracoesAtivas.length }}
          {{ configuracoesAtivas.length === 1 ? "configuração" : "configurações" }}
        </span>
        <span v-if="configuracaoSelecionadaId !== null" class="selecao-atual">
          Configuração #{{ configuracaoSelecionadaId }} selecionada
        </span>
      </footer>
    </template>
  </section>
</template>
