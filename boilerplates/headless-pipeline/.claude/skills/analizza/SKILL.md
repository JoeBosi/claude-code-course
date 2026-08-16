---
name: analizza
description: Il prompt di analisi della pipeline. Invocato da bin/02-analyze.sh, non a mano.
disable-model-invocation: true
---

Ricevi su stdin i dati grezzi raccolti dallo stadio 01.

Produci un'analisi conforme allo schema che ti è stato passato con `--json-schema`.

## Regole

1. **Non ripetere i dati.** Chi legge il report ha già accesso ai dati grezzi. Il tuo
   valore è la sintesi e il giudizio, non la trascrizione.

2. **Ogni affermazione deve essere ancorata.** Il campo `prova` di ogni rilievo deve citare
   qualcosa di verificabile nei dati in ingresso: un identificatore, una data, un valore.
   **Se non puoi citarlo, non affermarlo.**

3. **Gravità.** Usa `alta` solo per ciò che richiede un intervento oggi. Se tutto è `alta`,
   niente è `alta`.

4. **Assenza di rilievi è un risultato valido.** Un array `rilievi` vuoto è una risposta
   corretta. Non riempirlo per sembrare utile.

5. **Niente raccomandazioni generiche.** "Monitorare la situazione" non è un'azione.
   Se suggerisci qualcosa, deve essere qualcosa che si può fare.

## Se i dati sono incompleti

Se lo stadio 01 ha raccolto meno del previsto — un endpoint non ha risposto, un file è
vuoto — dillo nel campo `sintesi` e riduci la fiducia dei rilievi di conseguenza.
**Non compensare inventando.**
