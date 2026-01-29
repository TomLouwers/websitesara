# Prompt Packs

Proposed structure (implemented):

prompts/
  contracts/            # Prompt contract(s) and human-readable override summaries
  packs/
    nl-NL/<domain>/groep-<grade>/<level>/
      <CODE><grade>-<topic>.<interaction>.v<semver>.txt
  scratch/              # Temporary working area

Naming convention:
- CODE: GB (getal-en-bewerkingen), VH (verhoudingen), MM (meten-en-meetkunde).
- topic: kebab-case topic slug, aligned with content paths.
- interaction: mcq | numeric | etc. (matches prompt instructions).
- semver: start at 1.0 and bump on edits.

Sources migrated from docs/new/ai remain authoritative; this folder mirrors them for use in prompt tooling.
