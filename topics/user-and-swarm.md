# User and Swarm

A [`User`](../core-definitions/user.md) owns nodes, and the nodes one user owns
form that user's [`Swarm`](../core-definitions/swarm.md). This page explains
both in plain words, then shows how a node gets its owner: claimed for a user
from the user's words, or taken into a swarm the user already runs.
[Node Setup](node-setup.md) explains the node states and the manager this page
relies on.

## What a user is

A user is a person, represented on the network by an
[`Identity`](../core-definitions/identity.md): a key derived from words the
person keeps. A user sends no queries itself. It acts through the nodes it
controls, and it proves that control by signing a
[`Contract`](../core-definitions/contract.md) with each node: the user is the
issuer, the node is the subject, and the contract says "this node acts for
me". A node holding such a contract, active and unexpired, is `claimed`, and
the issuer is its owner.

The node keeps the user's private key once claimed, so it can sign as the
user, for example when it brings another node into the swarm.

## What a swarm is

A swarm is a group of nodes that check each other's membership themselves.
The nodes one user owns form that user's swarm. From a node's point of view,
the swarm of its own user is its [`Local Swarm`](../core-definitions/local-swarm.md).

* A node is a member while it holds an active membership contract the user
  signed. The claim contract is one.
* When a node first links to another member, the two exchange the contracts
  that prove membership, the user's expulsions, the relay contracts of the
  apps each hosts, and the user's asset list. A node that is already linked
  to a node when that node's first membership contract reaches it
  synchronises with that node as well.
* The user and every member may read the swarm, for example with
  [`user.info`](../protocols/user/ops/user.info.md) and
  [`user.list_siblings`](../protocols/user/ops/user.list_siblings.md).
* The user may change the swarm: adopt a node, or expel one for good with
  [`user.expel`](../protocols/user/ops/user.expel.md).

[user](../protocols/user/README.md) describes the protocol.

## Claiming a node

Claiming makes a user the owner of a node that has none: afterwards the node
holds the user's private key and an active node contract that the user issues
to the node. The claim runs as [one call](#one-call), or
[step by step](#step-by-step) with the same contract and the same rules.

### The user key

* A `User` identity is a `secp256k1` key derived from BIP-39 words along the
  BIP-32 path `m/1791'/0'/0'/0/0`. A Coldcard derives its Astral key on the same
  path, so one set of words derives one `User` on a Coldcard and in software.
* The words are the user's backup. The node keeps no copy of them. A lost set of
  words cannot be recovered from the node.
* A BIP-39 passphrase is optional. The same words with another passphrase derive
  another `User`.
* The node keeps the user's private key after the claim. The node signs as the
  user with it, for example in
  [`user.adopt`](../protocols/user/ops/user.adopt.md).

### Who may claim

* The claim runs on the node, from a local session.
  [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md),
  [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md),
  [`user.join`](../protocols/user/ops/user.join.md) and
  [`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md) refuse
  a query of origin `network`, `mcp` or any other origin than local.
* `user.bootstrap` and `user.join` admit two callers: the node and the
  [manager](node-setup.md#the-manager). The manager calls with its App token. A session with
  the node's token acts as the node.
* The default gate admits the claim operations on an `unclaimed` node, to a
  session with a token. A `fresh` node appoints a manager first
  ([Node Policies](node-policies.md#the-gate)).
* The node's token is a token that `tokens:` in `apphost.yaml` maps to
  `localnode`.

```yaml
tokens:
  "<node token>": localnode
```

* The node signs the claim contract as itself, and only under the claim rule of
  [`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md). The
  rule refuses any contract once the node has an active contract. A node whose
  contract has expired or is cleared can be claimed again.

### One call

[`user.bootstrap`](../protocols/user/ops/user.bootstrap.md) derives the key,
signs the claim contract as both parties, stores the key, activates the
contract and issues an access token for the user. It answers a
[`mod.user.bootstrap_result`](../protocols/user/types/mod.user.bootstrap_result.md).
The token authenticates the claiming app as the user.

The commands below run under the manager's token, on an `unclaimed` node
([Node Setup, Appointing the manager](node-setup.md#appointing-the-manager)):

```shellsession
$ export ASTRALD_APPHOST_TOKEN=k7m2q5x9r3v4n8p1
```

[`user.derive_identity`](../protocols/user/ops/user.derive_identity.md)
previews the claim. It answers the identity that words derive, with the
derivation of `user.bootstrap`, and changes nothing on the node. A client takes
the identity from the node and derives no key itself.

New identity: the node generates 24 words, the user records them, and the same
words claim the node.

```shellsession
$ astral-query user.derive_identity -generate true -out json
{"Type":"mod.user.derive_identity_result","Object":{"Identity":"02e96bd9...","Mnemonic":"penalty stadium garlic ... rifle fitness garage"}}
$ echo '{"Type":"string16","Object":"penalty stadium garlic ... rifle fitness garage"}' \
    | astral-query user.bootstrap -in json -out json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02e96bd9...","Mnemonic":"","Token":"b9c2e1a3d4f5867a"}}
```

The generated words appear in the first reply only.
`user.bootstrap -generate true` generates the words and claims in one call; a
reply lost after that claim leaves the node owned by a user whose words exist
nowhere.

Existing identity: the user's words preview the identity, and the same words
claim the node. The replies carry an empty `Mnemonic`.

```shellsession
$ echo '{"Type":"string16","Object":"horse soldier ... term change"}' > words.json
$ astral-query user.derive_identity -in json -out json < words.json
{"Type":"mod.user.derive_identity_result","Object":{"Identity":"02564ba7...","Mnemonic":""}}
$ astral-query user.bootstrap -in json -out json < words.json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02564ba7...","Mnemonic":"","Token":"b9c2e1a3d4f5867a"}}
```

### Step by step

Every step runs on a session authenticated with the node's token
([Who may claim](#who-may-claim)). A session without a token is
refused steps 1 to 8. The default gate also refuses steps 1 to 8 to the node's
token, because the `fresh` and `unclaimed` lists name none of their
operations. A node set up step by step lists them in `gate.states` for its
state: `fresh` for a new node, and `unclaimed` for a node that has a manager
or held a contract before. A list `apphost.yaml` supplies replaces the default
list ([Node Policies](node-policies.md#the-gate)):

```yaml
gate:
  states:
    fresh: [.spec, apphost.register_manager, user.info, bip137sig.new_entropy, bip137sig.mnemonic, bip137sig.seed, bip137sig.derive_key, objects.store, crypto.public_key, user.new_node_contract, auth.sign_contract, user.accept_contract]
    unclaimed: [.spec, user.info, user.derive_identity, user.bootstrap, user.join, apphost.register, apphost.bind, apphost.register_handler, apphost.cancel, bip137sig.new_entropy, bip137sig.mnemonic, bip137sig.seed, bip137sig.derive_key, objects.store, crypto.public_key, user.new_node_contract, auth.sign_contract, user.accept_contract]
```

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

#### Ending input

[`objects.store`](../protocols/objects/ops/objects.store.md),
[`crypto.public_key`](../protocols/crypto/ops/crypto.public_key.md) and
[`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md) read their
input in batch mode. Each one needs `-eos` before the operation name. Without
`-eos` the command prints its result and does not exit
([`astral-query`, Ending input](../tools/astral-query.md#ending-input)). A
batch-mode result ends with an `eos` line, which the next single-mode op does not
read: `head -1` keeps the result alone.

## Joining a swarm

A node of an existing swarm brings a new node under its user in one of two ways:

* The swarm node adopts the new node:
  [`user.adopt`](../protocols/user/ops/user.adopt.md) on the swarm node sends
  a membership contract to the new node's
  [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md).
  The new node calls `user.info` until the claim lands.
* The new node asks to join:
  [`user.join`](../protocols/user/ops/user.join.md) `-node <swarm node>` on
  the new node sends
  [`user.request_membership`](../protocols/user/ops/user.request_membership.md)
  to the swarm node, as the new node. The reply is the membership contract the
  new node now holds as its active contract.

### The route between the nodes

Both ways need a route between the two nodes, and the swarm node provides it.
A node before the claim cannot add an endpoint itself: the default gate
refuses [`nodes.add_endpoint`](../protocols/nodes/ops/nodes.add_endpoint.md)
on an `unclaimed` node, to the manager's token and the node's token alike. A
new node that knows no route answers `user.join` with `route not found`.

* For an adoption, the swarm node learns the new node's endpoint with
  `nodes.add_endpoint`.
* For a join, the swarm node opens a link to the new node with
  [`nodes.new_link`](../protocols/nodes/ops/nodes.new_link.md), and the join
  travels over that link. An endpoint the swarm node knows does not give the
  new node a route back.

Both operations run on the swarm node under the user's token. The new node's
endpoint is its address and the TCP port its `tcp.yaml` listens on, 1791 by
default. Nodes of one user on a shared local network find each other through
[`nearby`](../protocols/nearby/README.md).

### Adopting from the swarm node

On the swarm node, under the user's token, with the new node `02f7...`
listening at `192.168.1.30:1791`:

```shellsession
$ astral-query nodes.add_endpoint -identity 02f7... -endpoint tcp:192.168.1.30:1791 -out json
{"Type":"ack","Object":null}
$ astral-query user.adopt -identity 02f7... -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```

### Joining from the new node

On the swarm node `03b1...`, under the user's token, open a link to the new
node:

```shellsession
$ astral-query nodes.new_link -identity 02f7... -endpoint tcp:192.168.1.30:1791 -out json
{"Type":"mod.nodes.link_info","Object":{...}}
```

Then on the new node, under the manager's token:

```shellsession
$ astral-query user.join -node 03b1... -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```

### Policies

The swarm node's join policy decides a request, and the new node's invite
policy decides an invitation. The new node's contract accept policy decides a
contract activated with `user.accept_contract`. The join and invite policies
decline everything by default, and the contract accept policy accepts every
contract that passes validation ([user](../protocols/user/README.md)).
[Policy Delegates](node-policies.md) describes how an approval app decides
them instead. A node set up from a shell has no approval app: the new node's
`user.yaml` sets `policies.swarm_invite: accept_all` before its start, and for
a join the swarm node's `user.yaml` sets `policies.swarm_join: accept_all`. An
adoption needs no join policy.

After the claim the user holds no token on the new node, and the manager's
token reads nothing of the swarm (`user.swarm_status` answers `not
permitted`). The user manages the new node from the swarm node with
`<node>:<operation>`, or creates a token on it with the node's token and
[`apphost.create_token`](../protocols/apphost/ops/apphost.create_token.md)
`-identity <user>`.

## Replacing a node

A node claimed with the user's words is a member of the user's swarm, but no
other member holds its contract yet, and it holds no other member's contract.
Neither side synchronises with the other, so the node stays alone until it is
introduced. This is the case when the node that held the user's words is lost
and a new node is claimed with the same words.

Nodes of the same user that share a local network find and introduce each
other through [`nearby`](../protocols/nearby/README.md), with no call. Each
node reads the other's contract with
[`user.contract`](../protocols/user/ops/user.contract.md), checks it, and then
introduces itself ([user](../protocols/user/README.md)). Where the nodes share
no local network, `user.introduce` introduces them.

[`user.introduce`](../protocols/user/ops/user.introduce.md) `-identity <member>`
on the new node pushes the new node's contract to one running member, and the
two synchronise. The member sends the contracts of the other members and the
user's expulsions. The new node then links to the other members and
synchronises with each of them.

The commands below run on the new node. The manager claims it with the user's
words, and the user's token from the claim adds an endpoint of a running
member `03b1...` and introduces the node to it:

```shellsession
$ export ASTRALD_APPHOST_TOKEN=k7m2q5x9r3v4n8p1
$ astral-query user.bootstrap -in json -out json < words.json
{"Type":"mod.user.bootstrap_result","Object":{"Identity":"02564ba7...","Mnemonic":"","Token":"b9c2e1a3d4f5867a"}}
$ export ASTRALD_APPHOST_TOKEN=b9c2e1a3d4f5867a
$ astral-query nodes.add_endpoint -identity 03b1... -endpoint tcp:192.168.1.20:1791 -out json
{"Type":"ack","Object":null}
$ astral-query user.introduce -identity 03b1... -out json
{"Type":"ack","Object":null}
```

The `ack` precedes the synchronisation. Once the synchronisations and links
complete, [`user.swarm_status`](../protocols/user/ops/user.swarm_status.md) on
the new node lists every member: the lost node `02a9...` among them, with no
alias and no link, while its contract is valid.

```shellsession
$ astral-query user.swarm_status -out json
{"Type":"mod.users.swarm_member","Object":{"Identity":"02a9...","Alias":"","Linked":false}}
{"Type":"mod.users.swarm_member","Object":{"Identity":"03b1...","Alias":"laptop","Linked":true}}
{"Type":"mod.users.swarm_member","Object":{"Identity":"02c7...","Alias":"phone","Linked":true}}
{"Type":"mod.users.swarm_member","Object":{"Identity":"03e4...","Alias":"new","Linked":false}}
{"Type":"eos","Object":""}
```

* The caller holds `mod.user.admin_swarm_action`: the user's token holds it,
  and so does the node's token on a node `user.bootstrap` claimed.
* The default gate admits `user.introduce` on a `claimed` node, to a session
  with a token.
* The member refuses the contract when another user owns it or when the user
  has expelled the new node.
* The lost node stays a member until its contract expires. `user.expel` on a
  running member bans it for good.

## Losing the owner

* The claim contract of `user.bootstrap` expires 365 days after the claim. A
  running node keeps an expired contract until it restarts.
* A user who expels a node bans it from the swarm for good. The node's active
  contract is cleared.

Either way the node is `unclaimed` again, never `fresh`: it keeps its manager,
its identity, its tokens and its grants. It can be claimed again, and the swarm
invite and contract accept policies decide again while it has no active
contract ([Node Policies](node-policies.md#before-the-claim)).

## Refusals

| Answer | Cause | Remedy |
|--------|-------|--------|
| `apphost.register_manager`: `node is not fresh` | The node has a manager, has an active contract, or has held one before. | On an `unclaimed` node, claim with the manager's token or the node's token. A `claimed` node needs no setup. |
| `auth.sign_contract`: `sign as issuer: no signing scheme available for key secp256k1:<hex>: …` | The node does not hold the user's private key. | Store the key with `objects.store`, then sign again. |
| `auth.sign_contract`: `authorize issuer: cannot sign with another identity's key` | The claim rule refuses: the node has an active contract, or the contract is not the claim contract `user.new_node_contract` writes. | Claim a node without an active contract with the contract `user.new_node_contract` writes. |
| `user.bootstrap`: `node already claimed` | The node has an active contract. | — |
| `user.bootstrap`: `not permitted` | The caller is neither the node nor the manager. | Call with the manager's App token, or with the node's own token. |
| `user.bootstrap`: `claim refused: the claim rule of auth.sign_contract refuses this user` | The node was claimed while the claim was signed. | — |
| `user.bootstrap`: `invalid mnemonic` | The words fail the BIP-39 checksum. | Check the words. |
| any operation: `denied` | The gate refuses the operation: a session without a token sent an operation outside `gate.tokenless`, or the list of the node's state in `gate.states` does not name it. | Authenticate with a token, or wait for the state that lists the operation ([Node Policies](node-policies.md#the-gate)). |
| `user.join`: `unknown identity`, `zero identity` or `cannot join self` | `node` does not resolve, resolves to the anonymous identity, or names this node. | Name a node of the swarm. |
| `user.introduce`: `cannot introduce to self` | `identity` names this node or the user. | Name a running member of the swarm. |
| `user.introduce`: `not permitted` | The caller does not hold `mod.user.admin_swarm_action`, or the user has expelled the caller. | Call with the user's token. |
| `user.introduce`: `push to <identity>: rejected` | The named node refuses the contract: it has no active contract, another user owns it, or the user has expelled this node. | Name a running member of the user's swarm. |
| `user.join`: `route not found` | The new node knows no route to the swarm node. | Open a link from the swarm node with `nodes.new_link`, or adopt the node from there ([The route between the nodes](#the-route-between-the-nodes)). |
| `user.join`: `request declined` | The swarm node's join policy declines the request. Its default, `reject_all`, declines every request. | Approve the request on the swarm node, set its `policies.swarm_join`, or adopt the node from it. |
| `user.join`: `invitation declined` | This node's invite policy declines the contract. Its default, `reject_all`, declines every invitation. | Bind `swarm_invite` to the manager, or set `policies.swarm_invite`. |
| `user.accept_contract`: `contract declined` | The node's contract accept policy declines the contract, or its delegate does not answer. | Approve the contract on the delegate, or clear the delegate with `user.set_contract_accept_policy`. |
