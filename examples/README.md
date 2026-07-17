# Extra examples

Not from the book. These came out of building it — each one answers a question the
docs left open, and each was run against a real Foundry project before it landed here.

### [`rest-surface-probe/`](rest-surface-probe) — Prove how the two REST surfaces differ

Sends the wrong request on purpose and prints what comes back, then sends the right one. Shows the api-version split and the three-rung ladder from `agent` to `agent_reference`.

### [`streaming-with-citations/`](streaming-with-citations) — Stream an answer with its tools and sources

The Python twin of the Teams tab backend, in one dependency-free file. Shows what the event stream carries besides text — the tools the service ran, and the annotations that let you put a source under a claim.

### [`rbac-roles/`](rbac-roles) — What each Foundry role actually grants

Looks each role up by GUID and prints its dataActions, so you can see for yourself that Agent Consumer and Project Runtime User are two different permissions.

### [`cost-audit/`](cost-audit) — What in a resource group is billing you

Separates what charges you while idle from what is free to keep. Written after building the book's demos and wanting to be sure no meter was left running.

---

[← All chapters](../README.md)
