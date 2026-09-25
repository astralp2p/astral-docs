# mcp.agent

Return one agent's record without its access token. Local-only — queries from
the network are rejected.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any agent record is read when the caller is not
authorized, and a refused caller receives no bytes. A query from the network is
rejected before the action is submitted.

## Arguments

* identity (string8, required) – The agent, given as a hex public key or a name
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `identity` resolves to
  no identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it, or the record cannot be read. A caller
  distinguishes a mistyped name from an identity that is not an agent.
* An `mcp.agent_info` object describing the agent.

## Examples

```shellsession
$ astral-query mcp.agent -identity scout -out json
{"Type":"mcp.agent_info","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","ExpiresAt":"2027-08-20T10:00:00Z"}}
```

```shellsession
$ astral-query mcp.agent -identity 026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2 -out json
{"Type":"error_message","Object":"agent not found"}
```
