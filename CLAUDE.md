# Claude Code Tutorial — convenzioni del repo

Corso web in italiano su Claude Code, pubblicato su <https://claude-tutorial.giuseppebosi.com>.
Stack: Astro 7 + Starlight 0.41, output statico, deploy su Vercel.

## Regola zero — nessuna invenzione

Prima di scrivere un modulo, verifica ogni feature sui docs ufficiali partendo dall'indice
<https://code.claude.com/docs/en/claude_code_docs_map.md>. Ogni comando, flag, file di
configurazione, percorso e nome di feature deve corrispondere ai docs **attuali**: se la memoria di
training diverge dai docs, fanno fede i docs. Per gli strumenti di terze parti (Google Antigravity,
directory MCP) fanno fede i rispettivi siti ufficiali.

Vietati: lorem ipsum, placeholder, esempi non testabili, feature non verificate.

## Comandi

```bash
npm run dev      # dev server (la ricerca Pagefind NON funziona in dev)
npm run build    # build di produzione; fallisce se un link interno è rotto
npm run preview  # serve dist/ — usalo per provare la ricerca
```

Serve **Node ≥ 22** (Astro 7). Su questa macchina: `nvm use 22`.

## Struttura

- `src/content/docs/` — i moduli, in quattro cartelle: `fondamenta/`, `personalizzazione/`,
  `automazione/`, `professionale/`.
- `astro.config.mjs` — sidebar **esplicita** (non autogenerate): aggiungendo una pagina va aggiunta
  anche qui, altrimenti non compare in navigazione.
- `boilerplates/` — le tre cartelle-template del modulo 18. `npm run prebuild` le impacchetta in
  `public/downloads/*.zip` (zip generati, non versionati).
- `src/components/Footer.astro` — override del footer Starlight con il disclaimer di non affiliazione.
- `STATE.md` — checklist di avanzamento. **Aggiornala prima di iniziare e dopo aver chiuso un modulo.**

## Formato di ogni modulo

Otto sezioni, sempre nello stesso ordine:

1. Tempo stimato e prerequisiti (una riga)
2. Obiettivi (3–5 bullet)
3. Concetti chiave (max 600 parole)
4. Esempio guidato passo-passo, con comandi copia-incolla e output atteso
5. Esercizio pratico, con soluzione in `<details class="soluzione">`
6. Errori comuni & troubleshooting
7. Cheat-sheet in tabella
8. Fonti — link ai docs ufficiali con data dell'ultima verifica

## Convenzioni di scrittura

- Contenuti in **italiano**; codice, comandi e nomi di file in inglese.
- Comandi macOS/Windows sempre in `<Tabs syncKey="os">` con `<TabItem label="macOS">` e
  `<TabItem label="Windows">`. Il `syncKey` deve restare `"os"` ovunque, così la scelta del sistema
  operativo resta sincronizzata su tutto il sito.
- Solo **percorsi relativi**, mai path assoluti della macchina di sviluppo.
- Diagrammi in blocchi ` ```mermaid ` — resi da `astro-mermaid`, che nella config va **prima** di
  `starlight()`.
- Ogni pagina ha `title` e `description` in frontmatter: la description alimenta SEO e Open Graph.

## Git

Un commit per modulo: `feat(corso): modulo NN - titolo`.
Infrastruttura e rifiniture: `chore:` / `docs:`.
