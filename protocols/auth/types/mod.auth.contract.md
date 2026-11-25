# mod.auth.contract

A grant from one identity (the issuer) to another (the subject), authorising
the subject to perform a set of actions on the issuer's behalf until a given
expiry time. A contract on its own carries no signatures; once co-signed by
the issuer and the subject it becomes a `mod.auth.signed_contract` and can
be indexed by the `auth` module.

## Fields

* Issuer (identity) – Identity granting the permissions.
* Subject (identity) – Identity receiving the permissions.
* Permits ([mod.auth.permit]) – List of permits granted by this contract.
* ExpiresAt (time) – Time at which the contract stops being active.
* ApprovalID (object_id, optional) – Entry ID of the stored
  [`mod.user.signed_approval`](../../user/types/mod.user.signed_approval.md)
  this contract carries out, not the ID of the unsigned approval body. `null`
  when the contract carries out no approval, for example a membership the user
  key signs directly.

Fields encode in order, without tags. ApprovalID comes last, so the earlier
fields keep their offsets, but adding it changed the encoding and object ID of
every contract: a contract encoded before ApprovalID existed no longer decodes.

A contract grants an action if any of its permits matches the action's
object type and the action's constraint evaluation (if any) accepts the
permit's `Constraints` bundle.

The signable form of a contract is one ASCII line, used when signing with
text-only schemes (e.g. `bip137`):

```
<issuer> grants <subject> [<word> ]permits (<n>) until <YYYY-MM-DD hh:mm:ss>
```

`<n>` is the number of permits and the time is ExpiresAt. `<word>` is the
first valid permit word among the permits' actions, such as the tier of a
membership (`member`, `trusted` or `privileged_member`), and is absent when no
action declares one. A word is valid when it is 1 to 17 bytes of `a`–`z` and
`_`. The signer's commitment binds everything else, ApprovalID included.
Binary schemes (e.g. `asn1`) sign the contract's object ID.

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
    "ApprovalID": null
  }
}
```
