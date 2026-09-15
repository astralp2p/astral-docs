# nodes.close_link

Close an active link by its local id.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any link is closed when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* link_id (nonce64, required) – The local id of the link to close.
* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns one of:
* An `error_message` object if no link with that id exists.
* An `ack` object if the link was closed.

## Examples

```shellsession
$ astral-query nodes.close_link -link_id 7c1a93b50f2e4d18 -out json
{"Type":"ack","Object":null}
```
