<script setup lang="ts">
import CatalogoEstilos from "./components/CatalogoEstilos.vue";
</script>

<template>
  <div class="aplicacao">
    <header class="barra-superior">
      <a class="identidade" href="#conteudo-principal" aria-label="Marcenaria Digital - início">
        <span class="identidade__simbolo" aria-hidden="true"><i></i><i></i></span>
        <span>Marcenaria Digital</span>
      </a>

      <div class="perfil" aria-label="Perfil atual">
        <span class="perfil__contexto">Minha marcenaria</span>
        <span class="perfil__divisor" aria-hidden="true"></span>
        <span class="perfil__avatar" aria-hidden="true">MD</span>
        <span class="perfil__nome">Administrador</span>
        <svg viewBox="0 0 20 20" aria-hidden="true"><path d="m6 8 4 4 4-4" /></svg>
      </div>
    </header>

    <nav class="navegacao" aria-label="Navegação principal">
      <a class="navegacao__item navegacao__item--ativo" href="#conteudo-principal" aria-current="page">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="16" height="5" rx="1" />
          <rect x="4" y="14" width="7" height="6" rx="1" />
          <rect x="15" y="14" width="5" height="6" rx="1" />
        </svg>
        Configurações
      </a>
      <span class="navegacao__item navegacao__item--indisponivel" aria-disabled="true">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="m12 3 7 4v10l-7 4-7-4V7l7-4Z" />
          <path d="m5 7 7 4 7-4M12 11v10" />
        </svg>
        Móveis
        <small>Em breve</small>
      </span>
    </nav>

    <main id="conteudo-principal" class="conteudo">
      <header class="cabecalho-pagina">
        <p class="breadcrumb">Biblioteca / Configurações</p>
        <h1>Configurações cadastradas</h1>
        <p>Consulte os estilos disponíveis e selecione a configuração que deseja usar.</p>
      </header>
      <CatalogoEstilos />
    </main>

    <footer class="rodape">
      <span>© 2026 Marcenaria Digital</span>
      <span>Feito para dar forma às suas ideias.</span>
    </footer>
  </div>
</template>
