# messaging.create_mailbox

Create a mailbox with a fresh identity, optional alias, apphost token, and
signed relay and hosting contracts. The node holds the identity's key. This
creates a messaging participant, not a node user or a node claim.

Requires
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
A `network` or `mcp` query is answered `origin not allowed: <origin>` before
authorization; a denied caller is answered `not permitted`. [Mailbox
Hosting](../../../topics/mailbox-hosting.md#hosting) defines the contracts and
the separate send/receive permissions.

## Arguments

* alias (string) – Alias to bind. Empty binds none; none is generated.
* duration (duration) – Token lifetime. Zero or absent uses `token_duration` (8760h by default). Contract lifetimes are unaffected.

## Returned objects

* A [`messaging.mailbox_credential`](../types/messaging.mailbox_credential.md) with the new token.
* An `error_message` if key storage/indexing, contract signing/indexing/storage,
  alias binding, token issuance, or mailbox indexing fails.
  An occupied alias returns `alias already taken`. The mailbox index is written
  last; a failed call leaves no served mailbox.

## Examples

```shellsession
$ astral-query messaging.create_mailbox -alias scout -out json
{"Type":"messaging.mailbox_credential","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","Token":"h4d8s2w6y1b9t3n7","ExpiresAt":"2027-08-20T10:00:00Z"}}
```

```shellsession
$ astral-query messaging.create_mailbox -alias scout -out json
{"Type":"error_message","Object":"alias already taken"}
```
