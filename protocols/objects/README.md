# objects

The `objects` protocol provides access to typed astral objects across repositories: storing, reading, describing, searching, finding providers, and managing the repositories themselves.

* [Object Discovery](../../topics/object-discovery.md) - how `objects.search`, `objects.describe`, and `objects.find` fan out across registered providers
* [External Providers](../../topics/external-providers.md) - how an app registers as a searcher, describer, or finder and serves the discovery calls routed back to it
