# mod.user.contract_request

The unsigned body of a request for permits for an identity, for example an app
that the filing node hosts. FiledBy signs it. A Privileged member, or the user
key, answers it with an offer, a half-signed
[`mod.auth.contract`](../../auth/types/mod.auth.contract.md) from the answerer
to FiledBy that names this request as its `RequestID`, or closes it with a
[`mod.user.decline`](mod.user.decline.md). FiledBy adds its signature to an
offer for its own request only, and signs the permits onward to Identity
([App grants](../README.md#app-grants)). Wrap it in
[`mod.user.signed_contract_request`](mod.user.signed_contract_request.md)
before storing or propagating it.

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* FiledBy (identity) – Identity of the node that files the request and signs it.
* Identity (identity) – Identity the requested permits are for.
* Permits ([[]mod.auth.permit](../../auth/types/mod.auth.permit.md)) – The permits requested.
* FiledAt (time) – Time the request was filed.
* Timeout (time) – Time after which the request can no longer be answered. It
  is after FiledAt and at most 1 hour after it; a new request defaults to
  exactly 1 hour after FiledAt.

Two contracts relate to a request through their permits:

* A contract to FiledBy **answers** the request when its permits follow the
  [offer depth rule](../README.md#app-grants): it has at least one permit;
  each permit has the Action and Constraints of a requested permit, byte-equal,
  and a Delegation exactly one more than that permit's; no two of its permits
  are equal; and it carries no other permit. It may carry all of the requested
  permits or only some of them. An offer answers the request, and so does the
  completed approver-to-FiledBy contract, which has the offer's permits and
  both signatures.
* A contract to Identity **carries out** the request only when it has at least
  one permit and each of its permits encodes byte-equal, Action, Constraints
  and Delegation alike, to one of the requested Permits. A contract that copies
  Permits always qualifies.

Who issues each contract is checked separately.

The signable text is one ASCII line:

```
<filed by> requests permits (<n>) for <identity> until <YYYY-MM-DD hh:mm:ss>
```

`<n>` is the number of Permits. The time is Timeout in UTC, to the second; a
fraction of a second is dropped.

## Example

```json
{
  "Type": "mod.user.contract_request",
  "Object": {
    "FiledBy": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Identity": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "Permits": [
      { "Action": "mod.auth.serve_apps_action", "Constraints": null, "Delegation": 0 }
    ],
    "FiledAt": "2026-11-25T10:00:00Z",
    "Timeout": "2026-11-25T11:00:00Z"
  }
}
```
