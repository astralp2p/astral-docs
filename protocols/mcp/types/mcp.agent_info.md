# mcp.agent_info

An agent record without its token. Returned by
[`mcp.agent`](../ops/mcp.agent.md).

## Fields

* Identity (identity) – The agent's identity, minted by the node.
* Alias (string8) – The agent's alias. Empty when no alias is bound.
* ExpiresAt (time) – The instant at which the agent's access token expires.

## Example

```json
{
  "Type": "mcp.agent_info",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout",
    "ExpiresAt": "2027-08-20T10:00:00Z"
  }
}
```
