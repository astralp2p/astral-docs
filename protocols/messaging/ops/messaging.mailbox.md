# messaging.mailbox

Read a mailbox's identity and alias without credentials. The mailbox index
is read even when its hosting contract has expired or no longer authorizes.

Requires [`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
Network and `mcp` origins are rejected before authorization; denied callers
receive no bytes.

## Arguments

* identity (string8, required) – Mailbox identity as a hex public key or directory name.

## Returned objects

* A [`messaging.mailbox_info`](../types/messaging.mailbox_info.md).
* An `error_message` reading `unknown identity` when the name does not resolve.
* An `error_message` reading `identity not found` when the identity has no mailbox index entry.
* An `error_message` if the index cannot be read.

## Examples

```shellsession
$ astral-query messaging.mailbox -identity scout -out json
{"Type":"messaging.mailbox_info","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout"}}
```

```shellsession
$ astral-query messaging.mailbox -identity 026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2 -out json
{"Type":"error_message","Object":"identity not found"}
```
