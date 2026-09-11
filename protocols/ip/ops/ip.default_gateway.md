# ip.default_gateway

Return the IP address of the default network gateway.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before the gateway is read when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

None.

## Returned objects

The operation returns one of:
* An `error_message` object if the default gateway cannot be determined.
* A `mod.ip.ip_address` object containing the gateway address.

## Examples

```shellsession
$ astral-query ip.default_gateway -out json
{"Type":"mod.ip.ip_address","Object":"192.168.1.1"}
```
