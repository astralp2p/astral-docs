# auth.set_authorizer

Assign an external authorizer to an action type, for every actor or for one
actor, replacing the assignment of the same action and actor. The node asks
the authorizer last at each level of the
[authorization walk](../README.md#authorization), after the swarm root, the
handlers and the contract chain have not allowed the action. An assignment for
one actor takes precedence over the action-wide one. The assignment is stored
at `/mod/auth/authorizers` as part of a
[`mod.auth.authorizer_assignments`](../types/mod.auth.authorizer_assignment.md#the-stored-set)
and applies to the next authorization. At each start the node writes the
`external_authorizers` of `auth.yaml` over the stored action-wide assignment
of each action it names.

The node refuses the query in these cases, in this order:

* The query's origin is not local: answered with `origin not allowed:
  <origin>`. A `privileged_member` node holds the action this op asks through
  the swarm root, so a query over a link could install an authority on another
  node.
* The caller does not hold
  [`mod.auth.admin_manage_apps_action`](../types/mod.auth.admin_manage_apps_action.md):
  answered with `not permitted`.
* `action` is `mod.auth.sudo_action`, `mod.user.expel_action` or
  `mod.nodes.relay_for_action` and the caller is not the node's user:
  answered with `not permitted`. The swarm root never answers a sudo or an
  expel and relays only as the user, so only the user installs an authority
  that answers them.

## Arguments

* action (string8, required) – The action's object type, for example
  `mod.auth.see_objects_action`.
* endpoint (string8, required) – The authorizer: an `http://` or `https://`
  URL, or `astral://<identity or alias>:<op>`.
* actor (string8, optional) – The identity or alias the assignment answers
  for. Absent makes it action-wide.
* timeout (duration, optional) – How long the node waits for one answer. Zero
  takes the node's default.
* token (string8, optional) – The bearer token for an `http` or `https`
  endpoint.

## Returned objects

The operation returns one of:
* An `error_message` named in the cases above.
* An `error_message` if `actor` does not resolve.
* An `error_message` reading `the authority cannot be the actor` if an
  `astral://` endpoint names the actor itself.
* An `error_message` reading `external authorizer: endpoint <endpoint> names no
  transport: expected http://, https:// or astral://` for another scheme.
* An `error_message` if storing the assignment fails. The stored assignments
  are unchanged.
* An `ack` once the assignment is stored.

## Examples

```shellsession
$ astral-query auth.set_authorizer -action mod.messaging.send_action -endpoint astral://mailgate:mailgate.authorize -out json
{"Type":"ack","Object":null}
```
