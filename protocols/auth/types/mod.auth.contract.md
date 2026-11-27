# mod.auth.contract

A grant from one identity (the issuer) to another (the subject), authorising
the subject to perform a set of actions on the issuer's behalf until a given
expiry time. A contract on its own carries no signatures; once co-signed by
the issuer and the subject it becomes a `mod.auth.signed_contract` and can
be indexed by the `auth` module. A contract carries authority only when both
signed it ([Authority in a swarm](../README.md#authority-in-a-swarm)).

## Fields

* Issuer (identity) – Identity granting the permissions.
* Subject (identity) – Identity receiving the permissions.
* Permits ([mod.auth.permit]) – List of permits granted by this contract.
* ExpiresAt (time) – Time at which the contract stops being active.
* RequestID (object_id, optional) – Entry ID of the stored request this
  contract answers: a
  [`mod.user.signed_contract_request`](../../user/types/mod.user.signed_contract_request.md)
  for an offer and the contracts that carry it out, or a
  [`mod.user.signed_join_request`](../../user/types/mod.user.signed_join_request.md)
  for a membership a carrier signs. It is the ID of the signed request as
  stored, not of the unsigned body. `null` when the contract answers no
  request, for example a membership the user key signs directly. The field
  only links the contract to its request: it adds no authority and never
  redirects the walk of authority, which continues at the issuer.

Fields encode in order, without tags. RequestID comes last, in the place of the
approval link of earlier contracts, so the earlier fields keep their offsets.

A contract grants an action if any of its permits matches the action's
object type and the action's constraint evaluation (if any) accepts the
permit's `Constraints` bundle.

A contract grants an action only when it has valid signatures of both the
issuer and the subject. On a node with a swarm, a contract grants none of the
user's own authority unless the user key issued it: no
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
for the user, no
[`mod.user.admin_swarm_action`](../../user/types/mod.user.admin_swarm_action.md),
no [`mod.auth.sudo_action`](mod.auth.sudo_action.md) as the user and no
[`mod.user.expel_action`](../../user/types/mod.user.expel_action.md), whatever
its permits say and whatever its `RequestID` links to. Its other permits grant
as before. A Privileged member uses swarm administration and relaying as the user
itself and cannot pass them on. An app's relay contract names the app itself and is not affected.

The signable form of a contract is one ASCII line, used when signing with
text-only schemes (e.g. `bip137`):

```
<issuer> grants <subject> [<word> ]permits (<n>) <action>:<depth>[,<action>:<depth>]... until <YYYY-MM-DD hh:mm:ss>
```

`<n>` is the number of permits and the time is ExpiresAt. `<word>` is the
first valid permit word among the permits' actions, such as the tier of a
membership (`member`, `trusted` or `privileged_member`), and is absent when no
action declares one. A word is valid when it is 1 to 17 bytes of `a`–`z` and
`_`. `<action>:<depth>` lists each permit in order: the object type of its
action and its `Delegation`, so a signer sees what the contract grants and how
far the grantee may pass it on, not only how many permits it holds. A list
omits constraints, which only narrow a permit. A text of more than 240 bytes is
not signed by a text-only scheme, and the list is never shortened to fit. The
signer's commitment binds everything else, RequestID included. Binary schemes
(e.g. `asn1`) sign the contract's object ID.

## Example

```json
{
  "Type": "mod.auth.contract",
  "Object": {
    "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "Permits": [
      { "Action": "mod.user.see_swarm_action" }
    ],
    "ExpiresAt": "2027-05-27T12:00:00+02:00",
    "RequestID": null
  }
}
```
