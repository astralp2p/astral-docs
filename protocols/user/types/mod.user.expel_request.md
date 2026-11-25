# mod.user.expel_request

The unsigned body of a request to expel Subject from the swarm. FiledBy, a
Trusted or Privileged member, signs it. Only the user key carries it out, by
signing a [`mod.user.signed_expulsion`](mod.user.signed_expulsion.md) that
names Subject. Wrap it in
[`mod.user.signed_expel_request`](mod.user.signed_expel_request.md) before
storing or propagating it.

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* FiledBy (identity) – Identity of the member that files the request and signs it.
* Subject (identity) – Identity the request asks to expel.
* FiledAt (time) – Time the request was filed.
* Timeout (time) – Time after which the request can no longer be answered. It
  is after FiledAt and at most 1 hour after it; a new request defaults to
  exactly 1 hour after FiledAt.

The signable text is one ASCII line:

```
<filed by> asks to expel <subject> until <YYYY-MM-DD hh:mm:ss>
```

The time is Timeout.

## Example

```json
{
  "Type": "mod.user.expel_request",
  "Object": {
    "FiledBy": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "FiledAt": "2026-11-25T10:00:00Z",
    "Timeout": "2026-11-25T11:00:00Z"
  }
}
```
