# mod.objects.registration_lease

The lease granted to an external provider by `objects.register_searcher`,
`objects.register_describer`, or `objects.register_finder`. A registration is
valid only until it expires, and the registrant renews it by repeating the
registration op before then.

The node chooses the lease: it clamps the requested `duration` to its configured
maximum, so the granted `Duration` may be shorter than the one asked for and is
never longer.

`Duration` and `ExpiresAt` describe the same lease from two vantage points.
`Duration` is relative and needs no agreement about the current time, so a
registrant schedules renewal from it. `ExpiresAt` is the node's own record of
when the lease ends.

## Fields

* Duration (duration) – The granted lease lifetime, after clamping.
* ExpiresAt (time) – The instant the registration expires unless it is renewed.

## Example

A one-hour lease:

```json
{
  "Type": "mod.objects.registration_lease",
  "Object": {
    "Duration": 3600000000000,
    "ExpiresAt": "2026-07-29T07:00:00Z"
  }
}
```
