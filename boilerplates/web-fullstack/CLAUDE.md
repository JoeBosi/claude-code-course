# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

Next.js 16 (App Router) · React 19 · TypeScript 7 · Supabase Postgres · Drizzle · Tailwind 4.

## Comandi

- `npm run dev` — dev server
- `npm test` — Vitest. Lancia il singolo file, non la suite intera
- `npm run test:e2e` — Playwright
- `npm run typecheck` — **obbligatorio prima di ogni commit**
- `npm run lint` — ESLint + Prettier
- `npm run db:generate` — genera la migrazione dopo aver modificato `src/db/schema.ts`
- `npm run db:migrate` — applica le migrazioni

## Struttura

| Se stai scrivendo… | Va in |
| --- | --- |
| Routing e layout | `src/app/` — **solo routing**, nessuna logica di business |
| Logica di prodotto | `src/features/<capacita>/` con `actions.ts`, `queries.ts`, `schema.ts` |
| Componenti presentazionali | `src/components/` |
| Schema del database | `src/db/schema.ts` — l'unica definizione |
| Lettura di variabili d'ambiente | `src/lib/env.ts` — l'unico posto |

Le cartelle di route del framework cambiano a ogni major; `features/` no. Quando cerchi la
fatturazione, apri `features/billing/`.

## Regole non negoziabili

- **Ogni tabella ha una policy RLS.** Una tabella senza RLS è un incidente di sicurezza, non
  un TODO. Se aggiungi una tabella, aggiungi la policy nella stessa migrazione
- Server Component di default. `"use client"` solo quando servono davvero stato o effetti
- Ogni Server Action valida l'input con lo schema Zod di `schema.ts` **prima** di toccare il database
- Mai usare la service role key fuori da `src/app/api/webhooks/`
- Le migrazioni applicate non si modificano: se lo schema cambia, si crea una migrazione nuova
- Le migrazioni si **generano** con `db:generate`, non si scrivono a mano

## Cosa NON fare senza discuterne

- Introdurre un ORM diverso, o query SQL a mano fuori da `src/db/`
- Aggiungere uno state manager globale lato client: prima verifica se serve davvero
- Spostare logica dentro `src/app/`

## Trappole di questo progetto

- Supabase Realtime non rispetta la RLS sui canali di broadcast: filtra lato server
- Le Server Actions girano anche su richieste non autenticate: la sessione va verificata in
  ogni action, non solo nel layout

## Decisioni

Le scelte di stack e architettura sono in `docs/decisioni/`. **Leggile prima di proporre
cambi strutturali.**
