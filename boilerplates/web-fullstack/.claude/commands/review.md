---
description: Rivede la diff corrente cercando solo difetti di correttezza e sicurezza. Usalo prima di aprire una PR.
argument-hint: "[branch-base]"
disable-model-invocation: true
allowed-tools: Bash(git diff *), Bash(git log *), Bash(git status *), Read, Grep, Glob
---

## Diff da rivedere

!`git diff ${ARGUMENTS:-origin/main}...HEAD`

## File toccati

!`git diff ${ARGUMENTS:-origin/main}...HEAD --name-only`

## Istruzioni

Rivedi la diff qui sopra. Cerca **solo** questo, in quest'ordine:

1. **Sicurezza**
   - Tabelle nuove senza policy RLS
   - Uso della service role key fuori da `src/app/api/webhooks/`
   - Input di Server Action non validato con lo schema Zod prima di toccare il database
   - Segreti, chiavi o URL con credenziali finiti nel codice

2. **Correttezza**
   - Sessione non verificata in una Server Action
   - Casi limite non gestiti che producono un errore visibile all'utente
   - Migrazioni già applicate che sono state modificate invece di aggiunte

3. **Regressioni**
   - Comportamento esistente che questa diff rompe

Per ogni rilievo dai: **file:riga**, il problema in una frase, e uno **scenario di
fallimento concreto** — input, stato, cosa va storto.

Un rilievo senza scenario di fallimento non è un rilievo: non riportarlo.

**Non** segnalare stile, naming, formattazione, o "si potrebbe astrarre". Se non trovi
nulla che tocca sicurezza o correttezza, rispondi in una riga che la diff è pulita.
