# user.expel

Permanently ban a target node from the swarm and return the signed expulsion. The caller must hold `mod.user.admin_swarm_action`; the active contract's issuer holds it by default. Rejected with code `2` if the node has no active contract, with code `3` if the target identity does not resolve, and with code `4` if the caller is not authorized. The ban is identity-level and irreversible.

## Arguments

* target (string, required) – Alias or public key of the node to expel.

## Returned objects

The operation returns one of:
* An `error_message` object if identity resolution or expulsion fails.
* A `mod.user.signed_expulsion` object containing the issued ban.

## Examples

```shellsession
$ astral-query user.expel -target phone -out json
{"Type":"mod.user.signed_expulsion","Object":{...}}
```
