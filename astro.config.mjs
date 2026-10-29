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
				en: { label: 'English', lang: 'en' },
			},
			customCss: ['./src/styles/custom.css'],
			components: {
				Footer: './src/components/Footer.astro',
				SiteTitle: './src/components/SiteTitle.astro',
			},
			plugins: [starlightLinksValidator()],
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/JoeBosi/claude-code-course' },
			],
			head: [
				// Tema chiaro come predefinito per tutti, anche se il sistema del
				// visitatore è in modalità scura. Chi sceglie il tema col selettore
				// di Starlight viene comunque rispettato (il default vale solo se
				// non c'è ancora una preferenza salvata).
				{
					tag: 'script',
					content:
						"(function(){try{if(!localStorage.getItem('starlight-theme')){localStorage.setItem('starlight-theme','light');}if(localStorage.getItem('starlight-theme')==='light'){document.documentElement.dataset.theme='light';}}catch(e){}})();",
				},
				{
					tag: 'script',
					attrs: { type: 'application/ld+json' },
					content: JSON.stringify({
						'@context': 'https://schema.org',
						'@type': 'Course',
						name: 'Claude Code Tutorial',
						description: DESCRIZIONE,
						url: SITE,
						inLanguage: 'it',
						isAccessibleForFree: true,
						author: {
							'@type': 'Person',
							name: 'Prof. Giuseppe Bosi',
							url: 'https://www.giuseppebosi.com',
							sameAs: ['https://www.linkedin.com/in/giuseppebosi'],
							jobTitle: 'Professore di Scienze e Tecnologie Informatiche',
							hasCredential: 'Dottore in Ingegneria Elettronica (V.O.)',
						},
						provider: { '@type': 'Person', name: 'Prof. Giuseppe Bosi', url: 'https://www.giuseppebosi.com' },
					}),
				},
				{ tag: 'meta', attrs: { property: 'og:site_name', content: 'Claude Code Tutorial' } },
				{ tag: 'meta', attrs: { property: 'og:type', content: 'website' } },
				{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
			],
			pagination: true,
			lastUpdated: true,
			sidebar: [
				{
					label: 'Per orientarsi', translations: { en: 'Getting oriented' },
					items: [
						{ label: 'Le basi, prima di iniziare', translations: { en: 'The basics, before you start' }, slug: 'basi' },
						{ label: 'Glossario', translations: { en: 'Glossary' }, slug: 'glossario' },
					],
				},
				{
					label: 'Fondamenta', translations: { en: 'Foundations' },
					items: [
						{ label: '0 · Setup e installazione', translations: { en: '0 · Setup and installation' }, slug: 'fondamenta/setup' },
						{ label: '1 · Claude negli IDE', translations: { en: '1 · Claude in your IDE' }, slug: 'fondamenta/ide' },
						{ label: '2 · Anatomia dei file', translations: { en: '2 · Anatomy of the files' }, slug: 'fondamenta/anatomia-file' },
						{ label: '3 · Agentic Coding', slug: 'fondamenta/agentic-coding' },
						{ label: '4 · Memory & Context Engineering', slug: 'fondamenta/memoria-e-contesto' },
						{ label: '5 · Il file CLAUDE.md', translations: { en: '5 · The CLAUDE.md file' }, slug: 'fondamenta/claude-md' },
						{ label: '6 · Plan Mode', slug: 'fondamenta/plan-mode' },
					],
				},
				{
					label: 'Personalizzazione ed estensioni', translations: { en: 'Customization and extensions' },
					items: [
						{ label: '7 · Slash Commands', slug: 'personalizzazione/slash-commands' },
						{ label: '8 · Skills personalizzate', translations: { en: '8 · Custom skills' }, slug: 'personalizzazione/skills' },
						{ label: '9 · MCP e server remoti', translations: { en: '9 · MCP and remote servers' }, slug: 'personalizzazione/mcp' },
						{ label: '10 · Hooks e automazioni locali', translations: { en: '10 · Hooks and local automation' }, slug: 'personalizzazione/hooks' },
						{ label: '11 · Agents e Subagents', translations: { en: '11 · Agents and subagents' }, slug: 'personalizzazione/agents-subagents' },
					],
				},
				{
					label: 'Automazione e integrazione', translations: { en: 'Automation and integration' },
					items: [
						{ label: '12 · CLI scripting', slug: 'automazione/cli-scripting' },
						{ label: '13 · Output JSON', slug: 'automazione/output-json' },
						{ label: '14 · Pipeline locali', translations: { en: '14 · Local pipelines' }, slug: 'automazione/pipeline-locali' },
						{ label: '15 · Sessioni remote e lavoro asincrono', translations: { en: '15 · Remote sessions and async work' }, slug: 'automazione/sessioni-remote' },
					],
				},
				{
					label: 'Livello professionale', translations: { en: 'Professional level' },
					items: [
						{ label: '16 · Ecosistema e fonti', translations: { en: '16 · Ecosystem and sources' }, slug: 'professionale/ecosistema' },
						{ label: '17 · Stack, framework e architetture', translations: { en: '17 · Stacks, frameworks and architectures' }, slug: 'professionale/stack-architetture' },
						{ label: '18 · Boilerplate agentici riusabili', translations: { en: '18 · Reusable agentic boilerplates' }, slug: 'professionale/boilerplate' },
						{ label: '19 · Workflow professionali', translations: { en: '19 · Professional workflows' }, slug: 'professionale/workflow' },
					],
				},
			],
		}),
		sitemap({ i18n: { defaultLocale: 'it', locales: { it: 'it', en: 'en' } } }),
	],
});
