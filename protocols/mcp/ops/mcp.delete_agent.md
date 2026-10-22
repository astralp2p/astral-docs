# mcp.delete_agent

Delete an agent's mailbox through
[`messaging.delete_mailbox`](../../messaging/ops/messaging.delete_mailbox.md),
then delete its agent record. Correspondents' mail and signed contracts remain.

Requires [`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
Network queries are rejected before authorization; denied callers receive no bytes.

A missing mailbox does not prevent record deletion. Other mailbox-deletion
failures preserve the agent record for retry. A record already removed during
deletion is tolerated. If mailbox deletion has removed the alias, the remaining
agent record is addressed by its hex identity. `mcp.list_agents` may already
have removed that record.

## Arguments

* identity (string8, required) – Agent identity as a hex public key or directory name.

## Returned objects

* An `ack` when removed.
* An `error_message` reading `unknown identity` when the name does not resolve.
* An `error_message` reading `agent not found` when the initial record is absent or cannot be read.
* An `error_message` if mailbox or agent-record deletion fails.

## Examples

```shellsession
$ astral-query mcp.delete_agent -identity scout -out json
{"Type":"ack","Object":null}
```
