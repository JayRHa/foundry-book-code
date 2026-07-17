# Chapter 5 — Deploying Models: Deployment Types, Quotas, and Cost

Code from the book **Microsoft Foundry** by Jannik Reinhard.

| File | What it does |
|---|---|
| [`batch-input.jsonl`](batch-input.jsonl) | Input format for the Batch API — one request per line, 50% cheaper, 24h window. |
| [`create-deployment.sh`](create-deployment.sh) | Discover the exact model identity, then create the deployment with a capacity. |
| [`deployment.bicep`](deployment.bicep) | The deployment as a child resource of the account. |

---

[← All chapters](../README.md)
