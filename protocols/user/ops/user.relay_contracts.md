# user.relay_contracts

Stream the relay contracts the node holds for one issuer, terminated by `eos`.
A node routing a query to an app whose relay contract it does not hold calls
this operation on each swarm member it holds a link with
([App Routing, Resolving the host](../../../topics/app-routing.md#resolving-the-host)).

A relay contract is a contract with a permit for
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
([App Routing, Reach](../../../topics/app-routing.md#reach)). The node streams
each relay contract it holds that meets every condition below:

* `issuer` is its issuer.
* Its subject is not the caller: the caller holds the relay contracts of the
  apps it hosts.
* Every permit it carries is for `mod.nodes.relay_for_action`.
* It is active: started, not expired and not withdrawn on this node.
* It passes the admission rule of
  [App Routing, Reach](../../../topics/app-routing.md#reach) on this node: its
  subject is this node or a member of the local swarm, and both signatures
  verify.

The caller must be a member of the node's local swarm other than the node
itself, and is answered `not permitted` otherwise. A session that calls with a
user token calls as the user, which is not a member, and is answered `not
permitted`. The operation asks for no action.

## Arguments

* issuer (identity, required) – The identity whose relay contracts to stream,
  normally an app identity.
* out (string, optional) – Output encoding format. Defaults to the channel default.

## Returned objects

The operation returns one of:
* An `error_message` reading `not permitted` if the caller is not a member of
  the local swarm, or is the node itself.
* An `error_message` if reading the held contracts fails.
* A `mod.auth.signed_contract` for each relay contract that meets the
  conditions above, followed by an `eos` object terminating the stream. A node
  that holds no such contract answers `eos` alone.

## Examples

A session with the node's token calls as the node
([Session Identity, The node's token](../../../topics/session-identity.md#the-nodes-token)).
On a node of the same swarm, linked to `03b1...`, it reads the relay contracts
of the app `02c4...`:

```shellsession
$ export ASTRALD_APPHOST_TOKEN=<node token>
$ astral-query 03b1...:user.relay_contracts -issuer 02c4... -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
{"Type":"eos","Object":""}
```
