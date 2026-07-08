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


TEST_CASES = [
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
