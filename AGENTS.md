# Instruções para agentes de desenvolvimento

Este arquivo se aplica a todo o repositório. Antes de alterar o projeto, consulte
o `PRD.md` e os arquivos da fase correspondente em `specs/`. Eles são as fontes
de verdade para escopo, regras de negócio e critérios de aceite.

## Estado atual do projeto

- O desenvolvimento é incremental e está atualmente na Fase 1.
- O backend utiliza Python 3.12, FastAPI, Pydantic 2 e pytest.
- Até a Fase 7, as configurações são persistidas no arquivo JSON versionado.
- Não antecipe componentes, persistência ou funcionalidades previstos para fases
  futuras.

## Arquitetura

Preserve a separação definida no PRD:

```text
routes --> services --> repositories
              |              |
              +--> entities <-+
```

- `entities` contém entidades, enums, objetos de valor e exceções do negócio. Não
  deve depender de FastAPI, persistência nem das outras camadas.
- `services` contém os fluxos da aplicação, validações e regras de negócio. Pode
  depender de `entities` e dos contratos definidos em `repositories`, mas não de
  detalhes HTTP nem de tecnologias específicas de persistência.
- `repositories` contém os contratos e as implementações de persistência. Deve
  cuidar exclusivamente da gravação, recuperação e conversão dos dados.
- `routes` trata HTTP, define schemas de entrada e saída, chama os serviços e
  converte resultados e erros em respostas da API. Não coloque regras de negócio
  nas rotas nem acesse repositórios diretamente por elas.
- `main.py` deve criar os repositórios, injetá-los nos serviços e compor a API.
- `config.py` deve centralizar configurações de ambiente e logging. `main.py` e
  `config.py` são módulos de suporte, não camadas adicionais.

## Convenções de código

- Escreva identificadores, mensagens e documentação do domínio em português,
  seguindo o vocabulário já usado no projeto.
- Use anotações de tipo e mantenha as assinaturas explícitas.
- Toda nova classe, função ou método deve possuir uma docstring curta e objetiva
  que descreva sua responsabilidade.
- Use comentários internos somente para explicar decisões ou comportamentos que
  não sejam evidentes pelo próprio código. Evite comentários que apenas repitam
  a implementação.
- Mantenha funções e métodos focados em uma única responsabilidade.
- Preserve os contratos públicos e a compatibilidade com as fases já entregues.
- Não exponha detalhes internos, caminhos, credenciais ou rastros de exceção nas
  respostas da API.

## Persistência JSON

- Preserve a codificação UTF-8 e a estrutura versionada do arquivo.
- Valide os dados antes de gravar.
- Mantenha a gravação atômica para que uma falha não deixe JSON parcial ou
  inválido.
- Nos testes, use arquivos temporários. Não altere o JSON versionado como efeito
  colateral da suíte.

## Testes e critérios de aceite

- Adicione ou atualize testes quando uma mudança alterar comportamento.
- Cubra o fluxo esperado e os erros relevantes, especialmente validação,
  persistência e respostas HTTP.
- Confirme os critérios em `specs/fase-1/` para mudanças da fase atual.
- Execute a suíte completa do backend antes de concluir uma alteração.

## Comandos do backend

Execute os comandos a partir de `backend/`.

Preparação do ambiente no PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
```

Testes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Execução local:

```powershell
.\.venv\Scripts\python.exe -m uvicorn marcenaria_digital_api.main:app --reload
```

## Cuidados ao alterar o repositório

- Faça mudanças pequenas e restritas ao requisito solicitado.
- Preserve alterações existentes que não pertençam à tarefa atual.
- Não adicione dependências sem necessidade concreta e sem registrá-las no
  `pyproject.toml`.
- Atualize a documentação quando comandos, contratos ou decisões arquiteturais
  mudarem.
