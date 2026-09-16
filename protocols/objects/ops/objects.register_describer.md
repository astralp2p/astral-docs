# objects.register_describer

Register the caller as an external describer. The module proxies `objects.describe` calls back to the caller's identity until the registration's lease expires. Network-originated queries are rejected.

The caller must hold
[`mod.auth.serve_objects_action`](../../auth/types/mod.auth.serve_objects_action.md)
for the `describer` role. The query is rejected when the caller is not
authorized.

Registration is leased. The node clamps the requested `duration` to its
configured maximum and answers with the granted
[`mod.objects.registration_lease`](../types/mod.objects.registration_lease.md).
Repeating the op renews the caller's existing registration in place rather than
adding a second one, so a describer renews by registering again. Expiry is
silent: an expired registration receives no further describe calls and the node
sends the registrant no notice.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.
* duration (duration) – Requested lease lifetime. Defaults to 1 hour. The node clamps it to its configured maximum.

## Returned objects

The operation returns one of:
* An `error_message` object if the caller identity is missing/zero, the caller is the node itself, or the describer cannot be added.
* A `mod.objects.registration_lease` object once the external describer is registered, carrying the lease the node granted.

## Examples

```shellsession
$ astral-query objects.register_describer -out json
{"Type":"mod.objects.registration_lease","Object":{"Duration":3600000000000,"ExpiresAt":"2026-07-29T07:00:00Z"}}
```

A request above the node's maximum is answered with the clamped lease, not an
error:

```shellsession
$ astral-query objects.register_describer -duration 24h -out json
{"Type":"mod.objects.registration_lease","Object":{"Duration":21600000000000,"ExpiresAt":"2026-07-29T12:00:00Z"}}
```
