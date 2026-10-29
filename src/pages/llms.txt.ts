import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const SITE = 'https://claude-tutorial.giuseppebosi.com';

// Le sezioni seguono le cartelle dei moduli; le pagine senza cartella
// (home, basi, glossario) finiscono nella prima sezione.
const SEZIONI: [string, string, string][] = [
	['', 'Per orientarsi', 'Getting oriented'],
	['fondamenta/', 'Fondamenta', 'Foundations'],
	['personalizzazione/', 'Personalizzazione ed estensioni', 'Customization and extensions'],
	['automazione/', 'Automazione e integrazione', 'Automation and integration'],
	['professionale/', 'Livello professionale', 'Professional level'],
];

type Pagina = Awaited<ReturnType<typeof getCollection<'docs'>>>[number];

function elenco(pagine: Pagina[], prefisso: '' | 'en/', en: boolean): string[] {
	const righe: string[] = [];
	const qui = pagine
		.filter((p) => (prefisso ? p.id.startsWith(prefisso) : !p.id.startsWith('en/')))
		.map((p) => ({ p, rel: prefisso ? p.id.slice(prefisso.length) : p.id }));
	const sezione = (rel: string) => SEZIONI.findLastIndex(([pre]) => rel.startsWith(pre));
	SEZIONI.forEach(([, it, eng], i) => {
		const gruppo = qui
			.filter(({ rel }) => sezione(rel) === i)
			.sort((a, b) => a.rel.localeCompare(b.rel, 'it', { numeric: true }));
		if (!gruppo.length) return;
		righe.push('', `${en ? '###' : '##'} ${en ? eng : it}`, '');
		for (const { p, rel } of gruppo) {
			const percorso = rel === 'index' ? '' : `${rel}/`;
			righe.push(`- [${p.data.title}](${SITE}/${prefisso}${percorso}): ${p.data.description ?? ''}`);
		}
	});
	return righe;
}

export const GET: APIRoute = async () => {
	const pagine = (await getCollection('docs')).filter((p) => p.id !== '404' && p.id !== 'en/404');
	const righe = [
		'# Claude Code Tutorial',
		'',
		'> Corso gratuito su Claude Code (CLI, estensione VS Code, app desktop), da zero al livello professionale: venti moduli con esempi da eseguire, esercizi con soluzione e link alla documentazione ufficiale. In italiano, con versione inglese sotto /en/. Autore: Prof. Giuseppe Bosi (https://www.giuseppebosi.com, LinkedIn: https://www.linkedin.com/in/giuseppebosi).',
		'',
		`Testo completo di tutte le pagine in un solo file: ${SITE}/llms-full.txt`,
		...elenco(pagine, '', false),
		'',
		'## English version',
		'',
		`The same course in English, by Prof. Giuseppe Bosi (https://www.giuseppebosi.com/en/): ${SITE}/en/`,
		...elenco(pagine, 'en/', true),
		'',
		'## Altri corsi dello stesso autore',
		'',
		'- [Corso JSON & API](https://corso-api-json.giuseppebosi.com/)',
		'- [Corso pratico di llama.cpp](https://corso-llamacpp.giuseppebosi.com/)',
		'- [Costruisci la tua memoria AI](https://corso-rag.giuseppebosi.com/)',
		'',
	];
	return new Response(righe.join('\n'), {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
