# Foundry Local — command reference

Chapter 21 of **Microsoft Foundry** by Jannik Reinhard.

This is a reference, not a script: the lines below use `<placeholders>` and `|` to show
the grammar of each command, so they are meant to be read and adapted rather than run in
sequence. The one thing here you can run as-is is the install.

## Install

```bash
winget install Microsoft.FoundryLocal                            # Windows
brew tap microsoft/foundrylocal && brew install foundrylocal     # macOS
foundry --version
```

## Run a model

```bash
foundry model run qwen2.5-0.5b        # downloads on first use, then opens a chat
```

That single command is the whole pitch of Foundry Local: no resource, no deployment, no
endpoint — the model runs on the machine in front of you.

## Browse the catalog

```bash
foundry model list                              # catalog (downloads execution providers on first run)
foundry model list --filter device=GPU          # device=CPU|GPU|NPU
foundry model list --filter task=chat-completion
foundry model list --filter alias=qwen*
foundry model list --filter device=!GPU         # negation
```

## Manage models

```bash
foundry model download <model>
foundry model info <model> [--license]
foundry model load <model>
foundry model unload <model>
```

## The service

```bash
foundry service start | stop | restart | status | ps | diag
foundry service set <options>
```

`foundry service status` prints the local endpoint. That is the URL you point the OpenAI
client at — see [`local_endpoint.py`](local_endpoint.py).

## The cache

```bash
foundry cache location
foundry cache list
foundry cache cd <path>
foundry cache remove <model>
```

Worth knowing before you wonder where the disk went: models land in this cache and stay
there until you remove them.

## Upgrade

```bash
winget upgrade --id Microsoft.FoundryLocal      # Windows
brew upgrade foundrylocal                       # macOS
```

---

[← All chapters](../README.md)
