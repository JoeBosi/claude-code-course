/** true se la pagina corrente sta sotto /en/ (versione inglese del corso). */
export const isInglese = (url: URL) => url.pathname === '/en' || url.pathname.startsWith('/en/');
