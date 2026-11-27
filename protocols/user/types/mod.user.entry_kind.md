# mod.user.entry_kind

The SwarmState directory an entry belongs in. An entry is stored as
`swarmstate/<kind>/<object id>`.

The wire form is a `string8` holding the word itself. The text form is the word verbatim; JSON encodes the type as that same string. The empty word, and any word not listed below, is not a valid value.

## Values

| Value | Entries |
|-------|---------|
| `requests` | [`mod.user.signed_contract_request`](mod.user.signed_contract_request.md), [`mod.user.signed_join_request`](mod.user.signed_join_request.md), [`mod.user.signed_expel_request`](mod.user.signed_expel_request.md) |
| `approvals` | [`mod.user.signed_approval`](mod.user.signed_approval.md), of an expel request |
| `declines` | [`mod.user.signed_decline`](mod.user.signed_decline.md) |
| `contracts` | [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md): memberships, app contracts and half-signed offers |
| `expels` | [`mod.user.signed_expulsion`](mod.user.signed_expulsion.md) |

Only signed forms are entries. An unsigned body has no kind.

## Example

```json
{
  "Type": "mod.user.entry_kind",
  "Object": "approvals"
}
```
