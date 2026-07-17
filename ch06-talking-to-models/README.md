# Chapter 6 — Talking to Models in Code

Code from the book **Microsoft Foundry** by Jannik Reinhard.

| File | What it does |
|---|---|
| [`chat.py`](chat.py) | First chat completion and streaming against the v1 endpoint, with Entra auth. |
| [`claude.py`](claude.py) | Calling Claude on Foundry through the native Anthropic Messages API. |
| [`responses-api.sh`](responses-api.sh) | The Responses API over plain curl — no SDK, just a token. |
| [`responses.ts`](responses.ts) | The same call with the TypeScript SDK. |
| [`structured_and_vision.py`](structured_and_vision.py) | JSON-schema output and image input. |
| [`summarize_intune_errors.py`](summarize_intune_errors.py) | End to end: Foundry SDK plus structured output over real Intune error data. |

---

[← All chapters](../README.md)
