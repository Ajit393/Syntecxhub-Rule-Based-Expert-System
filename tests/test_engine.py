"""
test_engine.py
==============
Unit tests for the rule engine and the medical knowledge base.

Run:  python -m pytest tests/ -v
  or: python tests/test_engine.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import Rule, ExpertSystem
from knowledge_base import RULES, FINAL_DIAGNOSES


def test_single_rule_fires():
    rules = [Rule("T1", frozenset({"a", "b"}), "c")]
    es = ExpertSystem(rules)
    es.add_facts(["a", "b"])
    derived = es.run()
    assert "c" in derived
    assert len(es.inference_log) == 1


def test_rule_does_not_fire_when_conditions_missing():
    rules = [Rule("T1", frozenset({"a", "b"}), "c")]
    es = ExpertSystem(rules)
    es.add_facts(["a"])  # missing 'b'
    derived = es.run()
    assert "c" not in derived
    assert es.inference_log == []


def test_multi_step_chaining():
    """a,b -> x ; x,d -> goal  : goal requires two chained inferences."""
    rules = [
        Rule("T1", frozenset({"a", "b"}), "x"),
        Rule("T2", frozenset({"x", "d"}), "goal"),
    ]
    es = ExpertSystem(rules)
    es.add_facts(["a", "b", "d"])
    derived = es.run()
    assert "x" in derived
    assert "goal" in derived
    # The intermediate must fire before the final — order matters.
    assert es.inference_log[0].conclusion == "x"
    assert es.inference_log[1].conclusion == "goal"


def test_no_duplicate_firing():
    rules = [Rule("T1", frozenset({"a"}), "b")]
    es = ExpertSystem(rules)
    es.add_facts(["a"])
    es.run()
    es.run()  # running again should not re-fire an already-known conclusion
    assert len(es.inference_log) == 1


def test_termination_on_no_match():
    rules = [Rule("T1", frozenset({"z"}), "y")]
    es = ExpertSystem(rules)
    es.add_facts(["a"])
    derived = es.run()
    assert derived == set()


def test_medical_flu_chain():
    """Real KB: flu requires viral_infection (itself derived) + body_aches + high_fever."""
    es = ExpertSystem(RULES)
    es.add_facts(["fever", "cough", "fatigue", "body_aches", "high_fever"])
    es.run()
    diagnoses = es.conclusions(set(FINAL_DIAGNOSES))
    assert "influenza_flu" in diagnoses
    assert "viral_infection" in es.facts  # intermediate was derived


def test_medical_no_match():
    es = ExpertSystem(RULES)
    es.add_facts(["headache"])  # not enough for any rule
    es.run()
    assert es.conclusions(set(FINAL_DIAGNOSES)) == []


def test_reset():
    es = ExpertSystem(RULES)
    es.add_facts(["nausea", "diarrhea"])
    es.run()
    assert es.facts
    es.reset()
    assert es.facts == set()
    assert es.inference_log == []


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:
            print(f"ERROR {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed.")
