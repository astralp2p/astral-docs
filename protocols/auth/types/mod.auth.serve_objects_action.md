# mod.auth.serve_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
take a registered place in the node's object handling: as a describer, a
finder, or a searcher the node consults when it answers object queries, or as an
indexer the node feeds repository changes.

A describer, finder or searcher is not granted access to data. It is a place in
the node's answer path: once registered, the node calls out to the actor on
every matching query, whoever asked, and relays what comes back. Registering is
the mechanism — see [External Providers](../../../topics/external-providers.md).

An indexer is granted disclosure. The node sends it the object ID of every
object added to or removed from every repository with indexing enabled — see
the [`indexing`](../../indexing/README.md) protocol.

One action covers the four registration ops — `objects.register_describer`,
`objects.register_finder`, `objects.register_searcher` and
[`indexing.register_indexer`](../../indexing/ops/indexing.register_indexer.md).
[`indexing.subscribe`](../../indexing/ops/indexing.subscribe.md) submits the
action for the `indexer` role as well.

Role names which of the four a call asks for. Unlike the nouns the other object
actions declare, this one is evaluated.

A permit's `Constraints` bundle narrows the grant to the roles it names. An empty
bundle covers every role. A bundle otherwise holds `string8` roles and the permit
covers exactly those; an object of any other type in the bundle refuses the
permit outright, even alongside a role that matches.

The role names are `describer`, `finder`, `searcher` and `indexer`.

The user identity holds this action for the `indexer` role by default, and
nobody else holds any role by default. The node's own identity holds no role: a
local caller that presents no identity acts as the node, so a default for the
node would reach every such caller. Any other identity holds a role through a
node-local grant or a signed contract.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Role (string8) – The role the call asks for: `describer`, `finder`, `searcher`, or `indexer`.

## Example

```json
{
  "Type": "mod.auth.serve_objects_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "Role": "describer"
  }
}
```
