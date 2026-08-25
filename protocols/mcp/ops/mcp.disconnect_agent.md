# mcp.disconnect_agent

End an agent's live traffic: close the conversations the agent is in and drop
the queries waiting for it. Local-only — queries from the network are rejected.

The operation carries no permission and writes none. What an agent permits is
held by whoever owns it and is answered on the next call the node asks about
([`auth`](../../auth/README.md)); the traffic already flowing is the one part of
that change its owner cannot make elsewhere.

Silencing an agent is the account holder's decision, taken on the node. An
operation reachable over the network would let any caller end any agent's
conversations.

A parked `astral-listen` is left alone. A listener is the agent waiting to be
called, not a caller it is talking to, so draining one would end the agent's own
call rather than the traffic it is carrying.

## Arguments

* id (string, required) – The agent, given as a hex public key or alias
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `id` resolves to no
  identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it.
* An `ack` object if the agent's traffic was ended.

## Examples

```shellsession
$ astral-query mcp.disconnect_agent -id scout -out text
#[ack]
```
