# user.answer_request

Answer a request stored in SwarmState with an offer, an approval or a decline signed by this node, add the answer to SwarmState, and return it. The caller must hold `mod.user.admin_swarm_action` whose `Subject` is the identity the request names: a contract request's `Identity`, a join request's `Joiner`, or an expel request's `Subject`; answered `not permitted` otherwise.

What `approve` signs depends on the request:

* A contract request: an offer, a [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md) with only this node's signature, from this node to the node that filed the request. It carries the requested permits with a `Delegation` 1 more, names the request as its `RequestID`, and expires 3650 days after signing, or when this node's membership expires, if earlier ([App grants](../README.md#app-grants)). The filing node completes it.
* An expel request: a [`mod.user.signed_approval`](../types/mod.user.signed_approval.md). Only the user key expels, by signing the expulsion.
* A join request: nothing. Its carrier signs the membership, and `approve` is refused.

`decline` signs a [`mod.user.signed_decline`](../types/mod.user.signed_decline.md) for any request. A decline only closes the request: it takes back no contract that both parties signed ([Requests and answers](../README.md#requests-and-answers)).

This node answers only within its tier, read from its membership; a node that is its own root (unclaimed) answers every request: a `privileged_member` answers every request, a `trusted` node answers only a join request at tier `member`, and a `member` answers none ([`mod.user.approval`](../types/mod.user.approval.md)). An approval or an offer answers only a request whose status is `pending`. A decline answers a `pending`, `offered` or `approved` request. Nobody answers a request whose status is `fulfilled`, `expired` or `declined`. A refused answer writes nothing.

## Arguments

* id (object_id, required) – The request's entry ID, as [`user.swarm_requests`](user.swarm_requests.md) streams it.
* answer (string8, required) – `approve` or `decline`.

## Returned objects

The operation returns one of:
* An `error_message` reading `invalid answer` if `answer` is neither `approve` nor `decline`.
* An `error_message` reading `unknown request` if `id` names no stored request.
* An `error_message` reading `not permitted` if the caller is not authorized.
* An `error_message` reading `outside this node's tier` if this node has no membership, or its tier may not answer the request.
* An `error_message` reading `request is not open to this answer` if the request's status admits no such answer, or the request is a join request and the answer is `approve`.
* An `error_message` if signing fails or SwarmState refuses the answer.
* The signed answer, naming the request's entry ID: for `approve` on a contract request the offer, a `mod.auth.signed_contract`; for `approve` on an expel request a [`mod.user.signed_approval`](../types/mod.user.signed_approval.md); for `decline` a [`mod.user.signed_decline`](../types/mod.user.signed_decline.md). It is also returned when SwarmState holds the answer until the entries it needs arrive: a held answer is not stored yet, and a later merge may store it.

## Examples

```shellsession
$ astral-query user.answer_request -id data1... -answer approve -out json
{"Type":"mod.auth.signed_contract","Object":{"Contract":{"Issuer":"...","Subject":"...","Permits":[...],"ExpiresAt":"...","RequestID":"data1..."},"IssuerSig":{...},"SubjectSig":null}}
```
