# nearby.list

Returns the current cached set of nearby nodes as a stream of `mod.nearby.status` objects, one per cache entry, terminated by `eos`. Expired cache entries are pruned before iteration. The cache holds one entry per source IP and at most 512 entries.

Each `Identity` is the node identity the node established for the entry, from a recognizer or from the peer's `mod.nearby.public_profile`. It is null for a Stealth status that no recognizer matched. `Attachments` are the attachments as received, the `mod.nearby.status_proof` included.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The operation answers an `error_message` reading `not permitted` before the
cache is read when the caller is not authorized.

## Arguments

* out (string, optional) – Output encoding format. Defaults to the channel default.

## Returned objects

The operation returns one of:
* A `mod.nearby.status` object for each cached nearby peer.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query nearby.list -out json
{"Type":"mod.nearby.status","Object":{"Identity":"<identity>","Attachments":[...]}}
{"Type":"mod.nearby.status","Object":{"Identity":null,"Attachments":[...]}}
{"Type":"eos","Object":null}
```
