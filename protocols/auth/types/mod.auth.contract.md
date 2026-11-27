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
issuer and the subject, and only as far as the walk from its issuer reaches a
handler or the external authority that allows the action ([auth, Authority in a
swarm](../README.md#authority-in-a-swarm)). The user's own powers are decided by
their handlers: the user key's contract carries
[`mod.user.expel_action`](../../user/types/mod.user.expel_action.md),
[`mod.auth.sudo_action`](mod.auth.sudo_action.md) as the user and
[`mod.user.admin_swarm_action`](../../user/types/mod.user.admin_swarm_action.md),
and no contract a Privileged member issues carries
`mod.user.admin_swarm_action`. A contract's `RequestID` adds no authority.

The signable form of a contract is one printable ASCII line of at most 217
bytes (`MaxContractTextLen`), used when signing with text-only schemes (e.g.
`bip137`):

```
<issuer> grants <subject> <actions> depth <d> until <YYYY-MM-DD hh:mm:ss>
```

* `<actions>` lists the distinct actions of the permits, in permit order and
  separated by `,`, each by its word:
  * the action's permit word (`PermitWord`), when its type declares a valid
    one, such as the tier of a membership (`member`, `trusted` or
    `privileged_member`). A valid permit word is 1 to 17 bytes of `a`–`z` and
    `_`;
  * otherwise `<module>.<name>`, for an action type `mod.<module>.<name>_action`
    whose module and name are each 1 or more bytes of `a`–`z`, `0`–`9` and `_`,
    for example `auth.sudo` for `mod.auth.sudo_action`.
* An action with neither word is counted but not named. The words are taken
  in order, and a word is shown when the whole line, with that word, every
  earlier word and the `+<n>` suffix for the actions left out after it, is at
  most `MaxContractTextLen` bytes. The first word that does not fit ends the
  list: no later word is shown, even one that would fit. The list shown is
  the longest prefix of the words in which each word fits this way.
* When an action is not shown, the list ends with `+<n>`, the number of
  distinct actions not shown, so every action is counted. The suffix is
  `,+<n>` after a shown word, and `+<n>` when no word is shown. A contract
  without permits shows `none`.
* `<d>` is the largest `Delegation` among the permits. The time is ExpiresAt
  in UTC, to the second; a fraction of a second is dropped.
* Constraints are not shown: they only narrow a permit. The text therefore never
  shows a grant narrower than the one signed.

A text-only signer signs the line after a 23-byte commitment,
`[<20 base64 characters>] `: the first 15 bytes of the contract's object ID
hash, in standard base64. The signed line is therefore at most 240 bytes, which
a Coldcard signs ([coldcard](../../coldcard/README.md)), whatever the contract
holds. The commitment binds everything else, RequestID included. Binary schemes
(e.g. `asn1`) sign the contract's object ID.

A privileged membership, for example, reads:

```
<issuer> grants <subject> privileged_member depth 0 until 2027-11-25 10:00:00
```

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
