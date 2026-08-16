# Claude Code Tutorial

Corso web gratuito in italiano su **Claude Code** — CLI, estensione VS Code e app desktop Claude, su
macOS e Windows. Venti moduli, da zero al livello professionale, con ogni comando e percorso di file
verificato sulla [documentazione ufficiale](https://code.claude.com/docs/en/overview).

🌐 **<https://claude-tutorial.giuseppebosi.com>**

Corso indipendente, non affiliato ad Anthropic o Google.

## Contenuti

| Sezione | Moduli |
| --- | --- |
| **Fondamenta** | 0 Setup · 1 Claude negli IDE · 2 Anatomia dei file · 3 Agentic Coding · 4 Memory & Context · 5 CLAUDE.md · 6 Plan Mode |
| **Personalizzazione ed estensioni** | 7 Slash Commands · 8 Skills · 9 MCP · 10 Hooks · 11 Agents e Subagents |
| **Automazione e integrazione** | 12 CLI scripting · 13 Output JSON · 14 Pipeline locali · 15 Sessioni remote |
| **Livello professionale** | 16 Ecosistema e fonti · 17 Stack e architetture · 18 Boilerplate agentici · 19 Workflow professionali |

Lo stato di avanzamento della scrittura è in [`STATE.md`](./STATE.md).

## Stack

[Astro 7](https://astro.build) + [Starlight](https://starlight.astro.build) 0.41, output statico.
Ricerca [Pagefind](https://pagefind.app) integrata, diagrammi
[Mermaid](https://mermaid.js.org) via `astro-mermaid`, validazione dei link interni in build con
`starlight-links-validator`.

## Sviluppo locale

Serve **Node.js ≥ 22** (requisito di Astro 7).

```bash
npm install
npm run dev       # http://localhost:4321
```

| Comando | Cosa fa |
| --- | --- |
| `npm run dev` | Dev server con hot reload. **La ricerca non funziona in dev**: Pagefind indicizza solo la build. |
| `npm run build` | Build di produzione in `dist/`. Impacchetta i boilerplate e **fallisce se un link interno è rotto**. |
| `npm run preview` | Serve `dist/` in locale — l'unico modo per provare la ricerca. |
| `npm run check` | Type-check dei file Astro. |

Per provare la ricerca come in produzione:

```bash
npm run build && npm run preview
```

### Struttura

```
src/content/docs/     i moduli, in quattro cartelle (una per sezione)
astro.config.mjs      sidebar esplicita, integrazioni, SEO
boilerplates/         le tre cartelle-template del modulo 18
public/downloads/     zip generati in prebuild (non versionati)
scripts/              zip-boilerplates.mjs
```

La sidebar **non** è autogenerata: aggiungendo una pagina va aggiunta anche in `astro.config.mjs`.

## Deploy

Il sito è ospitato su **Vercel** come sito statico: nessun adapter Astro necessario.

| Impostazione | Valore |
| --- | --- |
| Framework preset | Astro |
| Build command | `npm run build` |
| Output directory | `dist` |
| Node version | 22.x |

Ogni push su `main` fa un deploy di produzione; ogni altro branch genera un deploy di preview.

### Dominio custom

Sul pannello DNS di `giuseppebosi.com`:

| Tipo | Nome | Valore | TTL |
| --- | --- | --- | --- |
| CNAME | `claude-tutorial` | `cname.vercel-dns.com` | auto (o 3600) |

Poi in Vercel: **Project → Settings → Domains → Add** `claude-tutorial.giuseppebosi.com`. Il
certificato HTTPS viene emesso automaticamente appena il DNS propaga.

## Licenza

Contenuti didattici a scopo formativo. I marchi citati appartengono ai rispettivi proprietari.
