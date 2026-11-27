# mod.user.tier

A swarm member's tier, fixed when it joins. A membership contract carries the
tier as its one tier permit (see
[SwarmState entries](../README.md#memberships)).

The wire form is a `string8` holding the word itself. The text form is the word verbatim; JSON encodes the type as that same string. The empty word, and any word not listed below, is not a valid value.

## Values

| Value | Tier permit | Meaning |
|-------|-------------|---------|
| `member` | [`mod.user.member_action`](mod.user.member_action.md) | Links to the swarm and syncs SwarmState. Adds nobody. |
| `trusted` | [`mod.user.trusted_action`](mod.user.trusted_action.md) | Issues the membership of a joiner at tier `member`, and declines join requests at that tier. |
| `privileged_member` | [`mod.user.privileged_member_action`](mod.user.privileged_member_action.md) | Issues memberships at `member` and `trusted`, answers contract requests with offers, and acts for the user in everything except expelling. Only the user key issues its membership. |

A membership is issued only at a tier the issuer's tier may issue
([Memberships](../README.md#memberships)): the user key any tier,
`privileged_member` the tiers `member` and `trusted`, `trusted` the tier
`member`. A tier never changes. A node that wants another tier joins through an
issuer allowed to issue it.

## Example

```json
{
  "Type": "mod.user.tier",
  "Object": "trusted"
}
```
