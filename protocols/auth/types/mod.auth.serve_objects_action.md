# mod.auth.serve_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
be consulted by the node when it answers object queries, as a describer, a
finder, or a searcher.

The authority is not access to data. It is a place in the node's answer path:
once registered, the node calls out to the actor on every matching query,
whoever asked, and relays what comes back. Registering is the mechanism — see
[External Providers](../../../topics/external-providers.md).

One action covers the three registration ops — `objects.register_describer`,
`objects.register_finder` and `objects.register_searcher`.

Role names which of the three a call asks for. Unlike the nouns the other object
actions declare, this one is evaluated.

A permit's `Constraints` bundle narrows the grant to the roles it names. An empty
bundle covers every role. A bundle otherwise holds `string8` roles and the permit
covers exactly those; an object of any other type in the bundle refuses the
permit outright, even alongside a role that matches.

The role names are `describer`, `finder` and `searcher`.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Role (string8) – The role the call asks for: `describer`, `finder`, or `searcher`.

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
