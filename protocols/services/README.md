# services

The `services` protocol manages discovery and synchronisation of named service advertisements across nodes. Each advertisement is represented as a `services.update` object that records whether a named service is available and which identity provides it.

`services.advertise` raises an advertisement on behalf of the caller and holds it for as long as its channel stays open, so an app that exits withdraws it by leaving. `services.discover` streams `services.update` objects visible to the caller; in follow mode the channel stays open for live updates. `services.sync` fetches advertisements from a remote identity and stores them in the local registry.

By convention a service `Name` is the operation namespace its provider serves: a consumer that discovers `contacts` calls `contacts.*`, with no second name to look up. An advertisement an app raised is served to local callers only.
