# apphost.grant

Record node-local grants for an identity that already exists.

A grant is this node's own record that an identity may perform an action here.
The grant is recorded, not signed: it authorizes on this node and travels
nowhere. Each permit is added beside the grants the identity already holds
([Grants](../README.md#grants)). A permit identical to a held one is stored
once, and granting it again sets that grant's expiry to the new value.

[`apphost.register`](apphost.register.md) writes grants only for the identity
it mints. This operation writes them for an identity the node already knows, so
an app reaches a newly guarded operation without re-registering under a fresh
identity.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The operation answers an `error_message` reading `not permitted` before the
input is read when the caller is not authorized. The operation also answers
`origin not allowed: network` to a query that arrived over a
[`Link`](../../../core-definitions/link.md), whatever the caller holds.

After accepting the query, the operation reads one
[`mod.apphost.grant_request`](../types/mod.apphost.grant_request.md) from the
channel. The request names the identity, the permits, and one `Duration` for
every grant it writes. A zero `Duration` writes grants that last until
[`apphost.revoke`](apphost.revoke.md) withdraws them. The operation checks
every permit before it writes any ([Grants](../README.md#grants)). It then
writes every permit in one transaction: either every grant is recorded or none
is.

Each recorded permit keeps its constraints as sent and carries no delegation: a
grant is not portable evidence, so a hop count on it would describe authority
it cannot carry. A
[`mod.services.service_discovery_action`](../../services/types/mod.services.service_discovery_action.md)
permit needs constraints holding exactly one
[`mod.services.discovery_scope`](../../services/types/mod.services.discovery_scope.md),
because that action covers nothing unconstrained. Constraints on an action that
does not evaluate them have no effect ([Grants](../README.md#grants)).

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

The grant request travels as the channel's single input object. The arguments
`identity`, `action`, `duration` and `constrained` are removed. A query that
names one is answered `unknown argument: <name>`, and nothing is written.

A channel that closes before the input object arrives receives no answer, and
nothing is written. `astral-query` keeps the channel open after stdin ends
([Ending input](../../../tools/astral-query.md#ending-input)).

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown argument: <name>` if the query
  names `identity`, `action`, `duration` or `constrained`.
* An `error_message` object reading `unexpected object: <type>` if the input
  object is not a `mod.apphost.grant_request`, for example
  `unexpected object: eos` for an `eos`.
* An `error_message` object reading `missing identity` if `Identity` is absent
  or zero.
* An `error_message` object reading `missing permits` if `Permits` is empty.
* An `error_message` object reading `negative duration` if `Duration` is
  negative.
* An `error_message` object reading `invalid permit: <action>: <detail>`, or
  `invalid permit: missing action`, if a permit fails the check. No grant is
  written.
* An `error_message` object if the grants were not written. No grant is
  recorded.
* An `ack` object if every grant was recorded.

## Examples

```shellsession
$ echo '{"Type":"mod.apphost.grant_request","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Duration":0,"Permits":[{"Action":"mod.auth.admin_manage_apps_action"}]}}' | astral-query apphost.grant -in json -out json
{"Type":"ack","Object":null}
```

Granting for a bounded time (720 hours, in nanoseconds):

```shellsession
$ echo '{"Type":"mod.apphost.grant_request","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Duration":2592000000000000,"Permits":[{"Action":"mod.auth.see_node_state_action"}]}}' | astral-query apphost.grant -in json -out json
{"Type":"ack","Object":null}
```

Granting discovery of one service:

```shellsession
$ echo '{"Type":"mod.apphost.grant_request","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Duration":0,"Permits":[{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["inference"],"Nodes":[]}]}}]}]}}' | astral-query apphost.grant -in json -out json
{"Type":"ack","Object":null}
```

Refused: a discovery permit without a scope:

```shellsession
$ echo '{"Type":"mod.apphost.grant_request","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Duration":0,"Permits":[{"Action":"mod.services.service_discovery_action"}]}}' | astral-query apphost.grant -in json -out json
{"Type":"error_message","Object":"invalid permit: mod.services.service_discovery_action: requires constraints"}
```
