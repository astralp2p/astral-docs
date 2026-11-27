# mod.user.approval

The unsigned body of an answer of yes to a stored expel request. Issuer signs
it. Wrap it in [`mod.user.signed_approval`](mod.user.signed_approval.md) before
storing or propagating it.

Only an expel request has an approval. The user key carries it out by signing a
[`mod.user.signed_expulsion`](mod.user.signed_expulsion.md). An approval counts
whenever it is given, because nodes cannot tell when it was signed; answering
nodes do not sign an answer to a request whose Timeout has passed. An approval
gives the expulsion no authority: only the user key's signature expels.

A contract request is answered with an offer, a half-signed
[`mod.auth.contract`](../../auth/types/mod.auth.contract.md) that names the
request as its `RequestID` ([App grants](../README.md#app-grants)), and a join
request is answered by the carrier signing the membership
([Joins](../README.md#joins)); neither is an approval.

Who may answer depends on the answering node's [tier](mod.user.tier.md):

| Answerer | May answer |
|----------|------------|
| `privileged_member` | every contract, join and expel request |
| `trusted` | a join request at tier `member` only |
| `member` | none |
| the user key | every request; it needs no tier |

The table decides who may answer a request with an approval, an offer or a
decline. A join request is answered with a decline only.

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* Issuer (identity) – Identity that answers and signs the approval.
* RequestID (object_id) – Entry ID of the stored
  [`mod.user.signed_expel_request`](mod.user.signed_expel_request.md) it
  answers. It is not the ID of the unsigned request body.

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
