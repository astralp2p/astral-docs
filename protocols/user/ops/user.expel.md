# user.expel

Permanently ban the named node from the swarm and return the signed expulsion. The caller must hold [`mod.user.expel_action`](../types/mod.user.expel_action.md); the user holds it, and an identity holds it only through a contract chain from the user (a `privileged_member` membership does not grant it). The user key signs the expulsion, and the node adds it to SwarmState. Answers an `error_message` reading `no active contract` if the node has no active contract. Answers an `error_message` reading `unknown identity` if `identity` does not resolve, and `zero identity` if it resolves to the anonymous identity. Answers `not permitted` if the caller is not authorized. The operation admits a query of any origin; the authorization decides, and a contract the user key signs is the user's delegation of the permit. The ban is identity-level and irreversible.

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
