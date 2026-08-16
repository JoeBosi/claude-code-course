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

Il dominio `giuseppebosi.com` è gestito da **IONOS** (nameserver `ns1125.ui-dns.com` e affini).
Due passaggi, in quest'ordine.

**1. Aggiungi il dominio in Vercel.** Project `claude-tutorial` → **Settings → Domains → Add**,
inserisci `claude-tutorial.giuseppebosi.com`. Vercel mostrerà il record da creare e resterà in
attesa: è normale.

**2. Crea il record DNS su IONOS.** Pannello IONOS → **Domini e SSL** → `giuseppebosi.com` →
**DNS** → *Aggiungi record*:

| Campo | Valore |
| --- | --- |
| Tipo | `CNAME` |
| Nome host | `claude-tutorial` |
| Punta a | `cname.vercel-dns.com` |
| TTL | 3600 (o il default) |

Nel campo *Nome host* va **solo** `claude-tutorial`, non il dominio completo: IONOS aggiunge da
sé `.giuseppebosi.com`. È l'errore più comune su questo pannello.

**Verifica.** La propagazione richiede da pochi minuti a un'ora:

```bash
dig +short claude-tutorial.giuseppebosi.com
# atteso: cname.vercel-dns.com.  seguito da uno o più IP
```

Quando il record risolve, Vercel emette il certificato HTTPS da solo e il dominio passa a
**Valid Configuration**. Non serve toccare nulla in Vercel dopo.

<!-- Il sottodominio `files.giuseppebosi.com` punta al VPS (164.68.123.249) e non viene
     toccato da questa configurazione. -->

### Aprire il repository al pubblico

Finché il repository resta privato, il link GitHub nell'header del sito è commentato in
`astro.config.mjs` per non mandare i visitatori su un 404. Quando lo rendi pubblico, togli il
commento e ricommetta.

## Licenza

Contenuti didattici a scopo formativo. I marchi citati appartengono ai rispettivi proprietari.
