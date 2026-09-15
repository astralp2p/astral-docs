# apphost.list_tokens

List access tokens, optionally filtered by identity. Local-only — queries from
the network are rejected.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before any token is read when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* identity (string8) – If set, only tokens for this identity are listed, given
  as a hex public key or a name resolved via the directory. When omitted or
  empty, every token is listed.

## Returned objects

The operation returns a stream of `apphost.access_token` objects, followed by an `eos` object. An `error_message` object is returned instead if `identity` is set and does not resolve. An `error_message` object reading `missing identity` is returned instead if `identity` resolves to the anonymous identity, as `anyone` does.

## Examples

```shellsession
$ astral-query apphost.list_tokens -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"apphost.access_token","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Token":"k7m2q5x9r3v4n8p1","ExpiresAt":"2027-05-27T12:00:00+02:00"}}
{"Type":"eos","Object":null}
```
