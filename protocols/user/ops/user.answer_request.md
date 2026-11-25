# user.answer_request

Answer a request stored in SwarmState with an approval or a decline signed by this node, add the answer to SwarmState, and return it. The caller must hold `mod.user.admin_swarm_action` whose `Subject` is the identity the request names: a contract request's `Identity`, a join request's `Joiner`, or an expel request's `Subject`; answered `not permitted` otherwise. The node does not serve this operation yet ([SwarmState entries](../README.md#swarmstate-entries)).

This node answers only within its tier, read from its membership: a `privileged_member` answers every request, a `trusted` node answers only a join request at tier `member`, and a `member` answers none ([`mod.user.approval`](../types/mod.user.approval.md)). An approval answers only a `pending` request. A decline answers a `pending` or an `approved` request, since a decline beats every approval. Nobody answers an `expired` or a `declined` request. A refused answer writes nothing.

## Arguments

* id (object_id, required) – The request's entry ID, as [`user.swarm_requests`](user.swarm_requests.md) streams it.
* answer (string8, required) – `approve` or `decline`.

## Returned objects

The operation returns one of:
* An `error_message` reading `invalid answer` if `answer` is neither `approve` nor `decline`.
* An `error_message` reading `unknown request` if `id` names no stored request.
* An `error_message` reading `not permitted` if the caller is not authorized.
* An `error_message` reading `outside this node's tier` if this node has no membership, or its tier may not answer the request.
* An `error_message` reading `request is not open to this answer` if the request's status admits no such answer.
* An `error_message` if signing fails or SwarmState refuses the answer.
* A [`mod.user.signed_approval`](../types/mod.user.signed_approval.md) for `approve`, or a [`mod.user.signed_decline`](../types/mod.user.signed_decline.md) for `decline`, signed by this node and naming the request's entry ID as `RequestID`. It is also returned when SwarmState holds the answer until the entries it needs arrive: a held answer is not stored yet, and a later merge may store it.

## Examples

```shellsession
$ astral-query user.answer_request -id data1... -answer approve -out json
{"Type":"mod.user.signed_approval","Object":{"Approval":{"Issuer":"...","RequestID":"data1..."},"IssuerSig":{...}}}
```
