# mcp.list_agents

Stream registered agents with their valid access tokens. This enumerates
credentials across tenants; [`mcp.agent`](mcp.agent.md) reads one record
without credentials.

Requires [`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
Network queries are rejected before authorization; denied callers receive no bytes.

An agent absent from the mailbox index is omitted and its record deleted;
deletion failure is logged without changing the answer. A token that no longer
authenticates as the agent, or whose check fails, is returned as an empty
`Token`. The record's expiry remains unchanged.

## Arguments

This operation takes no arguments.

## Returned objects

A stream of [`mcp.agent`](../types/mcp.agent.md), followed by `eos`.
An `error_message` is returned instead if the records or mailbox index cannot
be read.

## Examples

```shellsession
$ astral-query mcp.list_agents -out json
{"Type":"mcp.agent","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","Token":"h4d8s2w6y1b9t3n7","ExpiresAt":"2027-08-20T10:00:00Z"}}
{"Type":"mcp.agent","Object":{"Identity":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","Alias":"","Token":"c5v1k8m4p7q2z6r3","ExpiresAt":"2027-08-20T10:00:00Z"}}
{"Type":"eos","Object":null}
```
