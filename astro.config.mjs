// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';
import sitemap from '@astrojs/sitemap';
import starlightLinksValidator from 'starlight-links-validator';

const SITE = 'https://claude-tutorial.giuseppebosi.com';
const DESCRIZIONE =
	'Corso completo e gratuito su Claude Code in italiano: CLI, estensione VS Code e app desktop, da zero al livello professionale. Verificato sui docs ufficiali.';

// https://astro.build/config
export default defineConfig({
	site: SITE,
	integrations: [
		// astro-mermaid deve precedere starlight: registra la trasformazione
		// markdown prima che Starlight processi i contenuti.
		mermaid({ theme: 'default', autoTheme: true }),
		starlight({
			title: 'Claude Code Tutorial',
			description: DESCRIZIONE,
			defaultLocale: 'root',
			locales: {
				root: { label: 'Italiano', lang: 'it' },
			},
			customCss: ['./src/styles/custom.css'],
			components: {
				Footer: './src/components/Footer.astro',
			},
			plugins: [starlightLinksValidator()],
			social: [
				{
					icon: 'github',
					label: 'GitHub',
					href: 'https://github.com/JoeBosi/claude-tutorial',
				},
			],
			head: [
				{ tag: 'meta', attrs: { property: 'og:site_name', content: 'Claude Code Tutorial' } },
				{ tag: 'meta', attrs: { property: 'og:type', content: 'website' } },
				{ tag: 'meta', attrs: { property: 'og:locale', content: 'it_IT' } },
				{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
			],
			pagination: true,
			lastUpdated: true,
			sidebar: [
				{
					label: 'Fondamenta',
					items: [
						{ label: '0 · Setup e installazione', slug: 'fondamenta/setup' },
						{ label: '1 · Claude negli IDE', slug: 'fondamenta/ide' },
						{ label: '2 · Anatomia dei file', slug: 'fondamenta/anatomia-file' },
						{ label: '3 · Agentic Coding', slug: 'fondamenta/agentic-coding' },
						{ label: '4 · Memory & Context Engineering', slug: 'fondamenta/memoria-e-contesto' },
						{ label: '5 · Il file CLAUDE.md', slug: 'fondamenta/claude-md' },
						{ label: '6 · Plan Mode', slug: 'fondamenta/plan-mode' },
					],
				},
				{
					label: 'Personalizzazione ed estensioni',
					items: [
						{ label: '7 · Slash Commands', slug: 'personalizzazione/slash-commands' },
						{ label: '8 · Skills personalizzate', slug: 'personalizzazione/skills' },
						{ label: '9 · MCP e server remoti', slug: 'personalizzazione/mcp' },
						{ label: '10 · Hooks e automazioni locali', slug: 'personalizzazione/hooks' },
						{ label: '11 · Agents e Subagents', slug: 'personalizzazione/agents-subagents' },
					],
				},
				{
					label: 'Automazione e integrazione',
					items: [
						{ label: '12 · CLI scripting', slug: 'automazione/cli-scripting' },
						{ label: '13 · Output JSON', slug: 'automazione/output-json' },
						{ label: '14 · Pipeline locali', slug: 'automazione/pipeline-locali' },
						{ label: '15 · Sessioni remote e lavoro asincrono', slug: 'automazione/sessioni-remote' },
					],
				},
				{
					label: 'Livello professionale',
					items: [
						{ label: '16 · Ecosistema e fonti', slug: 'professionale/ecosistema' },
						{ label: '17 · Stack, framework e architetture', slug: 'professionale/stack-architetture' },
						{ label: '18 · Boilerplate agentici riusabili', slug: 'professionale/boilerplate' },
						{ label: '19 · Workflow professionali', slug: 'professionale/workflow' },
					],
				},
			],
		}),
		sitemap(),
	],
});
