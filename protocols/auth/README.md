# auth

The `auth` protocol manages capability contracts between identities. An issuer
gives a subject a set of `mod.auth.permit`s in a `mod.auth.contract`,
co-signed by both parties as a `mod.auth.signed_contract`. The node indexes
such contracts and consults them, alongside locally registered handlers,
when authorizing typed actions (`mod.auth.action` and its concrete subtypes).

[`auth.sign_contract`](ops/auth.sign_contract.md) co-signs a contract
presented on the stream using private keys held by the node, for a local caller
that may sign as both of its parties, or the claim contract of node setup for
the node's own session while the node has no active contract. The node indexes every
validly signed `mod.auth.signed_contract` in its local repository itself; no
operation indexes a contract on request.

## Authorization

An operation submits its action, and the node answers it in this order. The
first step that answers decides.

1. **Veto.** An identity the node vetoes is refused at every level of the walk,
   whatever it holds.
2. **Swarm root.** The swarm root is the user identity, or this node's identity
   while the node has no user. The root, and a node holding a
   `privileged_member` membership the root signed and not expelled, hold every
   action except [`mod.user.expel_action`](../user/types/mod.user.expel_action.md)
   and [`mod.auth.sudo_action`](types/mod.auth.sudo_action.md). A
   `privileged_member` node relays only as the user. This step answers at any
   level of a contract chain.
3. **Handlers.** The handlers the modules register for the action's type, such
   as the user module's rules for the user and the node. A node-local handler
   answers only for the caller itself, never for a link of a chain.
4. **Contract chain.** The node looks up the contracts it has indexed whose
   subject is the actor and whose permits match the action, and walks up each
   one, asking the same steps again for the identity above it. Each link's
   permit must cover the delegation used below it and pass its constraints, so
   a chain only narrows. A contract that names an `ApprovalID` continues at the
   node that signed that [Approval](../user/types/mod.user.approval.md), not at
   its issuer, and holds only while SwarmState shows the request approved, the
   Approval answers a request the contract carries out, and neither its issuer,
   its subject nor the approver is expelled. A contract without an
   `ApprovalID` from an issuer other than the root carries none of the user's
   authority: no relay as the user, no
   [`mod.user.admin_swarm_action`](../user/types/mod.user.admin_swarm_action.md),
   no sudo as the user and no expel.
5. **External authorizer.** The authority assigned to the actor for the
   action, otherwise the action-wide one
   ([`auth.set_authorizer`](ops/auth.set_authorizer.md)).

The anonymous identity holds no action.

## Operations

* [`auth.sign_contract`](ops/auth.sign_contract.md) – co-sign a contract with keys the node holds
* [`auth.set_authorizer`](ops/auth.set_authorizer.md) – assign an external authorizer to an action
* [`auth.list_authorizers`](ops/auth.list_authorizers.md) – list the external authorizer assignments
* [`auth.remove_authorizer`](ops/auth.remove_authorizer.md) – remove an external authorizer assignment

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

Sixteen more are declared by the protocols that own them:
[`mod.user.see_swarm_action`](../user/types/mod.user.see_swarm_action.md),
[`mod.user.admin_swarm_action`](../user/types/mod.user.admin_swarm_action.md),
[`mod.user.expel_action`](../user/types/mod.user.expel_action.md) and the tier
actions [`mod.user.member_action`](../user/types/mod.user.member_action.md),
[`mod.user.trusted_action`](../user/types/mod.user.trusted_action.md) and
[`mod.user.privileged_member_action`](../user/types/mod.user.privileged_member_action.md)
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

## Types

* [`mod.auth.authorizer_assignment`](types/mod.auth.authorizer_assignment.md) – an external authorizer the node asks about one action
