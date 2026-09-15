# apphost.list_grants

List the node-local grants an identity currently holds.

The listing reports what authorizes now: an expired grant is dropped, the way
the authorizer drops it. A [`mod.auth.permit`](../../auth/types/mod.auth.permit.md)
carries no expiry of its own, so a listing that included a lapsed grant could
not mark it as lapsed.

The listing covers grants only. An identity authorized by a
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
holds authority this operation does not report.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before any grant is read when the caller is not
authorized, and a refused caller receives no bytes. The operation also rejects
a query that arrived over a [`Link`](../../../core-definitions/link.md),
whatever the caller holds.

## Arguments

* identity (string8, required) – The identity whose grants are listed, given as
  a hex public key or a name resolved via the directory.
* out (string8) – Output format.

## Returned objects

The operation returns a stream of `mod.auth.permit` objects, followed by an
`eos` object. An `error_message` object is returned instead if `identity` does
not resolve, or if the grants could not be read. An `error_message` object
reading `missing identity` is returned instead if `identity` resolves to the
anonymous identity.

## Examples

```shellsession
$ astral-query apphost.list_grants -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"mod.auth.permit","Object":{"Action":"mod.auth.admin_manage_apps_action","Constraints":null,"Delegation":0}}
{"Type":"mod.auth.permit","Object":{"Action":"mod.auth.serve_apps_action","Constraints":null,"Delegation":0}}
{"Type":"eos","Object":null}
```

A grant is never delegable, so `Delegation` is `0` on every permit this
operation returns.
