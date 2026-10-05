# Backend — Fase 1

## Preparação

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
```

## Execução

```powershell
.\.venv\Scripts\python.exe -m uvicorn marcenaria_digital_api.main:app --reload
```

A documentação OpenAPI ficará disponível em `http://127.0.0.1:8000/docs`.

O caminho do arquivo de configurações pode ser sobrescrito pela variável de
ambiente `MARCENARIA_CONFIGURACOES_JSON_PATH`.

## Arquitetura

O backend utiliza Arquitetura em Camadas com o padrão
Route-Service-Repository:

```text
routes --> services --> repositories
              |              |
              +--> entities <-+
```

- `routes`: define os endpoints e schemas HTTP, chama os serviços e converte
  resultados e erros em respostas da API.
- `services`: coordena os fluxos da aplicação, as validações e as regras de
  negócio.
- `repositories`: define os contratos e implementa a persistência e recuperação
  dos dados. Na Fase 1, utiliza o arquivo JSON versionado.
- `entities`: contém entidades, enums, objetos de valor e exceções do negócio,
  sem depender das demais camadas.

As rotas não devem conter regras de negócio nem acessar repositórios diretamente.
Os repositórios são criados e injetados nos serviços pelo ponto de entrada
`marcenaria_digital_api.main`.

Estrutura principal:

```text
src/marcenaria_digital_api/
├── entities/
├── repositories/
├── routes/
├── services/
├── config.py
└── main.py
```

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest
```
