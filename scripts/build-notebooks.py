#!/usr/bin/env python3
"""Genera i notebook Colab (notebooks/*.ipynb, IT e EN) a partire dagli script dei moduli.

Gli script (hooks, gate.sh, migra.sh...) vengono letti direttamente dai file .mdx italiani,
cosi il notebook non puo divergere dal testo del corso. Uso: python3 scripts/build-notebooks.py
"""
import json, re, textwrap, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "src/content/docs"


def block(mdx, line):
    """Restituisce il contenuto (dedentato) del blocco di codice che inizia alla riga `line`."""
    L = (DOCS / mdx).read_text().split("\n")
    i = line - 1
    assert L[i].lstrip().startswith("```"), (mdx, line, L[i])
    j = i + 1
    while not re.match(r"^\s*```\s*$", L[j]):
        j += 1
    return textwrap.dedent("\n".join(L[i + 1:j])) + "\n"


def find_block(mdx, title):
    L = (DOCS / mdx).read_text().split("\n")
    for n, l in enumerate(L, 1):
        if l.lstrip().startswith("```") and f'title="{title}"' in l:
            return block(mdx, n)
    raise KeyError(title)


def find_containing(mdx, needle):
    """Blocco di codice che contiene `needle` (indipendente dai numeri di riga)."""
    L = (DOCS / mdx).read_text().split("\n")
    hits = [n for n, l in enumerate(L, 1)
            if l.lstrip().startswith("```") and needle in "\n".join(L[n:n + 60]).split("```")[0]]
    assert len(hits) == 1, (mdx, needle, hits)
    return block(mdx, hits[0])


def find_by_first_line(mdx, first):
    L = (DOCS / mdx).read_text().split("\n")
    for n, l in enumerate(L, 1):
        if l.lstrip().startswith("```") and n < len(L) and L[n].strip() == first:
            return block(mdx, n)
    raise KeyError(first)


def md(t):
    return {"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(t).strip("\n").splitlines(True)}


def code(t):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": textwrap.dedent(t).strip("\n").splitlines(True)}


def save(name, lang, cells, badge_note):
    nb = {"cells": cells,
          "metadata": {"colab": {"provenance": [], "name": f"{name}-{lang}.ipynb"},
                       "kernelspec": {"name": "python3", "display_name": "Python 3"},
                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 5}
    (ROOT / "notebooks" / f"{name}-{lang}.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


def wf(name, content):
    return code(f"%%writefile {name}\n{content}")


T = {
 "it": dict(
  run="Esegui le celle dall'alto verso il basso (Maiusc+Invio su ognuna).",
  see="Cosa dovresti vedere", ),
 "en": dict(
  run="Run the cells from top to bottom (Shift+Enter on each).",
  see="What you should see"),
}

# ---------------------------------------------------------------- 1. hooks
H = "personalizzazione/hooks.mdx"
block_rm = find_containing(H, "COMMAND=$(jq -r '.tool_input.command')")
protect = find_containing(H, 'case "$FILE" in')
testsh = find_containing(H, "qui manca la")
ctx = find_containing(H, "git branch --show-current")
gate_stop = find_containing("professionale/workflow.mdx", "git diff --quiet &&")

SETUP_HOOKS = """
%%bash
# jq e lo strumento che gli hook usano per leggere il JSON dell'evento
which jq >/dev/null || (apt-get -qq update && apt-get -qq install -y jq >/dev/null)
which npm >/dev/null || (apt-get -qq update && apt-get -qq install -y nodejs npm >/dev/null)
rm -rf /tmp/hooks-demo && mkdir -p /tmp/hooks-demo/.claude/hooks && cd /tmp/hooks-demo
git init -q . && git config user.email demo@example.com && git config user.name demo
jq --version; npm --version
"""

def hooks(lang):
    it = lang == "it"
    c = []
    c.append(md(f"""
    # {'Prova gli hook senza Claude Code' if it else 'Try the hooks without Claude Code'}
    {'Modulo *Hooks*, esercizio. Gli hook sono script che Claude Code lancia passando un JSON su stdin. Qui il JSON lo scrivi tu: così vedi, senza installare nulla e senza account, cosa risponde ogni hook.' if it else 'Module *Hooks*, exercise. Hooks are scripts that Claude Code runs, passing a JSON on stdin. Here you write the JSON yourself: so you see what each hook answers, with nothing to install and no account.'}

    {T[lang]['run']}
    """))
    c.append(code(SETUP_HOOKS))
    c.append(md("## 1. " + ("Hook che blocca `rm -rf`" if it else "Hook that blocks `rm -rf`")))
    c.append(wf("/tmp/hooks-demo/.claude/hooks/block-rm.sh", block_rm))
    c.append(code("""
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    echo '--- rm -rf build/ ---'
    echo '{"tool_input":{"command":"rm -rf build/"}}' | .claude/hooks/block-rm.sh; echo "exit code: $?"
    echo '--- ls ---'
    echo '{"tool_input":{"command":"ls"}}' | .claude/hooks/block-rm.sh; echo "exit code: $?"
    """))
    c.append(md(("Nel primo caso vedi un JSON con `permissionDecision: deny` e il motivo; nel secondo non stampa nulla (nessuna decisione, si applica il normale flusso dei permessi). In entrambi i casi l'exit code è 0." if it else "In the first case you see a JSON with `permissionDecision: deny` and the reason; in the second it prints nothing (no decision, the normal permission flow applies). The exit code is 0 in both cases.")))
    c.append(md("## 2. " + ("Hook che protegge le migrazioni" if it else "Hook that protects migrations")))
    c.append(wf("/tmp/hooks-demo/.claude/hooks/protect-migrations.sh", protect))
    c.append(code("""
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    echo '--- file in db/migrations ---'
    echo '{"tool_input":{"file_path":"/p/db/migrations/001.sql"}}' | .claude/hooks/protect-migrations.sh
    echo '--- file in src ---'
    echo '{"tool_input":{"file_path":"/p/src/app.js"}}' | .claude/hooks/protect-migrations.sh; echo "exit code: $?"
    """))
    c.append(md("## 3. " + ("Hook che lancia i test e riporta i fallimenti" if it else "Hook that runs the tests and reports failures")))
    c.append(wf("/tmp/hooks-demo/.claude/hooks/test.sh", testsh))
    c.append(code("""
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    # un "progetto" finto il cui test fallisce
    echo '{"name":"demo","scripts":{"test":"echo TEST FALLITO: atteso 200, ricevuto 500; exit 1"}}' > package.json
    echo '{"tool_input":{"file_path":"src/app.js"}}' | .claude/hooks/test.sh 2>&1; echo "exit code: $?"
    """.replace("TEST FALLITO: atteso 200, ricevuto 500", "TEST FAILED: expected 200, got 500") if not it else """
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    # un "progetto" finto il cui test fallisce
    echo '{"name":"demo","scripts":{"test":"echo TEST FALLITO: atteso 200, ricevuto 500; exit 1"}}' > package.json
    echo '{"tool_input":{"file_path":"src/app.js"}}' | .claude/hooks/test.sh 2>&1; echo "exit code: $?"
    """))
    c.append(md(("Exit code **2** e l'output del test su stderr: è il segnale con cui Claude Code rimanda l'errore a Claude. Se `package.json` avesse `\"test\": \"exit 0\"` l'hook uscirebbe con 0 senza stampare nulla." if it else "Exit code **2** and the test output on stderr: that is the signal Claude Code uses to send the error back to Claude. If `package.json` had `\"test\": \"exit 0\"` the hook would exit 0 and print nothing.")))
    c.append(md("## 4. " + ("Hook all'avvio della sessione" if it else "Hook at session start")))
    c.append(wf("/tmp/hooks-demo/.claude/hooks/context.sh", ctx))
    c.append(code("""
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    .claude/hooks/context.sh
    """))
    c.append(md(("Vedi un JSON con `additionalContext`: branch, numero di file modificati e stato dell'ultima CI. Qui la CI risulta «sconosciuto» perché nel notebook non c'è la CLI `gh` collegata a un repository GitHub." if it else "You see a JSON with `additionalContext`: branch, number of modified files and the status of the last CI run. Here the CI shows \"sconosciuto\" (unknown) because the notebook has no `gh` CLI connected to a GitHub repository.")))
    c.append(md("## 5. " + ("Hook `Stop`: non chiudere il turno se i test falliscono" if it else "`Stop` hook: do not end the turn if tests fail")))
    c.append(wf("/tmp/hooks-demo/.claude/hooks/gate.sh", gate_stop))
    c.append(code("""
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    echo "// base" > app.js
    git add -A && git commit -qm "base"
    echo '--- niente di nuovo da verificare ---'
    .claude/hooks/gate.sh 2>&1; echo "exit code: $?"
    echo '--- modifica + test che fallisce ---'
    echo "// modifica" >> app.js
    .claude/hooks/gate.sh 2>&1; echo "exit code: $?"
    """ if it else """
    %%bash
    cd /tmp/hooks-demo && chmod +x .claude/hooks/*.sh
    echo "// base" > app.js
    git add -A && git commit -qm "base"
    echo '--- nothing new to verify ---'
    .claude/hooks/gate.sh 2>&1; echo "exit code: $?"
    echo '--- change + failing test ---'
    echo "// change" >> app.js
    .claude/hooks/gate.sh 2>&1; echo "exit code: $?"
    """))
    c.append(md(("Prima volta: nessuna modifica rispetto all'ultimo commit, exit 0 senza output. Seconda: il test fallisce, le righe finali dell'output vanno su stderr ed exit **2** significa «non chiudere il turno, continua a lavorare»." if it else "First run: no change since the last commit, exit 0 with no output. Second run: the test fails, the last lines of the output go to stderr and exit **2** means \"do not end the turn, keep working\".")))
    return c

# ---------------------------------------------------------------- 2. script con claude finto
CLI = "automazione/cli-scripting.mdx"
gate_sh = find_block(CLI, "gate.sh")
PL = "automazione/pipeline-locali.mdx"
migra_sh = find_block(PL, "migra.sh")

STUB = r'''#!/usr/bin/env bash
# "claude" FINTO, solo per questo notebook: non chiama nessuna IA.
# Legge stdin e restituisce una risposta JSON preconfezionata, come farebbe `claude -p --output-format json`.
[ -t 0 ] || cat > /dev/null
[ "${CLAUDE_FINTO_FALLISCE:-0}" = 1 ] && exit 1
case "$*" in
  *Migrate*)
     # per la migrazione: risponde OK, tranne per i file con "rotto" nel nome
     case "$*" in *rotto*) echo "FAIL";; *) echo "OK";; esac ;;
  *)
     echo '{"is_error":false,"permission_denials":[],"total_cost_usd":0.01,"structured_output":{"bloccanti":[{"file":"app.py","riga":3,"problema":"divisione per zero","scenario":"con b = 0 la funzione solleva ZeroDivisionError"}]}}' ;;
esac
'''

def automazione(lang):
    it = lang == "it"
    c = []
    c.append(md(f"""
    # {'Prova gli script di automazione con un `claude` finto' if it else 'Try the automation scripts with a fake `claude`'}
    {"Moduli *Scripting da CLI* e *Pipeline locali*, esercizi. Per usare Claude Code servono un abbonamento o una API key, e questo notebook non ne usa. Qui un piccolo programma chiamato `claude` risponde sempre con una risposta JSON preconfezionata. Gli script del corso (`gate.sh`, `migra.sh`) girano **davvero**: vedi gli exit code, i file di marcatura e il riprova dei file falliti. Cambia solo l'IA, che è finta." if it else "Modules *CLI scripting* and *Local pipelines*, exercises. Using Claude Code needs a subscription or an API key, and this notebook uses none. Here a small program called `claude` always answers with a canned JSON response. The course scripts (`gate.sh`, `migra.sh`) run **for real**: you see the exit codes, the marker files and the retry of failed files. Only the AI is fake."}

    {T[lang]['run']}
    """))
    c.append(code("""
    %%bash
    which jq >/dev/null || (apt-get -qq update && apt-get -qq install -y jq >/dev/null)
    mkdir -p /tmp/finto /tmp/lab
    jq --version
    """))
    c.append(wf("/tmp/finto/claude", STUB))
    c.append(code("""
    import os
    os.chmod('/tmp/finto/claude', 0o755)
    os.environ['PATH'] = '/tmp/finto:' + os.environ['PATH']   # ora "claude" è quello finto
    """))
    c.append(md("## 1. " + ("`gate.sh`: la review come cancello di qualità" if it else "`gate.sh`: the review as a quality gate")))
    c.append(code("""
    %%bash
    # un mini repository con un branch "feature" che modifica un file
    rm -rf /tmp/lab/repo && mkdir -p /tmp/lab/repo && cd /tmp/lab/repo
    git init -q -b main . && git config user.email demo@example.com && git config user.name demo
    printf 'def dividi(a, b):\\n    return a / b\\n' > app.py
    git add . && git commit -qm base
    git checkout -qb feature
    printf '\\n# modifica\\n' >> app.py && git commit -qam modifica
    git log --oneline
    """ if it else """
    %%bash
    # a mini repository with a "feature" branch that changes a file
    rm -rf /tmp/lab/repo && mkdir -p /tmp/lab/repo && cd /tmp/lab/repo
    git init -q -b main . && git config user.email demo@example.com && git config user.name demo
    printf 'def divide(a, b):\\n    return a / b\\n' > app.py
    git add . && git commit -qm base
    git checkout -qb feature
    printf '\\n# change\\n' >> app.py && git commit -qam change
    git log --oneline
    """))
    c.append(wf("/tmp/lab/gate.sh", gate_sh))
    c.append(code("""
    %%bash
    cd /tmp/lab/repo && chmod +x /tmp/lab/gate.sh
    echo '--- 1) il finto claude trova un problema ---'
    /tmp/lab/gate.sh main 2>&1; echo "exit: $?"
    echo
    echo '--- 2) claude non riesce a girare ---'
    CLAUDE_FINTO_FALLISCE=1 /tmp/lab/gate.sh main 2>&1; echo "exit: $?"
    echo
    echo '--- 3) nessuna differenza da verificare ---'
    git checkout -q main
    /tmp/lab/gate.sh main 2>&1; echo "exit: $?"
    """ if it else """
    %%bash
    cd /tmp/lab/repo && chmod +x /tmp/lab/gate.sh
    echo '--- 1) the fake claude finds a problem ---'
    /tmp/lab/gate.sh main 2>&1; echo "exit: $?"
    echo
    echo '--- 2) claude cannot run ---'
    CLAUDE_FINTO_FALLISCE=1 /tmp/lab/gate.sh main 2>&1; echo "exit: $?"
    echo
    echo '--- 3) no difference to verify ---'
    git checkout -q main
    /tmp/lab/gate.sh main 2>&1; echo "exit: $?"
    """))
    c.append(md(("Tre esiti, tre exit code diversi: **1** = la review ha trovato problemi, **2** = lo strumento non ha funzionato, **0** = niente da segnalare. Una CI deve poterli distinguere." if it else "Three outcomes, three different exit codes: **1** = the review found problems, **2** = the tool did not work, **0** = nothing to report. A CI must be able to tell them apart.")))
    c.append(md("## 2. " + ("`migra.sh`: migrazione a lotti, riprendibile" if it else "`migra.sh`: batch migration, resumable")))
    c.append(wf("/tmp/lab/migra.sh", migra_sh))
    c.append(code("""
    %%bash
    rm -rf /tmp/lab/batch && mkdir -p /tmp/lab/batch/src && cd /tmp/lab/batch
    # quattro file da "migrare"; quello con "rotto" nel nome fa fallire il finto claude
    printf 'src/app.py\\nsrc/my_utils.py\\nsrc/rotto_config.py\\nsrc/db.py\\n' > files.txt
    chmod +x /tmp/lab/migra.sh
    /tmp/lab/migra.sh files.txt 2
    """))
    c.append(md(("Tre file riusciti (`ok`) e uno fallito (`FAIL`). Nota che `src/my_utils.py` ha un underscore nel nome: la lista di retry lo ricostruisce correttamente perché ogni marcatore di fallimento contiene il percorso vero." if it else "Three files succeeded (`ok`) and one failed (`FAIL`). Note that `src/my_utils.py` has an underscore in its name: the retry list rebuilds it correctly because each failure marker holds the real path.")))
    c.append(code("""
    %%bash
    cd /tmp/lab/batch
    echo '--- secondo giro: i file già fatti vengono saltati (idempotenza) ---'
    /tmp/lab/migra.sh files.txt 2
    echo
    echo '--- lista di retry ---'
    cat .migrazione/fail/* | tee retry.txt
    """ if it else """
    %%bash
    cd /tmp/lab/batch
    echo '--- second round: files already done are skipped (idempotence) ---'
    /tmp/lab/migra.sh files.txt 2
    echo
    echo '--- retry list ---'
    cat .migrazione/fail/* | tee retry.txt
    """))
    c.append(md(("Al secondo giro vedi `skip` per i tre file riusciti e `FAIL` solo per quello rotto. `retry.txt` contiene il solo percorso fallito, pronto per `./migra.sh retry.txt`." if it else "In the second round you see `skip` for the three successful files and `FAIL` only for the broken one. `retry.txt` holds only the failed path, ready for `./migra.sh retry.txt`.")))
    return c

# ---------------------------------------------------------------- 3. registry MCP
def registry(lang):
    it = lang == "it"
    c = []
    c.append(md(f"""
    # {'Interroga il registry ufficiale dei server MCP' if it else 'Query the official MCP server registry'}
    {"Modulo *Ecosistema*. Il registry ufficiale ha un'API pubblica, senza chiave e senza account: la chiami con `curl` o con Python. In questo notebook lo fai in due modi." if it else "Module *Ecosystem*. The official registry has a public API, no key and no account: you call it with `curl` or with Python. In this notebook you do it in two ways."}

    {T[lang]['run']}
    """))
    c.append(md("## 1. curl + jq"))
    c.append(code("""
    %%bash
    which jq >/dev/null || (apt-get -qq update && apt-get -qq install -y jq >/dev/null)
    curl -s "https://registry.modelcontextprotocol.io/v0/servers?limit=100&search=postgres" \\
      | jq -r '.servers[].server.name' | sort -u
    """))
    c.append(md(("Un elenco di nomi nel formato `dominio/nome-del-server`. L'elenco cambia nel tempo: conta il formato, non i nomi esatti." if it else "A list of names in the format `domain/server-name`. The list changes over time: what matters is the format, not the exact names.")))
    c.append(md("## 2. Python"))
    c.append(md(("Molte API rifiutano le richieste senza un `User-Agent` (la «firma» del programma che chiama) e rispondono 403. Questa no, ma indicarlo è una buona abitudine: costa una riga." if it else "Many APIs reject requests without a `User-Agent` (the \"signature\" of the calling program) and answer 403. This one does not, but setting it is a good habit: it costs one line.")))
    c.append(code("""
    %pip install -q requests
    import requests

    URL = "https://registry.modelcontextprotocol.io/v0/servers"
    risposta = requests.get(
        URL,
        params={"limit": 100, "search": "dbhub"},
        headers={"User-Agent": "claude-code-course-notebook/1.0"},
        timeout=30,
    )
    print("HTTP", risposta.status_code)
    nomi = sorted({s["server"]["name"] for s in risposta.json()["servers"]})
    for nome in nomi:
        print(nome)
    """ if it else """
    %pip install -q requests
    import requests

    URL = "https://registry.modelcontextprotocol.io/v0/servers"
    response = requests.get(
        URL,
        params={"limit": 100, "search": "dbhub"},
        headers={"User-Agent": "claude-code-course-notebook/1.0"},
        timeout=30,
    )
    print("HTTP", response.status_code)
    names = sorted({s["server"]["name"] for s in response.json()["servers"]})
    for name in names:
        print(name)
    """))
    c.append(md(("Vedi `HTTP 200` e, tra i nomi, `io.github.bytebase/dbhub`: è il server DBHub scelto nell'esempio del modulo." if it else "You see `HTTP 200` and, among the names, `io.github.bytebase/dbhub`: the DBHub server chosen in the module's example.")))
    return c

# ---------------------------------------------------------------- 4. boilerplate agentic-rag
def boiler(lang):
    it = lang == "it"
    c = []
    c.append(md(f"""
    # {'Scarica il boilerplate agentic-rag e fai passare i test' if it else 'Download the agentic-rag boilerplate and run its tests'}
    {"Modulo *Boilerplate*, esempio guidato (passi 1-4). Scarichi lo zip dal sito del corso, lo inizializzi e lanci i sette test Python. Non serve Claude Code né un account." if it else "Module *Boilerplate*, guided example (steps 1-4). You download the zip from the course site, initialise it and run the seven Python tests. No Claude Code and no account needed."}

    {T[lang]['run']}
    """))
    c.append(code("""
    %%bash
    rm -rf /tmp/boiler && mkdir /tmp/boiler && cd /tmp/boiler
    curl -fsSL -O https://claude-tutorial.giuseppebosi.com/downloads/agentic-rag.zip
    unzip -q agentic-rag.zip && cd agentic-rag
    ls -A
    """))
    c.append(code("""
    %%bash
    cd /tmp/boiler/agentic-rag
    ./init.sh "kb-interna" "Base di conoscenza interna sui runbook"
    """ if it else """
    %%bash
    cd /tmp/boiler/agentic-rag
    ./init.sh "internal-kb" "Internal knowledge base on runbooks"
    """))
    c.append(code("""
    %pip install -q uv
    """))
    c.append(code("""
    %%bash
    cd /tmp/boiler/agentic-rag
    uv sync 2>&1 | tail -3
    uv run pytest
    """))
    c.append(md(("In fondo vedi `7 passed`: sette test, tra cui quello che verifica che il dominio non importi librerie esterne." if it else "At the bottom you see `7 passed`: seven tests, including the one that checks that the domain does not import external libraries.")))
    return c

NBS = {"hooks-playground": hooks, "script-automazione-claude-finto": automazione,
       "registry-mcp": registry, "boilerplate-agentic-rag": boiler}

if __name__ == "__main__":
    (ROOT / "notebooks").mkdir(exist_ok=True)
    for name, fn in NBS.items():
        for lang in ("it", "en"):
            save(name, lang, fn(lang), "")
    print("notebook generati:", len(NBS) * 2)
