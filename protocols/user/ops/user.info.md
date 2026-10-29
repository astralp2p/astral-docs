# user.info

Return information about the user this node belongs to: aliases of the user
and node, and the active contract the node operates under.

The caller must hold `mod.user.see_swarm_action`; the user (issuer of the
active contract) and every node in the same local swarm hold it by default.
Answers an `error_message` reading `no active contract` if the node has no active contract.
Answers `not permitted` if the caller is not authorized.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns a `mod.user.info` object.

## Examples

```shellsession
$ astral-query user.info -out json
{"Type":"mod.user.info","Object":{"NodeAlias":"phone","UserAlias":"alice","ContractID":"...","Contract":{...}}}
```
