# apphost.request_grant

Ask the node for node-local grants for the calling session's own identity. Used
by a registered app or agent that needs an action it did not ask for at
[`apphost.register`](apphost.register.md).

The grantee is the identity of the session's access token. A query the session
makes as another identity under a
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) permit still
grants to the session's identity. Any IPC or WebSocket session with a token
may ask. Asking needs no permit.

After accepting the query, the operation reads one
[`mod.apphost.request_grant_request`](../types/mod.apphost.request_grant_request.md)
from the channel. The request carries the permits, with their constraints, and
one `Duration` for every grant. A zero `Duration` asks for grants that last
until [`apphost.revoke`](apphost.revoke.md) withdraws them. The operation
checks every permit before the policy is asked ([Grants](../README.md#grants)).

Asking is not receiving: the node's grant request policy decides the request as
a whole. The policy approves every permit asked for or none of them. The policy
is asked on every request, also when the identity already holds every permit
asked for.
[`apphost.set_grant_request_policy`](apphost.set_grant_request_policy.md)
selects the policy: `accept_all` approves every request that passes the check,
`reject_all` refuses every request, and a delegate decides each request. With
neither a mode nor a delegate set, the policy refuses every request, as
`reject_all` does. Under `accept_all`, any app with a token grants itself
any action it names. A delegate receives the request as a
[`mod.apphost.grant_policy_request`](../types/mod.apphost.grant_policy_request.md),
which carries the session's identity, its web origin, the permits asked for and
the `Duration`.

An approved request writes one node-local grant per permit, the record
[`apphost.grant`](apphost.grant.md) writes, in one transaction. Each recorded
permit keeps its constraints, carries no delegation, and lasts for the
requested `Duration`. Each grant is added beside the grants the identity
already holds ([Grants](../README.md#grants)). A permit identical to a held one
is stored once, and its expiry is set to the new value. A grant that allows its
action does so before any authorizer is asked, so it takes precedence over an
authorizer assignment recorded for the identity.

The default gate refuses a session without a token before routing, and
refuses every session on a `fresh` or `unclaimed` node
([Gate](../README.md#gate)).
The operation answers `not permitted` to any query that does not come from an
IPC or WebSocket session with a token, such as a query over the
[HTTP transport](../../../topics/http-transport.md) or a query the node issues
itself. A bearer token on an HTTP request does not make it such a session. The
operation also answers `origin not allowed: network` to a query that arrived
over a [`Link`](../../../core-definitions/link.md).

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

The request travels as the channel's single input object. The argument
`permits` is removed. A query that names it is answered
`unknown argument: permits`, and the policy is not asked.

A channel that closes before the input object arrives receives no answer, and
the policy is not asked. `astral-query` keeps the channel open after stdin ends
([Ending input](../../../tools/astral-query.md#ending-input)).

## Returned objects

The operation returns one of:
* An `error_message` object reading `origin not allowed: network` if the query
  arrived over a link.
* An `error_message` object reading `not permitted` if the query does not come
  from an IPC or WebSocket session with a token, including a query over the
  HTTP transport.
* An `error_message` object reading `unknown argument: permits` if the query
  names `permits`.
* An `error_message` object reading `unexpected object: <type>` if the input
  object is not a `mod.apphost.request_grant_request`, for example
  `unexpected object: eos` for an `eos`.
* An `error_message` object reading `missing permits` if `Permits` is empty.
* An `error_message` object reading `negative duration` if `Duration` is
  negative.
* An `error_message` object reading `invalid permit: <action>: <detail>`, or
  `invalid permit: missing action`, if a permit fails the check. The policy is
  not asked.
* An `error_message` object reading `grant declined` if the node's grant
  request policy refuses the request or cannot decide it.
* An `error_message` object if the grants were not written. No grant is
  recorded.
* An `ack` object if every permit asked for is granted.

The operation accepts the query before the grant request policy decides, so a
refused request receives `grant declined` rather than a rejection.

## Examples

Refused under `reject_all`, or with no policy set:

```shellsession
$ echo '{"Type":"mod.apphost.request_grant_request","Object":{"Permits":[{"Action":"mod.auth.see_objects_action"}],"Duration":0}}' | astral-query apphost.request_grant -in json -out json
{"Type":"error_message","Object":"grant declined"}
```

Discovery of one service, approved by the policy:

```shellsession
$ echo '{"Type":"mod.apphost.request_grant_request","Object":{"Permits":[{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["inference"],"Nodes":[]}]}}]}],"Duration":0}}' | astral-query apphost.request_grant -in json -out json
{"Type":"ack","Object":null}
```

Refused before the policy is asked: a discovery permit without a scope:

```shellsession
$ echo '{"Type":"mod.apphost.request_grant_request","Object":{"Permits":[{"Action":"mod.services.service_discovery_action"}],"Duration":0}}' | astral-query apphost.request_grant -in json -out json
{"Type":"error_message","Object":"invalid permit: mod.services.service_discovery_action: requires constraints"}
```
