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

## Returned objects

With `id` set, the operation returns one of:
* An `error_message` object if the caller is missing an identity, the object id is missing, or the database call failed.
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
