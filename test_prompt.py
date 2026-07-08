"""
Standalone prompt test harness.
Edit SYSTEM and TEST_CASES below, then run: py test_prompt.py
No need to run the full Streamlit/CLI app to test a single prompt.
"""

import ollama

OLLAMA_MODEL = "llama3.2:1b"

# Paste the system prompt you want to test here
SYSTEM = """You are a strict binary classifier.
    Task: decide if the user's message is a question about a legal document, contract or terms of service.

    Rule: questions about grammar, language, etymology, word origin, history of a country, science, math, or any topic
    that does not mention or imply a legal context are false.

    When in doubt, answer false.
    Respond with exactly one word: true or false. No explanation, no punctuation."""

SYSTEM = """You are a strict binary classifier that also simplifies questions.
    Respond ONLY in JSON, no markdown, no explanations:
    {"related": true/false, "simplified": "text or null"}

    Rules for "related":
        Task: decide if the user's message is a question about a legal document, contract or terms of service.

        Rule: questions about grammar, language, etymology, word origin, history of a country, science, math, or any topic
        that does not mention or imply a legal context are false.

        When in doubt, answer false.
        Respond with exactly one word: true or false. No explanation, no punctuation.

    Rules for "simplified":
        If related is true and the text contains <question>...</question>, rewrite the content of that tag: direct, objective, shorter than the original, without losing information.
        Do not lose any information present in the original question.
        Respond with the simplified question only, no explanation, no quotes.
    """

SYSTEM = """You are a legal concise writer."""


# List of (input, expected_substring_or_None)
# expected is optional, use None if you just want to eyeball the output
TEST_CASES_v11 = [
    # ("<question>8 + 5?</question>"),
    ("rewrite this question in a simple maner: <question>What the document is about? Should I be concerned about something? I was wondering</question>"),

    ("""simplify this question: <question>Why in English I can say: 'Tell me about china's history' and also 'tell me about 
    history of china'. Does the 'of' version comes from frensh influence?</question>
    """),
    ("""simplify this question: <question>3.3 Real Estate Agent Obligations
Licensed real estate agents must act in the best interest of their client throughout the property
transaction lifecycle. Agents are prohibited from representing conflicting interests in the same
transaction without written disclosure and informed consent from both parties. Commission
structures must be disclosed prior to engagement (Disclosure Form: REA-DISC-2024). Agents must</question>"""),
]
TEST_CASES_v12 = [
    ("8 + 5?"),
    ("What the document is about? Should I be concerned about something? I was wondering"),

    ("""Why in English I can say: 'Tell me about china's history' and also 'tell me about 
    history of china'. Does the 'of' version comes from frensh influence?
    """),
    ("""3.3 Real Estate Agent Obligations
Licensed real estate agents must act in the best interest of their client throughout the property
transaction lifecycle. Agents are prohibited from representing conflicting interests in the same
transaction without written disclosure and informed consent from both parties. Commission
structures must be disclosed prior to engagement (Disclosure Form: REA-DISC-2024). Agents must"""),
]

TEST_CASES = TEST_CASES_v11

def ask(system: str, question: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        options={
            "temperature": 0,
            "seed": 42,
        },
    )
    return response["message"]["content"].strip()


def run():
    for question in TEST_CASES:
        answer = ask(SYSTEM, question)
        print("-" * 60)
        print(f"INPUT:    {question}")
        print(f"OUTPUT:   {answer}")

    print("-" * 60)


if __name__ == "__main__":
    run()
