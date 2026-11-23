# services.not_granted

The requested services a caller holds no discovery permit for, sent first on a
[`services.discover`](../ops/services.discover.md) stream that names services.
A one-shot stream carries it at most once, before any other object. A follow
sends it again whenever an
[authority change](../ops/services.discover.md#authority-changes) alters the
list; each one replaces the previous list, and an empty `Services` means the
caller holds every requested permit.

`Services` lists each requested service for which the caller lacks
[`mod.services.service_discovery_action`](mod.services.service_discovery_action.md)
on at least one contributing node. On those nodes a
[swarm caller](../ops/services.discover.md#visibility) still receives the open
offerings of those services and no private one; any other caller receives
none. The list depends only on the caller's permits, never on providers. An
app can ask for a permit with
[`apphost.request_grant`](../../apphost/ops/apphost.request_grant.md).

## Fields

* Services (array of string8) – Requested services the caller is not granted, sorted.

## Example

```json
{
  "Type": "services.not_granted",
  "Object": { "Services": ["bitcoin-wallet"] }
}
```
