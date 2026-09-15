# services.sync

Fetch and store service advertisements from a remote identity, updating the local service registry. In follow mode the sync runs continuously until any data is received on the channel. The channel is cancelled as soon as any input arrives.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before `identity` is resolved or any sync starts when the
caller is not authorized, and a refused caller receives no bytes.

## Arguments

* identity (string8, required) – Identity to sync from, given as a hex public key or a name resolved via the directory.
* follow (bool) – If true, continue syncing until the channel receives input. Defaults to false.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if `identity` cannot be resolved or the sync fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query services.sync -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -out json
{"Type":"ack","Object":null}
```
