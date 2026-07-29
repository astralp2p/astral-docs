# Network Architecture

The *Astral Network* consists of different kinds of actors represented by [*Identities*](../core-definitions/identity.md), which communicate by sending each other [*Queries*](../core-definitions/query.md) and exchange data in the form of [*Objects*](../core-definitions/object.md).

An *Identity* might represent a [*User*](../core-definitions/user.md) or software ([*Nodes*](../core-definitions/node.md), [*Apps*](../core-definitions/app.md), *Agents*).

A *User* interacts with the network by signing *Contracts* with their secp256k1 keys. A *Contract* is a permission given by an *Identity* (the *Issuer*) to an *Identity* (the *Subject*) to represent the *Issuer* on the network in some capacity. The *User* signs a *Contract* with a *Node* to represent them on the network. *Apps* sign a *Contract* with their host *Node* to allow the *Node* to route traffic for them.

*Nodes* talk to each other over [*Links*](../core-definitions/link.md). A *Link* is a connection using the Astral Query Multiplexer protocol. *Links* can be established using the Noise XK protocol (which provides authentication and encryption) over any bidirectional bytestream. Default *Node* implementation supports several transports such as TCP, Tor, KCP (for post-NAT traversal UDP connections). *Links* are used to route *Queries* between the two *Nodes* as well as all traffic any *Contract* permits the *Nodes* to route.

*Nodes* form the backbone of the peer-to-peer Astral Network. They actively maintain and optimize links in order to route *Queries* as efficiently as possible.

The *Astral Network* is **not** a global broadcast network. By default, a *Node* does not attempt to link to any other *Node*. A *Node* will only try to link to other *Nodes*:

- after joining a [*Swarm*](../core-definitions/swarm.md) it will try to stay linked to other members of the *Swarm*
- when routing a query to or via another *Node*
- for other app-specific, explicitly defined reason

A *Swarm* is a group of *Nodes* and has rules that define who is allowed to join a *Swarm* and how the *Swarm* is managed internally. Each *Swarm* member enforces the rules of the *Swarm* independently while talking to other members. Some *Swarms* can be public, some might require a predefined key to sign memberships, some might define a more complex role system. Rules also specify how data is propagated through the *Swarm*, who has the right to publish, whether there is a persistent state members should maintain, etc. Real-life examples of *Swarms* are:

- all *Nodes* belonging to a single *User* (the subjective localswarm)
- *Nodes* wanting to buy/sell services (storage, xfer, apis) 
- social groups

*Nodes* keep an address book of other *Nodes* along with their endpoints - callable addresses in other networks (such as <IP>:<port> for TCP or UDP). *Nodes* help each other improve routability and discoverability by caching and propagating their endpoints explicitly marked as public.

*Apps* and *Agents* connect to the local *Node* (subjective *localnode*) via some form of RPC (unix, TCP, WebSocket) and use the *Node's* API to interact with the *Astral Network* or use services provided by the *Node*, such as storage, search, user sync, key management, data indexing, etc.

A *Query* is a singular call to an [*Op*](../core-definitions/op.md) from the *Caller* to the *Target* and can be rejected or accepted. An accepted *Query* results in a channel over which sides exchange data as *Objects* (or, in some cases, raw bytes).

A [*Zone*](../core-definitions/zone.md) — `device`, `virtual`, `network`, or a combination — accompanies a *Query* at each *Node* that routes it, and limits what that *Node* will do with it. A *Query* without the `network` zone is served only by the *Node* holding it, so a local app must authenticate (present an access token) to reach other *Nodes*. The *Zone* is not a field of the *Query* and does not travel with it: a *Node* receiving a *Query* over a *Link* routes it under all three zones.