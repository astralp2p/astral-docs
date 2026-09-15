# gateway.node_connect

Reserve an idle connection to a registered node. The caller receives a `mod.gateway.socket` describing the endpoint and nonce to present on the raw exonet connection.

The caller must hold
[`mod.auth.use_gateway_action`](../../auth/types/mod.auth.use_gateway_action.md),
which every caller holds while the gateway is enabled. The query is rejected
before any connection is reserved or connector state is allocated when the
gateway is disabled or the caller is not authorized, and a refused caller
receives no bytes.

## Arguments

* identity (string8, required) – Identity of the registered node to connect to, given as a hex public key or a name resolved via the directory.

## Returned objects

The operation rejects the query if the gateway is disabled or the caller is not authorized. Otherwise it returns one of:
* An `error_message` object if `identity` does not resolve.
* An `error_message` object reading `missing identity` if `identity` resolves to the anonymous identity.
* An `error_message` object if no idle connection is available for the named node.
* A `mod.gateway.socket` object containing the endpoint and nonce the caller must present over the raw exonet connection.

## Examples

```shellsession
$ astral-query gateway.node_connect -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -out json
{"Type":"mod.gateway.socket","Object":{"Endpoint":{"Type":"mod.gateway.endpoint","Object":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f:037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590"},"Nonce":"a1b2c3d4e5f60718"}}
```
