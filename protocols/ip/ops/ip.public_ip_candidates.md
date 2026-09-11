# ip.public_ip_candidates

Stream the candidate public IP addresses for the local node, collected from all registered `PublicIPCandidateProvider` sources.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any candidate is collected when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

None.

## Returned objects

The operation returns one of:
* A `mod.ip.ip_address` object for each candidate public address.
* An `error_message` object if sending an address fails.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query ip.public_ip_candidates -out json
{"Type":"mod.ip.ip_address","Object":"203.0.113.7"}
{"Type":"eos","Object":{}}
```
