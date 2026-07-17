#!/usr/bin/env bash
# Chapter 14 — Check whether the abuse-monitoring opt-out is actually in effect.
#
# From the book "Microsoft Foundry" by Jannik Reinhard.
# https://github.com/JayRHa/foundry-book-code
#
# The opt-out is not something you switch on: you apply for it, Microsoft approves it,
# and only then does the capability flip. So this reads the capability rather than
# setting it — which is the only way to know where you actually stand.
#
#   ./opt-out-abuse-monitoring.sh <account-name> <resource-group>
set -euo pipefail

ACCOUNT="${1:?usage: ./opt-out-abuse-monitoring.sh <account-name> <resource-group>}"
RG="${2:?usage: ./opt-out-abuse-monitoring.sh <account-name> <resource-group>}"

# Look for {"name":"ContentLogging","value":"false"} in the capabilities list
value=$(az cognitiveservices account show -n "$ACCOUNT" -g "$RG" \
  --query "properties.capabilities[?name=='ContentLogging'].value | [0]" -o tsv)

case "$value" in
  false) echo "ContentLogging=false — opt-out in effect. Prompts are not retained." ;;
  true)  echo "ContentLogging=true — prompts are retained for abuse monitoring (the default)." ;;
  *)     echo "ContentLogging not reported on this account (value: '${value:-none}')." ;;
esac
