# mcp.agent

A structure describing an agent registered with the `mcp` module, including the
access token the agent presents to the MCP endpoint. Returned by
`mcp.create_agent` and `mcp.list_agents`.

The token is a credential. `mcp.agent_info` is the same record without it, and
is what a caller reads when it does not hold the agent's credentials.

## Fields

* Identity (identity) – The agent's identity, minted by the node.
* Alias (string8) – The agent's alias. Empty when no alias is bound.
* Token (string8) – The access token authenticating the agent.
* ExpiresAt (time) – The instant at which the token expires.

## Example

```json
{
  "Type": "mcp.agent",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout",
    "Token": "h4d8s2w6y1b9t3n7",
    "ExpiresAt": "2027-08-20T12:00:00+02:00"
  }
}
```
