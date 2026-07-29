# gateway.node_connect

Reserve an idle connection to a registered target node. The caller receives a `mod.gateway.socket` describing the endpoint and nonce to present on the raw exonet connection.

## Arguments

* target (identity, required) – Identity of the registered node to connect to.

## Returned objects

The operation returns one of:
* An `error_message` object if no idle connection is available for the target.
* A `mod.gateway.socket` object containing the endpoint and nonce the caller must present over the raw exonet connection.

## Examples

```shellsession
$ astral-query gateway.node_connect -target 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -out json
{"Type":"mod.gateway.socket","Object":{"Endpoint":{"Type":"mod.gateway.endpoint","Object":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f:037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590"},"Nonce":"a1b2c3d4e5f60718"}}
```
