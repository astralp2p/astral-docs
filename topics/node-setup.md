# Node Setup

A [`Node`](../core-definitions/node.md) starts without a
[`User`](../core-definitions/user.md). Node setup claims the node for a `User`:
afterwards the node holds the user's private key and an active node contract
that the user issues to the node. Until then
[`user.info`](../protocols/user/ops/user.info.md) answers `no active contract`,
and the node logs `this node runs without a user` at startup.

Node setup runs in one call ([`user.bootstrap`](#one-call)) or
[step by step](#step-by-step). Both claim the node with the same contract and the
same rules. A node also joins an existing swarm from its own side
([`user.join`](#joining-a-swarm-from-the-new-node)).

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

* Setup runs on the node, from a local session.
* A session without a token reaches
  [`user.info`](../protocols/user/ops/user.info.md),
  [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md),
  [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md) and
  [`user.join`](../protocols/user/ops/user.join.md) while the node is unclaimed,
  and no other setup operation
  ([apphost, Sessions without a token](../protocols/apphost/README.md#sessions-without-a-token)).
  A local caller that presents no identity acts as the node.
* A session without a token also reaches `.spec`, before and after the claim.
  `.spec` lists the node's operations and changes nothing.
* A WebSocket session without a token reaches those operations only from a
  browser origin listed in `trusted_web_sources`. Any page open in a local
  browser reaches the WebSocket endpoint.
* The step-by-step operations run with the node's token: a token that
  `tokens:` in `apphost.yaml` maps to `localnode`. A session authenticated with
  it acts as the node.

```yaml
tokens:
  "<node token>": localnode
```

* `user.derive_identity`, `user.bootstrap`, `user.join` and
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
* Once the node is claimed, a session without a token reaches `user.info`,
  [`apphost.register`](../protocols/apphost/ops/apphost.register.md) and `.spec`
  only. Until
  [`apphost.set_app_register_policy`](../protocols/apphost/ops/apphost.set_app_register_policy.md)
  names a delegate, any local program that registers receives the permits it
  asks for.

## One call

[`user.bootstrap`](../protocols/user/ops/user.bootstrap.md) derives the key,
signs the claim contract as both parties, stores the key, activates the
contract and issues an access token for the user. It answers a
[`mod.user.bootstrap_result`](../protocols/user/types/mod.user.bootstrap_result.md).
The token authenticates the claiming app as the user.

[`user.derive_identity`](../protocols/user/ops/user.derive_identity.md) previews
the claim. It answers the identity that words derive, with the derivation of
`user.bootstrap`, and changes nothing on the node. A client takes the identity
from the node and derives no key itself.

New identity: the node generates 24 words, the user records them, and the same
words claim the node.

```shellsession
$ astral-query user.derive_identity -generate true -out json
{"Type":"mod.user.derive_identity_result","Object":{"Identity":"02e96bd9...","Mnemonic":"penalty stadium garlic ... rifle fitness garage"}}
$ echo '{"Type":"string16","Object":"penalty stadium garlic ... rifle fitness garage"}' \
    | astral-query user.bootstrap -in json -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02e96bd9...","Mnemonic":"","Token":"b9c2e1a3d4f5867a"}}
```

The generated words appear in the first reply only. `user.bootstrap -generate
true` generates the words and claims in one call; a reply lost after that claim
leaves the node owned by a user whose words exist nowhere.

Existing identity: the user's words preview the identity, and the same words
claim the node. The replies carry an empty `Mnemonic`.

```shellsession
$ echo '{"Type":"string16","Object":"horse soldier ... term change"}' > words.json
$ astral-query user.derive_identity -in json -out json < words.json
{"Type":"mod.user.derive_identity_result","Object":{"Identity":"02564ba7...","Mnemonic":""}}
$ astral-query user.bootstrap -in json -out json < words.json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02564ba7...","Mnemonic":"","Token":"b9c2e1a3d4f5867a"}}
```

## Step by step

Every step runs on a session authenticated with the node's token
([Who may set up a node](#who-may-set-up-a-node)). A session without a token is
refused steps 1 to 8.

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
$ export ASTRALD_APPHOST_TOKEN=<node token>
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

## Joining a swarm from the new node

A node of an existing swarm brings a new node under its user in one of two ways:

* The swarm node adopts the new node:
  [`user.adopt`](../protocols/user/ops/user.adopt.md) on the swarm node sends a
  membership contract to the new node's
  [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md).
  The new node calls `user.info` until the claim lands.
* The new node asks to join:
  [`user.join`](../protocols/user/ops/user.join.md) `-node <swarm node>` on the
  new node sends
  [`user.request_membership`](../protocols/user/ops/user.request_membership.md)
  to the swarm node, as the new node. The reply is the membership contract the
  new node now holds as its active contract.

```shellsession
$ astral-query user.join -node 03b1... -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```

The swarm node's join policy decides a request, and the new node's invite
policy decides an invitation. The new node's contract accept policy decides a
contract activated with `user.accept_contract`. All three accept everything by
default ([user](../protocols/user/README.md)).

## Refusals

| Answer | Cause | Remedy |
|--------|-------|--------|
| `user.info`: `no active contract` | The node has no active contract. | Run node setup. |
| `auth.sign_contract`: `sign as issuer: no signing scheme available for key secp256k1:<hex>: …` | The node does not hold the user's private key. | Store the key with `objects.store`, then sign again. |
| `auth.sign_contract`: `authorize issuer: cannot sign with another identity's key` | The claim rule refuses: the node has an active contract, the node minted the identity, or the node had this user before. | Use an identity derived from BIP-39 words, on an unclaimed node that never had this user. |
| `user.bootstrap`: `node already claimed` | The node has an active contract. | — |
| `user.bootstrap`: `query rejected (4)` | The caller is not the node. | Call from a local session without a token, or with the node's own token. |
| `user.bootstrap`: `claim refused: the claim rule of auth.sign_contract refuses this user` | The claim rule refuses the user. | As for `auth.sign_contract` above. |
| `user.bootstrap`: `invalid mnemonic` | The words fail the BIP-39 checksum. | Check the words. |
| any operation: `denied` | A session without a token sent an operation outside the active `anonymous_allowlist`, or a web page whose origin `trusted_web_sources` does not list sent one before the claim. | Authenticate with a token, or list the origin in `trusted_web_sources`. |
| `user.join`: `unknown identity`, `zero identity` or `cannot join self` | `node` does not resolve, resolves to the anonymous identity, or names this node. | Name a node of the swarm. |
| `user.join`: `request declined` | The swarm node's join policy declines the request. | Approve the request on the swarm node, or adopt the node from it. |
| `user.accept_contract`: `contract declined` | The node's contract accept policy declines the contract, or its delegate does not answer. | Approve the contract on the delegate, or clear the delegate with `user.set_contract_accept_policy`. |
