# mcp.set_exposed

Open or close an agent to callers other than itself. Local-only — queries from
the network are rejected.

Exposure is the account holder's decision, taken on the node. An agent deciding
its own reachability would let one tenant's compromised agent open itself to
the network.

Closing an agent takes effect on conversations already under way: the agent's
queued queries are dropped and its live sessions are closed.

## Arguments

* id (string, required) – The agent, given as a hex public key or alias
  resolved via the directory.
* exposed (bool, required) – True opens the agent, false closes it.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `id` resolves to no
  identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it.
* An `ack` object if the flag was written.

## Examples

```shellsession
$ astral-query mcp.set_exposed -id scout -exposed true -out json
{"Type":"ack","Object":null}
```

```shellsession
$ astral-query mcp.set_exposed -id scout -exposed false -out json
{"Type":"ack","Object":null}
```
