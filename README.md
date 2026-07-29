# The Astral Network

This documentation describes the Astral Network and how to interact with it.

These documents define abstract wire and protocol semantics — types, encodings, and operations are language-independent and carry no binding to any programming language.

Language SDKs implement this specification:

* [astral-go](https://github.com/astralp2p/astral-go) - the Go SDK; [astrald](https://github.com/astralp2p/astrald), the node daemon, builds on it
* [astral-py](https://github.com/astralp2p/astral-py) - the Python SDK
* [astral-js](https://github.com/astralp2p/astral-js) - the browser JavaScript SDK, with TypeScript typings

Contents:

* [Core primitives](core-definitions/README.md)
  * [Alias](core-definitions/alias.md)
  * [App](core-definitions/app.md)
  * [Bundle](core-definitions/bundle.md)
  * [Channel](core-definitions/channel.md)
  * [Contract](core-definitions/contract.md)
  * [Exonet](core-definitions/exonet.md)
  * [Identity](core-definitions/identity.md)
  * [Link](core-definitions/link.md)
  * [Local Swarm](core-definitions/local-swarm.md)
  * [Node](core-definitions/node.md)
  * [Object](core-definitions/object.md)
  * [Object ID](core-definitions/object-id.md)
  * [Object Stream](core-definitions/object-stream.md)
  * [Object Type](core-definitions/object-type.md)
  * [Op (Operation)](core-definitions/op.md)
  * [Permit](core-definitions/permit.md)
  * [Protocol](core-definitions/protocol.md)
  * [Query](core-definitions/query.md)
  * [Query String](core-definitions/query-string.md)
  * [Stamp](core-definitions/stamp.md)
  * [Structure](core-definitions/structure.md)
  * [Swarm](core-definitions/swarm.md)
  * [User](core-definitions/user.md)
  * [Zone](core-definitions/zone.md)
* [Common types](primitive-types/README.md) – common object types
  * [ack](primitive-types/ack.md)
  * [bool](primitive-types/bool.md)
  * [bytes8](primitive-types/bytes8.md)
  * [bytes16](primitive-types/bytes16.md)
  * [bytes32](primitive-types/bytes32.md)
  * [bytes64](primitive-types/bytes64.md)
  * [duration](primitive-types/duration.md)
  * [eos](primitive-types/eos.md)
  * [error_message](primitive-types/error_message.md)
  * [float32](primitive-types/float32.md)
  * [float64](primitive-types/float64.md)
  * [identity](primitive-types/identity.md)
  * [int8](primitive-types/int8.md)
  * [int16](primitive-types/int16.md)
  * [int32](primitive-types/int32.md)
  * [int64](primitive-types/int64.md)
  * [nonce64](primitive-types/nonce64.md)
  * [object](primitive-types/object.md)
  * [object_id.sha256](primitive-types/object_id.sha256.md)
  * [string8](primitive-types/string8.md)
  * [string16](primitive-types/string16.md)
  * [string32](primitive-types/string32.md)
  * [string64](primitive-types/string64.md)
  * [time](primitive-types/time.md)
  * [uint8](primitive-types/uint8.md)
  * [uint16](primitive-types/uint16.md)
  * [uint32](primitive-types/uint32.md)
  * [uint64](primitive-types/uint64.md)
  * [zone](primitive-types/zone.md)
* Protocols
  * [Basics](protocols/README.md) – protocol documentation structure
  * [apphost](protocols/apphost/README.md) - on-device API for local apps (tokens, handlers, contracts, holds)
  * [auth](protocols/auth/README.md) - capability contracts, signing, and action authorization
  * [bip137sig](protocols/bip137sig/README.md) - BIP-39/32/137 seed, key derivation, and message signing
  * [crypto](protocols/crypto/README.md) - signing and verifying hashes and text, public key derivation
  * [dir](protocols/dir/README.md) - alias management, identity resolution
  * [ether](protocols/ether/README.md) - LAN UDP broadcast for node presence and discovery
  * [lna](protocols/lna/README.md) - lightning network analytics
  * [nat](protocols/nat/README.md) - NAT traversal via UDP hole punching
  * [nodes](protocols/nodes/README.md) - encrypted links and multiplexed sessions between nodes
  * [objects](protocols/objects/README.md) - typed object storage, retrieval, and provider discovery
  * [player](protocols/player/README.md) - music playback and play queue control
  * [tor](protocols/tor/README.md) - onion-service transport over Tor
  * [tree](protocols/tree/README.md) - hierarchical key-value configuration store
  * [user](protocols/user/README.md) - user identity, swarm membership, asset list
  * [utp](protocols/utp/README.md) - uTP-over-UDP transport
* [Tools](tools/README.md) – command-line tools
  * [astral-query](tools/astral-query.md) - send queries from the command line
* Other topics
  * Narratives
    * [Network Architecture](topics/network-architecture.md) - how identities, nodes, links, swarms, and contracts compose at runtime
    * [Blueprints](topics/blueprints.md) - runtime wire-structure schemas that let a node encode and decode typed objects without compiled code
    * [Codec](topics/codec.md) - binary framing layer: type encoders, type tags, and the canonical form of typed objects
  * Wire mechanics
    * [Binary Encoding](topics/binary-encoding.md) - default payload encoding: big-endian, two's complement, payload bytes only
    * [JSON Encoding](topics/json-encoding.md) - optional JSON container encoding for typed objects
    * [Text Encoding](topics/text-encoding.md) - Base64-based text encoding of objects
    * [Op modes & composition](topics/op-modes.md) - single vs batch execution, and chaining single-mode ops into pipelines
  * Transports
    * [HTTP Transport](topics/http-transport.md) - request-response queries via the local node over HTTP
    * [WebSocket Transport](topics/ws-transport.md) - sending and receiving queries over the apphost WebSocket endpoint
    * [Astral IPC](topics/astral-ipc.md) - wire protocol for local processes routing queries through the node (mod/apphost)
    * [Link Multiplexer](topics/link-mux.md) - node-to-node link frames, sessions, and credit-based flow control
* Scripts – repo maintenance
    * [link-vocab.py](scripts/link-vocab.py) – link vocabulary terms at their first prose occurrence across docs