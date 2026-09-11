# nodes.sessions

List all open multiplexed sessions across all active links, ordered by creation time.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any session is listed when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns a stream of `mod.nodes.session_info` objects, terminated by `eos`. On a per-item send failure, an `error_message` is sent instead and the stream ends.

## Examples

```shellsession
$ astral-query nodes.sessions -out json
{"Type":"mod.nodes.session_info","Object":{"ID":"a1b2c3d4e5f60718","LinkID":"7c1a93b50f2e4d18","RemoteIdentity":"037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590","Outbound":true,"Query":"objects.get","Bytes":4096,"Age":12000000000}}
{"Type":"eos","Object":null}
```
