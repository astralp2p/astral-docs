# mod.user.tier

A swarm member's tier, fixed when it joins. A membership contract carries the
tier as its one tier permit (see
[SwarmState entries](../README.md#memberships)).

The wire form is a `string8` holding the word itself. The text form is the word verbatim; JSON encodes the type as that same string. The empty word, and any word not listed below, is not a valid value.

## Values

| Value | Tier permit | Meaning |
|-------|-------------|---------|
| `member` | [`mod.user.member_action`](mod.user.member_action.md) | Links to the swarm and syncs SwarmState. Adds nobody. |
| `trusted` | [`mod.user.trusted_action`](mod.user.trusted_action.md) | Adds members, and answers join requests at tier `member`. |
| `privileged_member` | [`mod.user.privileged_member_action`](mod.user.privileged_member_action.md) | Acts for the user in everything except expelling. Only the user key signs its membership. |

## Example

```json
{
  "Type": "mod.user.tier",
  "Object": "trusted"
}
```
