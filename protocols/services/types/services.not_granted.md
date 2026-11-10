# services.not_granted

The requested services a caller holds no discovery permit for, sent first on a
[`services.discover`](../ops/services.discover.md) stream that names services.
It appears at most once, before any other object.

`Services` lists each requested service for which the caller lacks
[`mod.services.service_discovery_action`](mod.services.service_discovery_action.md)
on at least one contributing node. The caller still receives open offerings of
those services; private offerings on those nodes are filtered. The list depends
only on the caller's permits, never on providers. An app can ask for a permit
with [`apphost.request_grant`](../../apphost/ops/apphost.request_grant.md).

## Fields

* Services (array of string8) – Requested services the caller is not granted, sorted.

## Example

```json
{
  "Type": "services.not_granted",
  "Object": { "Services": ["bitcoin-wallet"] }
}
```
