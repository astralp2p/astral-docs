# objects

The `objects` protocol provides access to typed astral objects across repositories: storing, reading, describing, searching, finding providers, and managing the repositories themselves.

* [Object Discovery](../../topics/object-discovery.md) - how `objects.search`, `objects.describe`, and `objects.find` fan out across registered providers
* [External Providers](../../topics/external-providers.md) - how an app registers as a searcher, describer, or finder and serves the discovery calls routed back to it

## Authorization

Every op in this protocol submits an action before it acts:

* Reads answer to [`mod.auth.see_objects_action`](../auth/types/mod.auth.see_objects_action.md).
* Writes answer to [`mod.auth.store_objects_action`](../auth/types/mod.auth.store_objects_action.md).
* The three registration ops answer to [`mod.auth.serve_objects_action`](../auth/types/mod.auth.serve_objects_action.md), each naming its role.
* Destroying answers to [`mod.auth.admin_objects_action`](../auth/types/mod.auth.admin_objects_action.md).

Writing and destroying are separate authorities. A caller granted the first may
add to a repository and not empty it.
