# mcp.agent_info

An agent's record without its access token: what a caller may read about an
agent whose credentials it does not hold. Returned by `mcp.agent`.

The token is absent from the type rather than left empty, so a caller never
reads a withheld token as an agent that has none.

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
    "ExpiresAt": "2027-08-20T12:00:00+02:00"
  }
}
```
