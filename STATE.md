# STATE — Corso "Claude Code Tutorial"

Stato di avanzamento. Aggiornato **prima** di iniziare un modulo e **dopo** averlo chiuso.
Se la sessione si interrompe, si riparte dal primo modulo non completato senza rifare lavoro.

Legenda: `[ ]` da fare · `[~]` in corso · `[x]` completato

Ultimo aggiornamento: 2026-08-16 — **tutti i 20 moduli completati**

## Infrastruttura

- [x] Scaffold Astro 7 + Starlight 0.41 (Node 22 via nvm)
- [x] Integrazioni: astro-mermaid, @astrojs/sitemap, starlight-links-validator
- [x] `astro.config.mjs` con sidebar a 4 sezioni, SEO/OG, footer override
- [x] `src/components/Footer.astro` con disclaimer di non affiliazione
- [x] `src/styles/custom.css`
- [x] `scripts/zip-boilerplates.mjs` + hook `prebuild`
- [x] Repo git + push su GitHub (`JoeBosi/claude-tutorial`) — repo **privato**
- [x] Progetto Vercel `claude-tutorial` collegato + deploy → https://claude-tutorial-ten.vercel.app

## Sezione 1 — Fondamenta

- [x] 00 · Setup e installazione — `fondamenta/setup`
- [x] 01 · Claude negli IDE — `fondamenta/ide`
- [x] 02 · Anatomia dei file — `fondamenta/anatomia-file`
- [x] 03 · Agentic Coding — `fondamenta/agentic-coding`
- [x] 04 · Memory & Context Engineering — `fondamenta/memoria-e-contesto`
- [x] 05 · Il file CLAUDE.md — `fondamenta/claude-md`
- [x] 06 · Plan Mode — `fondamenta/plan-mode`

## Sezione 2 — Personalizzazione ed estensioni

- [x] 07 · Slash Commands — `personalizzazione/slash-commands`
- [x] 08 · Skills personalizzate — `personalizzazione/skills`
- [x] 09 · MCP e server remoti — `personalizzazione/mcp`
- [x] 10 · Hooks e automazioni locali — `personalizzazione/hooks`
- [x] 11 · Agents e Subagents — `personalizzazione/agents-subagents`

## Sezione 3 — Automazione e integrazione

- [x] 12 · CLI scripting — `automazione/cli-scripting`
- [x] 13 · Output JSON — `automazione/output-json`
- [x] 14 · Pipeline locali — `automazione/pipeline-locali`
- [x] 15 · Sessioni remote e lavoro asincrono — `automazione/sessioni-remote`

## Sezione 4 — Livello professionale

- [x] 16 · Ecosistema e fonti — `professionale/ecosistema`
- [x] 17 · Stack, framework e architetture — `professionale/stack-architetture`
- [x] 18 · Boilerplate agentici riusabili — `professionale/boilerplate`
- [x] 19 · Workflow professionali — `professionale/workflow`

## Boilerplate scaricabili

- [x] `boilerplates/web-fullstack/` — 32 file, `init.sh` provato da zip estratto
- [x] `boilerplates/headless-pipeline/` — 36 file, `shellcheck` pulito su tutti gli script
- [x] `boilerplates/agentic-rag/` — 55 file, **7 test verdi** eseguiti da zip estratto

## Qualità finale

- [x] Homepage (pitch, indice, prerequisiti, badge data verifica)
- [x] SEO: `title` e `description` su tutte e 21 le pagine, Open Graph, sitemap con 21 URL
- [x] `README.md` con dev locale e deploy
- [x] `npm run build` verde + link interni validati da `starlight-links-validator`
- [x] Pagefind: indice con 21 pagine, `pagefind.js` servito, contenuti indicizzati verificati
- [x] 10 diagrammi Mermaid validati con il parser reale — 0 errori
- [x] Footer di non affiliazione su tutte e 21 le pagine
- [x] Link esterni verificati: 98 unici, 91 rispondono 2xx/3xx
- [x] Ri-verifica dei link esterni del modulo 16 (2026-08-16)
- [x] Dominio custom `claude-tutorial.giuseppebosi.com` — attivo, HTTPS ok (verificato 2026-09-12)

## Revisione didattica (2026-08-17)

Motivazione: feedback del committente — il corso era scritto per chi sa già. Piano approvato,
quattro regole editoriali (in `CLAUDE.md`): cosa/perché prima del come; nessun termine orfano;
nessun codice muto; box "Se parti da zero" per il binario principianti.

- [x] Fase 0 — Glossario (62 voci con anchor), pagina "Le basi", componente `Zero.astro`,
      sezione sidebar "Per orientarsi", regole editoriali nel `CLAUDE.md`
- [x] Fase 1 — moduli 0–6 + homepage rivisti (commit `refactor(corso): … moduli 00-06`)
- [x] Fase 2 — moduli 7–11 rivisti (aggiunti `/subtask` e `/statusline` al modulo 7)
- [x] Fase 3 — moduli 12–15 rivisti (fix incoerenze `--bare`, React→Vue, `github_token`, piani RC)
- [x] Fase 4 — moduli 16–19 rivisti (tre "schema", legenda tabella decisionale e diagrammi,
      `/ship` mostrato per intero, `init.sh` commentato riga per riga, TDD/nit/anchoring definiti)
- [x] Fase 5 — boilerplate: **bug fix** `run.sh` (exit code perso dentro `if !` → l'orchestratore
      usciva 0 a stadio fallito) + **bug fix** `01-fetch.sh` (doppio `[]` con pipefail) + `mkdir -p`
      per stadio + commenti per non-esperti in tutti gli script e nel dominio Python + import
      `collections.abc` (ruff pulito). Riprovato da zip estratto: 7 test verdi, shellcheck ok,
      smoke test run.sh con stadio rotto → exit 2 ✔
- [x] Fase 6 — build + links validator verdi; 10 Mermaid rivalidati col parser (0 errori);
      Pagefind: 23 pagine indicizzate incluse `/basi/` e `/glossario/`; grep di controllo
      termini-prima-della-definizione: pulito; deploy verificato (200 su tutte le pagine campione,
      zip in produzione col fix); 4 test del lettore non-programmatore (subagent, uno per sezione):
      34 rilievi, tutti valutati e i fondati corretti (system prompt/headless aggiunti al glossario,
      chmod nei passi 3-4 del modulo 10, structured_output spiegato nel 12, SSH/WSL/tmux/stash/
      feature flag/clone shallow/wrapper/SHA/CRUD/SaaS/edge/PII/rollback glossati inline)

## Da fare a consegna

- [x] Record CNAME su IONOS (valore per-progetto `*.vercel-dns-017.com` fornito da Vercel)
- [x] Dominio aggiunto in Vercel, certificato emesso (scade 2026-11-15, rinnovo automatico)
- [ ] Rendere pubblico il repo `JoeBosi/claude-tutorial` (scelta dell'utente, a lavoro finito)
- [ ] Riattivare il link GitHub nell'header: togliere il commento in `astro.config.mjs`

## Note

- **Link esterni in 403**: 7 URL rispondono 403 alle richieste automatiche da questo VPS
  (`claude.ai/*`, `npmjs.com`, `pulsemcp.com`). È protezione anti-bot su IP di datacenter, non
  link morti: `pulsemcp.com` è stato letto con successo via WebFetch, e gli URL `claude.ai`
  sono presi verbatim dalla documentazione ufficiale Anthropic.
- **Permessi**: le directory sotto `~/work` perdono periodicamente il bit di scrittura del
  proprietario. Succede anche agli altri progetti in `~/work`, quindi è precedente a questo
  lavoro. Se una scrittura fallisce: `chmod -R u+rwX .` nella root del progetto.
- **Node**: serve Node ≥ 22 (Astro 7). Installato con nvm come default.
