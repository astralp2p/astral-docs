# apphost.unhold_object

Release the calling app's hold on an object. Local-only — queries from the
network are rejected.

## Arguments

* id (object_id.sha256) – The object whose hold should be released. When omitted the op enters batch mode and reads object IDs from the input stream.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Object IDs to release; consumed only when `id` is omitted, until EOS/EOF.

Every `id`, given as `id` or streamed, is an
[`Object ID`](../../../core-definitions/object-id.md) with a nonzero `Size`.
The operation refuses an `Object ID` whose `Size` is 0 and releases nothing.
Its `error_message` carries the text `partial object id`, and the text
`missing object id` for the zero `Object ID`, which the operation refuses as a
missing argument before it tests the `Size`.

A hold is placed under an `Object ID` with a nonzero `Size`, because
[`apphost.hold_object`](apphost.hold_object.md) refuses any other. No hold is
reachable by a
[`Partial Object ID`](../../../core-definitions/object-id.md), so refusing one
separates an unusable argument from the `ack` that releasing an absent hold
returns.

The `Object ID` of the `Empty Object` has a `Size` of 0 and a nonzero `Hash`,
so this operation refuses it with the text `partial object id`.

## Returned objects

With `id` set, the operation returns one of:
* An `error_message` object if the caller is missing an identity, the object id is missing, the object id is a `Partial Object ID`, or the database call failed.
* An `ack` object if the hold was released. Releasing a hold that does not exist also returns an `ack`.

In batch mode the operation returns one `ack` or `error_message` per input, in input order; a failed input does not end the batch, and an input of an unexpected type is answered with an `error_message`. An explicit EOS input is answered with a final EOS; a stream ended by EOF is not.

## Examples

```shellsession
$ astral-query apphost.unhold_object -id sha256:3b1f5d8c... -out text
#[ack]
```

```shellsession
$ printf '%s\n' '{"Type":"object_id.sha256","Object":"sha256:3b1f5d8c..."}' '{"Type":"object_id.sha256","Object":"sha256:9c2e41aa..."}' | astral-query apphost.unhold_object -in json -out json
{"Type":"ack","Object":null}
{"Type":"ack","Object":null}
```
