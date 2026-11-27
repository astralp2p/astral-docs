# user.carry_join

Carry the caller's join request into SwarmState and sign its membership with
the caller, in this query's session. The caller is a node without an active
contract running [`user.join`](user.join.md); this node is its carrier.

After accepting the query, the operation reads one
[`mod.user.signed_join_request`](../types/mod.user.signed_join_request.md). It
must name the caller as `Joiner`, carry the joiner's signature, name this node
as `Carrier`, name a valid tier, and have a `FiledAt` no later than this
node's time. This node must hold a `trusted` or
`privileged_member` membership. The operation adds the request to SwarmState
(a resent request is stored already) and runs the handshake while the caller
stays connected ([Joins](../README.md#joins)):

1. The request is the first message, read from the caller.
2. The operation answers the membership signed by its issuer, a
   [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
   without the subject's signature:
   * at tier `member`, when this node is `trusted` or `privileged_member`, and
     at tier `trusted`, when this node is `privileged_member`, the issuer is
     this node, and it signs at once. It expires at the request's `FiledAt`
     plus the membership validity this node is configured with, or when this
     node's own membership expires, if earlier. A request for a tier this
     node's tier may not issue is refused;
   * at tier `privileged_member`, the issuer is the user key, and the
     operation waits until the key has signed. It expires at the request's
     `FiledAt` plus the membership validity this node is configured with,
     with no cap, since the user key holds no membership. With a Coldcard the key signs at
     once after the user presses the device; with a software user key held on
     this node, the user confirms with
     [`user.confirm_join`](user.confirm_join.md). A node that reaches no user
     key refuses.
3. The caller checks the membership against its request, signs it as subject,
   and sends the contract back.
4. The operation checks both signatures and the body it signed, adds the
   contract to SwarmState, and confirms it: it answers the contract with both
   signatures, then the user identity.

A decline of the request, the request's timeout, or an expelled joiner ends the
join: this node signs no membership for a declined or expired request. A
dropped connection only pauses it: the joiner resends the same request, and the
operation answers a membership with the same body, while this node's configured
validity and its own membership are unchanged.

No action guards the operation: the caller holds nothing yet, and this node's
tier decides what it signs.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

* A `mod.auth.signed_contract` holding the joiner's membership with the issuer's
  signature only, then, once the caller has returned it signed, the same
  contract with both signatures followed by the user identity (`identity`) the
  membership derives from. The joiner activates the membership only after this
  last answer.
* An `error_message` reading `no active contract` if this node is unclaimed.
* An `error_message` reading `not permitted` if the request does not name the
  caller as `Joiner`.
* An `error_message` reading `join request declined` or `join request expired`.
* An `error_message` reading `join request names another carrier`, `join
  request names an invalid tier`, `join request is not signed` or `only a
  trusted or privileged member carries a join request`.
* An `error_message` reading `tier above what this node may issue` if this
  node's tier may not issue the tier asked for.
* An `error_message` reading `a privileged membership needs the user key's
  signature` for a `privileged_member` request on a node that reaches no user
  key.
* An `error_message` reading `membership is not signed by the joiner` if the
  contract the caller returns lacks its signature or differs from the one this
  node signed.
* An `error_message` if the request's `FiledAt` is later than this node's time.
* An `error_message` if the request cannot be read, stored or carried out.
