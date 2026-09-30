<div align="center">

# 🪚 Marcenaria Digital

### Do projeto do móvel ao plano de corte, tudo em um só lugar.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-F2A900?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Angular](https://img.shields.io/badge/Frontend-Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)

</div>

> [!IMPORTANT]
> Este projeto está em desenvolvimento. As funcionalidades serão disponibilizadas de forma incremental.

## Sobre o projeto

O **Marcenaria Digital** é uma aplicação para auxiliar no planejamento e na fabricação de móveis sob medida. A partir das dimensões e características informadas, o sistema calculará as peças, os materiais necessários e a melhor distribuição dos cortes em chapas de MDF.

O objetivo é substituir cálculos manuais, reduzir erros e desperdícios e tornar o processo de construção mais simples e visual. O escopo inicial é voltado a **armários de MDF**.

## Funcionalidades planejadas

- Configuração de armários multiuso, guarda-roupas e armários aéreos;
- Cálculo automático de peças, materiais e ferragens;
- Visualização do móvel em 2D e 3D;
- Otimização do plano de corte em chapas de MDF;
- Cadastro e gerenciamento dos projetos;
- Exportação do plano de corte e do manual de montagem em PDF.

## Tecnologias

| Área | Tecnologias planejadas |
|---|---|
| Backend | Python, FastAPI e API REST |
| Frontend | Angular |
| Visualização 3D | Three.js |
| Persistência | JSON e PostgreSQL |
| Infraestrutura | Docker |
| Arquitetura | Clean Architecture |

## Fluxo da aplicação

```text
Configurar o móvel → Validar medidas → Calcular peças e materiais
        → Visualizar em 2D/3D → Otimizar cortes → Exportar documentos
```

## Roadmap

O desenvolvimento foi dividido em entregas progressivas: configurações e catálogo de estilos, cálculo do móvel, resultados e visualizações, plano de corte, persistência em banco de dados e geração de documentos.

Consulte o [PRD](PRD.md) para conhecer os requisitos, as regras de negócio e o roadmap completo do produto.

---

<div align="center">
  Projeto de portfólio criado para unir tecnologia, planejamento e marcenaria. 🪵
</div>
