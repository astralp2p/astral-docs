# gateway.node_register

Register the caller as a node reachable through the gateway. If the caller is already registered, the visibility is updated and the existing `Socket` is returned.

The caller must hold
[`mod.auth.use_gateway_action`](../../auth/types/mod.auth.use_gateway_action.md),
which every caller holds while the gateway is enabled. The query is rejected
before any registration is created or updated when the gateway is disabled or
the caller is not authorized, and a refused caller receives no bytes.

## Arguments

* visibility (string8, required) – Visibility of the registered node; `"public"` or `"private"`.

## Returned objects

The operation rejects the query if the gateway is disabled or the caller is not authorized. Otherwise it returns one of:
* An `error_message` object if the endpoint cannot be resolved.
* A `mod.gateway.socket` object containing the endpoint and nonce the caller must present over the raw exonet connection.

## Examples

```shellsession
$ astral-query gateway.node_register -visibility public -out json
{"Type":"mod.gateway.socket","Object":{"Endpoint":{"Type":"mod.gateway.endpoint","Object":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f:02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"},"Nonce":"3f7a1c2e9b0d4e5f"}}
```
