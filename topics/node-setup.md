# Node Setup

A [`Node`](../core-definitions/node.md) starts without a
[`User`](../core-definitions/user.md). Node setup claims the node for a `User`:
afterwards the node holds the user's private key and an active node contract
that the user issues to the node. Until then
[`user.info`](../protocols/user/ops/user.info.md) rejects with code `2`, and the
node logs `this node runs without a user` at startup.

Node setup runs in one call ([`user.bootstrap`](#one-call)) or
[step by step](#step-by-step). Both claim the node with the same contract and the
same rules.

## The user key

* A `User` identity is a `secp256k1` key derived from BIP-39 words along the
  BIP-32 path `m/1791'/0'/0'/0/0`. A Coldcard derives its Astral key on the same
  path, so one set of words derives one `User` on a Coldcard and in software.
* The words are the user's backup. The node keeps no copy of them. A lost set of
  words cannot be recovered from the node.
* A BIP-39 passphrase is optional. The same words with another passphrase derive
  another `User`.
* The node keeps the user's private key after setup. The node signs as the user
  with it, for example in [`user.adopt`](../protocols/user/ops/user.adopt.md).

## Who may set up a node

* Setup runs on the node, from a local session. A local caller that presents no
  identity acts as the node.
* [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md) and
  [`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md) reject a
  query of origin `network`, `mcp` or any other origin than local.
* The node signs the claim contract for its own session only, and only under the
  claim rule of
  [`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md). The rule
  refuses:
  * any contract once the node has an active contract;
  * an identity the node minted, through
    [`apphost.register`](../protocols/apphost/ops/apphost.register.md),
    [`messaging.create_mailbox`](../protocols/messaging/ops/messaging.create_mailbox.md)
    or [`mcp.create_agent`](../protocols/mcp/ops/mcp.create_agent.md);
  * a `User` the node has had, even after that user's contract has expired.

## One call

[`user.bootstrap`](../protocols/user/ops/user.bootstrap.md) derives the key,
signs the claim contract as both parties, stores the key and activates the
contract. It answers a
[`mod.user.bootstrap_result`](../protocols/user/types/mod.user.bootstrap_result.md).

New identity: the node generates 24 words and returns them in the reply.

```shellsession
$ astral-query user.bootstrap -generate true -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02e96bd9...","Mnemonic":"penalty stadium garlic ... rifle fitness garage"}}
```

The generated words appear in this reply only. A reply lost after the claim
leaves the node owned by a user whose words exist nowhere. A client that confirms
the user's backup before the claim generates the words with the first two steps
of [Step by step](#step-by-step) and then sends them to `user.bootstrap`.

Existing identity: the words arrive in the input stream. The reply carries an
empty `Mnemonic`.

```shellsession
$ echo '{"Type":"string16","Object":"horse soldier ... term change"}' \
    | astral-query user.bootstrap -in json -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02564ba7...","Mnemonic":""}}
```

## Step by step

| Step | Op | Input | Result |
|------|----|-------|--------|
| 1. Words | [`bip137sig.new_entropy`](../protocols/bip137sig/ops/bip137sig.new_entropy.md), [`bip137sig.mnemonic`](../protocols/bip137sig/ops/bip137sig.mnemonic.md) | — | `string16` words |
| 2. Seed | [`bip137sig.seed`](../protocols/bip137sig/ops/bip137sig.seed.md) | words | `bip137sig.seed` |
| 3. Key | [`bip137sig.derive_key`](../protocols/bip137sig/ops/bip137sig.derive_key.md) `-path "m/1791'/0'/0'/0/0"` | seed | `mod.crypto.private_key` |
| 4. Hold the key | [`objects.store`](../protocols/objects/ops/objects.store.md) | private key | `object_id` |
| 5. User identity | [`crypto.public_key`](../protocols/crypto/ops/crypto.public_key.md) | private key | `mod.crypto.public_key` |
| 6. Contract | [`user.new_node_contract`](../protocols/user/ops/user.new_node_contract.md) `-user <identity>` | — | `mod.auth.contract` |
| 7. Sign | [`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md) | contract | `mod.auth.signed_contract` |
| 8. Activate | [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md) | signed contract | `ack` |
| 9. Verify | [`user.info`](../protocols/user/ops/user.info.md) | — | `mod.user.info` |

* The `bip137sig` ops return values and persist nothing. A derived key is not
  usable by the node until step 4 stores it.
* [`objects.store`](../protocols/objects/ops/objects.store.md) writes the key to
  the `local` repository. The `crypto` module indexes every private key stored
  there, and the node then signs as the key's identity.
* The `User` identity is the compressed public key in hex. The text output of
  `crypto.public_key` prints it after `secp256k1:`.
* The existing-identity flow starts at step 2 with the user's words.

New identity:

```shellsession
$ astral-query bip137sig.new_entropy -bits 256 -out json \
    | astral-query bip137sig.mnemonic -in json -out json > words.json
$ astral-query bip137sig.seed -in json -out json < words.json \
    | astral-query bip137sig.derive_key -in json -out json -path "m/1791'/0'/0'/0/0" > key.json
$ astral-query -eos objects.store -in json -out json < key.json
{"Type":"object_id.sha256","Object":"data1rqceqtcaboxix35pcbnc56b14xkr7q4y8khzkrns88fan85m6suet"}
{"Type":"eos","Object":null}
$ USER_ID=$(astral-query -eos crypto.public_key -in json -out text < key.json \
    | awk -F'secp256k1:' 'NF>1{print $2}')
$ astral-query user.new_node_contract -user "$USER_ID" -out json > contract.json
$ astral-query -eos auth.sign_contract -in json -out json < contract.json \
    | head -1 > signed.json
$ astral-query user.accept_contract -in json -out json < signed.json
{"Type":"ack","Object":null}
$ astral-query user.info -out json
{"Type":"mod.user.info","Object":{...}}
```

Existing identity: the first command writes the user's words instead.

```shellsession
$ echo '{"Type":"string16","Object":"horse soldier ... term change"}' > words.json
```

`words.json` and `key.json` hold the user's secret. A shell session that follows
these steps deletes both files after step 8.

### Ending input

[`objects.store`](../protocols/objects/ops/objects.store.md),
[`crypto.public_key`](../protocols/crypto/ops/crypto.public_key.md) and
[`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md) read their
input in batch mode. Each one needs `-eos` before the operation name. Without
`-eos` the command prints its result and does not exit
([`astral-query`, Ending input](../tools/astral-query.md#ending-input)). A
batch-mode result ends with an `eos` line, which the next single-mode op does not
read: `head -1` keeps the result alone.

## Refusals

| Answer | Cause | Remedy |
|--------|-------|--------|
| `user.info`: `query rejected (2)` | The node has no active contract. | Run node setup. |
| `auth.sign_contract`: `sign as issuer: unsupported` | The node does not hold the user's private key. | Store the key with `objects.store`, then sign again. |
| `auth.sign_contract`: `authorize issuer: cannot sign with another identity's key` | The claim rule refuses: the node has an active contract, the node minted the identity, or the node had this user before. | Use an identity derived from BIP-39 words, on an unclaimed node that never had this user. |
| `user.bootstrap`: `query rejected (2)` | The node has an active contract. | — |
| `user.bootstrap`: `query rejected (4)` | The caller is not the node. | Call from a local session without a token, or with the node's own token. |
| `user.bootstrap`: `claim refused: the claim rule of auth.sign_contract refuses this user` | The claim rule refuses the user. | As for `auth.sign_contract` above. |
| `user.bootstrap`: `invalid mnemonic` | The words fail the BIP-39 checksum. | Check the words. |
