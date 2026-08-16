# STATE — Corso "Claude Code Tutorial"

Stato di avanzamento. Aggiornato **prima** di iniziare un modulo e **dopo** averlo chiuso.
Se la sessione si interrompe, si riparte dal primo modulo non completato senza rifare lavoro.

Legenda: `[ ]` da fare · `[~]` in corso · `[x]` completato

Ultimo aggiornamento: 2026-08-16

## Infrastruttura

- [x] Scaffold Astro 7 + Starlight 0.41 (Node 22 via nvm)
- [x] Integrazioni: astro-mermaid, @astrojs/sitemap, starlight-links-validator
- [x] `astro.config.mjs` con sidebar a 4 sezioni, SEO/OG, footer override
- [x] `src/components/Footer.astro` con disclaimer di non affiliazione
- [x] `src/styles/custom.css`
- [x] `scripts/zip-boilerplates.mjs` + hook `prebuild`
- [x] Repo git + push su GitHub (`JoeBosi/claude-tutorial`) — repo **privato**
- [x] Progetto Vercel `claude-tutorial` collegato + primo deploy → https://claude-tutorial-ten.vercel.app

## Sezione 1 — Fondamenta

- [x] 00 · Setup e installazione — `fondamenta/setup`
- [ ] 01 · Claude negli IDE — `fondamenta/ide`
- [ ] 02 · Anatomia dei file — `fondamenta/anatomia-file`
- [ ] 03 · Agentic Coding — `fondamenta/agentic-coding`
- [ ] 04 · Memory & Context Engineering — `fondamenta/memoria-e-contesto`
- [ ] 05 · Il file CLAUDE.md — `fondamenta/claude-md`
- [ ] 06 · Plan Mode — `fondamenta/plan-mode`

## Sezione 2 — Personalizzazione ed estensioni

- [ ] 07 · Slash Commands — `personalizzazione/slash-commands`
- [ ] 08 · Skills personalizzate — `personalizzazione/skills`
- [ ] 09 · MCP e server remoti — `personalizzazione/mcp`
- [ ] 10 · Hooks e automazioni locali — `personalizzazione/hooks`
- [ ] 11 · Agents e Subagents — `personalizzazione/agents-subagents`

## Sezione 3 — Automazione e integrazione

- [ ] 12 · CLI scripting — `automazione/cli-scripting`
- [ ] 13 · Output JSON — `automazione/output-json`
- [ ] 14 · Pipeline locali — `automazione/pipeline-locali`
- [ ] 15 · Sessioni remote e lavoro asincrono — `automazione/sessioni-remote`

## Sezione 4 — Livello professionale

- [ ] 16 · Ecosistema e fonti — `professionale/ecosistema`
- [ ] 17 · Stack, framework e architetture — `professionale/stack-architetture`
- [ ] 18 · Boilerplate agentici riusabili — `professionale/boilerplate`
- [ ] 19 · Workflow professionali — `professionale/workflow`

## Boilerplate scaricabili

- [ ] `boilerplates/web-fullstack/`
- [ ] `boilerplates/headless-pipeline/`
- [ ] `boilerplates/agentic-rag/`

## Qualità finale

- [x] Homepage (pitch, indice, prerequisiti, badge data verifica)
- [ ] SEO per pagina + sitemap + Open Graph
- [x] `README.md` con dev locale e deploy
- [ ] `npm run build` verde + link interni validati
- [ ] Pagefind verificato su build di produzione
- [ ] Ri-verifica dei link esterni del modulo 16
- [ ] Deploy produzione + dominio custom + checklist DNS
