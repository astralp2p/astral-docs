# mcp.create_agent

Create a mailbox through the messaging module and store an agent record with
its access token. Mailbox creation follows
[`messaging.create_mailbox`](../../messaging/ops/messaging.create_mailbox.md).
[`mcp.list_agents`](mcp.list_agents.md) can recover the token later.
The agent identity cannot claim a node: its relay contract excludes it from
the claim exception of [`auth.sign_contract`](../../auth/ops/auth.sign_contract.md).

Requires [`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
Network queries are rejected before authorization; denied callers receive no
bytes. If storing the agent record fails, the node attempts to delete the new
mailbox. Cleanup failure is logged; the record error remains the answer.

## Arguments

* alias (string) – Alias to bind; empty binds none and generates none.
* duration (duration) – Token lifetime. Zero or absent uses messaging's `token_duration` (8760h by default).

## Returned objects

* An [`mcp.agent`](../types/mcp.agent.md) with its token.
* An `error_message` from mailbox creation or agent-record storage. An occupied alias returns `alias already taken`.

## Examples

```shellsession
$ astral-query mcp.create_agent -alias scout -out json
{"Type":"mcp.agent","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","Token":"h4d8s2w6y1b9t3n7","ExpiresAt":"2027-08-20T10:00:00Z"}}
```

```shellsession
$ astral-query mcp.create_agent -alias scout -out json
{"Type":"error_message","Object":"alias already taken"}
```
