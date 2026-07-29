# gateway.node_register

Register the caller as a node reachable through the gateway. If the caller is already registered, the visibility is updated and the existing `Socket` is returned. Access is denied unless the caller passes the gateway's authorization check.

## Arguments

* visibility (string8, required) – Visibility of the registered node; `"public"` or `"private"`.

## Returned objects

The operation returns one of:
* An `error_message` object if authorization fails or the endpoint cannot be resolved.
* A `mod.gateway.socket` object containing the endpoint and nonce the caller must present over the raw exonet connection.

## Examples

```shellsession
$ astral-query gateway.node_register -visibility public -out json
{"Type":"mod.gateway.socket","Object":{"Endpoint":{"Type":"mod.gateway.endpoint","Object":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f:02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"},"Nonce":"3f7a1c2e9b0d4e5f"}}
```
