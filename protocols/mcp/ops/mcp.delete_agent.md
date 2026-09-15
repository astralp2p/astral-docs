# mcp.delete_agent

Remove an agent: revoke its access token, unset its alias, and delete its
record. The agent's queued queries are dropped and its live sessions closed.
The signed relay contract stays indexed until it expires. Local-only — queries
from the network are rejected.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before the agent is resolved when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* identity (string8, required) – The agent, given as a hex public key or a name
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `identity` resolves to
  no identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it.
* An `error_message` object if revoking the token, unsetting the alias, or
  deleting the record failed.
* An `ack` object if the agent was removed.

## Examples

```shellsession
$ astral-query mcp.delete_agent -identity scout -out json
{"Type":"ack","Object":null}
```
