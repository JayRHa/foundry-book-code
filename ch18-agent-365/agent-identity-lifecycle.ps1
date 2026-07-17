# Every agent identity in the tenant, with the blueprint it derives from.
Connect-MgGraph -Scopes "AgentIdentity.Read.All"

$uri = "https://graph.microsoft.com/beta/servicePrincipals/microsoft.graph.agentIdentity"

(Invoke-MgGraphRequest -Method GET -Uri $uri).value |
    Select-Object displayName, id, agentIdentityBlueprintId, accountEnabled, createdDateTime
