"""Math agent that solves questions using tools in a ReAct loop."""

import json
import time

from dotenv import load_dotenv
from pydantic_ai import Agent
from calculator import calculate

load_dotenv()

# Configure your model below. Examples:
#   "google-gla:gemini-2.5-flash"       (needs GOOGLE_API_KEY)
#   "openai:gpt-4o-mini"                (needs OPENAI_API_KEY)
#   "anthropic:claude-sonnet-4-6"    (needs ANTHROPIC_API_KEY)
MODEL = "google-gla:gemini-2.5-flash"

agent = Agent(
    MODEL,
    system_prompt=(
        "You are a helpful assistant. Solve each question step by step. "
        "Use the calculator tool for arithmetic. "
        "Use the product_lookup tool when a question mentions products from the catalog. "
        "You MUST use the product_lookup tool to get product prices. NEVER say you don't have access to product information. "
        "Always look up prices using the product_lookup tool before answering product-related questions. "
        "If a question cannot be answered with the information given, say so."
    ),
)


@agent.tool_plain
def calculator_tool(expression: str) -> str:
    """Evaluate a math expression and return the result.

    Examples: "847 * 293", "10000 * (1.07 ** 5)", "23 % 4"
    """
    return calculate(expression)


@agent.tool_plain
def product_lookup(product_name: str) -> str:
    """Look up the price of a product by name.
    Use this when a question asks about product prices from the catalog.
    """
    with open("products.json") as f:
        catalog = json.load(f)

    for name, price in catalog.items():
        if name.lower() == product_name.strip().lower():
            return f"{name}: ${price}"

    available = ", ".join(catalog.keys())
    return f"Product '{product_name}' not found. Available products: {available}"


def load_questions(path: str = "math_questions.md") -> list[str]:
    """Load numbered questions from the markdown file."""
    questions = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and line[0].isdigit() and ". " in line[:4]:
                questions.append(line.split(". ", 1)[1])
    return questions


def main():
    questions = load_questions()
    for i, question in enumerate(questions, 1):
        print(f"## Question {i}")
        print(f"> {question}\n")

        # Retry up to 5 times on 503 errors
        for attempt in range(5):
            try:
                result = agent.run_sync(question)
                break
            except Exception as e:
                if "503" in str(e) and attempt < 4:
                    print(f"  (503 error, retrying in 10s... attempt {attempt + 2}/5)")
                    time.sleep(10)
                else:
                    raise

        print("### Trace")
        for message in result.all_messages():
            for part in message.parts:
                kind = part.part_kind
                if kind in ("user-prompt", "system-prompt"):
                    continue
                elif kind == "text":
                    print(f"- **Reason:** {part.content}")
                elif kind == "tool-call":
                    print(f"- **Act:** `{part.tool_name}({part.args})`")
                elif kind == "tool-return":
                    print(f"- **Result:** `{part.content}`")

        print(f"\n**Answer:** {result.output}\n")
        print("---\n")


if __name__ == "__main__":
    main()
