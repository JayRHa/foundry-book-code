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

<!-- jr-brand-footer:start -->
---

[Articles and guides](https://jannikreinhard.com/) · [Repository index](https://github.com/JayRHa/.github/blob/main/REPOSITORIES.md)
<!-- jr-brand-footer:end -->
