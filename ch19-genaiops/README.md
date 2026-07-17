# Chapter 19 — From Prototype to Production: GenAIOps

Code from the book **Microsoft Foundry** by Jannik Reinhard.

| File | What it does |
|---|---|
| [`.github/workflows/evaluate.yml`](.github/workflows/evaluate.yml) | CI/CD with an evaluation gate: a PR that lowers quality does not merge. |
| [`deploy.sh`](deploy.sh) | Deploy it. |
| [`enable-tracing.sh`](enable-tracing.sh) | Tracing without touching application code. |
| [`evaluation-config.json`](evaluation-config.json) | The thresholds the gate enforces. |
| [`main.bicep`](main.bicep) | The full Foundry deployment as Bicep — account, project, deployments, RBAC. |
| [`main.tf`](main.tf) | The Terraform equivalent, including where the provider still needs azapi. |
| [`policy-definition.xml`](policy-definition.xml) | The APIM policy in front of Foundry. |

---

[← All chapters](../README.md)
