---
description: Prepara la modifica corrente per il rilascio: verifica, commit, push e apertura della PR.
argument-hint: "[descrizione della modifica]"
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(npm run typecheck), Bash(npm run lint*), Bash(npm test*), Bash(gh pr *)
---

## Stato corrente

!`git status --short`

## Commit sul branch

!`git log --oneline origin/main..HEAD`

## Istruzioni

Porta questa modifica fino alla pull request, **fermandoti al primo passo che fallisce**.

1. **Verifica.** Nell'ordine: `npm run typecheck`, `npm run lint`, `npm test`.
   Se uno fallisce, **fermati e riporta l'errore**. Non correggere di tua iniziativa:
   la correzione è una decisione dell'utente.

2. **Branch.** Se sei su `main`, crea un branch prima di committare.
   Nome: `tipo/descrizione-breve`, per esempio `feat/billing-webhook`.

3. **Commit.** Conventional commit, in inglese, minuscolo dopo il prefisso.
   Il corpo spiega **perché**, non cosa: il cosa si legge dalla diff.

4. **Push** con `-u` se il branch è nuovo.

5. **Pull request** con `gh pr create`. Corpo in italiano, con esattamente queste sezioni:

   ### Cosa cambia
   Due o tre bullet, dal punto di vista di chi usa il prodotto.

   ### Perché
   Una frase. Se c'è una issue collegata, linkala.

   ### Come verificarlo
   Passi concreti che il revisore può eseguire.

   ### Rischi
   Cosa può rompersi. Se niente, scrivi "nessuno noto" e spiega perché.

6. **Riporta l'URL della PR.**

Contesto aggiuntivo dall'utente: $ARGUMENTS
