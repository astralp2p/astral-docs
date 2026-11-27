# mod.user.join_request

The unsigned body of a request for Joiner to join the swarm at a tier, carried
in by Carrier, a Trusted or Privileged member. Joiner signs it with Carrier
already named, and resends the same signed object to resume a join. Carrier
signs the membership with Joiner in the session that carries the request
([Joins](../README.md#joins)). Wrap it in
[`mod.user.signed_join_request`](mod.user.signed_join_request.md) before
storing or propagating it.

A join request has no approval. Carrier signs the membership itself, at a tier
its own tier may issue: a Trusted Carrier issues `member`, a Privileged Carrier
`member` or `trusted`. The user key signs a `privileged_member` membership in a
ceremony. A Privileged member or the user key may decline any join request, and
a Trusted member a join request at tier `member`; a decline closes the request
and Carrier signs no membership for it.

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* Joiner (identity) – Identity of the node that asks to join and signs the request.
* Carrier (identity) – Identity of the Trusted or Privileged member that carries the request in.
* Tier ([mod.user.tier](mod.user.tier.md)) – The tier the joiner asks for.
* FiledAt (time) – Time the request was filed.
* Timeout (time) – Time after which the request can no longer be answered. It
  is after FiledAt and at most 1 hour after it; a new request defaults to
  exactly 1 hour after FiledAt.

The signable text is one ASCII line:

```
<joiner> asks <carrier> to join as <tier> until <YYYY-MM-DD hh:mm:ss>
```

The time is Timeout. A Tier that is not one of the three tiers shows as
`invalid`.

## Example

```json
{
  "Type": "mod.user.join_request",
  "Object": {
    "Joiner": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "Carrier": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Tier": "member",
    "FiledAt": "2026-11-25T10:00:00Z",
    "Timeout": "2026-11-25T11:00:00Z"
  }
}
```
