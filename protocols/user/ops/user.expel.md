# user.expel

Permanently ban the named node from the swarm and return the signed expulsion. The caller must hold [`mod.user.expel_action`](../types/mod.user.expel_action.md); only the user holds it (a `privileged_member` node does not). The user key signs the expulsion, and the node adds it to SwarmState. Answers an `error_message` reading `no active contract` if the node has no active contract. Answers an `error_message` reading `unknown identity` if `identity` does not resolve, and `zero identity` if it resolves to the anonymous identity. Answers `not permitted` if the caller is not authorized. Accepted only from a local query: any other origin is answered `origin not allowed: <origin>`, even with the user as caller, since a `privileged_member` node may relay as the user. The ban is identity-level and irreversible.

## Arguments

* identity (string8, required) – The node to expel, given as a hex public key or a name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if identity resolution or expulsion fails.
* An `error_message` reading `origin not allowed: <origin>` if the query's origin is not local.
* A `mod.user.signed_expulsion` object containing the issued ban.

## Examples

```shellsession
$ astral-query user.expel -identity phone -out json
{"Type":"mod.user.signed_expulsion","Object":{...}}
```
