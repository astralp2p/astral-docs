# user.mnemonic

Answer the BIP-39 words that [`user.bootstrap`](user.bootstrap.md) stored for
the node's user, so the user can back them up after the claim. The reply is a
[`mod.user.mnemonic`](../types/mod.user.mnemonic.md). The words hold the
user's key: any holder of them acts as the user. The passphrase is never stored
and is not part of the reply.

The node refuses the query in these cases, in this order:

* The query's origin is `network`, `mcp` or any origin other than local:
  answered with an `error_message` reading `origin not allowed: <origin>`.
* The node has no user (it is unclaimed): answered with `no mnemonic stored`,
  whoever the caller is.
* The caller is neither the node's user, the issuer of its active contract,
  nor the node's [manager](../../sys/README.md#manager): answered with
  `not permitted`.

The words stay stored until [`user.forget_mnemonic`](user.forget_mnemonic.md)
deletes them. They are not a user asset and never sync to other nodes.

## Arguments

* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns one of:
* A `mod.user.mnemonic` holding the stored words.
* An `error_message` reading `no mnemonic stored` if the node holds no words
  for the user: the node was claimed by another path, or the words were
  forgotten.
* An `error_message` if reading the stored object fails.

## Examples

```shellsession
$ astral-query user.mnemonic -out json
{"Type":"mod.user.mnemonic","Object":{"Words":"penalty stadium garlic ... rifle fitness garage"}}
```
