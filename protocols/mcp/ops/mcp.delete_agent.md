# mcp.delete_agent

Remove an agent: revoke its access token, unset its alias, and delete its
record. The agent's queued queries are dropped and its live sessions closed.
The signed relay contract stays indexed until it expires. Local-only — queries
from the network are rejected.

## Arguments

* id (string, required) – The agent, given as a hex public key or alias
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `id` resolves to no
  identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it.
* An `error_message` object if revoking the token, unsetting the alias, or
  deleting the record failed.
* An `ack` object if the agent was removed.

## Examples

```shellsession
$ astral-query mcp.delete_agent -id scout -out json
{"Type":"ack","Object":null}
```
