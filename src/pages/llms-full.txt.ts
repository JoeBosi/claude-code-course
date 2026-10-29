import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const SITE = 'https://claude-tutorial.giuseppebosi.com';

// Il sorgente MDX di ogni pagina così com'è: i componenti (Tabs, Zero...)
// restano come tag, ma testo, comandi e codice sono completi.
export const GET: APIRoute = async () => {
	const pagine = (await getCollection('docs'))
		.filter((p) => p.id !== '404')
		.sort((a, b) => a.id.localeCompare(b.id, 'it', { numeric: true }));
	const blocchi = pagine.map((p) => {
		const url = p.id === 'index' ? `${SITE}/` : `${SITE}/${p.id}/`;
		return `# ${p.data.title}\n\nURL: ${url}\n\n${p.data.description ?? ''}\n\n${p.body ?? ''}`;
	});
	return new Response(blocchi.join('\n\n---\n\n'), {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
