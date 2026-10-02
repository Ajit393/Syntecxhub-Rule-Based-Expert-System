# Rule-Based PC & Laptop Troubleshooting Expert System

A small expert system that reasons about common PC and laptop problems using **if-then rules and forward chaining**. The user reports the problems they are experiencing, the system applies its rules to infer possible issues, and it shows the full reasoning path so you can see exactly how each conclusion was reached.

This project was built for the **Syntecxhub AI Internship (Week 1, Project 2)**.

**Author:** Ajit Singh Chauhan

> **Note:** This is an educational demonstration of rule-based reasoning. It is not a professional hardware diagnostic tool. The suggested causes are based only on the rules programmed into the system.

---

## Overview

An expert system is a program that captures knowledge as a set of rules and applies those rules to reach conclusions, much like a human expert working through a problem step by step.

This project focuses on **PC and laptop troubleshooting**. It takes a list of problems reported by the user and applies a rule-based inference engine to identify possible hardware, performance, display, network, battery, or input-related issues.

The project demonstrates four important requirements:

1. A rule engine built from **if-then rules**, together with a facts base that holds what is currently known.
2. The ability to take problems from the user and infer conclusions using **forward chaining**.
3. Support for **multi-step rule chaining**, where a conclusion from one rule can trigger another rule.
4. A complete **inference log**, allowing the user to see every rule that fired and understand how the final conclusion was reached.

---

## How the Engine Works

The inference engine is **general purpose** and does not contain PC-specific troubleshooting logic itself.

It holds:

- A set of facts
- A list of rules
- An inference log

Each rule contains:

```text
IF conditions are satisfied
THEN add a new conclusion
```

When the system runs, it scans the rules and checks whether all conditions of a rule are present in the current facts.

If they are, the rule fires and its conclusion becomes a new fact.

The newly derived fact can then satisfy another rule on the next pass. This allows the system to perform **multi-step forward chaining**.

The process continues until a complete pass produces no new facts.

### Example of Multi-Step Reasoning

Suppose the user selects:

```text
Screen is black
External monitor works
```

The system first evaluates **R2**:

```text
IF screen is black
THEN display_problem
```

This creates the intermediate fact:

```text
display_problem
```

The system then evaluates **R3**:

```text
IF display_problem
AND external monitor works
THEN possible_internal_display_issue
```

The final result becomes:

```text
Possible Internal Display Issue
```

The user never directly entered `display_problem`. The system derived it from the first rule and then used it to trigger the second rule.

This demonstrates the **multi-step chaining** required by the project.

---

## Project Structure

```text
engine.py
    The general rule engine: facts, rules, forward chaining,
    and the inference log.

knowledge_base.py
    The PC/laptop troubleshooting knowledge:
    symptoms, rules, intermediate facts, and final conclusions.

cli.py
    Command-line interface for interacting with the expert system.

app.py
    Flask web application that connects the inference engine
    to the browser interface.

templates/
    index.html
        Dashboard-style web interface for the troubleshooting system.

tests/
    test_engine.py
        Unit tests for the inference engine and knowledge base.

requirements.txt
    Project dependencies.

README.md
    Project documentation.
```

The engine and knowledge base are deliberately kept separate.

The **engine handles reasoning**, while the **knowledge base contains domain-specific knowledge**.

Because of this separation, the same inference engine could be used for another domain, such as car troubleshooting or equipment diagnosis, simply by replacing the knowledge base.

---

## Running the Project

### 1. Install Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

---

### 2. Run the Command-Line Version

Start the command-line interface with:

```bash
python cli.py
```

The CLI allows the user to select troubleshooting problems and displays the resulting conclusions and reasoning path.

---

### 3. Run the Web Version

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The web interface allows users to select multiple PC or laptop problems and run the rule-based troubleshooting system.

The application displays:

- Selected problems
- Possible troubleshooting conclusions
- Intermediate findings
- Rules that fired
- Conditions that triggered each rule
- The complete reasoning path

---

### 4. Run the Tests

Run the test suite using:

```bash
python -m pytest tests
```

If `pytest` is not installed, the test file can also be run directly:

```bash
python tests/test_engine.py
```

---

## The Rules

The knowledge base contains **11 troubleshooting rules**.

Some rules directly produce final conclusions, while others create **intermediate facts** that can be used by later rules.

| Rule | Conditions | Conclusion |
|---|---|---|
| R1 | Laptop does not turn on + Charger is connected + Charging light is off | Possible Charger / Power Supply Issue |
| R2 | Screen is black | Display problem (intermediate) |
| R3 | Display problem + External monitor works | Possible Internal Display Issue |
| R4 | Laptop turns on + Screen is black + Fans are running | Possible Display Issue |
| R5 | Laptop gets very hot + Fan noise is very high | Possible Overheating Issue |
| R6 | Laptop is running slowly + Many applications are running in background | Possible Background Process Issue |
| R7 | Laptop is running slowly + Disk usage is very high | Possible Storage Performance Issue |
| R8 | Wi-Fi is not working + Other devices have working Wi-Fi | Possible Laptop Network Issue |
| R9 | Battery drains quickly + Laptop gets very hot | Possible Battery / Power Management Issue |
| R10 | Keyboard is not working + External keyboard works | Possible Internal Keyboard Issue |
| R11 | Storage is almost full + Laptop is running slowly | Possible Low Storage Issue |

### Intermediate Rule

The most important multi-step example is:

```text
R2:
IF screen is black
THEN display_problem
```

followed by:

```text
R3:
IF display_problem
AND external monitor works
THEN possible_internal_display_issue
```

This allows the system to demonstrate that a rule's conclusion can become the condition for another rule.

---

## Example Troubleshooting Session

A user selects:

```text
✓ Screen is black
✓ External monitor works
```

The inference engine starts with these facts:

```text
screen_black
external_monitor_works
```

### Step 1

Rule R2 is satisfied:

```text
screen_black
        ↓
display_problem
```

The engine records this as an intermediate finding.

### Step 2

The newly derived `display_problem` fact is now available.

R3 is satisfied:

```text
display_problem
+
external_monitor_works
        ↓
possible_internal_display_issue
```

### Final Result

The application displays:

```text
Possible Internal Display Issue
```

And the reasoning path shows both rules:

```text
R2
screen_black
    ↓
display_problem

R3
display_problem + external_monitor_works
    ↓
possible_internal_display_issue
```

This makes the reasoning process transparent instead of simply giving the user a conclusion.

---

## Technology

The project uses:

- **Python 3.10+**
- **Flask** for the web interface
- **HTML/CSS/JavaScript** for the dashboard UI
- **Python standard library** for the inference engine
- **Forward chaining** for rule-based inference

The core inference engine does not require machine learning, an external AI API, or a database.

---

## Key AI Concepts Demonstrated

This project demonstrates several fundamental concepts in Artificial Intelligence:

### 1. Knowledge Representation

Troubleshooting knowledge is represented using facts and IF–THEN rules.

### 2. Rule-Based Reasoning

The system uses predefined rules to derive conclusions from known facts.

### 3. Forward Chaining

The engine starts with user-provided facts and works forward toward possible conclusions.

### 4. Inference

New facts are derived when the conditions of rules are satisfied.

### 5. Multi-Step Reasoning

A conclusion produced by one rule can become a condition for another rule.

### 6. Explainable Reasoning

Every rule that fires is stored in an inference log, allowing the system to explain how it reached its conclusion.

---

## Advantages

- Simple and easy to understand
- Explainable reasoning
- No machine-learning training required
- Easy to add new troubleshooting rules
- Supports multi-step inference
- Separates reasoning logic from domain knowledge
- Provides both command-line and web interfaces

---

## Limitations

- The system can only reason about situations covered by its programmed rules.
- It does not perform actual hardware testing.
- It does not automatically inspect the computer's hardware or operating system.
- It does not use machine learning.
- Multiple possible issues may exist for the same symptoms.
- The conclusions should be treated as educational troubleshooting suggestions rather than professional hardware diagnoses.

---

## Future Scope

The system could be extended with:

- More PC and laptop troubleshooting rules
- Printer and peripheral troubleshooting
- Automatic system information collection
- Hardware monitoring
- More detailed troubleshooting recommendations
- A larger knowledge base
- Additional expert-system reasoning strategies
- A database for storing troubleshooting knowledge
- A more advanced diagnostic dashboard

---

## Author

**Ajit Singh Chauhan**

**Syntecxhub AI Internship — Week 1, Project 2**

**Project:** Rule-Based PC & Laptop Troubleshooting Expert System