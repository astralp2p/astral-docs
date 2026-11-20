# user.relay_digest

Stream the object IDs of the relay contracts the node holds, terminated by
`eos`. A node synchronising with a swarm member calls this operation on the
member before it pushes relay contracts, and pushes only the relay contracts
whose IDs the member did not list
([user](../README.md)).

A relay contract is a contract whose every permit is for
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
([App Routing, Reach](../../../topics/app-routing.md#reach)). A contract that
carries any other permit beside it is not a relay contract for this operation,
matching [`user.relay_contracts`](user.relay_contracts.md). The node streams
the [`Object ID`](../../../core-definitions/object-id.md) of each active
relay contract in its own index, in no particular order: a contract that is
started, not expired and not withdrawn on this node. The ID is the one of the
`mod.auth.signed_contract` object that a push of the contract carries.

The operation applies no other condition. It names no issuer, and it does not
omit a contract whose subject is the caller or one that fails the admission
rule of [App Routing, Reach](../../../topics/app-routing.md#reach). The
caller decides which contracts to push; the digest only tells it which ones
this node already holds. A contract the node refused or never received is
absent from the stream, so the caller pushes it again.

The operation is a hint. It changes no admission: a contract pushed after the
digest passes the admission rule on the receiving node as any pushed contract
does, and a contract listed in the digest is never admitted by being listed.

The caller must be a member of the node's local swarm other than the node
itself, and is answered `not permitted` otherwise. A session that calls with a
user token calls as the user, which is not a member, and is answered `not
permitted`. The operation asks for no action. The guard is the one of
[`user.relay_contracts`](user.relay_contracts.md): the stream tells its reader
which apps the swarm hosts.

A caller treats an answer that is not a complete stream as no digest: an
`error_message`, a refusal, an unknown operation, a stream that ends without
`eos`, or no answer within 10 seconds. It then pushes every relay contract it
would push without a digest, never none.

## Arguments

* out (string, optional) – Output encoding format. Defaults to the channel default.

## Returned objects

The operation returns one of:
* An `error_message` reading `not permitted` if the caller is not a member of
  the local swarm, or is the node itself.
* An `error_message` if reading the held contracts fails.
* An `object_id` for each held relay contract, followed by an `eos` object
  terminating the stream. A node that holds no relay contract answers `eos`
  alone.

## Examples

A session with the node's token calls as the node
([Session Identity, The node's token](../../../topics/session-identity.md#the-nodes-token)).
On a node of the same swarm, linked to `03b1...`, it reads the digest of the
relay contracts that node holds:

```shellsession
$ export ASTRALD_APPHOST_TOKEN=<node token>
$ astral-query 03b1...:user.relay_digest -out json
{"Type":"object_id","Object":"data1..."}
{"Type":"object_id","Object":"data1..."}
{"Type":"eos","Object":""}
```
