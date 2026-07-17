"""Stream an agent's answer and show the tools it ran and the sources it used.

Not from the book — this is the Python twin of the Teams tab's backend
(https://github.com/JayRHa/foundry-agent-tab), reduced to one file with no dependencies
beyond the az CLI.

The point is what the event stream actually contains. A streamed response is not just
text: the service tells you which tools it decided to run, and the final event carries
the annotations that let you show a source under a claim. Most samples throw both away
and print the text — which is exactly how you end up unable to answer "where did the
agent get that?".

Events this handles (there are more; these are the load-bearing ones):
    response.output_text.delta   a piece of the answer
    response.output_item.added   an item started — item.type "..._call" means a tool ran
    response.completed           the final response, with output[].content[].annotations[]

Run:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
    python stream.py MyAgent "What changed in Microsoft Foundry this month?"
"""
import json
import os
import subprocess
import sys
import urllib.request

ENDPOINT = os.environ["PROJECT_ENDPOINT"].rstrip("/")
AGENT = sys.argv[1] if len(sys.argv) > 1 else "MyAgent"
QUESTION = " ".join(sys.argv[2:]) or "What changed in Microsoft Foundry this month?"

DIM, BOLD, RESET = "\033[2m", "\033[1m", "\033[0m"


def token() -> str:
    return subprocess.check_output(
        ["az", "account", "get-access-token", "--scope", "https://ai.azure.com/.default",
         "--query", "accessToken", "-o", "tsv"],
        text=True,
    ).strip()


def events(response):
    """Yield parsed SSE payloads. Frames are separated by a blank line."""
    buffer = ""
    for chunk in response:
        buffer += chunk.decode("utf-8", "replace")
        while "\n\n" in buffer:
            frame, buffer = buffer.split("\n\n", 1)
            for line in frame.split("\n"):
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload and payload != "[DONE]":
                    try:
                        yield json.loads(payload)
                    except json.JSONDecodeError:
                        pass


def main() -> None:
    tok = token()
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}

    # A conversation is server-side state. Reuse its id to give the agent a memory of
    # this exchange; drop it and every turn starts from nothing.
    req = urllib.request.Request(f"{ENDPOINT}/openai/v1/conversations",
                                 data=b"{}", headers=headers)
    conversation = json.load(urllib.request.urlopen(req))["id"]

    body = {
        "agent_reference": {"name": AGENT, "type": "agent_reference"},
        "conversation": conversation,
        "input": [{"role": "user", "content": QUESTION}],
        "stream": True,
    }
    req = urllib.request.Request(f"{ENDPOINT}/openai/v1/responses",
                                 data=json.dumps(body).encode(), headers=headers)

    tools, sources, usage = [], [], None
    print(f"{DIM}> {QUESTION}{RESET}\n")

    with urllib.request.urlopen(req) as response:
        for event in events(response):
            kind = event.get("type", "")

            if kind == "response.output_text.delta":
                print(event.get("delta", ""), end="", flush=True)

            elif kind == "response.output_item.added":
                item_type = event.get("item", {}).get("type", "")
                if item_type.endswith("_call") and item_type not in tools:
                    tools.append(item_type)

            elif kind == "response.completed":
                result = event.get("response", {})
                usage = result.get("usage")
                for item in result.get("output", []):
                    for part in item.get("content", []):
                        for ann in part.get("annotations", []):
                            if ann.get("url") and ann["url"] not in [s["url"] for s in sources]:
                                sources.append({"title": ann.get("title") or ann["url"],
                                                "url": ann["url"]})

    print("\n")
    if tools:
        print(f"{BOLD}Tools the service ran:{RESET} " + ", ".join(tools))
    if sources:
        print(f"{BOLD}Sources:{RESET}")
        for i, s in enumerate(sources, 1):
            print(f"  [{i}] {s['title']}\n      {DIM}{s['url']}{RESET}")
    if not sources:
        print(f"{DIM}No sources — the model answered from its own weights, not from the web.{RESET}")
    if usage:
        print(f"{DIM}{usage.get('total_tokens')} tokens · conversation {conversation}{RESET}")


if __name__ == "__main__":
    main()
