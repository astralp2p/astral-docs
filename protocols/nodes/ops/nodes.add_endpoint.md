# nodes.add_endpoint

Register a network endpoint for a given identity. The endpoint is stored with a default TTL of 90 days.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before the endpoint is parsed or stored when the caller is
not authorized, and a refused caller receives no bytes.

## Arguments

* id (identity, required) – The identity of the node the endpoint belongs to.
* endpoint (string, required) – The endpoint to add, formatted as `<network>:<address>` (e.g. `tcp:1.2.3.4:1791`).
* in (string) – Input format hint for the channel (e.g. `json`).
* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns one of:
* An `error_message` object if the endpoint cannot be parsed or stored.
* An `ack` object if the endpoint was registered successfully.

## Examples

```shellsession
$ astral-query nodes.add_endpoint -id 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f -endpoint tcp:1.2.3.4:1791 -out json
{"Type":"ack","Object":null}
```
