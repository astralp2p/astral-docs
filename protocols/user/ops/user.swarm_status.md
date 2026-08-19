# user.swarm_status

List all nodes currently in the user's swarm, with their alias and link
status. A node belongs to the swarm if it holds an active SwarmAccess contract
issued by the same user as this node.

The caller must hold `mod.user.see_swarm_action`. Rejected with code `2` if
this node has no active contract, and with code `4` if the caller is not
authorized.

## Arguments

This operation takes no arguments.

## Returned objects

The operation streams one `mod.users.swarm_member` per node in the swarm, then
an `eos`. An `error_message` is returned instead if encoding fails.

## Examples

```shellsession
$ astral-query user.swarm_status -out json
{"Type":"mod.users.swarm_member","Object":{"Identity":"...","Alias":"phone","Linked":true}}
{"Type":"mod.users.swarm_member","Object":{"Identity":"...","Alias":"laptop","Linked":false}}
{"Type":"eos","Object":""}
```
