# mod.user.decline

The unsigned body of an answer of no to a stored request. Issuer signs it.
Wrap it in [`mod.user.signed_decline`](mod.user.signed_decline.md) before storing
or propagating it.

A decline closes its request and nothing else. The merge check drops every new
offer for the request, the node an offer names as subject refuses to co-sign a
stored one, and a carrier signs no membership for it. A decline takes nothing
back: a contract that both parties signed already keeps its authority, and a
signed expulsion stays ([SwarmState entries](../README.md#requests-and-answers)).
A contract is taken back only by expelling a party in its chain, or when it
expires.

Who may answer depends on the answering node's [tier](mod.user.tier.md):

| Answerer | May answer |
|----------|------------|
| `privileged_member` | every contract, join and expel request |
| `trusted` | a join request at tier `member` only |
| `member` | none |
| the user key | every request; it needs no tier |

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* Issuer (identity) – Identity that answers and signs the decline.
* RequestID (object_id) – Entry ID of the stored signed request it answers: a
  [`mod.user.signed_contract_request`](mod.user.signed_contract_request.md),
  [`mod.user.signed_join_request`](mod.user.signed_join_request.md) or
  [`mod.user.signed_expel_request`](mod.user.signed_expel_request.md). It is
  not the ID of the unsigned request body.

The signable text is one ASCII line:

```
<issuer> declines request <request id>
```

A missing RequestID shows as `none`.

## Example

```json
{
  "Type": "mod.user.decline",
  "Object": {
    "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp"
  }
}
```
