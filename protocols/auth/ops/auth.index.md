# auth.index

Add a stored `mod.auth.signed_contract` to the local auth index. The
referenced object is loaded from the `objects` module, both signatures are
verified, and the contract is stored so it can be consulted by future
authorization decisions. Indexing is idempotent — re-indexing the same
contract is a no-op.

## Arguments

* id (object_id.sha256) – Object ID of the `mod.auth.signed_contract` to index. When omitted the op enters batch mode and reads object IDs from the input stream.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Object IDs of contracts to index; consumed only when `id` is omitted, until EOS/EOF.

## Returned objects

With `id` set, the operation returns one of:
* An `error_message` object if the object cannot be loaded, is not a
  `mod.auth.signed_contract`, or either signature fails to verify.
* An `ack` object once the contract has been indexed (or was already
  present).

In batch mode the operation returns one `ack` or `error_message` per input, in input order; a failed input does not end the batch, and an input of an unexpected type is answered with an `error_message`. An explicit EOS input is answered with a final EOS; a stream ended by EOF is not.

## Examples

```shellsession
$ astral-query auth.index -id 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 -out json
{"Type":"ack","Object":{}}
```

```shellsession
$ printf '%s\n' '{"Type":"object_id.sha256","Object":"9f86d081..."}' '{"Type":"object_id.sha256","Object":"4ba51ce0..."}' | astral-query auth.index -in json -out json
{"Type":"ack","Object":{}}
{"Type":"ack","Object":{}}
```
