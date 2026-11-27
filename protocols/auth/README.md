# auth

The `auth` protocol manages capability grants between identities. An issuer
grants a subject a set of `mod.auth.permit`s in a `mod.auth.contract`,
co-signed by both parties as a `mod.auth.signed_contract`. The node indexes
such contracts and consults them, alongside locally registered handlers,
when authorizing typed actions (`mod.auth.action` and its concrete subtypes).

[`auth.sign_contract`](ops/auth.sign_contract.md) co-signs a contract
presented on the stream using private keys held by the node, for a local caller
that may sign as both of its parties, or the claim contract of node setup for
the node's own session while the node has no active contract. The node indexes every
validly signed `mod.auth.signed_contract` in its local repository itself; no
operation indexes a contract on request.

## Authority in a swarm

On a node with a swarm, a contract carries authority only when both its issuer
and its subject signed it. A contract with a missing or invalid signature of
either grants nothing, whatever its permits say, and a contract with the
issuer's signature alone, an offer in
[SwarmState](../user/README.md#swarmstate-entries), never counts.

The node authorizes an action for an actor by walking contracts from the actor
to the root:

* The walk starts at the actor and takes a contract whose subject is the hop's
  identity, that has both signatures, has not expired, and whose permit matches
  the action and accepts its constraints.
* It continues at the contract's **issuer**: the issuer must hold the permit in
  turn, through a contract it received, until the walk reaches the root. The
  walk never continues at the node that answered a request. A contract's
  `RequestID` only links the contract to the request it answers; it adds no
  authority and redirects nothing.
* Each hop that passes a permit on needs a `Delegation` of at least 1 on the
  contract that gave it, which a further hop reduces by 1. Constraints only
  narrow along the walk.
* A walk stops at a party that is expelled, and at a contract that has expired.
  The expiry of a chain is the earliest expiry in it, and so expelling or
  expiring a party ends everything that passes through it.

**The root.** The root is the user key. A node that holds a
`privileged_member` membership the user key issued answers as the root wherever
the walk reaches it, for every action but the four user powers below, and so
does an unclaimed node for itself. A grant from such a node therefore has the
standing of the user's own authority.

**User powers.** Four things belong to the user: expelling
([`mod.user.expel_action`](../user/types/mod.user.expel_action.md)), administering
the swarm
([`mod.user.admin_swarm_action`](../user/types/mod.user.admin_swarm_action.md)),
relaying as the user
([`mod.nodes.relay_for_action`](../nodes/types/mod.nodes.relay_for_action.md)
with the user as `ForID`) and acting as the user
([`mod.auth.sudo_action`](types/mod.auth.sudo_action.md) with the user as
`AsID`). A contract grants any of them only when its issuer is the user key
itself. A Privileged member answers swarm administration and relaying as the
user only when it is the actor itself, and never passes them on: a contract it
issues carries none of the four, so an app that reaches the root through a
Privileged member holds none of them. The membership of a Privileged member
covers neither expelling nor acting as the user: expelling always needs the
user key, in a ceremony, and acting as the user needs a contract the user key
issued. An app grant passes through the app's host,
which issues the app's contract, so it carries none of the four, even from an
offer the user key made. An app that needs one of the four holds it through a
contract the user key issues to the app itself.

**App grants** are two contracts: the approver's to the app's host, whose
permits each have a `Delegation` exactly one more than the requested permit's,
then the host's to the app. The walk from the app passes the
host, then the approver, then the root, so the host is in every chain
([user, App grants](../user/README.md#app-grants)).

## Actions

An action names a capability. A permit matches an action by object type, and
an operation submits its action before it acts.

* [`mod.auth.sudo_action`](types/mod.auth.sudo_action.md) – act as another identity
* [`mod.auth.see_objects_action`](types/mod.auth.see_objects_action.md) – read objects, their metadata, and the repository namespace
* [`mod.auth.store_objects_action`](types/mod.auth.store_objects_action.md) – write objects into the node, and change what it indexes
* [`mod.auth.serve_objects_action`](types/mod.auth.serve_objects_action.md) – stand in the node's answer path as a describer, finder, or searcher, or receive repository changes as an indexer
* [`mod.auth.admin_objects_action`](types/mod.auth.admin_objects_action.md) – change which repositories the node has
* [`mod.auth.admin_network_action`](types/mod.auth.admin_network_action.md) – read the node's network state, make it do network work, and control its links and listeners
* [`mod.auth.admin_manage_apps_action`](types/mod.auth.admin_manage_apps_action.md) – issue, list, and delete app access tokens and MCP agents, and create and delete messaging participants
* [`mod.auth.configure_node_state_action`](types/mod.auth.configure_node_state_action.md) – change the node's tree and its identity aliases
* [`mod.auth.serve_apps_action`](types/mod.auth.serve_apps_action.md) – host an app handler and a service advertisement on the node
* [`mod.auth.register_signer_action`](types/mod.auth.register_signer_action.md) – claim a key on a [`crypto.register_signer`](../crypto/ops/crypto.register_signer.md) binding
* [`mod.auth.see_node_state_action`](types/mod.auth.see_node_state_action.md) – read the node's tree, directory aliases and filters, agent and participant metadata, and log stream
* [`mod.auth.use_gateway_action`](types/mod.auth.use_gateway_action.md) – register with the node's gateway, reserve a connection through it, and be forwarded by it
* [`mod.auth.use_blueprints_action`](types/mod.auth.use_blueprints_action.md) – read and register the node's blueprints

Twelve more are declared by the protocols that own them:
[`mod.user.see_swarm_action`](../user/types/mod.user.see_swarm_action.md) and
[`mod.user.admin_swarm_action`](../user/types/mod.user.admin_swarm_action.md)
in the [`user`](../user/README.md) protocol,
[`mod.nodes.relay_for_action`](../nodes/types/mod.nodes.relay_for_action.md) in
[`nodes`](../nodes/README.md),
[`mod.messaging.send_action`](../messaging/types/mod.messaging.send_action.md),
[`mod.messaging.receive_action`](../messaging/types/mod.messaging.receive_action.md),
[`mod.messaging.host_mailbox_action`](../messaging/types/mod.messaging.host_mailbox_action.md)
and
[`mod.messaging.read_mailbox_action`](../messaging/types/mod.messaging.read_mailbox_action.md)
in [`messaging`](../messaging/README.md),
[`mod.services.service_discovery_action`](../services/types/mod.services.service_discovery_action.md)
in [`services`](../services/README.md),
[`mod.shell.shell_action`](../shell/types/mod.shell.shell_action.md) in
[`shell`](../shell/README.md), and
[`mod.vfs.read_action`](../vfs/types/mod.vfs.read_action.md),
[`mod.vfs.write_action`](../vfs/types/mod.vfs.write_action.md) and
[`mod.vfs.manage_action`](../vfs/types/mod.vfs.manage_action.md) in
[`vfs`](../vfs/README.md).

Only `mod.auth.serve_objects_action`,
`mod.services.service_discovery_action`, `mod.vfs.read_action` and
`mod.vfs.write_action` evaluate a permit's `Constraints` bundle.
`mod.vfs.read_action` and `mod.vfs.write_action` read a bundle of `identity`
objects and cover exactly the VFSes it lists; a permit without constraints
covers none.
Every other action except `mod.auth.sudo_action` and `mod.shell.shell_action`
refuses a permit carrying constraints rather than granting it in full, because
an action that does not evaluate a constraint is permitted regardless of one.

[`mod.auth.sudo_action`](types/mod.auth.sudo_action.md) is the exception: a sudo
permit is always unconstrained. The action does not evaluate constraints, so a
sudo permit grants the full authority of the identity it names whatever
`Constraints` it carries, and an expiry or delegation limit on it does not narrow
what the holder may do as that identity.

[`mod.shell.shell_action`](../shell/types/mod.shell.shell_action.md) is the
other exception: a shell permit is always unconstrained. The action does not
evaluate constraints, so a shell permit admits its holder to a full session
whatever `Constraints` it carries.

[`mod.messaging.read_mailbox_action`](../messaging/types/mod.messaging.read_mailbox_action.md)
refuses every permit, constrained or not, so no contract carries it: only a
handler or the external authority asked about the actor itself grants it.
