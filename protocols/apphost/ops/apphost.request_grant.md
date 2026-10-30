# apphost.request_grant

Ask the node for node-local grants for the calling session's own identity. Used
by a registered app or agent that needs an action it did not ask for at
[`apphost.register`](apphost.register.md).

The grantee is the identity of the session's access token. A query the session
makes as another identity under a
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) permit still
grants to the session's identity. Any IPC or WebSocket session with a token
may ask. Asking needs no permit.

Asking is not receiving: the node's grant request policy decides the request as
a whole. The policy approves every permit asked for or none of them.
[`apphost.set_grant_request_policy`](apphost.set_grant_request_policy.md)
selects the policy. The policy receives the request as a
[`mod.apphost.grant_request`](../types/mod.apphost.grant_request.md), which
carries the session's identity, its web origin and the permits asked for. Until
`apphost.set_grant_request_policy` names a delegate, the default policy refuses
every request.

An approved request writes one node-local grant per permit, the record
[`apphost.grant`](apphost.grant.md) writes. Each recorded permit carries no
constraints and no delegation, and lasts until
[`apphost.revoke`](apphost.revoke.md) withdraws it. A grant replaces whatever
the identity held for the same action. A grant that allows its action does so
before any authorizer is asked, so it takes precedence over an authorizer
assignment recorded for the identity. An unconstrained
[`mod.services.service_discovery_action`](../../services/types/mod.services.service_discovery_action.md)
permit allows nothing, so an approved request for it replaces a constrained
discovery grant with one that allows nothing.
[`apphost.grant`](apphost.grant.md) with `-constrained true` records a
constrained discovery grant.

The default `anonymous_allowlist` refuses a session without a token before
routing ([Sessions without a token](../README.md#sessions-without-a-token)).
The operation answers `not permitted` to any query that does not come from an
IPC or WebSocket session with a token, such as a query over the
[HTTP transport](../../../topics/http-transport.md) or a query the node issues
itself. A bearer token on an HTTP request does not make it such a session. The
operation also answers
`origin not allowed: network` to a query that arrived over a
[`Link`](../../../core-definitions/link.md).

## Arguments

* permits (string8, required) – Actions the session asks to hold as node-local
  grants, comma-separated (e.g. `mod.auth.see_objects_action`). An action name
  carries no comma. Blank entries are dropped.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object reading `origin not allowed: network` if the query
  arrived over a link.
* An `error_message` object reading `not permitted` if the query does not come
  from an IPC or WebSocket session with a token, including a query over the
  HTTP transport.
* An `error_message` object reading `missing permits` if `permits` names no
  action.
* An `error_message` object reading `grant declined` if the node's grant
  request policy refuses the request or cannot decide it.
* An `error_message` object if a grant was not written. The grants written
  before it are kept.
* An `ack` object if every permit asked for is granted.

The operation accepts the query before the grant request policy decides, so a
refused request receives `grant declined` rather than a rejection.

## Examples

Refused by the default policy:

```shellsession
$ astral-query apphost.request_grant -permits mod.auth.see_objects_action -out json
{"Type":"error_message","Object":"grant declined"}
```

Approved by a delegated grant request policy:

```shellsession
$ astral-query apphost.request_grant -permits mod.auth.see_objects_action,mod.user.see_swarm_action -out json
{"Type":"ack","Object":null}
```
