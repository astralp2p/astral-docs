# mcp.agent

Return one agent's record without its access token. Local-only — queries from
the network are rejected.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any agent record is read when the caller is not
authorized, and a refused caller receives no bytes. A query from the network is
rejected before the action is submitted.

**An agent whose participant is gone is not found.**
[`messaging.delete_identity`](../../messaging/ops/messaging.delete_identity.md)
on an agent's identity withdraws the participant and leaves the agent record.
The node reads the agent record, then looks the agent's identity up in this
node's mailbox index. An agent the index no longer names is answered
`agent not found`, and its record stays, because
`mod.auth.see_node_state_action` grants no change to the state it reads.
[`mcp.list_agents`](mcp.list_agents.md) and
[`mcp.delete_agent`](mcp.delete_agent.md) delete that record.

## Arguments

* identity (string8, required) – The agent, given as a hex public key or a name
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `identity` resolves to
  no identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it, this node's mailbox index no longer
  names it, or the record or the index cannot be read. A caller distinguishes a
  mistyped name from an identity that is not an agent.
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
