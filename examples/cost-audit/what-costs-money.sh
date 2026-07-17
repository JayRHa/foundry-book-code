#!/usr/bin/env bash
# Show what in a Foundry resource group is actually billing you, and what is free.
#
# Not from the book — this is the script I wrote after building the book's demos and
# wanting to be sure I had not left a meter running.
#
# The mental model that costs people money: "I deleted the agent, so I am done." You are
# not. The agent is free. What bills is what the agent was attached to — the AI Search
# index, the Bot Service registration the publish wizard silently created, a provisioned
# throughput deployment, a fine-tuned model you left hosted.
#
# This prints every resource in the group, sorted by whether it charges you when idle:
#
#   ./what-costs-money.sh <resource-group>
#
# It reads only. Nothing here deletes anything — the delete commands are printed for you
# to read first and run yourself.
#
# Requires: az, jq
set -euo pipefail

RG="${1:-}"
if [[ -z "$RG" ]]; then
  echo "usage: ./what-costs-money.sh <resource-group>" >&2
  exit 1
fi

echo
echo "Resource group: $RG"
echo

# --- Things that bill you even when nobody is using them ------------------------------
echo "BILLS WHILE IDLE"
echo "────────────────"
idle=$(az resource list -g "$RG" -o json | jq -r '
  .[] | select(
    (.type | test("Microsoft.Search/searchServices"; "i")) or
    (.type | test("Microsoft.BotService/botServices"; "i")) or
    (.type | test("Microsoft.ContainerRegistry"; "i")) or
    (.type | test("Microsoft.Web/serverfarms"; "i")) or
    (.type | test("Microsoft.DocumentDB"; "i")) or
    (.type | test("Microsoft.Compute/virtualMachines"; "i"))
  ) | "  \(.type | split("/") | last)\t\(.name)\t\(.sku.name // .sku.tier // "-")\t\(.id)"')
if [[ -n "$idle" ]]; then
  printf '%s\n' "$idle" | cut -f1-3 | column -t -s $'\t'
  echo
  echo "  These charge per hour regardless of traffic. If the demo is over, delete them"
  echo "  by id — read the list above first, then run:"
  printf '%s\n' "$idle" | cut -f4 | sed 's|^|    az resource delete --ids |'
else
  echo "  (none — nothing here charges you for sitting still)"
fi

# --- Model deployments: free to keep, pay per token ------------------------------------
echo
echo "PAY PER TOKEN (free to keep, but check the SKU)"
echo "──────────────────────────────────────────────"
for acct in $(az cognitiveservices account list -g "$RG" --query "[].name" -o tsv); do
  echo "  $acct"
  az cognitiveservices account deployment list -g "$RG" -n "$acct" -o json 2>/dev/null | jq -r '
    .[] | "    \(.name)\t\(.sku.name)\t cap \(.sku.capacity)\t\(
      if (.sku.name | test("Provisioned|ProvisionedManaged"; "i"))
      then "<-- PROVISIONED: billed hourly, not per token"
      else "per-token" end)"' | column -t -s $'\t'
done

# --- Fine-tuned models: hosting is the meter -------------------------------------------
echo
echo "FINE-TUNED MODELS"
echo "─────────────────"
found=0
for acct in $(az cognitiveservices account list -g "$RG" --query "[].name" -o tsv); do
  deployed=$(az cognitiveservices account deployment list -g "$RG" -n "$acct" -o json 2>/dev/null |
    jq -r '.[] | select(.properties.model.name | test("ft|ft-"; "i")) | "    \(.name) on \(.properties.model.name)"')
  if [[ -n "$deployed" ]]; then
    printf '%s\n' "$deployed"
    found=1
  fi
done
[[ $found == 0 ]] && echo "  (none deployed — an untrained-but-undeployed model costs nothing to keep)"

cat <<'NOTE'

The rule
────────
  Agents, projects, and the Foundry resource itself: free.
  Model deployments: free to keep, you pay per token — unless the SKU is Provisioned.
  Everything in the first list: billing right now.

The one people miss: publishing an agent to Teams creates an Azure Bot Service
registration (SKU S1) in the background. Deleting the agent does not delete it.
NOTE
