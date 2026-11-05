# Node Setup

A new [`Node`](../core-definitions/node.md) belongs to nobody. Node setup gives
it an app that looks after it, the manager, and an owner, a
[`User`](../core-definitions/user.md). This page is the starting point: it
explains the whole path in plain words and links to the pages that hold the
details.

* [Node Policies](node-policies.md) – what is open in each state, and who
  decides what is let in.
* [User and Swarm](user-and-swarm.md) – what a user and a swarm are, and how a
  node is claimed or joins a swarm.

## In short

1. The node starts with its own identity and no user. It is `fresh`.
2. One local app asks to become the node's manager. The node appoints it and
   is now `unclaimed`.
3. The manager claims the node for a user: it creates a new user from 24 words,
   restores a user from words the user already has, or joins a swarm the user
   already runs. The node is now `claimed`.
4. From then on, the user's authorization and the node's policies decide who
   may do what. The manager keeps answering the policies it took on.

## A new node

The first start gives the node a key pair, and so an
[`Identity`](../core-definitions/identity.md) of its own. Nothing else is in
place: no user, no manager, no apps. The node can link to other nodes and can
host apps, but nobody speaks for it.

The node does not invent an owner. An owner is a person, and a person proves
ownership by holding a key the node cannot produce on its own. Until the user
signs a contract that names the node, the node only knows that it is waiting
for someone.

## Three states

A node is always in one of three states.
[`user.info`](../protocols/user/ops/user.info.md) reports the state and the
manager to any session the gate lets through.

```text
             appoint a manager                claim
   fresh  ─────────────────────►  unclaimed  ───────►  claimed
                                     ▲                    │
                                     └────────────────────┘
                                   contract expires or the
                                   user expels the node
```

* `fresh` – no manager, and no user has ever owned the node.
* `unclaimed` – no user owns the node right now, but it has a manager, or a
  user owned it before.
* `claimed` – a user owns the node: it holds an active contract the user
  signed.

A node never goes back to `fresh`. A node whose contract expired, or whose user
expelled it, is `unclaimed`, so the first local app that comes along cannot
make itself the manager of a node that already had an owner. The node records
at `/mod/user/config/owned` that it was owned, and expiry and expulsion do not
clear the record. Starting over means removing the node's data directory,
which also gives the node a new identity
([Node Exposure, Reset](node-exposure.md#reset)).

[apphost, Node states](../protocols/apphost/README.md#node-states) defines the
states.

## The manager

The manager is an [`App`](../core-definitions/app.md), for example the setup
or settings app a distribution ships. It exists because a node has to ask
someone before it lets anything in: which apps may register, which nodes may
join the user's swarm, which invitations to accept. Before a user owns the
node, nobody is there to ask. The manager is that someone.

### Appointing the manager

The app calls
[`apphost.register_manager`](../protocols/apphost/ops/apphost.register_manager.md)
on a `fresh` node, from a local session. It sends one
[`mod.apphost.register_manager_request`](../protocols/apphost/types/mod.apphost.register_manager_request.md):
the permits it asks for, as in
[`apphost.register`](../protocols/apphost/ops/apphost.register.md), and the
policies it takes on, one
[`mod.apphost.policy_binding`](../protocols/apphost/types/mod.apphost.policy_binding.md)
each. A binding names the policy, the operation the node asks on the manager,
and how long the node waits for one answer.

```shellsession
$ echo '{"Type":"mod.apphost.register_manager_request","Object":{"Name":"setup","GrantPermits":[],"ContractPermits":[],"Policies":[{"Policy":"app_register","Operation":"setup.approve_app","Timeout":0},{"Policy":"swarm_join","Operation":"setup.approve_join","Timeout":300000000000}]}}' \
    | astral-query apphost.register_manager -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef0...","Token":"k7m2q5x9r3v4n8p1","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

The node then:

1. checks the request: valid permits, known policy names, none named twice, an
   operation in every binding, and a timeout of at most 10 minutes;
2. creates the app identity as `apphost.register` does, without asking the app
   register policy, since no policy has anyone to ask yet;
3. stores each binding as the delegate of its policy, with the manager as the
   delegate, and clears the delegate of every policy the request does not
   name;
4. records the manager at `/mod/apphost/manager`, and answers the manager's
   access token.

The node is now `unclaimed`. If a step before 4 fails, the node stays `fresh`
and the app can try again. Of two apps that ask at once, one is appointed and
the other is answered `node is not fresh`.

The appointment is first come, first served. Any local program, or any page in
a local browser, can appoint itself the manager of a `fresh` node, so a
distribution appoints its manager before it starts anything else.

### What the manager may do

* Answer the policies it took on. The node asks the manager each time
  ([Node Policies](node-policies.md)).
* Change any policy, without holding
  [`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md).
* Claim the node for the user with its own token
  ([User and Swarm, Claiming a node](user-and-swarm.md#claiming-a-node)).

A node has at most one manager. No operation removes or replaces it, and the
claim keeps it. A policy the manager did not take on applies its configured
value: out of the box, a manager that takes on no policy leaves the node
refusing every app registration.

## Claiming

Claiming makes a user the node's owner. The user signs a contract that says
"this node acts for me", and the node signs it too. There are three ways in:

* **A new user.** The node generates 24 words, the user writes them down, and
  the same words claim the node.
* **An existing user.** The user types the words they already have.
* **An existing swarm.** The node asks a node the user already owns to take it
  in, or that node adopts this one. No words are typed on the new node.

The first two run as one call,
[`user.bootstrap`](../protocols/user/ops/user.bootstrap.md), which answers an
access token for the user. Whoever made the call, the manager in a
distribution, now holds the user's credential. A node claimed with words the
user already has holds its own contract alone. Nodes of the same user that
share a local network find and introduce each other through
[`nearby`](../protocols/nearby/README.md). Elsewhere,
[`user.introduce`](../protocols/user/ops/user.introduce.md) brings the node
into the user's running swarm
([User and Swarm, Replacing a node](user-and-swarm.md#replacing-a-node)).
[User and Swarm](user-and-swarm.md) explains what a user and a swarm are, and
shows each way with commands.

## What guards the node

Two things decide what reaches the node:

* **The gate** decides which operations are open at all, by whether the caller
  has a token and what state the node is in. A caller without a token only
  reaches the node itself, never an app on it, and only a few operations. A
  `fresh` node opens only the manager appointment and `user.info`.
* **The policies** decide when someone knocks: may this app register, may this
  node join the swarm, should this node accept that invitation. Each one
  accepts everything, refuses everything, or asks a delegate, usually the
  manager.

[Node Policies](node-policies.md) describes both, and
[Session Identity](session-identity.md) describes what a session is.

## Two kinds of node

The same node software serves two very different situations, and the
configuration chooses between them.

* **A distribution** – a phone, a desktop install, a device. The default
  configuration leaves one clear path: appoint the manager, then let the
  manager claim. A `fresh` node opens nothing else, and app registration, swarm
  joins and swarm invitations are refused until the manager takes them on.
* **A test or development node.** A test that only needs a claimed node should
  not have to bring up a manager first. Its configuration opens every
  operation on a `fresh` node, lets a session without a token claim, and sets
  every policy to accept everything.

[Node Policies, Distribution and test configuration](node-policies.md#distribution-and-test-configuration)
shows both configurations.

## After the claim

* Each operation checks whether the caller is authorized. The user and the
  user's other nodes are authorized for the swarm's own operations, such as
  `user.info`. Other identities need a grant or a contract.
* A caller without a token reaches only app registration, the manager
  appointment and `user.info`. The node is not `fresh`, so the appointment
  answers `node is not fresh`.
* The manager stays. It keeps answering the policies it took on, and it may
  still change them.
* The contract `user.bootstrap` signs expires after 365 days. An expired or
  expelled node is `unclaimed` again, and it can be claimed again
  ([User and Swarm, Losing the owner](user-and-swarm.md#losing-the-owner)).

[Node Exposure](node-exposure.md) lists every surface a node opens before and
after the claim.
