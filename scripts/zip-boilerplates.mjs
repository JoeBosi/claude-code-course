/**
 * Impacchetta ogni cartella in `boilerplates/` in uno zip scaricabile da `public/downloads/`.
 * Girato automaticamente da `npm run prebuild`, così il sito non contiene mai zip obsoleti.
 */
import { execFile } from 'node:child_process';
import { mkdir, readdir, rm } from 'node:fs/promises';
import { promisify } from 'node:util';

const run = promisify(execFile);

const SORGENTE = 'boilerplates';
const DESTINAZIONE = 'public/downloads';

// Non finiscono mai in uno zip consegnato all'utente.
const ESCLUSI = ['*/node_modules/*', '*/.git/*', '*/dist/*', '*/.DS_Store', '*/__pycache__/*', '*/.venv/*'];

const cartelle = await readdir(SORGENTE, { withFileTypes: true })
	.then((voci) => voci.filter((v) => v.isDirectory()).map((v) => v.name))
	.catch(() => []);

if (cartelle.length === 0) {
	console.log(`[zip-boilerplates] nessuna cartella in ${SORGENTE}/, niente da fare.`);
	process.exit(0);
}

await mkdir(DESTINAZIONE, { recursive: true });

for (const nome of cartelle) {
	const zip = `../${DESTINAZIONE}/${nome}.zip`;
	// `zip` non sovrascrive: rimuoviamo prima per evitare archivi che accumulano file rimossi.
	await rm(`${DESTINAZIONE}/${nome}.zip`, { force: true });
	await run('zip', ['-r', '-q', '-X', zip, nome, '-x', ...ESCLUSI], { cwd: SORGENTE });
	console.log(`[zip-boilerplates] ${DESTINAZIONE}/${nome}.zip`);
}

console.log(`[zip-boilerplates] ${cartelle.length} boilerplate impacchettati.`);
