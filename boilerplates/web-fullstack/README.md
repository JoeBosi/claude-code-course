# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Boilerplate agentico per web app full-stack: Next.js 16 · React 19 · TypeScript 7 ·
Supabase Postgres · Drizzle · Tailwind 4.

## Cosa contiene, oltre al codice

| File | A cosa serve |
| --- | --- |
| `CLAUDE.md` | Convenzioni e regole che Claude legge a ogni sessione |
| `.claude/settings.json` | Permessi e hook |
| `.claude/hooks/protect.sh` | Blocca le modifiche a migrazioni, `.env` e lockfile |
| `.claude/hooks/lint-and-typecheck.sh` | Formatta e riporta lint e type error dopo ogni modifica |
| `.claude/commands/review.md` | `/review` — revisione della diff, solo correttezza e sicurezza |
| `.claude/commands/ship.md` | `/ship` — verifica, commit, push e apertura PR |
| `.claude/skills/frontend/` | Convenzioni React e Server Action |
| `.claude/agents/reviewer.md` | Subagent di revisione, sola lettura, con memoria |
| `.mcp.json` | Server MCP Supabase e Vercel |
| `PLAN.md` / `STATE.md` | Piano corrente e stato di avanzamento |

## Avvio

```bash
./init.sh "nome-progetto" "Descrizione del progetto"
npm install
cp .env.example .env.local   # e riempilo
npm run dev
```

Serve `jq` per gli hook.

## Da personalizzare

- `CLAUDE.md` — le sezioni **Regole non negoziabili** e **Trappole**: quelle di default
  valgono per Supabase + Drizzle, cambiale se cambi stack
- `.mcp.json` — togli i server che non usi
- `.claude/settings.json` — la `deny` list riflette scelte di questo boilerplate

## Da lasciare com'è

- La struttura `app/` vs `features/`
- Gli hook: sono la rete di sicurezza, non un accessorio
- Il formato di `/review` e `/ship`
