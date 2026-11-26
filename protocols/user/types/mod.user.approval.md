# mod.user.approval

The unsigned body of an answer of yes to a stored request. Issuer signs it.
Wrap it in [`mod.user.signed_approval`](mod.user.signed_approval.md) before storing
or propagating it.

The node the approval touches carries it out: it signs a contract whose
`ApprovalID` ([`mod.auth.contract`](../../auth/types/mod.auth.contract.md)) is the entry ID of this approval's
[`mod.user.signed_approval`](mod.user.signed_approval.md). An approval counts
whenever it is given, because nodes cannot tell when it was signed; answering
nodes do not sign an answer to a request whose Timeout has passed.

Who may answer depends on the answering node's [tier](mod.user.tier.md):

| Answerer | May answer |
|----------|------------|
| `privileged_member` | every contract, join and expel request |
| `trusted` | a join request at tier `member` only |
| `member` | none |
| the user key | every request; it needs no tier |

[`user.answer_request`](../ops/user.answer_request.md) signs one, as a [`mod.user.signed_approval`](mod.user.signed_approval.md), and adds it to SwarmState. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* Issuer (identity) – Identity that answers and signs the approval.
* RequestID (object_id) – Entry ID of the stored signed request it answers: a
  [`mod.user.signed_contract_request`](mod.user.signed_contract_request.md),
  [`mod.user.signed_join_request`](mod.user.signed_join_request.md) or
  [`mod.user.signed_expel_request`](mod.user.signed_expel_request.md). It is
  not the ID of the unsigned request body.

The signable text is one ASCII line:

```
<issuer> approves request <request id>
```

A missing RequestID shows as `none`.

## Example

```json
{
  "Type": "mod.user.approval",
  "Object": {
    "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp"
  }
}
```
