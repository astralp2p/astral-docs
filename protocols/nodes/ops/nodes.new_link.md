# nodes.new_link

Establish a new link to the named node, either by dialing a specific endpoint or by running the configured link strategies until one succeeds.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before `identity` is resolved or any link task is
scheduled when the caller is not authorized, and a refused caller receives no
bytes.

## Arguments

* identity (string8, required) – The identity of the node to link to, given as a hex public key or a name resolved via the directory.
* endpoint (string) – If set, dial this specific endpoint, formatted as `<network>:<address>`. Otherwise the operation runs link strategies.
* strategies (string) – Comma-separated list of link strategy names to try (e.g. `basic,tor,nat`). If empty, all registered strategies are used. Ignored when `endpoint` is set.
* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns one of:
* A query rejection with code `2` if `identity` cannot be resolved or the endpoint format is invalid.
* A query rejection with code `3` if the endpoint cannot be parsed.
* A query rejection with code `4` if the context is cancelled or endpoint resolution fails.
* A query rejection with code `5` if the link task cannot be scheduled.
* An `error_message` object if linking fails for another reason.
* A `mod.nodes.link_info` object describing the newly created link.

## Examples

```shellsession
$ astral-query nodes.new_link -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -strategies basic -out json
{"Type":"mod.nodes.link_info","Object":{"ID":"7c1a93b50f2e4d18","LocalIdentity":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","RemoteIdentity":"037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590","LocalEndpoint":{"Type":"tcp.endpoint","Object":"10.0.0.5:1791"},"RemoteEndpoint":{"Type":"tcp.endpoint","Object":"1.2.3.4:1791"},"Outbound":true,"Network":"tcp","HighPressure":false,"BytesThroughput":0}}
```

```shellsession
$ astral-query nodes.new_link -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -endpoint tcp:1.2.3.4:1791 -out json
{"Type":"mod.nodes.link_info","Object":{"ID":"3e7d2c1b9a40f582","LocalIdentity":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","RemoteIdentity":"037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590","LocalEndpoint":{"Type":"tcp.endpoint","Object":"10.0.0.5:1791"},"RemoteEndpoint":{"Type":"tcp.endpoint","Object":"1.2.3.4:1791"},"Outbound":true,"Network":"tcp","HighPressure":false,"BytesThroughput":0}}
```
