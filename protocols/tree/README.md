# tree

The `tree` protocol provides access to a hierarchical key-value store. Values are stored at paths (e.g. `/mod/tcp/settings/listen`) and can hold any typed object. The tree is used by modules to expose and persist their configuration settings.

A module setting set through the tree persists across restarts unless the module's config file states that key, which replaces the stored value at every start; an unset setting follows the module's built-in default; tor `listen` is the exception and is rewritten from `tor.yaml` or the built-in default at every start.
