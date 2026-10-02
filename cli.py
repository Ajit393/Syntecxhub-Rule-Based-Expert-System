"""
cli.py
======
Command-line interface for the rule-based medical expert system.

Run:  python cli.py

Presents the list of symptoms, lets the user select which they have, runs
forward chaining, then prints both the conclusions and the full reasoning path.
"""

from engine import ExpertSystem
from knowledge_base import (
    SYMPTOMS, RULES, FINAL_DIAGNOSES, INTERMEDIATE_FACTS, DISCLAIMER,
)


def prompt_symptoms() -> list[str]:
    """Show the numbered symptom menu and collect the user's selections."""
    print("\nAvailable symptoms:\n")
    keys = list(SYMPTOMS.keys())
    for i, key in enumerate(keys, start=1):
        print(f"  {i:>2}. {SYMPTOMS[key]}")

    print("\nEnter the numbers of your symptoms, separated by commas "
          "(e.g. 1,2,4). Press Enter with nothing to quit.")
    raw = input("> ").strip()
    if not raw:
        return []

    selected: list[str] = []
    for token in raw.split(","):
        token = token.strip()
        if not token.isdigit():
            print(f"  (ignoring invalid entry: '{token}')")
            continue
        idx = int(token)
        if 1 <= idx <= len(keys):
            selected.append(keys[idx - 1])
        else:
            print(f"  (ignoring out-of-range number: {idx})")
    return selected


def run_once() -> None:
    selected = prompt_symptoms()
    if not selected:
        return

    es = ExpertSystem(rules=RULES)
    es.add_facts(selected)
    es.run()

    print("\n" + "=" * 60)
    print("REPORTED SYMPTOMS")
    print("=" * 60)
    for key in selected:
        print(f"  - {SYMPTOMS.get(key, key)}")

    diagnoses = es.conclusions(set(FINAL_DIAGNOSES))
    print("\n" + "=" * 60)
    print("CONCLUSIONS")
    print("=" * 60)
    if diagnoses:
        for d in diagnoses:
            print(f"  * {FINAL_DIAGNOSES[d]}")
    else:
        print("  No specific condition matched the reported symptoms.")

    intermediates = es.conclusions(set(INTERMEDIATE_FACTS))
    if intermediates:
        print("\n  Intermediate findings derived along the way:")
        for f in intermediates:
            print(f"    - {INTERMEDIATE_FACTS[f]}")

    print("\n" + "=" * 60)
    print("REASONING PATH (how these conclusions were reached)")
    print("=" * 60)
    print(es.reasoning_path())

    print("\n" + "-" * 60)
    print(DISCLAIMER)
    print("-" * 60)


def main() -> None:
    print("=" * 60)
    print(" Rule-Based Medical Expert System  (Syntecxhub Project 2)")
    print("=" * 60)
    print(DISCLAIMER)

    while True:
        run_once()
        again = input("\nCheck another set of symptoms? (y/n) > ").strip().lower()
        if again != "y":
            print("Goodbye — take care.")
            break


if __name__ == "__main__":
    main()
