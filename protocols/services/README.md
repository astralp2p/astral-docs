# services

The `services` protocol manages discovery and synchronisation of named service advertisements across nodes. Each advertisement is represented as a `services.update` object that records whether a named service is available and which identity provides it.

`services.advertise` raises an advertisement on behalf of the caller and holds it for as long as its channel stays open, so an app that exits withdraws it by leaving. `services.discover` streams `services.update` objects visible to the caller; in follow mode the channel stays open for live updates. `services.sync` fetches advertisements from a remote identity and stores them in the local registry.

A service `Name` identifies the provider, not the interface it serves: an app answering on the `contacts` namespace may advertise itself as `contacts-backend`. A provider that wants a consumer to know which namespace to call puts that in `Info`, which is what the bundle is for. An advertisement an app raised is served to local callers and to the node's own swarm, and to nobody else.
