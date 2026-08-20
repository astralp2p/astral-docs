# objects

The `objects` protocol provides access to typed astral objects across repositories: storing, reading, describing, searching, finding providers, and managing the repositories themselves.

* [Object Discovery](../../topics/object-discovery.md) - how `objects.search`, `objects.describe`, and `objects.find` fan out across registered providers
* [External Providers](../../topics/external-providers.md) - how an app registers as a searcher, describer, or finder and serves the discovery calls routed back to it

## Authorization

Every op in this protocol submits an action before it acts:

* Reads answer to [`mod.auth.see_objects_action`](../auth/types/mod.auth.see_objects_action.md).
* Writes answer to [`mod.auth.store_objects_action`](../auth/types/mod.auth.store_objects_action.md).
* The three registration ops answer to [`mod.auth.serve_objects_action`](../auth/types/mod.auth.serve_objects_action.md), each naming its role.

`objects.delete`, `objects.purge` and `objects.remove_repository` submit no
action.
