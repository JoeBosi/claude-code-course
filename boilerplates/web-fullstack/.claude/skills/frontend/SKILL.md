---
name: frontend
description: Convenzioni per i componenti React e le Server Action di questo progetto. Usala quando scrivi o modifichi qualcosa sotto src/components/ o src/features/.
---

# Convenzioni frontend

## Server e client

- **Server Component di default.** Aggiungi `"use client"` solo quando servono stato,
  effetti o handler di eventi del browser
- Se un componente ha bisogno di `"use client"` solo per un pulsante, estrai il pulsante
  in un componente client e lascia il resto sul server
- I dati si leggono nei Server Component o in `features/<x>/queries.ts`, mai con `useEffect`

## Server Action

Ogni action segue questa forma, senza eccezioni:

```ts
"use server";

import { creaProgetto } from "./schema";

export async function creaProgettoAction(input: unknown) {
  // 1. sessione — sempre, anche se il layout la verifica già
  const utente = await requireUtente();

  // 2. validazione — prima di toccare il database
  const dati = creaProgetto.parse(input);

  // 3. lavoro
  // 4. revalidate del percorso interessato
}
```

I tre passi in quest'ordine. Un'action che valida dopo aver letto dal database è un bug.

## Struttura di una feature

```
src/features/<capacita>/
├── schema.ts     # schemi Zod, condivisi tra actions e queries
├── queries.ts    # letture
└── actions.ts    # mutazioni
```

Lo schema è la fonte di verità dei tipi: i tipi si derivano da lì con `z.infer`, non si
riscrivono a mano.

## Stile

- Tailwind. Niente CSS modules, niente styled-components
- Classi condizionali con `cn()` da `src/lib/utils.ts`
- Niente valori magici: spaziature e colori vengono dal tema

## Accessibilità

- Ogni elemento interattivo è raggiungibile da tastiera
- Ogni input ha una `<label>` associata
- Gli stati di caricamento e di errore sono annunciati, non solo visivi
