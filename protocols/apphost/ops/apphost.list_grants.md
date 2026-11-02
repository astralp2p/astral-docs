# apphost.list_grants

List the node-local grants an identity currently holds, one
[`mod.apphost.grant`](../types/mod.apphost.grant.md) each.

The listing reports what authorizes now: an expired grant is dropped, the way
the authorizer drops it. Each grant carries its ID, which names it to
[`apphost.revoke`](apphost.revoke.md), and its expiry. An identity can hold
several grants for one action ([Grants](../README.md#grants)); the listing
reports each one.

The listing covers grants only. An identity authorized by a
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
holds authority this operation does not report.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The operation answers an `error_message` reading `not permitted` before any
grant is read when the caller is not authorized. The operation also answers
`origin not allowed: network` to a query that arrived over a
[`Link`](../../../core-definitions/link.md), whatever the caller holds.

## Arguments

* identity (string8, required) – The identity whose grants are listed, given as
  a hex public key or a name resolved via the directory.
* out (string8) – Output format.

## Returned objects

The operation returns a stream of
[`mod.apphost.grant`](../types/mod.apphost.grant.md) objects, one per unexpired
grant in ID order, followed by an `eos` object. An `error_message` object is
returned instead if `identity` does not resolve, or if the grants could not be
read. An `error_message` object reading `missing identity` is returned instead
if `identity` resolves to the anonymous identity.

## Examples

```shellsession
$ astral-query apphost.list_grants -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"mod.apphost.grant","Object":{"ID":1,"Permit":{"Action":"mod.auth.serve_apps_action","Constraints":null,"Delegation":0},"ExpiresAt":"2036-05-23T10:00:00Z"}}
{"Type":"mod.apphost.grant","Object":{"ID":2,"Permit":{"Action":"mod.auth.use_blueprints_action","Constraints":null,"Delegation":0},"ExpiresAt":"2036-05-23T10:00:00Z"}}
{"Type":"mod.apphost.grant","Object":{"ID":7,"Permit":{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["inference"],"Nodes":[]}]}}],"Delegation":0},"ExpiresAt":null}}
{"Type":"eos","Object":null}
```

`ExpiresAt` is `null` on a grant that lasts until revoked. A grant is never
delegable, so `Delegation` is `0` on the permit inside every grant.
