# indexing.remove_index

Remove a registered indexer identified by `nonce`, unregistering it from future change delivery.

## Arguments

* nonce (nonce64, required) – Nonce of the indexer to remove.

## Returned objects

The operation returns one of:
* An `error_message` object if the nonce does not identify a known indexer or removal fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query indexing.remove_index -nonce 0102030405060708 -out json
{"Type":"ack","Object":{}}
```
