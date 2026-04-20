# Week 4 Starter: Math Agent

A ReAct agent that solves questions using tool calls.

## Video Walkthrough

https://www.youtube.com/watch?v=L5UIjJO2ZjI

## Setup

1. Install __uv__ if you don't have it.
2. Copy `.env.example` to `.env` and add your API key:

```
cp .env.example .env
```

Then edit `.env` and replace `your-key-here` with your key from __Google AI Studio__.
To use a different provider, change the `MODEL` variable in `agent.py` and set the matching key in `.env`.
3. Make sure `.env` is in your `.gitignore` so you don't commit your key.

## Run

```
uv run agent.py
```

uv will install dependencies automatically on first run.
The agent will work through each question in `math_questions.md` and print the ReAct trace (Reason / Act / Result) for each one.

## Files

* `agent.py` - the ReAct agent (with product_lookup implemented)
* `calculator.py` - calculator tool
* `products.json` - product catalog with prices
* `math_questions.md` - the questions the agent solves
* `.env.example` - template for your API key
