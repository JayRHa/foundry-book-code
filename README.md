<!-- jr-brand:start -->
<div align="center">
  <a href="https://jannikreinhard.com/">
    <img src="https://raw.githubusercontent.com/JayRHa/.github/main/assets/readme/learning.svg" alt="Jannik Reinhard — AI, Cloud and Endpoint Management" width="100%">
  </a>
  <h1>Microsoft Foundry · Book Code</h1>
  <p><strong>All the code from the book 'Microsoft Foundry' by Jannik Reinhard — every listing as a runnable file, plus extra examples.</strong></p>
  <p>
  <a href="https://jannikreinhard.com/"><img src="https://img.shields.io/badge/Website-0A5FC0?style=flat-square&amp;logo=wordpress&amp;logoColor=white" alt="Website"></a>
  <a href="https://github.com/JayRHa"><img src="https://img.shields.io/badge/GitHub-081427?style=flat-square&amp;logo=github&amp;logoColor=white" alt="GitHub"></a>
  <a href="https://www.linkedin.com/in/jannik-r/"><img src="https://img.shields.io/badge/LinkedIn-0795FF?style=flat-square&amp;logo=linkedin&amp;logoColor=white" alt="LinkedIn"></a>
  <a href="https://x.com/jannik_reinhard"><img src="https://img.shields.io/badge/X-081427?style=flat-square&amp;logo=x&amp;logoColor=white" alt="X"></a>
  <a href="https://www.youtube.com/@ModernDevMgmt/featured"><img src="https://img.shields.io/badge/YouTube-0A5FC0?style=flat-square&amp;logo=youtube&amp;logoColor=white" alt="YouTube"></a>
</p>
  <p><sub>Book · Sample · Pattern · Python · Practical by design</sub></p>
</div>
<!-- jr-brand:end -->

## About This Repository

Every listing from the book **Microsoft Foundry** by [Jannik Reinhard](https://jannikreinhard.com),
as a file you can run, plus a handful of extra examples that came out of writing it.

## Start Here

```bash
git clone https://github.com/JayRHa/foundry-book-code
cd foundry-book-code

az login
export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export FOUNDRY_OPENAI_BASE_URL="https://<resource>.openai.azure.com/openai/v1/"

pip install -r requirements.txt
python ch08-first-agent/create_agent.py
```

Both endpoints are on the project's overview page in the Foundry portal. Nothing here
uses an API key — see [Chapter 13](ch13-identity-access) for why.

## Chapters

| | Chapter | What is in it |
|---|---|---|
| 3 | [Your First Foundry Resource](ch03-first-resource) | The resource and project, in CLI and Bicep |
| 4 | [The Model Catalog](ch04-model-catalog) | What you can really deploy, in this region, today |
| 5 | [Deploying Models](ch05-deploying-models) | Deployments, SKUs, and the Batch API |
| 6 | [Talking to Models in Code](ch06-talking-to-models) | Chat, streaming, structured output, vision, Claude |
| 7 | [Grounding AI in Your Data](ch07-grounding) | Connections and knowledge bases |
| 8 | [Your First Agent](ch08-first-agent) | Agent, conversation, response — SDK and REST |
| 9 | [Agent Tools](ch09-agent-tools) | Function calling, OpenAPI, MCP |
| 10 | [Multi-Agent and Memory](ch10-multi-agent) | A2A, orchestration, hosted agents, memory |
| 11 | [Fine-Tuning](ch11-fine-tuning) | Training data, the job, the deployment |
| 12 | [Beyond Text](ch12-beyond-text) | Images, video, Foundry Tools |
| 13 | [Identity and Access](ch13-identity-access) | RBAC, killing the keys, agent identity |
| 14 | [Network Security](ch14-network-security) | Private endpoints, abuse-monitoring opt-out |
| 15 | [Guardrails](ch15-guardrails) | Handling a content-filter block honestly |
| 16 | [Evaluations and Red Teaming](ch16-evaluations) | Scoring an agent, attacking an agent |
| 17 | [The Control Plane](ch17-control-plane) | Azure Policy over models |
| 18 | [Agent 365](ch18-agent-365) | The agent registry and its policies |
| 19 | [GenAIOps](ch19-genaiops) | Bicep, Terraform, CI/CD with an evaluation gate |
| 20 | [Publishing Agents](ch20-publishing) | Versions, updates, rollback |
| 21 | [Foundry at the Edge](ch21-foundry-local) | Foundry Local |
| — | [Appendix](appendix) | RBAC table, az cheat sheet, Bicep skeleton |

## Extra Examples

Not in the book. Each one answers a question the docs left open, and each was run
against a real project before it landed here.

| | What it answers |
|---|---|
| [`rest-surface-probe/`](examples/rest-surface-probe) | Why does the same project endpoint want `api-version` on one path and reject it on another? |
| [`streaming-with-citations/`](examples/streaming-with-citations) | What is in the event stream besides text? |
| [`rbac-roles/`](examples/rbac-roles) | What does each Foundry role actually grant? |
| [`cost-audit/`](examples/cost-audit) | What in this resource group is billing me right now? |

## About the Code

**These are the book's listings, not a rewrite of them.** A listing printed in a book can
lean on the prose around it: the book explains what `PROJECT_ENDPOINT` is a page earlier,
so the listing just uses it. A file cannot. So each file here adds the bootstrap the book
resolves in prose — reading the endpoint from the environment, constructing the client —
and otherwise leaves the code exactly as printed. Where the book shows a fragment on
purpose, the file says so in its docstring and shows the surrounding lines it needs.

Where reality has since diverged from what shipped, the file says so rather than
pretending. See the note at the top of [`ch16-evaluations/red_team.py`](ch16-evaluations/red_team.py)
for an example.

Every file starts with a docstring naming its chapter and the exact `export` lines it
needs. There is no shared config module: each file stands alone, so you can copy one out
of here and into your own project without dragging anything with it.

## Related

- 📕 The book: **Microsoft Foundry** — Jannik Reinhard
- 💬 [foundry-agent-tab](https://github.com/JayRHa/foundry-agent-tab) — chat with your Foundry agents from a Teams tab
- 🌐 [jannikreinhard.com](https://jannikreinhard.com)

## License

MIT — see [LICENSE](LICENSE).

<!-- jr-brand-footer:start -->

---

<div align="center">
  <p><sub>Built and maintained by <a href="https://jannikreinhard.com/">Jannik Reinhard</a> · Microsoft MVP for Security and AI Platform.</sub></p>
  <p><a href="https://www.buymeacoffee.com/jannikreinf">Support the open-source work</a></p>
  <p><strong>Stay healthy, Cheers Jannik</strong></p>
</div>

<!-- jr-brand-footer:end -->
