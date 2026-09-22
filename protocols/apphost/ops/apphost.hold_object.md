# apphost.hold_object

Place a hold on an object on behalf of the calling app, preventing it from
being purged for the hold's duration. Local-only — queries from the network
are rejected.

## Arguments

* id (object_id.sha256) – The object to hold. When omitted the op enters batch mode and reads object IDs from the input stream.
* duration (duration) – How long to hold the object. No duration means an indefinite hold. In batch mode the duration applies to every input.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Object IDs to hold; consumed only when `id` is omitted, until EOS/EOF.

Every `id`, given as `id` or streamed, is an
[`Object ID`](../../../core-definitions/object-id.md) with a nonzero `Size`.
The operation refuses an `Object ID` whose `Size` is 0 and stores nothing. Its
`error_message` carries the text `partial object id`, and the text
`missing object id` for the zero `Object ID`, which the operation refuses as a
missing argument before it tests the `Size`.

[`objects.purge`](../../objects/ops/objects.purge.md) matches a hold by the
`Object ID` it was placed under, and every `Object ID` it tests has a nonzero
`Size`. A hold placed under a
[`Partial Object ID`](../../../core-definitions/object-id.md) matches no such
test, so the object it names is purged while the hold stands.

An app can hold an object before the node has its bytes, so the operation reads
no repository and resolves no `Partial Object ID`.

The `Object ID` of the `Empty Object` has a `Size` of 0 and a nonzero `Hash`,
so this operation refuses it with the text `partial object id`.

## Returned objects

With `id` set, the operation returns one of:
* An `error_message` object if the caller is missing an identity, the object id is missing, the object id is a `Partial Object ID`, or the database call failed.
* An `ack` object if the hold was placed.

In batch mode the operation returns one `ack` or `error_message` per input, in input order; a failed input does not end the batch, and an input of an unexpected type is answered with an `error_message`. An explicit EOS input is answered with a final EOS; a stream ended by EOF is not.

## Examples

```shellsession
$ astral-query apphost.hold_object -id sha256:3b1f5d8c... -duration 24h -out text
#[ack]
```

```shellsession
$ printf '%s\n' '{"Type":"object_id.sha256","Object":"sha256:3b1f5d8c..."}' '{"Type":"object_id.sha256","Object":"sha256:9c2e41aa..."}' | astral-query apphost.hold_object -in json -out json
{"Type":"ack","Object":null}
{"Type":"ack","Object":null}
```
