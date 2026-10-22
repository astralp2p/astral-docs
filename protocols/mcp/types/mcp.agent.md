# mcp.agent

An agent record with its apphost bearer token. Returned by
[`mcp.create_agent`](../ops/mcp.create_agent.md) and
[`mcp.list_agents`](../ops/mcp.list_agents.md).

## Fields

* Identity (identity) – The agent's identity, minted by the node.
* Alias (string8) – The agent's alias. Empty when no alias is bound.
* Token (string8) – The access token authenticating the agent. Empty in an
  `mcp.list_agents` answer when the token no longer authenticates as the agent.
* ExpiresAt (time) – The instant at which the token expires.

## Example

```json
{
  "Type": "mcp.agent",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout",
    "Token": "h4d8s2w6y1b9t3n7",
    "ExpiresAt": "2027-08-20T10:00:00Z"
  }
}
```
