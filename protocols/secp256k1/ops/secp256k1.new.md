# secp256k1.new

Generate a new secp256k1 private key and return it to the caller.

## Arguments

No arguments.

## Returned objects

The operation returns one of:
* A `mod.crypto.private_key` object containing the generated key.

## Examples

```shellsession
$ astral-query secp256k1.new -out json
{"Type":"mod.crypto.private_key","Object":{"Key":"Yt+8a1q4XbPnGZsbT5gV/Sj5y4kCmWNL2L4y3rXh0vQ=","Type":"secp256k1"}}
```
