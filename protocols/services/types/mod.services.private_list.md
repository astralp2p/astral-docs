# mod.services.private_list

The node's list of providers made private by the user. An entry makes every
binding it covers private, whatever the binding advertised. An entry never
makes a binding open. To show a private provider to an app, the user grants
the app [`mod.services.service_discovery_action`](mod.services.service_discovery_action.md).

The list is stored in the node's tree at `/mod/services/private`. It is set
and read with [`tree.set`](../../tree/ops/tree.set.md) and
[`tree.get`](../../tree/ops/tree.get.md), which require
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md)
and [`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
An absent value is an empty list. Each node's list covers only the providers it
hosts.

A change takes effect at once: the node re-evaluates the affected bindings for
the followers of their services, and a follow that may no longer see an
offering receives [`services.removed`](services.removed.md) for it.

## Fields

* Entries (array of [`mod.services.private_entry`](mod.services.private_entry.md)) – The entries.

## Example

```json
{
  "Type": "mod.services.private_list",
  "Object": {
    "Entries": [
      { "Service": "bitcoin-wallet", "ProviderID": null },
      { "Service": "player", "ProviderID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f" }
    ]
  }
}
```

```shellsession
$ echo '{"Type":"mod.services.private_list","Object":{"Entries":[{"Service":"bitcoin-wallet","ProviderID":null}]}}' \
    | astral-query tree.set -path /mod/services/private -in json
```
