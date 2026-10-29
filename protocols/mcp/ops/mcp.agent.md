# mcp.agent

Read one agent without its token. An agent absent from the mailbox index is
reported as missing; its record remains. [`mcp.list_agents`](mcp.list_agents.md)
and [`mcp.delete_agent`](mcp.delete_agent.md) remove such records.

Requires
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
A network query is answered `origin not allowed: network` before authorization;
a denied caller is answered `not permitted`.

## Arguments

* identity (string8, required) – Agent identity as a hex public key or directory name.

## Returned objects

* An [`mcp.agent_info`](../types/mcp.agent_info.md).
* An `error_message` reading `unknown identity` when the name does not resolve.
* An `error_message` reading `agent not found` when the agent record or mailbox index entry is absent, or either cannot be read.

## Examples

```shellsession
$ astral-query mcp.agent -identity scout -out json
{"Type":"mcp.agent_info","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","ExpiresAt":"2027-08-20T10:00:00Z"}}
```

```shellsession
$ astral-query mcp.agent -identity 026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2 -out json
{"Type":"error_message","Object":"agent not found"}
```
