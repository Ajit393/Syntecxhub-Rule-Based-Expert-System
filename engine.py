"""
engine.py
=========
A small, general-purpose rule-based inference engine.

The engine is domain-agnostic: it knows nothing about medicine. It only knows
how to hold a set of *facts*, apply a set of *if-then rules*, and repeatedly
fire any rule whose conditions are all satisfied (forward chaining) until no
new facts can be derived. Every rule that fires is recorded in an inference
log so the full reasoning path can be replayed to the user.

This separation (engine vs. knowledge) is deliberate: the same engine could
reason about car faults or animal taxonomy just by swapping the knowledge base.
"""

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    """A single if-then rule.

    Attributes:
        name:        Human-readable identifier, e.g. "R3".
        conditions:  Facts that must ALL be present for the rule to fire.
        conclusion:  The fact added when the rule fires.
        explanation: Plain-English description of what the rule means.
    """
    name: str
    conditions: frozenset[str]
    conclusion: str
    explanation: str = ""

    def is_satisfied_by(self, facts: set[str]) -> bool:
        """True when every condition of this rule is already a known fact."""
        return self.conditions.issubset(facts)


@dataclass
class InferenceStep:
    """One entry in the reasoning path: a rule that fired during inference."""
    rule_name: str
    triggered_by: frozenset[str]
    conclusion: str
    explanation: str

    def __str__(self) -> str:
        triggers = ", ".join(sorted(self.triggered_by))
        return (f"[{self.rule_name}] {triggers}  ==>  {self.conclusion}"
                + (f"   ({self.explanation})" if self.explanation else ""))


@dataclass
class ExpertSystem:
    """Forward-chaining inference engine.

    Usage:
        es = ExpertSystem(rules)
        es.add_facts(["fever", "cough"])
        derived = es.run()          # performs forward chaining
        es.inference_log            # list[InferenceStep] — the reasoning path
    """
    rules: list[Rule]
    facts: set[str] = field(default_factory=set)
    inference_log: list[InferenceStep] = field(default_factory=list)

    # ----- fact management -------------------------------------------------
    def add_fact(self, fact: str) -> None:
        self.facts.add(fact.strip().lower())

    def add_facts(self, facts: Iterable[str]) -> None:
        for f in facts:
            self.add_fact(f)

    def reset(self) -> None:
        """Clear facts and log so the engine can be re-run from scratch."""
        self.facts.clear()
        self.inference_log.clear()

    # ----- inference -------------------------------------------------------
    def run(self) -> set[str]:
        """Run forward chaining until no new facts are produced.

        On each pass we scan every rule. A rule fires when all its conditions
        are in the facts base AND its conclusion is not already known. Firing a
        rule adds a new fact, which may satisfy another rule on the next pass —
        this is what gives multi-step (chained) inference. We loop until a full
        pass adds nothing new, guaranteeing termination.

        Returns the set of facts that were *derived* (not the ones supplied).
        """
        supplied = set(self.facts)
        new_fact_found = True

        while new_fact_found:
            new_fact_found = False
            for rule in self.rules:
                if rule.conclusion in self.facts:
                    continue  # already concluded; don't fire twice
                if rule.is_satisfied_by(self.facts):
                    self.facts.add(rule.conclusion)
                    self.inference_log.append(
                        InferenceStep(
                            rule_name=rule.name,
                            triggered_by=rule.conditions,
                            conclusion=rule.conclusion,
                            explanation=rule.explanation,
                        )
                    )
                    new_fact_found = True

        return self.facts - supplied

    # ----- reporting -------------------------------------------------------
    def conclusions(self, candidate_conclusions: set[str]) -> list[str]:
        """Return the subset of `candidate_conclusions` that were derived.

        Lets a knowledge base distinguish final diagnoses from intermediate
        facts (e.g. 'viral_infection') that were only stepping stones.
        """
        return sorted(self.facts & candidate_conclusions)

    def reasoning_path(self) -> str:
        """Pretty-printed inference log for display."""
        if not self.inference_log:
            return "No rules fired — no conclusions could be drawn."
        lines = [f"{i + 1}. {step}" for i, step in enumerate(self.inference_log)]
        return "\n".join(lines)
