# user.forget_mnemonic

Delete the BIP-39 words that [`user.bootstrap`](user.bootstrap.md) stored for
the node's user, once the user has backed them up. The node deletes the
[`mod.user.mnemonic`](../types/mod.user.mnemonic.md) object from its
repository and its record of it. A later [`user.mnemonic`](user.mnemonic.md)
is answered with `no mnemonic stored`. The user's private key stays on the node.

The node refuses the query in these cases, in this order:

* The query's origin is `network`, `mcp` or any origin other than local:
  answered with an `error_message` reading `origin not allowed: <origin>`.
* The node has no user (it is unclaimed): answered with `no mnemonic stored`,
  whoever the caller is.
* The caller is neither the node's user, the issuer of its active contract,
  nor the node's [manager](../../sys/README.md#manager): answered with
  `not permitted`.

## Arguments

* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns one of:
* An `ack` once the words are deleted.
* An `error_message` reading `no mnemonic stored` if the node holds no words
  for the user.
* An `error_message` reading `object in use` if a holder holds the
  `mod.user.mnemonic` object or a store committed it since the delete began; the words stay stored and `user.mnemonic` still
  answers them.
* An `error_message` if the deletion fails otherwise.

## Examples

```shellsession
$ astral-query user.forget_mnemonic -out json
{"Type":"ack","Object":null}
```
