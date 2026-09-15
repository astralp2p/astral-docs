# nodes.resolve_endpoints

Resolve all known endpoints for an identity by querying every registered endpoint resolver.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before the identity is resolved when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* identity (string8, required) – The identity whose endpoints are resolved, given as a hex public key or a name resolved via the directory.
* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns a stream of `mod.nodes.endpoint_with_ttl` objects, terminated by `eos`. If the identity cannot be resolved the operation is rejected with code `2`; if resolver lookup fails internally the operation is rejected with an internal error code.

## Examples

```shellsession
$ astral-query nodes.resolve_endpoints -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -out json
{"Type":"mod.nodes.endpoint_with_ttl","Object":{"Endpoint":{"Type":"tcp.endpoint","Object":"1.2.3.4:1791"},"TTL":7776000}}
{"Type":"mod.nodes.endpoint_with_ttl","Object":{"Endpoint":{"Type":"tor.endpoint","Object":"abcdefghijklmnop.onion:1791"},"TTL":null}}
{"Type":"eos","Object":null}
```
