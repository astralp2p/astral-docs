# services.removed

A notice on a [`services.discover`](../ops/services.discover.md) stream that
listed offerings left the caller's view. It contains only keys previously shown
as available. `Cause` states why the node retracted them.

A [`services.update`](services.update.md) with `Available: false` instead
withdraws an offering by the provider's own answer.

## Cause

`Cause` is a `uint8`. The value is one of:

* `1` – member_lost: the carry to the contributing swarm member ended. On a
  follow, the node retries the member when a link appears or after a backoff
  of 1 s to 60 s, and recovered offerings arrive as
  [`services.update`](services.update.md). A one-shot discovery does not
  retry: a member whose discovery fails before its initial outcome has the
  offerings it already showed removed with `member_lost`, and they do not
  return on that stream.
* `2` – member_left: the contributing swarm member left the swarm set. The node
  does not retry the member.
* `3` – member_removed: the contributing swarm member sent `services.removed`
  for the offering.
* `4` – binding_closed: the provider's advertise binding or native registration
  on the node ended, including a binding the node ended for unanswered asks.
* `5` – hidden: the caller may no longer see the offering.

A cause describes the hop the node itself saw. A `services.removed` that a swarm
member sends to the node reaches the caller with `member_removed`, whatever the
member's own cause.

Each `services.removed` carries one cause. Keys the node retracts for different
causes arrive in separate `services.removed` objects. A key retracted twice
before its removal is written keeps the first cause.

## Fields

* Offerings (array of [`services.offering_key`](services.offering_key.md)) – The offerings no longer valid.
* Cause (uint8) – Why the node retracted the offerings, from the list above.

## Example

```json
{
  "Type": "services.removed",
  "Object": {
    "Offerings": [
      {
        "ProviderID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
        "Name": "player"
      }
    ],
    "Cause": 1
  }
}
```
