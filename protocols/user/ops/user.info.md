# user.info

Return the node's state and manager, and on a claimed node the user this node
belongs to: aliases of the user and node, and the active contract the node
operates under.

`State` is `fresh`, `unclaimed` or `claimed`
([apphost, Node states](../../apphost/README.md#node-states)). `Manager` is the
identity [`apphost.register_manager`](../../apphost/ops/apphost.register_manager.md)
appointed, or null when none is appointed.

On a `fresh` or `unclaimed` node, the operation answers `State` and `Manager`
to every caller, and leaves `NodeAlias`, `UserAlias`, `ContractID` and
`Contract` empty. The [gate](../../apphost/README.md#gate) decides which
sessions reach the operation.

On a `claimed` node, the caller must hold `mod.user.see_swarm_action`; the user
(issuer of the active contract) and every node in the same local swarm hold it
by default. Answers `not permitted` if the caller is not authorized.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns one of:
* A `mod.user.info` object.
* An `error_message` object reading `not permitted` if the node is `claimed`
  and the caller is not authorized.

## Examples

```shellsession
$ astral-query user.info -out json
{"Type":"mod.user.info","Object":{"NodeAlias":"phone","UserAlias":"alice","ContractID":"...","Contract":{...},"State":"claimed","Manager":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"}}
```

A fresh node:

```shellsession
$ astral-query user.info -out json
{"Type":"mod.user.info","Object":{"NodeAlias":"","UserAlias":"","ContractID":null,"Contract":null,"State":"fresh","Manager":null}}
```
