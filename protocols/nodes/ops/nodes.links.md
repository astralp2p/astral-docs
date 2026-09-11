# nodes.links

List all currently active links, ordered by creation time.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any link is listed when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns a stream of `mod.nodes.link_info` objects, terminated by `eos`. On a per-item send failure, an `error_message` is sent instead and the stream ends.

## Examples

```shellsession
$ astral-query nodes.links -out json
{"Type":"mod.nodes.link_info","Object":{"ID":"7c1a93b50f2e4d18","LocalIdentity":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","RemoteIdentity":"037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590","LocalEndpoint":{"Type":"tcp.endpoint","Object":"10.0.0.5:1791"},"RemoteEndpoint":{"Type":"tcp.endpoint","Object":"1.2.3.4:1791"},"Outbound":true,"Network":"tcp","HighPressure":false,"BytesThroughput":1024}}
{"Type":"eos","Object":null}
```
