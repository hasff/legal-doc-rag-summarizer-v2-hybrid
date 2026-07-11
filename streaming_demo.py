"""
streaming_demo.py

Side demo for Part 05. Shows two ways to get a streaming response from
Ollama in Python, so you can see the same "letters appearing" effect
we saw in the browser, but from the terminal.

Run it with:
    py streaming_demo.py
"""

import json
import requests
import ollama

QUESTION = "What is the capital of Portugal?"


def stream_with_ollama_module():
    print("\n--- Streaming with the ollama module ---\n")

    stream = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": QUESTION}],
        stream=True,
    )

    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)

    print("\n")


def stream_with_requests():
    print("\n--- Streaming with raw requests (manual parsing) ---\n")

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2:1b",
            "messages": [{"role": "user", "content": QUESTION}],
            "stream": True,
        },
        stream=True,
    )

    for line in response.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        print(chunk["message"]["content"], end="", flush=True)

    print("\n")


if __name__ == "__main__":
    stream_with_ollama_module()
    stream_with_requests()
