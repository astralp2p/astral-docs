# apphost.list_tokens

List access tokens, optionally filtered by identity.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before any token is read when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (identity) – If set, only tokens for this identity are listed.

## Returned objects

The operation returns a stream of `apphost.access_token` objects, followed by an `eos` object.

## Examples

```shellsession
$ astral-query apphost.list_tokens -id 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"apphost.access_token","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Token":"k7m2q5x9r3v4n8p1","ExpiresAt":"2027-05-27T12:00:00+02:00"}}
{"Type":"eos","Object":null}
```
