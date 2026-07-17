#!/usr/bin/env bash
# Print the Foundry roles with the data actions they actually grant.
#
# Not from the book — this answers two questions the role names refuse to answer.
#
# 1. What is this role allowed to do? "Foundry Agent Consumer" and "Foundry Project
#    Runtime User" sound like one permission wearing two names. They are not: one lets
#    an identity interact with an agent, the other lets it create responses. An app that
#    lists agents fine and then 403s the moment you hit send is almost always this
#    distinction — and no amount of staring at the names tells you so. The dataActions do.
#
# 2. What is this role called today? The roles were renamed in 2026 (Azure AI User ->
#    Foundry User, and so on) and the old names still surface in places. So this script
#    looks each role up by its GUID, which did not change, and prints whatever name your
#    tenant currently returns. That is also why the book tells you to write GUIDs, not
#    names, into scripts and templates: the GUID is the stable identifier.
#
#   ./list-foundry-roles.sh
#
# Requires: az, jq
set -euo pipefail

# GUID -> what the book calls it. Stable across every tenant.
ROLES=(
  "53ca6127-db72-4b80-b1b0-d745d6d5456d  Foundry User"
  "c883944f-8b7b-4483-af10-35834be79c4a  Foundry Owner"
  "e47c6f54-e4a2-4754-9501-8e0985b135e1  Foundry Account Owner"
  "eadc314b-1a2d-4efa-be10-5d325db5065e  Foundry Project Manager"
  "eed3b665-ab3a-47b6-8f48-c9382fb1dad6  Foundry Agent Consumer"
  "142bfaed-a13f-4c2d-bed2-6db62c4a1009  Foundry Project Runtime User"
)

SCOPE="/subscriptions/$(az account show --query id -o tsv)"
echo
echo "Scope: $SCOPE"

for entry in "${ROLES[@]}"; do
  guid="${entry%% *}"
  book_name="$(sed 's/^[^ ]*  *//' <<<"$entry")"

  json=$(az role definition list --scope "$SCOPE" --query "[?name=='$guid']" -o json 2>/dev/null || echo '[]')
  if [[ "$(jq 'length' <<<"$json")" == "0" ]]; then
    printf '\n%s\n  %s\n  not visible at this scope\n' "$book_name" "$guid"
    continue
  fi

  live_name=$(jq -r '.[0].roleName' <<<"$json")
  printf '\n%s\n  %s\n' "$live_name" "$guid"
  [[ "$live_name" != "$book_name" ]] && printf '  (the book calls this "%s")\n' "$book_name"
  shorten() { sed "s|Microsoft.CognitiveServices/accounts/|.../|; s|^|  $1 |"; }
  jq -r '.[0].permissions[0].dataActions[]?' <<<"$json" | shorten "data  "
  jq -r '.[0].permissions[0].notDataActions[]?' <<<"$json" | shorten "EXCEPT"
  [[ -z "$(jq -r '.[0].permissions[0].dataActions[]?' <<<"$json")" ]] &&
    echo "  (control plane only — no data actions)"
done

cat <<'NOTE'

The pair that gets confused
───────────────────────────
  Foundry Agent Consumer        .../endpoints/interact/action   talk to an agent
  Foundry Project Runtime User  .../responses/*                 create responses

Two roles, not one. Assign both — at project scope, not account scope — to anything
that chats with an agent, including the managed identity of your own app.
NOTE
