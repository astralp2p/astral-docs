# inference

The `inference` protocol lets a client ask an astral node to generate text — or
anything a model can produce from text, images, audio and video — and to learn
first what models are on offer and what they cost to run. An answer streams
back with the model's thinking kept apart, and with the tool calls a model makes
when the client offers it tools, so an agent can run its tool loop over astral.

The provider on the far side speaks an OpenAI-compatible API. The near side is
astral-native: an app advertises a service, a caller discovers it, and one
channel carries a request and its streamed answer.

This is version 2 of the protocol, and every type below is version 2's. Version
1 is withdrawn; [Version 2](#version-2) says why it was replaced under the same
names and what that asks of a running node.

## Design notes

* **Discovery is the inventory.** A provider advertises itself as the
  [`services`](../services/README.md) service named `inference`. Its offering's
  `Info` bundle carries three objects:
  * an [`inference.models`](types/inference.models.md), so a caller learns the
    model list, each model's context window, output ceiling, supported
    modalities, effort levels and tool support in the same round trip that
    finds the provider;
  * an [`inference.provider`](types/inference.provider.md), the name its
    operator gave it, so a caller can show a name rather than an identity;
  * a [`services.operations_list`](../services/types/services.operations_list.md)
    naming `inference.models` and `inference.complete`.

  There is no second call to make before the first one.
  [`inference.models`](ops/inference.models.md) exists for a caller that already
  knows a provider and wants the inventory again, or a fresher one. A provider
  whose inventory or admissions change sends
  [`services.change`](../services/types/services.change.md), so a caller that
  follows discovery receives the new offering without asking.

* **The offering is per caller.** A provider evaluates each caller on its own,
  exactly as [`services`](../../topics/services.md) defines an offering. A caller
  the provider will not serve is shown no offering at all — not an empty one —
  and a caller it will serve sees only the models it may use. An inventory is
  therefore never global, and a client must not cache one across callers.

* **Everything is gated on the caller's identity.** Authorization reads the
  caller of the incoming query, never anything the caller says about itself. By
  default the local User identity and the local node identity are allowed; every
  other caller needs an explicit allowance (`-allow` in astral-inference, the
  reference provider). A caller asks its own node, so the identity the provider
  sees is the one the node authenticated, whether the query came from a local
  app, the CLI, or across a [`Link`](../../core-definitions/link.md).

* **Apps of the user's swarm are admitted only by choice.** The User's apps run
  on many nodes, each under an identity of its own that no operator can list
  ahead of time. A provider may admit them by where they run instead
  (astral-inference: `-admit swarm-apps`). For a caller that is an app, the
  provider asks its own node [`apphost.hosts`](../apphost/ops/apphost.hosts.md)
  `-app <caller>`, and admits the caller when one of the hosts is the provider's
  own node or a member of that node's user swarm
  ([`user.swarm_status`](../user/ops/user.swarm_status.md)). Both queries need
  [`mod.user.see_swarm_action`](../user/types/mod.user.see_swarm_action.md),
  which the provider asks for when it registers. A remote app's hosts are known
  to the provider's node once the app's relay contract reached it, which the
  app's own swarm discovery brings about.

  The rule is off unless the operator turns it on. A node's default register
  policy makes any local program an app, so the rule admits every program on
  every node of the user's swarm. A caller outside the swarm still needs an
  explicit allowance.

* **Effort is a first-class field, not a passthrough.** A model lists the effort
  levels it honours — `off`, `low`, `medium`, `high`, or provider-defined
  names — each with a description and an optional token budget, and names the
  one it uses when a request names none. `off` means the model does not think.
  The consumer chooses between named levels; how the provider realises one on
  its far side (a reasoning-effort parameter, a server's own request fields, a
  token cap, or nothing at all) is its business. A passthrough of one vendor's
  parameter would leak that vendor into the protocol and mean nothing to a
  caller facing a different far side.

* **Tools are astral types, not a vendor's JSON.** A request describes each
  function the model may call as an [`inference.tool`](types/inference.tool.md).
  The model's calls stream back as
  [`inference.tool_call_delta`](types/inference.tool_call_delta.md) pieces of
  each chunk, and return in the history as
  [`inference.tool_call`](types/inference.tool_call.md) objects on the assistant
  turn, each answered by a `tool` turn that names it. Only two values stay JSON
  text: a tool's parameter schema, which is JSON Schema — a standard, not a
  vendor's format — and the arguments the model wrote, which are only as well
  formed as the model made them.

* **Media is referenced, not re-sent.** A content part carries media in one of
  three ways. *Inline* bytes suit a picture the client already holds. *Object*
  names an [`object_id.sha256`](../../core-definitions/object-id.md) the
  network already addresses, and the provider reads it once through
  [`objects.read`](../objects/ops/objects.read.md) — so a caller that has the
  media on the network never uploads it again, and a provider can serve the same
  asset to many callers from one copy. *URL* names an address the provider is
  allowed to fetch itself. This is what makes multimodal calls reasonable on a
  network where a byte that is addressable need not be transported twice.

* **Text and media are not capped at 64 KiB.** Every text a request or chunk
  carries is a [`string32`](../../primitive-types/string32.md) and inline media
  a [`bytes32`](../../primitive-types/bytes32.md). An agent's conversation holds
  whole files, long tool results and screenshots, and a `string16` would refuse
  them at the sender. A decoder may still bound what one object costs it
  ([Codec § Decoding limits](../../topics/codec.md#decoding-limits)), and a
  provider may bound the media it takes.

* **Errors say what to do next.** Both operations report a refusal or a failure
  as an [`inference.error`](types/inference.error.md): a Kind that tells a
  refusal from a bad request, an overflowing context, a rate limit, an
  unavailable server and a failed one, with the server's HTTP status, its
  message word for word and how long to wait. A bare string would leave the
  consumer only one move: give up.

* **Streaming is the default.** [`inference.complete`](ops/inference.complete.md)
  is a channel operation: the caller sends one request and reads
  [`inference.chunk`](types/inference.chunk.md) deltas in `Index` order, then an
  [`inference.usage`](types/inference.usage.md) when the far side reported one,
  then `eos`. A chunk with a non-empty `FinishReason` is the last of the answer,
  and a failure is an `inference.error`, then `eos`. The
  [stream rules](ops/inference.complete.md#stream-rules) give the whole
  contract. Per [op modes](../../topics/op-modes.md), a client never blocks
  waiting for `eos`: EOF is a legitimate end of any response.

* **Closing the channel cancels the work.** A caller that closes its channel
  cancels the request at once: the provider cancels it on its far side and
  releases the connection, while the server is still reading the prompt as much
  as while the answer streams. There is no separate cancel operation.

## Discovery

```shellsession
$ astral-query services.discover -services inference -out json
{"Type":"services.update","Object":{"Available":true,"Name":"inference","ProviderID":"02c00992…","Info":[{"Type":"inference.models","Object":{"Models":[{"ID":"atlas-32b","DisplayName":"Atlas 32B","ContextWindow":131072,"MaxOutput":8192,"Modalities":["text","image"],"EffortLevels":[{"Name":"off","Description":"answer without thinking","TokenBudget":0},{"Name":"low","Description":"think briefly","TokenBudget":1024}],"Streams":true,"Description":"","DefaultEffort":"low","Tools":true}]}},{"Type":"inference.provider","Object":{"Name":"ai0","Description":"the GPU box in the office"}},{"Type":"services.operations_list","Object":{"Operations":["inference.models","inference.complete"]}}]}}
{"Type":"eos","Object":null}
```

A caller that is not allowed sees no offering from that provider. A provider
that serves several callers differently shows each of them a different
inventory.

## Version 2

Version 1 of this protocol is withdrawn. Its types had the names listed below
and other shapes; it could not carry tool calls, typed errors, or text and media
past 64 KiB. Nothing answers a version 1 request any more.

### Same names, new shapes

[Blueprints § Versioning](../../topics/blueprints.md#versioning) makes a
registered blueprint final, and gives a changed shape a new `.vN` name. Version
2 departs from that rule on purpose: its types keep version 1's names. The rule
protects two things, and neither exists here:

* **Objects already written.** Inference objects are never stored. They live on
  a completion's channel or in a discovery offering and end with them, so no
  stored bytes depend on the version 1 shapes.
* **Peers that still speak the old shape.** No version 1 provider or consumer is
  deployed. The one implementation moved to version 2 whole, its CLI included.

A `.v2` suffix would have stayed on every type for good, for a version nobody
runs.

### Cutover

A node holds the shapes it was given until it stops. astrald keeps pushed
blueprints in memory and never replaces a name it holds:

* an app's blueprint sync (astral-go `apps.SyncBlueprints`) skips every name the
  node already lists;
* [`objects.register_blueprint`](../objects/ops/objects.register_blueprint.md)
  answers "blueprint already registered" whether the shapes match or not.

A node that loaded the version 1 shapes since it started therefore decodes
version 2 objects with them. Fields go missing or the stream breaks, and no
error names the cause. **Restart every node that has run a version 1 provider
or consumer since it started.**

### Blueprint guard

Every provider and consumer guards against a node that missed the restart.
After pushing its blueprints, on each connection to its node, it compares each
`inference.*` blueprint the node holds with its own by
[`Object ID`](../../core-definitions/object-id.md): it fetches the node's with
[`objects.get_blueprint`](../objects/ops/objects.get_blueprint.md)
`-type <name>`, which needs
[`mod.auth.see_objects_action`](../auth/types/mod.auth.see_objects_action.md),
and compares the Object ID of its canonical form with that of its own. On a
mismatch it stops, serving and sending nothing, with:

```text
node {id} holds an older {type}; restart the node
```

`{id}` is the node's identity and `{type}` the type whose shapes differ. One
query per type turns a silent corruption into a failure that names its cure.

## Operations

* [inference.models](ops/inference.models.md) – the caller's inventory, again
* [inference.complete](ops/inference.complete.md) – run one completion, streaming

## Types

* [inference.model](types/inference.model.md) – one model and its capabilities
* [inference.models](types/inference.models.md) – an inventory
* [inference.effort_level](types/inference.effort_level.md) – one settable effort
* [inference.provider](types/inference.provider.md) – who is offering
* [inference.request](types/inference.request.md) – one completion request
* [inference.message](types/inference.message.md) – one turn of a conversation
* [inference.content_part](types/inference.content_part.md) – text or media
* [inference.media_ref](types/inference.media_ref.md) – where a part's bytes come from
* [inference.tool](types/inference.tool.md) – a function the model may call
* [inference.tool_call](types/inference.tool_call.md) – one call the model made, as history carries it
* [inference.chunk](types/inference.chunk.md) – one delta of an answer
* [inference.tool_call_delta](types/inference.tool_call_delta.md) – one piece of a call while it streams
* [inference.usage](types/inference.usage.md) – what a request cost
* [inference.error](types/inference.error.md) – a refusal or a failure, and what to do about it
