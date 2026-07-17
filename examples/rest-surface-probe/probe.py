"""Probe the two REST surfaces a Foundry project exposes, and prove how they differ.

Not from the book — this is the script I wish I had had while writing it.

One project endpoint serves two APIs that disagree about versioning, and the error
messages only tell you about one problem at a time. This script makes all of it visible
in one run: it sends the wrong request on purpose, prints what comes back, then sends
the right one.

Run:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
    python probe.py [AgentName]

Reads nothing, writes nothing, creates nothing — except one conversation and one
response if you pass an agent name.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ENDPOINT = os.environ["PROJECT_ENDPOINT"].rstrip("/")
AGENT = sys.argv[1] if len(sys.argv) > 1 else None


def token() -> str:
    """az CLI rather than DefaultAzureCredential, to keep this file dependency-free."""
    return subprocess.check_output(
        ["az", "account", "get-access-token", "--scope", "https://ai.azure.com/.default",
         "--query", "accessToken", "-o", "tsv"],
        text=True,
    ).strip()


def call(method: str, url: str, body: dict | None, tok: str) -> tuple[int, str]:
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def show(label: str, status: int, body: str) -> None:
    mark = "OK  " if 200 <= status < 300 else "FAIL"
    print(f"  [{mark} {status}] {label}")
    if not 200 <= status < 300:
        try:
            msg = json.loads(body)["error"]["message"]
        except Exception:
            msg = body[:160]
        print(f"         -> {msg[:150]}")


def main() -> None:
    tok = token()
    print(f"\nProject: {ENDPOINT}\n")

    print("1. The control surface wants api-version:")
    show("GET /agents?api-version=v1", *call("GET", f"{ENDPOINT}/agents?api-version=v1", None, tok))
    show("GET /agents  (no api-version)", *call("GET", f"{ENDPOINT}/agents", None, tok))

    print("\n2. The OpenAI-compatible surface refuses it:")
    show("POST /openai/v1/conversations?api-version=v1",
         *call("POST", f"{ENDPOINT}/openai/v1/conversations?api-version=v1", {}, tok))
    status, body = call("POST", f"{ENDPOINT}/openai/v1/conversations", {}, tok)
    show("POST /openai/v1/conversations", status, body)
    conversation = json.loads(body)["id"] if 200 <= status < 300 else None

    if not AGENT:
        print("\nPass an agent name to also probe the response payload shape.")
        return

    print(f"\n3. How the agent must be referenced (agent={AGENT!r}).")
    print("   Each rejection reveals exactly one problem, so you climb this ladder one")
    print("   rung at a time. Note that 'deprecated' only shows up once the shape is right:")
    base = {"conversation": conversation, "input": [{"role": "user", "content": "Say OK."}]}
    show('{"agent": "<name>"}',
         *call("POST", f"{ENDPOINT}/openai/v1/responses", {**base, "agent": AGENT}, tok))
    show('{"agent": {"name": ..., "type": ...}}',
         *call("POST", f"{ENDPOINT}/openai/v1/responses",
               {**base, "agent": {"name": AGENT, "type": "agent_reference"}}, tok))
    show('{"agent_reference": {"name": ...}}',
         *call("POST", f"{ENDPOINT}/openai/v1/responses",
               {**base, "agent_reference": {"name": AGENT}}, tok))
    status, body = call("POST", f"{ENDPOINT}/openai/v1/responses",
                        {**base, "agent_reference": {"name": AGENT, "type": "agent_reference"}}, tok)
    show('{"agent_reference": {"name": ..., "type": "agent_reference"}}', status, body)
    if 200 <= status < 300:
        text = "".join(c.get("text", "")
                       for item in json.loads(body).get("output", [])
                       for c in item.get("content", []))
        print(f"         -> agent said: {text.strip()[:80]!r}")


if __name__ == "__main__":
    main()
