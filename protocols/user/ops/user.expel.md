# user.expel

Permanently ban the named node from the swarm and return the signed expulsion. The caller must hold `mod.user.admin_swarm_action`; the active contract's issuer holds it by default. Rejected with code `2` if the node has no active contract, with code `3` if `identity` does not resolve or resolves to the anonymous identity, and with code `4` if the caller is not authorized. The ban is identity-level and irreversible.

## Arguments

* identity (string8, required) – The node to expel, given as a hex public key or a name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if identity resolution or expulsion fails.
* A `mod.user.signed_expulsion` object containing the issued ban.

## Examples

```shellsession
$ astral-query user.expel -identity phone -out json
{"Type":"mod.user.signed_expulsion","Object":{...}}
```
