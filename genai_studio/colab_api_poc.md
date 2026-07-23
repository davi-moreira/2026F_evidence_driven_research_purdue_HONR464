# Colab API proof-of-concept — calling GenAI Studio roles from a notebook

*A documented, copy-paste cell sequence that calls a GenAI Studio reviewer role
from Google Colab through the OpenAI-compatible API, keeps your key in Colab
Secrets, fails gracefully, and prints a pre-filled AI Research Ledger row. This is
the **level-4 enhancement** path. The **manual UI path** at the bottom is equal in
standing and is the guaranteed way every milestone touchpoint works.*

---

## Before you start: which path are you on?

There are two ways to consult a reviewer role, and **neither is second-class**:

- **Manual UI (guaranteed).** A browser and your Purdue login. Every M5/M7/M9/M13
  touchpoint is designed to work this way. Jump to *Manual-UI fallback* below.
- **API / Colab (this document, an enhancement).** Lets you call a role from code
  and script the Week-16 sequence. It needs a personal API key, which the
  instructor confirms is available during setup (the open item). If your key does
  not work, you lose nothing essential — use the UI.

Read the whole document before running it. Every cell is written to paste into a
fresh Colab notebook in order.

---

## ⚠️ Two rules that never bend

1. **Never put your API key in code.** Not in a cell, not in a variable literal,
   not in a `.env` file. In Colab, keys live in **Secrets** (the 🔑 icon in the
   left sidebar). A key pasted into a cell is exposed the moment you share or
   publish the notebook.
2. **Never send personal data to a role.** No student data, no survey responses,
   no identifying information about research subjects. You are sending text to a
   Purdue-hosted model, but the course rule is the same as for the knowledge base:
   course-authored and your own de-identified material only.

---

## Cell 1 — Configuration (no secrets in code)

```python
# Cell 1 — configuration. Reads your key from Colab Secrets; nothing sensitive
# is ever written in this notebook.
#
# One-time setup before running this cell:
#   1. In Colab, click the key icon (🔑) in the left sidebar to open "Secrets".
#   2. Add a secret named exactly:  GENAI_API_KEY
#      Its value is the key you generated in GenAI Studio under
#      Settings -> Account. Do NOT type the key anywhere in this notebook.
#   3. Toggle "Notebook access" on for that secret.

from google.colab import userdata

BASE_URL = "https://genai.rcac.purdue.edu"
API_URL  = f"{BASE_URL}/api/chat/completions"   # OpenAI-compatible endpoint

# Set MODEL to the EXACT model id shown in your GenAI Studio model list.
# GenAI Studio serves open-source models (the LLaMA family; others by RCAC
# ticket). The instructor confirms the available id during setup — paste that id
# here. The placeholder below is a guess and will fail if it is not in your list.
MODEL = "llama3.1:8b"

try:
    GENAI_KEY = userdata.get("GENAI_API_KEY")
    if not GENAI_KEY:
        raise ValueError("empty")
    print("✓ Key loaded from Colab Secrets.")
except Exception:
    GENAI_KEY = None
    print("⚠️ No usable GENAI_API_KEY in Colab Secrets.")
    print("   Add it via the 🔑 sidebar, or use the manual UI path (see the doc).")

print(f"Base URL: {BASE_URL}")
print(f"Model:    {MODEL}")
```

**What this does.** Loads your key from Secrets, sets the endpoint and model, and
tells you plainly if the key is missing. It never prints the key and never stores
it in the notebook.

---

## Cell 2 — Role selector (loads the course system prompts)

```python
# Cell 2 — pick a reviewer role. The system prompts are the ones in the public
# course repo (genai_studio/roles/); this cell fetches the chosen role's prompt
# so your API call uses exactly the same instruction as the UI custom model.

import requests, re

RAW_BASE = ("https://raw.githubusercontent.com/davi-moreira/"
            "2026F_evidence_driven_research_purdue_HONR464/main/genai_studio/roles/")

ROLE_FILES = {
    "Socratic Research Tutor":          "socratic_research_tutor.md",
    "Evidence & Citation Verifier":     "evidence_citation_verifier.md",
    "Research Question Diagnostician":  "research_question_diagnostician.md",
    "MIDA Design Reviewer":             "mida_design_reviewer.md",
    "Observational Descriptive Auditor":"observational_descriptive_auditor.md",
    "Causal Identification Skeptic":    "causal_identification_skeptic.md",
    "Experimental Design Reviewer":     "experimental_design_reviewer.md",
    "Prediction & Leakage Auditor":     "prediction_leakage_auditor.md",
    "Robustness & Sensitivity Reviewer":"robustness_sensitivity_reviewer.md",
    "Poster Critic":                    "poster_critic.md",
    "Reproducibility Auditor":          "reproducibility_auditor.md",
    "Research Note Reviewer":           "research_note_reviewer.md",
    "AI Research Team Orchestrator":    "ai_research_team_orchestrator.md",
}

def load_system_prompt(role_name):
    """Fetch a role's spec and extract the fenced block under '## System Prompt'."""
    url = RAW_BASE + ROLE_FILES[role_name]
    text = requests.get(url, timeout=30).text
    after = text.split("## System Prompt", 1)[1]
    block = re.search(r"```(.*?)```", after, re.DOTALL)
    return block.group(1).strip()

# --- choose your role here ---
ROLE = "Causal Identification Skeptic"     # any key from ROLE_FILES

SYSTEM_PROMPT = load_system_prompt(ROLE)
print(f"✓ Loaded system prompt for: {ROLE}  ({len(SYSTEM_PROMPT)} chars)")
```

**What this does.** Pulls the exact system prompt for the role you name from the
public repo, so an API call behaves like the saved UI model. Change `ROLE` to any
of the thirteen names.

---

## Cell 3 — The call (graceful failure, never a stack trace)

```python
# Cell 3 — send your artifact to the chosen role. On any failure it prints a
# clear message and points you to the manual UI path — never a raw traceback.

def ask_role(system_prompt, user_text, timeout=90):
    if not GENAI_KEY:
        return None, ("No API key loaded. Use the manual UI path: Workspace -> the "
                      f"course group's 'HONR464 — {ROLE}' -> paste your artifact.")
    headers = {"Authorization": f"Bearer {GENAI_KEY}",
               "Content-Type": "application/json"}
    payload = {"model": MODEL,
               "messages": [{"role": "system", "content": system_prompt},
                            {"role": "user",   "content": user_text}]}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)
        if r.status_code != 200:
            return None, (f"GenAI Studio returned status {r.status_code}. "
                          f"Check that MODEL ('{MODEL}') is in your model list and "
                          "your key is current. Meanwhile, use the manual UI path.")
        return r.json()["choices"][0]["message"]["content"], None
    except requests.exceptions.Timeout:
        return None, ("The request timed out. Try again, or use the manual UI path "
                      "— it needs only a browser.")
    except Exception:
        return None, ("Could not reach GenAI Studio from Colab. Use the manual UI "
                      "path: Workspace -> the course group's role model -> paste "
                      "your artifact and copy the structured output.")

# --- paste your artifact here (your own, de-identified material only) ---
MY_ARTIFACT = """
Paste the input this role expects (see the role's 'Expected Input' section).
For the Causal Identification Skeptic: your causal question, intervention and
outcome, identification strategy, the comparison, and its assumptions.
"""

reply, error = ask_role(SYSTEM_PROMPT, MY_ARTIFACT)
if error:
    print("⚠️", error)
else:
    print(reply)
```

**What this does.** Sends your artifact with the role's system prompt in an
OpenAI-style payload, with a timeout. Any problem becomes a plain sentence plus the
UI fallback, so a failed call never dumps a stack trace or blocks your milestone.

---

## Cell 4 — Ledger hook (prints a row for you to complete)

```python
# Cell 4 — after a call, print a pre-filled AI Research Ledger row. You STILL fill
# the output summary, decision, verification, and remaining-concern columns. The
# ledger is the point of the exercise; the call is not.

def ledger_row(role, model, prompt_text, got_reply):
    tool = f"GenAI Studio / {role} / {model}"
    task = "REPLACE: the one job you handed to this role, in a sentence"
    return (
        "| Task delegated | Tool used | Prompt | Output summary | Decision | "
        "Verification method | Remaining concern | Responsible student |\n"
        "|---|---|---|---|---|---|---|---|\n"
        f"| {task} | {tool} | "
        f"{prompt_text.strip()[:80]}... | "
        "TODO: what came back, in your words | "
        "TODO: accepted / edited / rejected (your call) | "
        "TODO: how you confirmed it (name a method — not 'looks right') | "
        "TODO: what you are still unsure about | You |"
    )

if not error:
    print("Copy this row into your AI Research Ledger and complete every TODO:\n")
    print(ledger_row(ROLE, MODEL, MY_ARTIFACT, reply))
```

**What this does.** Emits a ready-to-paste ledger row with the task, tool, and
prompt pre-filled and the judgment columns left as `TODO`. Those TODOs are the
graded part: the row is not done until *you* write the output summary, your
decision, a named verification method, and your remaining concern.

---

## Verification, not acceptance

Getting a reply is the easy half. The response is a **proposal you must verify**,
exactly as in the UI. A role's output — however fluent — is not evidence until you
have checked it against your own materials and named the check in the ledger's
verification column. "It looked right" is not a verification. If the role touched a
required touchpoint (M5, M7, M9, M13), the ledger row is required, and it is graded
on the quality of your verification, not on the model's answer.

Remember the correlated-error warning: if you also ran this past Gemini and the two
agree, that agreement is **not** confirmation. Both are large models trained on
overlapping data and can be wrong together. Verify independently.

**And once more: never send personal data.** Course-authored and your own
de-identified material only.

---

## Manual-UI fallback (equal standing)

If you have no API key, the API is down, or you simply prefer it, this path does
everything the touchpoints require:

1. Sign in at `https://genai.rcac.purdue.edu` with your Purdue account.
2. Go to **Workspace** and open the course group's model, named
   **HONR464 — <Role>** (for example, *HONR464 — Causal Identification Skeptic*).
3. Paste your artifact into the chat — the same input the role's *Expected Input*
   section describes. Send only course-authored and de-identified material.
4. Read the structured reply. Copy the sections the role's *Output Schema* names.
5. Verify each output against your own materials.
6. Complete an AI Research Ledger row by hand — same eight fields as Cell 4, same
   graded TODOs.

This path needs no code, no key, and no Colab. It is the guaranteed way to satisfy
every required touchpoint, and choosing it costs you nothing.
