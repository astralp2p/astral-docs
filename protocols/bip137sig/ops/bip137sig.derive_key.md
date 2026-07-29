# bip137sig.derive_key

Derive a `secp256k1` private key from a BIP-39 seed along a BIP-32 derivation path. The seed is treated as the root for `hdkeychain.NewMaster` on Bitcoin MainNet parameters.

## Arguments

* path (string, required) – BIP-32 derivation path, e.g. `m/44'/0'/0'/0/0`. The leading `m/` is optional. Hardened indices may be marked with `'` or `h`. An empty path or `m` returns the master key.
* (stream) – A `bip137sig.seed` object to derive from.

## Returned objects

The operation returns one of:
* An `error_message` object if the path is malformed or derivation fails.
* A `mod.crypto.private_key` object with `Type = "secp256k1"` holding the raw 32-byte private key.

## Examples

```shellsession
$ echo '{"Type":"bip137sig.seed","Object":"5eed0102...64bytes...cafef00d"}' \
    | astral-query bip137sig.derive_key -path "m/44'/0'/0'/0/0" -in json -out json
{"Type":"mod.crypto.private_key","Object":{"Type":"secp256k1","Key":"3082..."}}
```
