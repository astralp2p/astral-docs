# user

The `user` protocol manages the identity of the user that owns this node, the
swarm of nodes operating under that user, and the user's asset list.

A node joins a user's swarm by holding a membership: a
[`mod.auth.signed_contract`](../auth/types/mod.auth.signed_contract.md) with one
tier permit (`member`, `trusted` or `privileged_member`), signed by its issuer
and by its subject, whose issuer may issue that tier
([SwarmState entries](#swarmstate-entries)). The swarm's members are the
identities whose membership holds there. Once a node has an active contract
it can serve information about the user (`user.info`), enumerate the swarm
(`user.swarm_status`, `user.list_siblings`), maintain a synchronised list of
user assets (`user.assets`, `user.add_asset`, `user.remove_asset`,
`user.sync_assets`, `user.sync_with`). `user.contract` answers the active
contract to any caller that holds a direct link to the node.

The user key signs every `privileged_member` membership in a ceremony.
`user.bootstrap` claims a node without an active contract in one call: it
derives the user's key from BIP-39 words, signs the node's privileged
membership for both parties, activates it and issues an access token for the
user. `user.accept_contract` activates a privileged membership already signed
by the user key and by this node (node setup and the cold-card path).
`user.derive_identity` answers the user that words derive and changes nothing.
`user.mnemonic` answers the words `user.bootstrap` stored, to the user or the
manager, for a later backup; `user.forget_mnemonic` deletes them.
[`user.join`](ops/user.join.md) makes a node without an active contract ask to
join through a `trusted` or `privileged_member` node, its carrier, with a join
request; the carrier writes it into SwarmState with
[`user.carry_join`](ops/user.carry_join.md) and signs the membership with the
joiner in that session ([Joins](#joins)). `user.introduce` pushes a claimed node's active
contract to a member of its user's swarm. Only the user expels: `user.expel`
needs `mod.user.expel_action`, signs the ban with the user key and adds it to
SwarmState; the list of bans is inspectable via `user.list_expelled`. Banned
nodes hold a `mod.user.signed_expulsion`.

The user module applies no admission policy. A join is signed by a carrier whose
tier may issue the tier asked for, and an app's permits are a request in
SwarmState that a node with the right tier answers with an offer
([SwarmState entries](#swarmstate-entries)).

A node emits a
[`mod.user.swarm_member_joined`](types/mod.user.swarm_member_joined.md) or
[`mod.user.swarm_member_left`](types/mod.user.swarm_member_left.md) event for
each node that enters or leaves its local swarm member set.

```yaml
reconcile_interval: 1h
sibling_sync_interval: 6h
sibling_sync_disabled: false
```

Two actions gate the protocol. `mod.user.see_swarm_action` covers every read
except `user.contract` — `user.info`, `user.assets`, `user.sync_assets`,
`user.list_siblings`, `user.swarm_status` and `user.list_expelled` — and
`user.new_node_contract` when `user` is omitted on a claimed node.
`user.contract` asks for no action and answers every directly linked caller.
`user.relay_contracts` and `user.relay_digest` ask for no action and answer only
the other members of the local swarm.
`mod.user.admin_swarm_action` covers every change to what the swarm holds —
`user.introduce`, `user.add_asset`, `user.remove_asset`, `user.sync_with`, which
applies another node's entries to this one, and `user.answer_request`.
`mod.user.expel_action` covers `user.expel`. The user holds every action; a
`privileged_member` node holds `mod.user.see_swarm_action` and
`mod.user.admin_swarm_action`, but not `mod.user.expel_action`, through the
swarm root ([auth, Authority in a swarm](../auth/README.md#authority-in-a-swarm)).
It uses them itself and cannot pass `mod.user.admin_swarm_action` or
`mod.user.expel_action` on: a contract carries either only when the user key
issued it.

Each time a node gains a link to a swarm member, inbound or outbound, it
synchronises with it, in this order: it pushes the active contract, the user's
expulsions and the membership contracts of the other members, pulls the
member's alias, pushes the relay contracts of the apps the swarm's members
host that the member lacks, and pulls the member's asset updates. Every new
link runs the synchronisation, not only the first link to the member. The alias and asset
pulls query the member as the user, and the member admits them only once it
holds this node's contract. A node also synchronises with a linked node when a
pushed membership contract admits that node to its local swarm, because the
link to that node preceded the contract. A node also synchronises with a
member when one of its links to the member closes and another link to the
member remains. A new link to a member makes the node probe its older links to
that member ([Link Mux, Keepalive](../../topics/link-mux.md#keepalive)), so a
dead older link closes within its ping timeout and the synchronisation runs
over a remaining link. The node runs one such synchronisation per member at a
time; closes during it start at most one more after it. The relay contracts
it pushes are those it holds that pass the admission rule of
[App Routing](../../topics/app-routing.md#reach), except those whose subject is
the member and except those the member holds. Before it pushes, the node asks
the member which relay contracts it holds with
[`user.relay_digest`](ops/user.relay_digest.md), as itself, within 10 seconds,
and skips each relay contract whose object ID the member lists. A node pushes
no relay contract when the member lists all of them. A relay contract the member
refused or never received is absent from its digest, so the node pushes it on
the next synchronisation. A digest that fails, whether by error, refusal,
unknown operation, an unfinished stream or the 10 seconds, leaves the node
pushing every relay contract it would push without a digest. The digest changes
no admission: the member admits each pushed relay contract by the same rule as
any other. A pushed app relay contract lets the member route a query addressed
to the app through the app's host. An app registered while the two nodes are
already linked reaches the member when it registers: the node pushes the
registered app's relay contract to every linked member at once, and pushes it
again to a member the push did not reach, up to 3 times, after 10 seconds, after
1 minute and after 5 minutes. A member's retries stop at its first answer,
whether the member accepts the contract or refuses it, when the member is no
longer a linked member, and when the node stops. A member that refuses the
contract receives it again from a later synchronisation, once its local swarm
lists the node.
A member that routes a query to an app whose relay contract it does not hold
asks its linked members for it with `user.relay_contracts`, once per miss
([App Routing, Resolving the host](../../topics/app-routing.md#resolving-the-host)).

A node synchronises with every linked member again every `sibling_sync_interval`
(`user.yaml`, default 6 hours), in the order and by the rules of a new link's
synchronisation, so a member that missed a relay contract for any reason holds it
within one interval. Each wait lasts the interval plus a random delay of up to
10 % of it. A zero `sibling_sync_interval` selects the default; a negative one,
or `sibling_sync_disabled: true`, turns the periodic synchronisation off. The
periodic synchronisation reaches linked members only. It starts one
synchronisation per linked member, concurrently, and skips a member whose
previous periodic synchronisation has not finished. A link-triggered
synchronisation with the member is unaffected and runs when its link event
fires.

A node wakes its link to a member of its local swarm when a
[`mod.nodes.endpoints_updated_event`](../nodes/types/mod.nodes.endpoints_updated_event.md)
names the member: a node that is not linked to the member dials at once instead
of waiting out the link's backoff of up to 15 minutes
([Endpoint exchange in the local swarm](../nodes/README.md#endpoint-exchange-in-the-local-swarm)).

A node redelivers the user's expulsions. Each time a node gains a link to a
node its user has expelled, it pushes the user's expulsions to that node, the
expelled node's own expulsion included, and synchronises nothing else with it.
Every `reconcile_interval` (`user.yaml`, default 1 hour) a node pushes the
user's expulsions to every linked swarm member and to every linked node its
user has expelled. A zero or negative `reconcile_interval` selects the default.
A node that receives an expulsion it already holds stores nothing new and closes
its links to the expelled node again. A node that receives its own expulsion
leaves the swarm: it stops maintaining its links to the members, closes them and
clears its active contract.

A node refuses links with a node its user has expelled once the expelled node
has answered a push of its own expulsion from this node, by accepting it or by
rejecting it ([Link admission](../nodes/README.md#link-admission)). Until that
answer the node admits the expelled node's links, so the expelled node can
receive its expulsion over them. When the answer arrives, the node closes its
links with the expelled node, and it neither dials the expelled node nor
accepts its connections again. The node keeps the answers in memory only: after
a restart it admits the expelled node until the expelled node answers again. A
node without an active contract refuses no node. On the node that issues the
expulsion, the answer ends the direct push of the expulsion to the expelled
node, so that push completes before the node closes its links with it.

A node contacts the nodes [`nearby`](../nearby/README.md) finds on the local
network only when the peer's `mod.nearby.peer_seen` names the node's own user.
It links at once to such a peer that is a member of its local swarm and is not
linked, instead of waiting out the link's backoff of up to 15 minutes. It
contacts any other such peer at most once a minute, and at most once an hour
after the peer's contract failed the check. A failed link or query holds the next
attempt for a minute only. The node keeps these limits for at most 512 peers; when
it holds 512, it forgets the peer whose next attempt comes first. It links to the peer at the
endpoints nearby resolves, reads the peer's contract with `user.contract`, and
checks it: a node contract issued by the node's user to the peer, both
signatures valid, not expired, and the peer not expelled. Only when the check
passes does the node introduce itself as `user.introduce` does: it pushes its
active contract, and the two synchronise. A failed check sends nothing of the
node's own. Unowned nodes and nodes of other users are listed, never contacted.
A `user.introduce` call is unaffected.

The active contract is validated on every application — the issuer's signature,
the subject's signature, subject identity match, remaining validity, and one
tier permit — so a stored value that fails validation never takes effect. A node
a carrier admitted stores the user identity beside it, since its membership's
issuer is the carrier.

## SwarmState entries

The `user` protocol defines the entry types of SwarmState, the signed record of
who belongs to a user's swarm and what its members asked for and were given.
The `user` module keeps each node's copy, checks every entry before it stores
it, and syncs it ([Synchronisation](#synchronisation)).
[`user.swarm_requests`](ops/user.swarm_requests.md) lists the stored requests
with their status, and [`user.answer_request`](ops/user.answer_request.md)
answers one with an approval, an offer or a decline signed by the node.
[`user.confirm_join`](ops/user.confirm_join.md) is the user's confirmation of a
join request at tier `privileged_member` when the user key is a software key
held on the node; it is accepted only from a local query by the user.

An entry is a signed object, stored as `swarmstate/<kind>/<object id>`, where
the kind is a [`mod.user.entry_kind`](types/mod.user.entry_kind.md):

| Kind | Entry | Signed by |
|------|-------|-----------|
| `requests` | [`mod.user.signed_contract_request`](types/mod.user.signed_contract_request.md) | the filing node |
| `requests` | [`mod.user.signed_join_request`](types/mod.user.signed_join_request.md) | the joining node |
| `requests` | [`mod.user.signed_expel_request`](types/mod.user.signed_expel_request.md) | the filing member |
| `approvals` | [`mod.user.signed_approval`](types/mod.user.signed_approval.md), of an expel request only | the answering member or the user key |
| `declines` | [`mod.user.signed_decline`](types/mod.user.signed_decline.md) | the answering member or the user key |
| `contracts` | [`mod.auth.signed_contract`](../auth/types/mod.auth.signed_contract.md): a membership, an app contract, or an offer | issuer and subject; an offer, the issuer only |
| `expels` | [`mod.user.signed_expulsion`](types/mod.user.signed_expulsion.md) | the user key |

An entry's ID is the object ID of the signed form exactly as stored, signatures
included. Every reference holds that ID: an answer's `RequestID` and a
contract's `RequestID`. It differs from the ID of the unsigned body, which the
signatures commit to. A half-signed contract and its completed form are two
entries with two IDs and one unsigned body, and the ID of that body matches
them to each other.

Each signed body's signable text is one ASCII line of at most 217 bytes, so
with the signer's 23-byte commitment it is at most 240 bytes and a Coldcard can
sign it ([coldcard](../coldcard/README.md)). A contract's text keeps that bound
whatever the contract holds: it names each action by a short word and ends its
list in a count of the actions it has no room to name
([`mod.auth.contract`](../auth/types/mod.auth.contract.md)).

### Requests and answers

A request stays answerable for at most 1 hour: its `Timeout` is after its
`FiledAt` and at most 1 hour after it, and a new request defaults to exactly 1
hour. Its status is a [`mod.user.request_status`](types/mod.user.request_status.md),
derived from the stored entries and never stored. Who may answer a request
depends on the answerer's [tier](types/mod.user.tier.md), as
[`mod.user.approval`](types/mod.user.approval.md) lists. The merge check decides
each offered entry with a
[`mod.user.entry_verdict`](types/mod.user.entry_verdict.md).

An answer is a reaction to a request and gives no authority to anything. What a
request yields is a contract, and the contract's authority is its own two
signatures ([Two signatures](#two-signatures)).

* A contract request is answered by an **offer**: a half-signed contract that
  names the request as its `RequestID` ([App grants](#app-grants)).
* An expel request is answered by an **approval**. The user key carries it out
  by signing a `mod.user.signed_expulsion`.
* A join request is answered by no entry. Its carrier signs the membership in
  the carrier session ([Joins](#joins)).
* Any request may be closed by a **decline**.

A decline only closes its request. The merge check drops every new offer for a
declined request, and the node a half-signed offer names as subject refuses to
co-sign a stored one; a carrier signs no membership for it. A decline takes
nothing back: a contract that both parties already signed keeps its authority,
and a signed expulsion stays. A contract is taken back only by expelling a
party in its chain, or when it expires. The swarm cannot revoke a single
contract, and an app contract lasts up to 3650 days, so a grant given in error
lasts until its host is expelled.

A request is `fulfilled` once a contract with both signatures names it. A
request that is `fulfilled` stays so whatever the answers that follow.

### Two signatures

A contract carries authority only when both its issuer and its subject signed
it. A contract with only the issuer's signature, an offer, is stored and passed
on but never counts: it makes no one a member, grants no permit, and adds no
link to a chain. A contract with a missing or invalid subject signature grants
nothing, wherever it is held, and every producer of a membership collects the
subject's signature: the carrier, the user key's ceremony, `user.bootstrap` and
`user.confirm_join`.

The authority of a contract is walked from the actor to the root through
issuers ([auth, Authority in a swarm](../auth/README.md#authority-in-a-swarm)).
A contract's `RequestID` only links it to the request it answers. It never adds
authority, and it never redirects the walk to the node that answered the
request.

The merge check applies the rule to each entry offered under `contracts`:

* A contract with both signatures valid is stored in these cases, and dropped
  in every other:
  * it is a membership, and its issuer is the user key, or a member, not
    expelled, whose current tier may issue the membership's tier
    ([Memberships](#memberships));
  * it names a stored contract request as its `RequestID`, and either its
    subject is the request's filer and its issuer may answer the request with
    permits no wider than the request's (the approver's contract to the host),
    or its issuer is the request's filer and its subject is the identity the
    request names (the host's contract to its app);
  * its issuer is the user key.
* A contract with only the issuer's signature is an offer. It is stored only
  when all of these hold; it waits while its request has not arrived, and is
  dropped when one of the others fails:
  * `RequestID` names a stored contract request, and the offer's subject is
    that request's `FiledBy`;
  * its permits are no wider than the request's: each permit has the action
    and constraints of one requested permit and a delegation depth exactly 1
    more than that permit's, and it carries no other permit;
  * its issuer may answer that request, and is not expelled;
  * the request has no stored decline.

An entry that fails these checks is neither stored nor passed on. A held entry
waits at most 1024 at once and is checked again after the next accepted merge.

### Memberships

A membership is a [`mod.auth.contract`](../auth/types/mod.auth.contract.md) by
which the issuer admits the subject at a [tier](types/mod.user.tier.md). There
is no separate membership wire type: SwarmState stores a membership as a
`mod.auth.signed_contract` in `contracts`.

A contract is a membership when it carries exactly one tier permit, one of
[`mod.user.member_action`](types/mod.user.member_action.md),
[`mod.user.trusted_action`](types/mod.user.trusted_action.md) and
[`mod.user.privileged_member_action`](types/mod.user.privileged_member_action.md);
that permit names its tier. A contract with no tier permit, or with more than
one, is not a membership. Reading a contract as a membership checks neither its
signatures, its expiry nor the user's expels.

A new membership carries that one tier permit, with no constraints and no
delegation, and an expiry. Its `RequestID` names the join request it answers,
or is `null` when the user key signs it directly. A membership holds only when
that tier permit is its only permit, with no constraints and no delegation: a
membership with any other permit grants nothing, not even its tier. The permit
puts the tier in the contract's signable text, so a Coldcard shows it, for
example:

```
<issuer> grants <subject> privileged_member depth 0 until 2027-11-25 10:00:00
```

**Who may issue which tier.** Tier permits cannot be delegated, so the chain of
contracts cannot say who may issue a membership. The merge check and the view
apply this table to the membership's issuer, read from its current membership:

| Issuer | May issue a membership at |
|--------|---------------------------|
| the user key | `member`, `trusted`, `privileged_member` |
| `privileged_member` | `member`, `trusted` |
| `trusted` | `member` |
| `member` | none |

A membership an issuer may not issue grants nothing and is dropped by the merge
check. A membership holds only while its issuer's own membership holds, and
expires with it at the latest.

A node holds one membership at a time as far as the swarm is concerned, though
it may have stored several, for example after joining again through another
carrier. The view reads the membership of the highest tier, and among those the
one that expires last. A tier is fixed when a node joins: there is no promotion.
A higher tier means joining through an issuer allowed to grant it, and
`privileged_member` comes only from the user key, signed in a ceremony with the
joiner present. A lower tier takes expelling the node and a new join.

### App grants

An app's permits come from the swarm through the app's host. The grant is two
contracts, each with both signatures:

```
host files ContractRequest{FiledBy: host, Identity: app, Permits: Q}
approver publishes offer Contract{Issuer: approver, Subject: host, Q with
                                  Delegation +1, RequestID}          IssuerSig
host adds SubjectSig to the offer for its own request              approver -> host
host signs Contract{Issuer: host, Subject: app, Q}; both keys are on the host
auth walks: app -> host -> approver -> root
```

* The approver answers a contract request with the offer, signed with its key
  and published into SwarmState as an ordinary entry. Its `Delegation` is one
  more than the request's, so that the host may pass the permits on. It expires
  3650 days after signing, or when its issuer's membership expires, if earlier;
  an offer the user key issues expires 3650 days after signing.
* **Who offers.** A member whose tier may answer the request offers with
  [`user.answer_request`](ops/user.answer_request.md), and the user key offers
  with the same operation, run as the user with `as` set to `user`. Several
  issuers may offer for one request, each once, while it is `pending` or
  `offered`. The host co-signs one of them, and an offer that arrives after the
  host co-signed stays unused.
* **The host is in every chain.** The expiry nests: the app's contract ends no
  later than the host's, and the host's no later than the approver's. Expelling
  the host, or the end of its membership, ends the app's grant as well. A grant
  issued straight from the approver to the app would leave the host out of the
  chain, and an expelled host would keep its apps' grants while it holds their
  keys; the protocol does not allow that.
* **Travel.** The offer is pushed to the host as every entry is pushed to linked
  members. The host is a member, so no other transport is needed. An offer that
  arrives before its request waits in the held set.
* **The host co-signs only what it asked for.** It adds its `SubjectSig` only
  when all of these hold:
  * the request is in the host's own records, not only in SwarmState;
  * the request is not declined, has not expired and is not superseded: the
    host has filed no later request for the same app with the same set of
    permits;
  * the offer is no wider than the request;
  * the permits go onward only to that app;
  * the offer's issuer may answer the request;
  * the host has not co-signed another offer for this request. When several
    offers qualify, the host takes the one the user key issued, then the one
    that expires last, then the one with the lowest entry ID.

  The host's consent is the request it signed, and the approver's decision is
  its signature, so co-signing needs no other decision. Whether a person
  confirms first is the host's policy, not part of the protocol.
* **Residual risk.** The host's contract from the approver carries a
  delegation depth of 1, and the depth limits how far a grant passes on, not
  whom it passes to. The host may sign the permits to any identity, including
  one outside the swarm, and need not publish that contract to SwarmState: a
  node's auth indexes a contract it receives from anywhere. A permit's
  constraints cannot narrow this, because an action evaluates them without
  knowing the contract it was reached through. The host already holds the
  app's key and acts as the app with these permits. What the protocol adds is
  that the host can pass them to identities that act without it, until the host
  is expelled or its contract expires. A swarm accepts this when it approves a
  request.
* **User powers do not pass through an app grant.** The host issues the app's
  contract, so the chain carries none of the four user powers
  ([auth, Authority in a swarm](../auth/README.md#authority-in-a-swarm)), even
  when the user key made the offer. An app that needs one of them holds a
  contract the user key issues to the app itself. This protocol defines no
  operation that requests such a contract.

### Joins

A joiner is not a member and cannot read SwarmState, so its membership cannot
travel to it for a second signature. It is signed while the joiner is
connected to its carrier:
[`user.carry_join`](ops/user.carry_join.md) runs four messages in one session.

1. The joiner sends its signed join request.
2. The carrier answers a membership with the issuer's signature: the carrier's
   own for a tier it may issue, or the user key's, signed in a ceremony, for
   `privileged_member`.
3. The joiner checks the membership against its request, signs it as subject,
   and sends it back.
4. The carrier stores the contract, with both signatures, in SwarmState and
   confirms it to the joiner: it answers the contract and the user identity.

The joiner activates the membership only after the confirmation. The membership's expiry is a function of the request and the
issuer's membership alone, never of the time of signing, so a joiner that
resends the same request after a dropped connection receives a membership with
the same body.

* The membership's issuer is the carrier, or the user key. It is checked against
  the table of who may issue which tier, so a Trusted carrier issues only
  `member`, a Privileged carrier `member` or `trusted`, and `privileged_member`
  is the user key's alone.
* The carrier signs without waiting for any entry in SwarmState: the join
  request, signed by the joiner, names it, and its tier decides what it may
  issue. It signs nothing for a request that is declined or has expired, or
  whose joiner is expelled.
* The membership's `RequestID` is the join request's entry ID.

### Synchronisation

Each node's copy of SwarmState lives in the node's own [VFS](../vfs/README.md),
owned by the node identity, under `swarmstate/<kind>/<object id>`. `/swarmhead`
holds the number of stored entries in decimal; it only grows and is never
synced. A merge is a union: nothing is overwritten or deleted. The merge check
([Two signatures](#two-signatures)) runs on every entry from every route, and
again on every stored entry when the node starts: an entry that fails it is left
out of the copy and never served.

Three operations exchange the set between nodes:

* [`user.swarm_digest`](ops/user.swarm_digest.md) answers the entry IDs this
  node stores;
* [`user.swarm_fetch`](ops/user.swarm_fetch.md) answers the stored entries
  among the IDs it receives;
* [`user.swarm_push`](ops/user.swarm_push.md) offers one entry.

`user.swarm_digest` and `user.swarm_fetch` serve this node, the user, and
every identity whose membership holds here. `user.swarm_push` serves every
identified caller, since the check decides what enters. A node pulls (digest,
then fetch of what it lacks, at most 256 IDs per fetch) from every linked swarm
member every 15 seconds. On a first link of a claimed node it first offers the
peer its own membership, so the peer admits its pull, and then pulls. When the
node stores its own membership, as at a claim, it does the same with every
peer it holds a link with. A node claimed while already linked therefore needs
no new link. Every entry this node stores is pushed to its linked swarm
members. Each member gets its own push, in the order the entries were stored,
and each push is bounded to 15 s. The write that stored the entries does not
wait for these pushes. A failed push is not retried: the member's pull repairs
it.

### Events

The module emits an event for each change of what the stored entries mean, as a
`mod.events.event` to the node's own receivers
([events](../events/README.md)). An event is a signal to read the entries
again, and a receiver acts on the current state, not on the event. Each node
emits an event for every valid entry it holds, and a receiver filters by the
subject it serves. A node emits nothing for the entries it already holds when
it starts.

| Event | Emitted when |
|-------|--------------|
| [`mod.user.swarm_request_filed`](types/mod.user.swarm_request_filed.md) | a valid request appears |
| [`mod.user.swarm_offer_added`](types/mod.user.swarm_offer_added.md) | a valid offer appears: its request is live and not declined, and its issuer is not expelled |
| [`mod.user.swarm_contract_added`](types/mod.user.swarm_contract_added.md) | a contract that counts appears: both signatures are valid |
| [`mod.user.swarm_request_approved`](types/mod.user.swarm_request_approved.md) | an expel request gets a counting approval |
| [`mod.user.swarm_request_declined`](types/mod.user.swarm_request_declined.md) | a request's status becomes `declined` |
| [`mod.user.swarm_request_expired`](types/mod.user.swarm_request_expired.md) | a request's status becomes `expired` |
| [`mod.user.swarm_node_banned`](types/mod.user.swarm_node_banned.md) | a valid expulsion of a node takes effect on this node |
| [`mod.user.swarm_member_joined`](types/mod.user.swarm_member_joined.md), [`mod.user.swarm_member_left`](types/mod.user.swarm_member_left.md) | the set of members changes |
