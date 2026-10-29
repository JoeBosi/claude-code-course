import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const SITE = 'https://claude-tutorial.giuseppebosi.com';

// Le sezioni seguono le cartelle dei moduli; le pagine senza cartella
// (home, basi, glossario) finiscono in "Per orientarsi".
const SEZIONI: [string, string][] = [
	['', 'Per orientarsi'],
	['fondamenta/', 'Fondamenta'],
	['personalizzazione/', 'Personalizzazione ed estensioni'],
	['automazione/', 'Automazione e integrazione'],
	['professionale/', 'Livello professionale'],
];

export const GET: APIRoute = async () => {
	const pagine = (await getCollection('docs')).filter((p) => p.id !== '404');
	const sezione = (id: string) => SEZIONI.findLastIndex(([pre]) => id.startsWith(pre));
	const righe = [
		'# Claude Code Tutorial',
		'',
		'> Corso gratuito in italiano su Claude Code (CLI, estensione VS Code, app desktop), da zero al livello professionale: venti moduli con esempi da eseguire, esercizi con soluzione e link alla documentazione ufficiale. Autore: Prof. Giuseppe Bosi (https://www.giuseppebosi.com, LinkedIn: https://www.linkedin.com/in/giuseppebosi).',
		'',
		`Testo completo di tutte le pagine in un solo file: ${SITE}/llms-full.txt`,
	];
	SEZIONI.forEach(([, titolo], i) => {
		const qui = pagine
			.filter((p) => sezione(p.id) === i)
			.sort((a, b) => a.id.localeCompare(b.id, 'it', { numeric: true }));
		if (!qui.length) return;
		righe.push('', `## ${titolo}`, '');
		for (const p of qui) {
			const url = p.id === 'index' ? `${SITE}/` : `${SITE}/${p.id}/`;
			righe.push(`- [${p.data.title}](${url}): ${p.data.description ?? ''}`);
		}
	});
	righe.push(
		'',
		'## Altri corsi dello stesso autore',
		'',
		'- [Corso JSON & API](https://corso-api-json.giuseppebosi.com/)',
		'- [Corso pratico di llama.cpp](https://corso-llamacpp.giuseppebosi.com/)',
		'- [Costruisci la tua memoria AI](https://corso-rag.giuseppebosi.com/)',
		'',
	);
	return new Response(righe.join('\n'), {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
