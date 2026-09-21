# auth

The `auth` protocol manages capability grants between identities. An issuer
grants a subject a set of `mod.auth.permit`s in a `mod.auth.contract`,
co-signed by both parties as a `mod.auth.signed_contract`. The node indexes
such contracts and consults them, alongside locally registered handlers,
when authorizing typed actions (`mod.auth.action` and its concrete subtypes).

Two operations are exposed: `auth.sign_contract` co-signs a contract
presented on the stream using private keys held by the node, and `auth.index`
verifies a stored `mod.auth.signed_contract` and adds it to the local index.

## Actions

An action names a capability. A permit matches an action by object type, and
an operation submits its action before it acts.

* [`mod.auth.sudo_action`](types/mod.auth.sudo_action.md) – act as another identity
* [`mod.auth.see_objects_action`](types/mod.auth.see_objects_action.md) – read objects, their metadata, and the repository namespace
* [`mod.auth.store_objects_action`](types/mod.auth.store_objects_action.md) – write objects into the node, and change what it indexes
* [`mod.auth.serve_objects_action`](types/mod.auth.serve_objects_action.md) – stand in the node's answer path as a describer, finder, or searcher, or receive repository changes as an indexer
* [`mod.auth.admin_objects_action`](types/mod.auth.admin_objects_action.md) – change which repositories the node has
* [`mod.auth.admin_network_action`](types/mod.auth.admin_network_action.md) – read the node's network state, make it do network work, and control its links and listeners
* [`mod.auth.admin_manage_apps_action`](types/mod.auth.admin_manage_apps_action.md) – issue, list, and delete app access tokens and MCP agents
* [`mod.auth.configure_node_state_action`](types/mod.auth.configure_node_state_action.md) – change the node's tree and its identity aliases
* [`mod.auth.serve_apps_action`](types/mod.auth.serve_apps_action.md) – host an app handler and a service advertisement on the node
* [`mod.auth.see_node_state_action`](types/mod.auth.see_node_state_action.md) – read the node's tree, directory aliases and filters, agent metadata, and log stream
* [`mod.auth.use_gateway_action`](types/mod.auth.use_gateway_action.md) – register with the node's gateway, reserve a connection through it, and be forwarded by it

Six more are declared by the protocols that own them:
[`mod.user.see_swarm_action`](../user/types/mod.user.see_swarm_action.md) and
[`mod.user.admin_swarm_action`](../user/types/mod.user.admin_swarm_action.md)
in the [`user`](../user/README.md) protocol,
[`mod.nodes.relay_for_action`](../nodes/types/mod.nodes.relay_for_action.md) in
[`nodes`](../nodes/README.md),
[`mod.mcp.call_agent_action`](../mcp/types/mod.mcp.call_agent_action.md) and
[`mod.mcp.answer_agent_action`](../mcp/types/mod.mcp.answer_agent_action.md) in
[`mcp`](../mcp/README.md), and
[`mod.coldcard.scan_action`](../coldcard/types/mod.coldcard.scan_action.md) in
[`coldcard`](../coldcard/README.md).

Only `mod.auth.serve_objects_action` evaluates a permit's `Constraints` bundle.
Every other action refuses a permit carrying constraints rather than granting it
in full, because an action that does not evaluate a constraint is permitted
regardless of one.
