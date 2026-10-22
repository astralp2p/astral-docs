# user.bootstrap

Claim this unclaimed node for a user in one call. The user's key is derived
from BIP-39 words along the path `m/1791'/0'/0'/0/0`, the path a Coldcard
derives its Astral key on. The words arrive in the input stream, or the node
generates 24 words when `generate` is set. The node signs the claim contract as
the user, with the derived key held in memory, and as itself. The node then
validates the contract, stores and indexes the user's private key, stores the
contract, and sets the contract as the active contract. The reply is a
[`mod.user.bootstrap_result`](../types/mod.user.bootstrap_result.md).

`user.bootstrap` is the one-call form of [node setup](../../../topics/node-setup.md). It claims the node with the
same contract as the chain
[`bip137sig.seed`](../../bip137sig/ops/bip137sig.seed.md),
[`bip137sig.derive_key`](../../bip137sig/ops/bip137sig.derive_key.md),
[`objects.store`](../../objects/ops/objects.store.md),
[`user.new_node_contract`](user.new_node_contract.md),
[`auth.sign_contract`](../../auth/ops/auth.sign_contract.md) and
[`user.accept_contract`](user.accept_contract.md). The contract carries the
permits of `user.new_node_contract` and expires 365 days after the call.

The query is rejected before it is accepted in these cases, in this order:

* The query's origin is `network`, `mcp` or any origin other than local.
* The node has an active contract: code `2`.
* The caller is not the node: code `4`. A local caller that presents no
  identity is rewritten to the node's identity.

The claim contract passes the claim rule of
[`auth.sign_contract`](../../auth/ops/auth.sign_contract.md) before any
signature. A user the rule refuses is answered with an `error_message`, and the
node is unchanged. The rule refuses a user the node has had, even after its
contract has expired, and an identity the node minted.

The words never appear in a log line or a stored object. Words the caller sends
never appear in a reply. Generated words appear in one reply only, and the node
keeps no copy of them. A reply lost after a claim with `generate` leaves the node
owned by a user whose words exist nowhere.

Nothing changes on the node before the claim contract is validated. A failure
after the user's private key is stored leaves the node unclaimed and holding the
key; a repeat call with the same words completes the claim. The node keeps the
user's private key after the claim.

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

The query is rejected with code `2` or `4`, or without a code, in the cases
above. Otherwise the operation returns one of:
* A `mod.user.bootstrap_result` once the node is claimed. Its `Mnemonic` holds
  the generated words, and is empty when the caller sent the words.
* An `error_message` reading `invalid mnemonic` or
  `mnemonic must be 12, 15, 18, 21, or 24 words` if the words are not valid
  BIP-39 words.
* An `error_message` reading
  `claim refused: the claim rule of auth.sign_contract refuses this user` if the
  claim rule refuses the user.
* An `error_message` reading `user.bootstrap requires the bip137sig module` if
  the node runs without the `bip137sig` module.
* An `error_message` reading `the node has an active contract` if another
  claim completes after this query is accepted and before this claim.
* An `error_message` if the input is missing or is not a `string16`, or if word
  generation, signing or storage fails.

## Examples

```shellsession
$ astral-query user.bootstrap -generate true -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02a1...","Mnemonic":"penalty stadium garlic ... rifle fitness garage"}}
```

```shellsession
$ echo '{"Type":"string16","Object":"penalty stadium garlic ... rifle fitness garage"}' \
    | astral-query user.bootstrap -in json -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02a1...","Mnemonic":""}}
```
