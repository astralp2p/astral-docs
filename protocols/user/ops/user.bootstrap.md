# user.bootstrap

Claim this unclaimed node for a user in one call. The user's key is derived
from BIP-39 words along the path `m/1791'/0'/0'/0/0`, the path a Coldcard
derives its Astral key on. The words arrive in the input stream, or the node
generates 24 words when `generate` is set. The node signs the claim contract as
the user, with the derived key held in memory, and as itself. The node then
validates the contract, stores and indexes the user's private key, stores the
contract, and sets the contract as the active contract. Last, the node issues
an access token for the user. The reply is a
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

The node refuses the query in these cases, in this order:

* The query's origin is `network`, `mcp` or any origin other than local:
  answered with an `error_message` reading `origin not allowed: <origin>`.
* The node has an active contract: answered with an `error_message` reading
  `node already claimed`.
* The caller is not the node: answered with `not permitted`. A local caller
  that presents no identity is rewritten to the node's identity.

The claim contract passes the claim rule of
[`auth.sign_contract`](../../auth/ops/auth.sign_contract.md) before any
signature. A user the rule refuses is answered with an `error_message`, and the
node is unchanged. A user the node has had re-claims it with the same words once
its contract has expired or is cleared.

The words never appear in a log line or a stored object. Words the caller sends
never appear in a reply. Generated words appear in one reply only, and the node
keeps no copy of them. A reply lost after a claim with `generate` leaves the node
owned by a user whose words exist nowhere. A client that confirms the user's
backup before the claim generates the words with
[`user.derive_identity`](user.derive_identity.md) and sends them here.

The access token authenticates an [apphost](../../apphost/README.md) session as
the user, and expires 365 days after the call. The token is the claiming app's
credential as the user: once the node is claimed, a session without a token
reaches only the operations on the claimed list of apphost's
`anonymous_allowlist`.

Nothing changes on the node before the claim contract is validated. A failure
after the user's private key is stored leaves the node unclaimed and holding the
key; a repeat call with the same words completes the claim. The node keeps the
user's private key after the claim. A failure to issue the access token leaves
the node claimed.

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

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns one of:
* A `mod.user.bootstrap_result` once the node is claimed. Its `Mnemonic` holds
  the generated words, and is empty when the caller sent the words. Its `Token`
  holds the user's access token.
* An `error_message` reading `invalid mnemonic` or
  `mnemonic must be 12, 15, 18, 21, or 24 words` if the words are not valid
  BIP-39 words.
* An `error_message` reading
  `claim refused: the claim rule of auth.sign_contract refuses this user` if the
  claim rule refuses the user.
* An `error_message` reading `user key derivation requires the bip137sig module`
  if the node runs without the `bip137sig` module.
* An `error_message` reading `the node has an active contract` if another
  claim completes after this query is accepted and before this claim.
* An `error_message` if the input is missing or is not a `string16`, or if word
  generation, signing or storage fails.
* An `error_message` if the access token cannot be issued. The node is claimed.

## Examples

```shellsession
$ astral-query user.bootstrap -generate true -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02a1...","Mnemonic":"penalty stadium garlic ... rifle fitness garage","Token":"b9c2e1a3d4f5867a"}}
```

```shellsession
$ echo '{"Type":"string16","Object":"penalty stadium garlic ... rifle fitness garage"}' \
    | astral-query user.bootstrap -in json -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02a1...","Mnemonic":"","Token":"b9c2e1a3d4f5867a"}}
```
