# Frontend — Fase 2

Aplicação Vue 3 com TypeScript e Vite para o catálogo visual de configurações.

## Preparação

```powershell
cd frontend
npm install
```

## Execução

Com o backend disponível em `http://127.0.0.1:8000`:

```powershell
npm run dev
```

O catálogo ficará disponível em `http://localhost:5173`.

## Verificação

```powershell
npm run typecheck
npm test
npm run build
```

Defina `VITE_API_BASE_URL` somente quando a API não estiver disponível pelo
proxy local `/api/v1` configurado no Vite.
