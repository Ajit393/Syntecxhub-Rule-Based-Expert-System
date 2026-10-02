"""
app.py
======
Flask web interface for the rule-based PC and laptop
troubleshooting expert system.

Run:
    python app.py

Then open:
    http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify

from engine import ExpertSystem
from knowledge_base import (
    SYMPTOMS,
    RULES,
    FINAL_DIAGNOSES,
    INTERMEDIATE_FACTS,
    DISCLAIMER,
)

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Display the troubleshooting interface."""
    return render_template(
        "index.html",
        symptoms=SYMPTOMS,
        disclaimer=DISCLAIMER,
    )


# ---------------------------------------------------------------------------
# Troubleshooting / inference endpoint
# ---------------------------------------------------------------------------

@app.route("/diagnose", methods=["POST"])
def diagnose():
    """
    Receive selected problems from the browser, run the
    forward-chaining inference engine, and return the results.
    """

    # Read JSON data sent by the frontend
    data = request.get_json(silent=True) or {}

    # Get selected symptoms/problems
    selected = data.get("symptoms", [])

    # Create a fresh expert system for every troubleshooting session
    es = ExpertSystem(rules=RULES)

    # Add the user's selected problems as initial facts
    es.add_facts(selected)

    # Run forward chaining
    es.run()

    # -----------------------------------------------------------------------
    # Final conclusions
    # -----------------------------------------------------------------------

    diagnoses = [
        {
            "key": key,
            "label": FINAL_DIAGNOSES[key],
        }
        for key in es.conclusions(set(FINAL_DIAGNOSES))
    ]

    # -----------------------------------------------------------------------
    # Intermediate facts
    # -----------------------------------------------------------------------

    intermediates = [
        {
            "key": key,
            "label": INTERMEDIATE_FACTS[key],
        }
        for key in es.conclusions(set(INTERMEDIATE_FACTS))
    ]

    # -----------------------------------------------------------------------
    # Reasoning / inference path
    # -----------------------------------------------------------------------

    steps = [
        {
            "rule": step.rule_name,
            "triggered_by": [
                SYMPTOMS.get(fact, fact)
                for fact in sorted(step.triggered_by)
            ],
            "conclusion": step.conclusion,
            "conclusion_label": (
                FINAL_DIAGNOSES.get(
                    step.conclusion,
                    INTERMEDIATE_FACTS.get(
                        step.conclusion,
                        step.conclusion
                    )
                )
            ),
            "explanation": step.explanation,
        }
        for step in es.inference_log
    ]

    # -----------------------------------------------------------------------
    # Return results to frontend
    # -----------------------------------------------------------------------

    return jsonify(
        {
            "reported": [
                SYMPTOMS.get(symptom, symptom)
                for symptom in selected
            ],
            "diagnoses": diagnoses,
            "intermediates": intermediates,
            "steps": steps,
        }
    )


# ---------------------------------------------------------------------------
# Start Flask application
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)