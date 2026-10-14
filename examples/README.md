<!-- jr-brand:start -->
<p align="center">
  <a href="https://jannikreinhard.com/">
    <img src="https://raw.githubusercontent.com/JayRHa/.github/main/assets/readme/brand-header.png" alt="Jannik Reinhard — I help enterprises ship secure AI agents" width="100%">
  </a>
</p>
<p align="center">
  <a href="https://jannikreinhard.com/">Website</a> ·
  <a href="https://www.linkedin.com/in/jannik-r/">LinkedIn</a> ·
  <a href="https://x.com/jannik_reinhard">X</a> ·
  <a href="https://www.youtube.com/@jannikreinhard">YouTube</a>
</p>
<!-- jr-brand:end -->

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

<!-- jr-brand-footer:start -->
---

[Articles and guides](https://jannikreinhard.com/) · [Repository index](https://github.com/JayRHa/.github/blob/main/REPOSITORIES.md)
<!-- jr-brand-footer:end -->
