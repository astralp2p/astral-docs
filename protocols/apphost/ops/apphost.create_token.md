# apphost.create_token

Create a new access token for an identity. Local-only — queries from the
network are rejected.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before a token is issued when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* identity (string8, required) – The identity the token will authenticate,
  given as a hex public key or a name resolved via the directory.
* duration (duration) – Lifetime of the token. Defaults to 1 year.

## Returned objects

The operation returns one of:
* An `error_message` object if `identity` does not resolve.
* An `error_message` object reading `missing identity` if `identity` resolves to
  the anonymous identity.
* An `error_message` object if there was an error.
* An `apphost.access_token` object if the token was created.

## Examples

```shellsession
$ astral-query apphost.create_token -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"apphost.access_token","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Token":"k7m2q5x9r3v4n8p1","ExpiresAt":"2027-05-27T12:00:00+02:00"}}
```
