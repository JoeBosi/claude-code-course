# Revisione per la divulgazione pubblica — claude-tutorial.giuseppebosi.com

Data: 28/10/2026. Richiesta del Controller (Giuseppe, 27/10). Verifiche fatte sul repo e sul sito live.

## Stato di fatto (diverso dalla premessa del compito)

- **Il sito è GIÀ pubblico, senza password.** Nessun blocco nel Caddyfile del VPS: il sito sta su
  **Vercel**, non dietro Caddy. Non esiste alcun `basic_auth` né utenti di prova da togliere.
- Il sito risponde anche su **claude-tutorial-ten.vercel.app** (indirizzo tecnico di Vercel, sempre
  aperto): un eventuale limite di 5 visitatori fatto con Caddy sul dominio custom sarebbe **aggirabile**
  da quell'indirizzo. Se il limite servirà davvero, va deciso come (vedi rischi, punto 5).

## 1. Revisione come opera di divulgazione

**Giudizio complessivo: fatto bene.** 20 moduli + glossario (64 voci) + pagina "Le basi"; doppio
binario (sviluppatori / principianti) con box "Se parti da zero"; ogni modulo dichiara fonti ufficiali
e data di verifica; ricerca interna; 3 boilerplate scaricabili testati; 4 test di lettura con persona
non programmatrice già fatti e corretti a settembre.

**Link:** ricontrollati oggi tutti i link esterni (116 unici). Nessun link rotto. I non-200 sono:
placeholder didattici voluti (`example.com`, `tuo-utente`), endpoint MCP che rispondono 401 perché
chiedono login (corretto così), e 7 URL con 403 anti-bot da IP datacenter (claude.ai, npmjs,
pulsemcp) già verificati a mano in agosto: non sono morti.

**Parti datate (non errate):** i contenuti dichiarano "verificato il 16 agosto 2026". Oggi sono
passati 2 mesi e mezzo: le **versioni dei pacchetti nel modulo 17** (Next.js 16.3.1, Astro 7.2.2…)
e i numeri delle directory MCP nel modulo 16 sono quasi certamente superati. Non è un errore (la data
è dichiarata), ma per un'opera citata nel CV conviene un giro di ri-verifica periodico.

**Diciture mancanti (le proposte, in ordine di importanza):**

1. **Autore e data di aggiornamento** nel footer: "Un corso di Giuseppe Bosi · ultimo aggiornamento
   28/10/2026". Oggi il sito non dice da nessuna parte di chi è: per il CV è la riga che conta di più.
2. **Avvertenza IA**: "Contenuti prodotti con l'aiuto dell'IA (Claude) e rivisti dall'autore;
   verificati sulla documentazione ufficiale alle date indicate in ogni modulo."
3. **Non affiliazione**: già presente nel footer ("Corso indipendente, non affiliato ad Anthropic o
   Google…"). Ok così, nessuna modifica necessaria.
4. **Copyright/licenza**: aggiungere "© 2026 Giuseppe Bosi". Per la licenza dei contenuti propongo
   **CC BY-NC-SA 4.0** (riuso non commerciale con attribuzione): è la scelta tipica per la
   divulgazione, ma è una concessione di diritti **irreversibile** → la applico solo dopo conferma
   esplicita di Giuseppe. Intanto metto il solo ©, che non concede nulla.
5. **Privacy/cookie**: il sito è statico, senza analytics, senza form, senza cookie. Basta una riga
   nel footer: "Questo sito non usa cookie e non raccoglie dati personali." (Niente banner: non serve.)
6. **Contatti**: `info@giuseppebosi.com` (la casella dei progetti, non il Gmail personale).
7. (Facoltativo, dopo) Rendere pubblico il repo GitHub e riattivare l'icona nell'header: per
   un'opera di divulgazione il sorgente aperto rafforza la citazione nel CV. Decisione di Giuseppe.

## 2. Rischi dell'apertura al pubblico

Superficie minima: **sito statico**, nessuna API propria, nessun backend, nessun form, nessun
cookie, nessun database. In dettaglio:

1. **Segreti/chiavi: nessuno.** Scansione fatta su repo e zip: solo `.env.example` con segnaposto.
   Il repo è privato; nei contenuti non ci sono percorsi di macchine reali.
2. **Dati personali: nessuno** sul sito (solo il dominio giuseppebosi.com e, dopo le modifiche, nome
   dell'autore e mail di progetto — voluti).
3. **Costi/banda (il rischio concreto):** il piano Vercel gratuito ha ~100 GB/mese. Gli zip pesano
   ~54 KB in tutto: anche un abuso di download costa poco. In caso di traffico anomalo Vercel
   **sospende** il sito (non fattura): fastidio, non costo. Mitigazione possibile più avanti:
   firewall/rate-limit di Vercel.
4. **basic_auth / utenti di prova: non esistono** (vedi stato di fatto). Niente da bonificare.
5. **Limite 5 visitatori:** con l'hosting attuale (Vercel) Caddy non c'entra; e il dominio vercel.app
   resta comunque aperto. Opzioni se servirà: spostare l'hosting dietro Caddy sul VPS (allora il
   limite si fa lì e si disattiva il dominio vercel.app), oppure rinunciare al limite (per un sito
   statico non serve a proteggere nulla). Decisione del Controller/Giuseppe: **non tocco nulla**.
6. **Abusi sui contenuti:** il corso insegna comandi potenti (hook, pipeline) ma su macchina del
   lettore; nessun esempio punta a sistemi di Giuseppe. Ok.

## Cosa sistemare prima di aprire

Niente di bloccante: il sito è di fatto già aperto e non espone nulla. Le diciture 1-2-4-5-6 sono
state applicate (vedi commit); la licenza CC e il repo pubblico aspettano l'ok esplicito di Giuseppe.
