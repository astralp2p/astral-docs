# messaging.delete_mailbox

Remove a mailbox: revoke all its apphost tokens and local grants, unset its
alias, and delete its index entry and owned mail, including archived mail.
Correspondents' copies and signed contracts remain.

Requires [`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
Network and `mcp` origins are rejected before authorization; denied callers
receive no bytes. [Deletion and retry behavior](../../../topics/mailbox-hosting.md#expiry-and-deletion)
defines partial failures and in-flight sends. An MCP agent is removed through
[`mcp.delete_agent`](../../mcp/ops/mcp.delete_agent.md), which also deletes its record.

## Arguments

* identity (string8, required) – Mailbox identity as a hex public key or directory name.

## Returned objects

* An `ack` when removed.
* An `error_message` reading `unknown identity` when the name does not resolve.
* An `error_message` reading `identity not found` for the zero identity or an identity absent from the mailbox index. Nothing is revoked.
* An `error_message` on index lookup, token/grant revocation, alias removal, or mailbox deletion failure.

## Examples

```shellsession
$ astral-query messaging.delete_mailbox -identity scout -out json
{"Type":"ack","Object":null}
```
