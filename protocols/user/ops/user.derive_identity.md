# user.derive_identity

Answer the user that BIP-39 words derive, without claiming the node. The user's
key is derived along the path `m/1791'/0'/0'/0/0`, the path of
[`user.bootstrap`](user.bootstrap.md). The words arrive in the input stream, or
the node generates 24 words when `generate` is set. The node derives the key in
memory, stores nothing, signs nothing and changes no state. The reply is a
[`mod.user.derive_identity_result`](../types/mod.user.derive_identity_result.md).

`user.derive_identity` previews the claim of `user.bootstrap`: one function
derives the key for both operations, so the same words and passphrase give the
identity `user.bootstrap` claims the node for. A client that sets up a node for
a new user calls `user.derive_identity` with `generate`, shows the words and the
identity, and sends the same words to `user.bootstrap` once the user has
recorded them. A client that restores a user sends the user's words and shows
the identity before the claim. The client derives no key itself.

A query whose origin is `network`, `mcp` or any origin other than local is
answered with an `error_message` reading `origin not allowed: <origin>`.

The words never appear in a log line or a stored object. Words the caller sends
never appear in a reply. Generated words appear in one reply only, and the node
keeps no copy of them.

## Arguments

* generate (bool, optional) – When true, the node generates 24 words from 256
  bits of entropy and reads no input. Defaults to false.
* passphrase (string, optional) – BIP-39 passphrase of the seed. Defaults to
  empty.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Without `generate`: one `string16` holding the BIP-39 words,
  separated by whitespace.

## Returned objects

The query is answered `origin not allowed: <origin>` in the case above.
Otherwise the operation returns one of:
* A `mod.user.derive_identity_result`. Its `Mnemonic` holds the generated
  words, and is empty when the caller sent the words.
* An `error_message` reading `invalid mnemonic` or
  `mnemonic must be 12, 15, 18, 21, or 24 words` if the words are not valid
  BIP-39 words.
* An `error_message` reading `user key derivation requires the bip137sig module`
  if the node runs without the `bip137sig` module.
* An `error_message` if the input is missing or is not a `string16`, or if word
  generation fails.

## Examples

```shellsession
$ astral-query user.derive_identity -generate true -out json
{"Type":"mod.user.derive_identity_result","Object":{"Identity":"02a1...","Mnemonic":"penalty stadium garlic ... rifle fitness garage"}}
```

```shellsession
$ echo '{"Type":"string16","Object":"horse soldier ... term change"}' \
    | astral-query user.derive_identity -in json -out json
{"Type":"mod.user.derive_identity_result","Object":{"Identity":"02564ba7...","Mnemonic":""}}
```
