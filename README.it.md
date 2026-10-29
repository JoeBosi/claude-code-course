# Claude Code Course

[English](README.md) · **Italiano**

Corso web gratuito, in italiano e in inglese, su [Claude Code](https://code.claude.com/docs), lo strumento di coding agentico di Anthropic: la CLI, l'estensione VS Code e l'app desktop, dalla prima installazione ai workflow agentici di produzione.

**Sito:** <https://claude-tutorial.giuseppebosi.com> · inglese: <https://claude-tutorial.giuseppebosi.com/en/>

## Cosa contiene

- **20 moduli** in quattro parti: fondamenta (setup, IDE, CLAUDE.md, Plan Mode), personalizzazione (slash command, skill, MCP, hook, subagent), automazione (scripting da CLI, output JSON, pipeline locali, sessioni remote) e livello professionale (ecosistema, stack, boilerplate riusabili, workflow di team).
- Due binari di lettura: il testo principale per sviluppatori, più i box "Se parti da zero" e un glossario di oltre 60 voci per chi non lo è.
- Ogni modulo ha un esempio guidato con l'output atteso, un esercizio con soluzione, gli errori comuni, un cheat-sheet e i link ai docs ufficiali.
- Tre **boilerplate** scaricabili (`boilerplates/`): un'app web full-stack, un servizio RAG agentico con test offline e una pipeline headless di Claude Code.
- Ricerca interna (Pagefind), diagrammi Mermaid, `llms.txt` / `llms-full.txt` per gli assistenti IA, sitemap e dati strutturati.

## Avviarlo in locale

Serve **Node.js 22 o superiore**.

```bash
npm install
npm run dev       # server di sviluppo su http://localhost:4321 (qui la ricerca non funziona)
npm run build     # build di produzione in dist/; fallisce se un link interno è rotto
npm run preview   # serve dist/, ricerca compresa
```

`npm run build` prima impacchetta ogni cartella di `boilerplates/` in `public/downloads/*.zip`.

## Struttura

```text
src/content/docs/   le pagine del corso (MDX), una cartella per parte; l'inglese in en/
docs/               glossario e istruzioni per la traduzione italiano → inglese
src/components/     override di Starlight (titolo nell'header, footer) e il box "Zero"
src/pages/          gli endpoint llms.txt e llms-full.txt
boilerplates/       i tre template scaricabili
scripts/            script di build (zip dei boilerplate)
astro.config.mjs    configurazione del sito e sidebar esplicita
```

Stack: [Astro](https://astro.build) + [Starlight](https://starlight.astro.build), output statico, pubblicato su Vercel.

## Licenza

- **Testi e immagini del corso:** [Creative Commons Attribuzione 4.0 Internazionale (CC BY 4.0)](LICENSE-CONTENT).
- **Codice** (sorgenti del sito, esempi, boilerplate): [MIT](LICENSE).

## Autore

**Giuseppe Bosi** · [www.giuseppebosi.com](https://www.giuseppebosi.com) · [LinkedIn](https://www.linkedin.com/in/giuseppebosi)

Corso indipendente, non affiliato ad Anthropic o Google e da loro non approvato. Claude e Claude Code sono marchi di Anthropic.
