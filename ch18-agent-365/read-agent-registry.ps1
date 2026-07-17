# List every agent in the tenant that is surfaced in Microsoft 365 Copilot,
# and show which platform built it. Requires an Agent 365 license.
Connect-MgGraph -Scopes "CopilotPackages.Read.All"

$uri = "https://graph.microsoft.com/beta/copilot/admin/catalog/packages" +
       "?`$filter=supportedHosts/any(h:h eq 'Copilot')"

$agents = (Invoke-MgGraphRequest -Method GET -Uri $uri).value

$agents |
    Select-Object displayName, publisher, platform, isBlocked, lastModifiedDateTime |
    Sort-Object platform |
    Format-Table -AutoSize
