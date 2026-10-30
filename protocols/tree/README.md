# tree

The `tree` protocol provides access to a hierarchical key-value store. Values are stored at paths (e.g. `/mod/tcp/settings/listen`) and can hold any typed object. The tree is used by modules to expose and persist their configuration settings.

A module setting set through the tree persists across restarts unless the module's config file states that key, which then replaces the stored value at every start. A value the config file wrote stays in the tree after the key is removed from the file. An unset setting follows the module's built-in default, and a `tree.set` of a `nil` object unsets a setting. A `tree.set` of an unset setting needs an explicit `type`, because there is no current value to infer it from. tor `listen` and `dial` are the exception: `tor.yaml` or the built-in default rewrites them at every start.
