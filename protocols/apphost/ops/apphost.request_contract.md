# apphost.request_contract

Ask the swarm for permits for the calling session's own identity. Used by a
registered app that needs an action its node does not grant it. The permits
arrive as a contract the app's host signs, not as node-local grants
([Contract requests](../README.md#contract-requests)).

The running node does not route this operation yet. A node that routes it
before its SwarmState is in place answers `contract requests not available`.

The requester is the identity of the session's access token. A query the
session makes as another identity under a
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) permit still
asks for the session's identity. Any IPC or WebSocket session with a token may
ask. Asking needs no permit.

After accepting the query, the operation reads
[`mod.auth.permit`](../../auth/types/mod.auth.permit.md) objects from the
channel until an `eos`. Each permit carries its constraints. The operation
checks every permit before it files anything, with the check
[`apphost.request_grant`](apphost.request_grant.md) applies
([Grants](../README.md#grants)).

The node then files a
[`mod.user.signed_contract_request`](../../user/types/mod.user.signed_contract_request.md)
into SwarmState: filed and signed by this node, naming the requester as
`Identity`, carrying the permits, with a `Timeout` 1 hour after `FiledAt`. A
live request this node filed for the same identity with the same set of
permits is not filed again: a pending request before its `Timeout`, or an
approved one. The operation then answers that request's entry ID, and the
permits' order does not matter. A changed set of permits is a new request.

The node rate-limits the requests it files, over a sliding window of 1 hour:

* at most 4 new requests per requesting identity;
* at most 64 new requests for the whole node.

A live request answered again does not count. A request over either limit is
refused, and nothing is filed.

After filing, the operation sends the request's entry ID and waits while the
caller stays connected. A Privileged node answers the request with a
[`mod.user.signed_approval`](../../user/types/mod.user.signed_approval.md) or
a [`mod.user.signed_decline`](../../user/types/mod.user.signed_decline.md). On
an approval, this node signs a
[`mod.auth.contract`](../../auth/types/mod.auth.contract.md) that:

* has this node as `Issuer` and the identity the request names as `Subject`;
* carries exactly the request's permits;
* names the approval's entry ID as `ApprovalID`;
* expires 3650 days after signing, or when this node's membership expires,
  if earlier.

The node adds the contract to SwarmState and sends it to the caller. A request
answered by several approvals is carried out once. A caller that disconnects
calls again with the same permits: the operation answers the same request ID,
then the outcome as soon as there is one. An outcome reached while nobody waits
is kept in SwarmState.

A decline beats every approval of the same request, also after the contract is
signed. A request with no answer at its `Timeout` expires. Either outcome ends
the request, and the next call with the same permits files a new one.

The default gate refuses a session without a token before routing, and
refuses every session on a `fresh` or `unclaimed` node
([Gate](../README.md#gate)).
The operation answers `not permitted` to any query that does not come from an
IPC or WebSocket session with a token, such as a query over the
[HTTP transport](../../../topics/http-transport.md) from a loopback address or
a query the node issues itself. The operation answers
`origin not allowed: network` to a query that arrived over a
[`Link`](../../../core-definitions/link.md) or over the HTTP transport from a
non-loopback address.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

The permits travel as the channel's input objects, ended by `eos`. A channel
that closes before the `eos` arrives receives no answer, and nothing is filed.

## Returned objects

The operation returns one of:
* An `error_message` object reading `origin not allowed: network` if the query
  arrived over a link or over the HTTP transport from a non-loopback address.
* An `error_message` object reading `not permitted` if the query does not come
  from an IPC or WebSocket session with a token.
* An `error_message` object reading `contract requests not available` if the
  node has no SwarmState to file into.
* An `error_message` object reading `unexpected object: <type>` if an input
  object is neither a `mod.auth.permit` nor an `eos`.
* An `error_message` object reading `missing permits` if no permit arrives
  before the `eos`.
* An `error_message` object reading `invalid permit: <action>: <detail>`, or
  `invalid permit: missing action`, if a permit fails the check. Nothing is
  filed.
* An `error_message` object reading `too many contract requests` if a new
  request is over a rate limit. Nothing is filed.
* An `error_message` object if the request was not filed.
* An `object_id` object, the request's entry ID, followed by one of:
  * A `mod.auth.signed_contract` object, the contract that carries out the
    request's approval.
  * An `error_message` object reading `contract request declined` if a decline
    names the request.
  * An `error_message` object reading `contract request expired` if the
    request's `Timeout` passed with no answer.

The operation accepts the query before it files, so a refused request receives
an `error_message` rather than a rejection.

## Examples

Discovery of one service, approved on a Privileged node:

```shellsession
$ printf '%s\n' '{"Type":"mod.auth.permit","Object":{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["bitcoin-wallet"],"Nodes":[]}]}}],"Delegation":0}}' '{"Type":"eos","Object":""}' | astral-query apphost.request_contract -in json -out json
{"Type":"object_id","Object":"data1..."}
{"Type":"mod.auth.signed_contract","Object":{"Contract":{"Issuer":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Subject":"03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6","Permits":[{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["bitcoin-wallet"],"Nodes":[]}]}}],"Delegation":0}],"ExpiresAt":"2027-05-27T12:00:00+02:00","ApprovalID":"data1..."},"IssuerSig":{"Data":"MEUCIQ...","Scheme":"asn1"},"SubjectSig":{"Data":"MEQCIA...","Scheme":"asn1"}}}
```

Declined:

```shellsession
$ printf '%s\n' '{"Type":"mod.auth.permit","Object":{"Action":"mod.auth.see_objects_action"}}' '{"Type":"eos","Object":""}' | astral-query apphost.request_contract -in json -out json
{"Type":"object_id","Object":"data1..."}
{"Type":"error_message","Object":"contract request declined"}
```
