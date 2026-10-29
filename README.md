# Claude Code Course: free Claude Code tutorial, from zero to agentic workflows

**English** · [Italiano](README.it.md)

**Learn Claude Code step by step**: a free, open course (in Italian and English) on Anthropic's AI coding agent, covering the CLI, the VS Code extension and the desktop app, CLAUDE.md, Plan Mode, skills, MCP servers, hooks, subagents and headless automation, with runnable examples and three ready-to-use boilerplates.

**Live site:** <https://claude-tutorial.giuseppebosi.com> · English: <https://claude-tutorial.giuseppebosi.com/en/>

## What it covers

- **20 modules** in four parts: foundations (setup, IDEs, CLAUDE.md, Plan Mode), customization (slash commands, skills, MCP, hooks, subagents), automation (CLI scripting, JSON output, local pipelines, remote sessions) and professional practice (ecosystem, stacks, reusable boilerplates, team workflows).
- Two reading tracks: the main text for developers, plus "Se parti da zero" boxes and a 60+ term glossary for readers who are not.
- Every module has a guided example with expected output, an exercise with solution, a troubleshooting section, a cheat sheet and links to the official docs.
- Three downloadable **boilerplates** (`boilerplates/`): a full-stack web app, an agentic RAG service with an offline test suite, and a headless Claude Code pipeline.
- Built-in search (Pagefind), Mermaid diagrams, `llms.txt` / `llms-full.txt` for AI assistants, sitemap and structured data.

## Run it locally

Requires **Node.js 22+**.

```bash
npm install
npm run dev       # dev server on http://localhost:4321 (search does not work in dev)
npm run build     # production build in dist/; fails on broken internal links
npm run preview   # serve dist/, search included
```

`npm run build` first packs each folder in `boilerplates/` into `public/downloads/*.zip`.

## Project structure

```text
src/content/docs/   course pages (MDX), one folder per part; English under en/
docs/               Italian → English translation glossary and brief
src/components/     Starlight overrides (header title, footer) and the "Zero" box
src/pages/          llms.txt and llms-full.txt endpoints
boilerplates/       the three downloadable templates
scripts/            build helpers (boilerplate zipping)
astro.config.mjs    site config and the explicit sidebar
```

Stack: [Astro](https://astro.build) + [Starlight](https://starlight.astro.build), static output, deployed on Vercel.

## License

- **Course text and images:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-CONTENT).
- **Code** (site source, examples, boilerplates): [MIT](LICENSE).

## Author

**Giuseppe Bosi** · [www.giuseppebosi.com](https://www.giuseppebosi.com) · [LinkedIn](https://www.linkedin.com/in/giuseppebosi)

This is an independent course, not affiliated with or endorsed by Anthropic or Google. Claude and Claude Code are trademarks of Anthropic.
