# user.confirm_join

Confirm, as the user, a pending join request at tier `privileged_member`: the user key signs the joining node's privileged membership, adds it to SwarmState, and returns it. The node that carries the join hands it to the joiner. Only the user identity may call this operation; every other caller, the node included, is answered `not permitted`, whatever it is granted. The node does not serve this operation yet ([SwarmState entries](../README.md#swarmstate-entries)).

A privileged membership is signed only after a user action. A Coldcard shows the membership's tier and signs on a press, and that press is the action. A software user key held on the node signs with no action, so the carrier of such a join signs nothing and waits for this confirmation, until the request is declined or times out. [`user.swarm_requests`](user.swarm_requests.md) lists the pending request with the entry ID this operation takes. An approval of the request does not stand in for the confirmation.

A confirmation is refused, writing nothing, when the request is declined or expired or its joiner is expelled. A repeated confirmation returns the membership the first one stored.

## Arguments

* id (object_id, required) – The join request's entry ID, as [`user.swarm_requests`](user.swarm_requests.md) streams it.

## Returned objects

The operation returns one of:
* An `error_message` reading `no user key on this node` if this node cannot reach the user key.
* An `error_message` reading `not permitted` if the caller is not the user.
* An `error_message` reading `unknown request` if `id` names no stored request.
* An `error_message` reading `not a privileged join request` if the request is not a join request at tier `privileged_member`.
* An `error_message` reading `request is not open to this answer` if the request is declined or expired, or its joiner is expelled.
* An `error_message` if signing fails or SwarmState refuses the membership.
* A [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md): the joiner's privileged membership, issued by the user key with no `ApprovalID`. It is also returned when SwarmState holds it until the entries it needs arrive.

## Examples

```shellsession
$ astral-query user.confirm_join -id data1... -out json
{"Type":"mod.auth.signed_contract","Object":{"Issuer":"...","Subject":"...","Permits":[...],"ExpiresAt":"...","IssuerSig":{...}}}
```
