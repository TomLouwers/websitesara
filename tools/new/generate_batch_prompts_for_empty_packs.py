#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, os, re
from typing import Any, Dict, List, Tuple, Optional

BASE_V12 = """Je bent een oefeningengenerator voor het Nederlandse basisonderwijs
(rekenen-wiskunde), inspectie-proof, SLO-aligned en strikt schema-gedreven.

JE TAAK
Genereer een JSON-array met EXACT {N} oefeningen voor:
- domain: "{DOMAIN}"
- grade: {GRADE}
- level: "{LEVEL}"
- topic: "{TOPIC}"

OUTPUTFORMAT (HARD)
- Output is EXACT één JSON-array (start met [ en eindig met ]).
- GEEN extra tekst, geen markdown, geen uitleg.
- Elke oefening is één JSON-object met schemaVersion "1.0.0".
- Alle objecten voldoen exact aan ExerciseSchema.json.

DIDACTIEK (HARD)
- Niveau {LEVEL}: één kernhandeling per oefening.
- Leerlingtaal, geen vakjargon.
- Geen verborgen hints in de prompt.

ANTI-DUPLICATIE REGELS (HARD)
1) Unieke kern: geen identieke sommen/paren/tabellen.
2) Promptvariatie: minimaal 5 verschillende startzinnen.
3) MCQ: minimaal 3 optie-banken, geen identieke opties+antwoord.
4) Contextvariatie: één contextwoord niet >40%.

NIVEAU-SPECIFIEK
- n2: geen 'waarom/leg uit', geen foutanalyse, geen strategie-vergelijking.
- n3: geen antwoord lekt uit prompt; geen strategie-woord letterlijk in opties.

MISCONCEPT-LOGICA (HARD)
- EXACT 1 misconceptKey per oefening, bestaande keys, gelijkmatig verdeeld.

CONTROLE (HARD)
- EXACT {N} items, ids uniek/sequentieel, schema-proof, taskForm toegestaan.

GENEREER NU DE JSON-ARRAY.
"""

def find_exercises_files(root: str) -> List[str]:
    out=[]
    for r,_,files in os.walk(root):
        for fn in files:
            if fn=="exercises.json":
                out.append(os.path.join(r,fn))
    return sorted(out)

def load_json_safe(path: str) -> Tuple[str, Any]:
    try:
        with open(path,"r",encoding="utf-8") as f:
            raw=f.read()
        if raw.strip()=="":
            return "empty_file", None
        return "ok", json.loads(raw)
    except Exception:
        return "parse_error", None

def parse_meta(path: str) -> Dict[str, Any]:
    p = path.replace("\\","/")
    parts = p.split("/")
    meta={"domain":"","group":"","level":"","topic":"","grade":0}
    if "nl-NL" in parts:
        i=parts.index("nl-NL")
        if i+1<len(parts): meta["domain"]=parts[i+1]
    for part in parts:
        if part.startswith("groep-"):
            try: meta["grade"]=int(part.split("-")[1])
            except: meta["grade"]=0
        if part in ("n1","n2","n3","n4"):
            meta["level"]=part
    if "topics" in parts:
        j=parts.index("topics")
        if j+1<len(parts): meta["topic"]=parts[j+1]
    return meta

def suggest_id_prefix(domain: str, grade: int, topic: str) -> str:
    dom_map = {
        "getal-en-bewerkingen": "GB",
        "verhoudingen": "VH",
        "meten-en-meetkunde": "MM",
    }
    d = dom_map.get(domain, "XX")
    parts = re.split(r"[-_]+", topic)
    code = "".join([p[:1].upper() for p in parts if p])[:4] or "TOP"
    return f"{d}{grade}-{code}"

def load_overrides(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {"overrides": [], "domain_defaults": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_obj(match: Dict[str, Any], domain: str, grade: int, level: str, topic: str) -> bool:
    if "domain" in match and match["domain"] != domain: return False
    if "grade" in match and match["grade"] != grade: return False
    if "level" in match and match["level"] != level: return False
    if "topic" in match and match["topic"] != topic: return False
    return True

def find_topic_override(cfg: Dict[str, Any], domain: str, grade: int, level: str, topic: str) -> Optional[Dict[str, Any]]:
    for o in cfg.get("overrides", []):
        if match_obj(o.get("match", {}), domain, grade, level, topic):
            return o.get("settings", {})
    return None

def find_domain_defaults(cfg: Dict[str, Any], domain: str) -> Dict[str, Any]:
    for o in cfg.get("domain_defaults", []):
        if match_obj(o.get("match", {}), domain, grade=0, level="", topic=""):
            return o.get("settings", {})
    return {}

def heuristic_interaction_taskform(domain: str, level: str, topic: str, dom_defaults: Dict[str, Any]) -> Tuple[str, str, str]:
    t = topic.lower()

    if any(k in t for k in ["vergelijken","herkennen","betekenis"]):
        interaction="mcq"
        taskForm="select_single"
        extra = "- interaction.type = \"mcq\"\\n- taskForm = \"select_single\"\\n- 4 opties, 1 correct."
        return interaction, taskForm, extra

    if any(k in t for k in ["verhoudingstabel","tabellen","tabel"]):
        interaction="numeric"
        taskForm="context_single_step" if level=="n2" else "numeric_simple"
        extra = "- interaction.type = \"numeric\"\\n- Eenvoudige verhoudingstabel met 1 ontbrekende waarde."
        return interaction, taskForm, extra

    if any(k in t for k in ["omrekenen","grootheden","eenheden","meter","cm","km","liter","ml"]):
        interaction="numeric"
        taskForm="guided_focus" if level=="n2" else "context_single_step"
        extra = "- interaction.type = \"numeric\"\\n- Eén omzetting per opgave."
        return interaction, taskForm, extra

    interaction="numeric"
    # domain default if provided
    if level == "n2":
        taskForm = dom_defaults.get("default_taskForm_n2", "numeric_simple")
    elif level == "n3":
        taskForm = dom_defaults.get("default_taskForm_n3", "select_single")
    else:
        taskForm = "numeric_simple"
    extra = "- interaction.type = \"numeric\"\\n- Eén bewerking per opgave, antwoord numeriek."
    return interaction, taskForm, extra

def render_override_addendum(settings: Dict[str, Any], fallback_id_prefix: str, fallback_taskForm: str, fallback_interaction: str) -> Tuple[int, str]:
    n_items = int(settings.get("n_items", 30))

    interaction = settings.get("interaction_type", fallback_interaction)
    id_pattern = settings.get("id_pattern", f"{fallback_id_prefix}-###")
    task_forms = settings.get("taskForm_allowed", [fallback_taskForm])

    lines = []
    lines.append("TOPIC-OVERRIDE (HARD)")
    lines.append(f"- interaction.type = \"{interaction}\"")
    if isinstance(task_forms, list) and task_forms:
        if len(task_forms) == 1:
            lines.append(f"- taskForm = \"{task_forms[0]}\" (verplicht)")
        else:
            lines.append(f"- taskForm ∈ {task_forms}")
    lines.append(f"- id patroon: \"{id_pattern}\"")

    dist = settings.get("taskForm_distribution")
    if isinstance(dist, dict):
        lines.append("- taskForm verdeling (HARD):")
        for k, v in dist.items():
            lines.append(f"  - {k}: {v}")

    # constraints and rules
    for key in ["constraints", "solution_format_rules", "anti_dup_rules", "mcq_options_rules"]:
        if key in settings and isinstance(settings[key], list) and settings[key]:
            lines.append(f"- {key}:")
            for r in settings[key]:
                lines.append(f"  - {r}")

    if "forbidden_phrases" in settings and isinstance(settings["forbidden_phrases"], list):
        lines.append("- verboden zinnen/woorden (HARD):")
        for ph in settings["forbidden_phrases"]:
            lines.append(f"  - {ph}")

    if "misconceptKeys_allowed" in settings and isinstance(settings["misconceptKeys_allowed"], list):
        lines.append("- misconceptKeys (HARD): gebruik EXACT 1 uit:")
        for k in settings["misconceptKeys_allowed"]:
            lines.append(f"  - {k}")

    if "allowed_fractions" in settings and isinstance(settings["allowed_fractions"], list):
        lines.append("- toegestane breuken (HARD): " + ", ".join(settings["allowed_fractions"]))

    if "allowed_percentages" in settings and isinstance(settings["allowed_percentages"], list):
        lines.append("- toegestane percentages (HARD): " + ", ".join(settings["allowed_percentages"]))

    if "option_banks" in settings and isinstance(settings["option_banks"], list):
        lines.append("- optie-banken (HARD): roteer, geen identieke set+antwoord:")
        for i, bank in enumerate(settings["option_banks"], 1):
            lines.append(f"  - bank {i}: {bank}")

    if "prompt_forms" in settings and isinstance(settings["prompt_forms"], list):
        lines.append("- promptvormen (HARD):")
        for pf in settings["prompt_forms"]:
            lines.append(f"  - {pf}")

    if "prompt_starters" in settings and isinstance(settings["prompt_starters"], list):
        lines.append("- startzinnen (HARD): gebruik minimaal 5 varianten; kies uit:")
        for s in settings["prompt_starters"]:
            lines.append(f"  - {s}")

    return n_items, "\n".join(lines) + "\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--content-root", required=True)
    ap.add_argument("--out-root", default="docs/new/batch-prompts")
    ap.add_argument("--min-items", type=int, default=30)
    ap.add_argument("--groups", default="4,5,6")
    ap.add_argument("--levels", default="n2,n3")
    ap.add_argument("--overrides", default="docs/new/prompt-overrides.json")
    args=ap.parse_args()

    groups=set(int(x.strip()) for x in args.groups.split(",") if x.strip())
    levels=set(x.strip() for x in args.levels.split(",") if x.strip())

    cfg = load_overrides(args.overrides)

    files=find_exercises_files(args.content_root)
    targets=[]

    for p in files:
        meta=parse_meta(p)
        if meta["grade"] not in groups: 
            continue
        if meta["level"] not in levels:
            continue
        st,data=load_json_safe(p)
        if st=="ok" and isinstance(data,list) and len(data)==0:
            targets.append((p,meta))

    os.makedirs(args.out_root, exist_ok=True)

    created=0
    for _, meta in targets:
        domain=meta["domain"]
        grade=meta["grade"]
        level=meta["level"]
        topic=meta["topic"]

        dom_defaults = find_domain_defaults(cfg, domain)
        interaction, taskForm, extra = heuristic_interaction_taskform(domain, level, topic, dom_defaults)
        id_prefix = suggest_id_prefix(domain, grade, topic)

        settings = find_topic_override(cfg, domain, grade, level, topic)

        if settings:
            n_items, addendum = render_override_addendum(settings, id_prefix, taskForm, interaction)
        else:
            n_items = args.min_items
            addendum = f"""TOPIC-SPECIFIEK (HARD)
- interaction.type = "{interaction}"
- taskForm = "{taskForm}"
- id patroon: "{id_prefix}-###" (001 t/m {n_items:03d})
{extra}

Let op:
- solution-format moet schema-proof zijn voor het gekozen interaction-type.
- misconceptKeys: gebruik alleen bestaande keys uit misconcepts/{domain}.json.
"""

        prompt = BASE_V12.format(
            N=n_items,
            DOMAIN=domain,
            GRADE=grade,
            LEVEL=level,
            TOPIC=topic
        ) + "\n" + addendum.strip() + "\n"

        out_dir = os.path.join(args.out_root, domain, f"groep-{grade}", level, topic)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "batch_prompt.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        created += 1

    print(f"Created {created} batch prompts under: {args.out_root}")
    print(f"Overrides used from: {args.overrides}")

if __name__=="__main__":
    main()
