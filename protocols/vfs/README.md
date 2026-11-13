# vfs

The `vfs` protocol gives each identity a tree of named folders and files. A VFS belongs to the identity that names it, and one identity names at most one VFS. A file holds one object in the `local` repository group, and its [`mod.vfs.entry`](types/mod.vfs.entry.md) reports the [`Object ID`](../../core-definitions/object-id.md) of that content. A folder's entry reports the `Object ID` of its [`mod.vfs.directory`](types/mod.vfs.directory.md), the canonical form of the folder, and the `Object ID` of the root directory identifies the whole VFS. The node also stores each directory as an object in the `local` repository group (see [Directories](#directories)). A VFS holds the `Object ID` of each of its files and the current directory of each of its folders, so [`objects.purge`](../objects/ops/objects.purge.md) never deletes them. Every change to a VFS is complete or absent, and changes to one VFS happen one at a time.

A path starts with `/`, joins names with `/`, and has no empty segment and no trailing `/` except the root `/`. A path in a request is at most 4096 bytes. A name is valid UTF-8 of 1 to 255 bytes, contains no `/` and no NUL byte, and is not `.` and not `..`. Names compare byte by byte, with no Unicode normalization and no case rule. A path that breaks these rules is refused with `invalid path` and is never repaired. A VFS has a byte limit and an inode limit, and `0` means no limit. Each entry, file or folder, uses one inode. The root uses no inode. A new VFS gets the limits from the `byte_limit` and `inode_limit` keys of the module configuration, `1073741824` bytes and `1000000` inodes by default. No operation deletes a VFS.

The read operations [`vfs.ls`](ops/vfs.ls.md), [`vfs.stat`](ops/vfs.stat.md), [`vfs.statfs`](ops/vfs.statfs.md) and [`vfs.read`](ops/vfs.read.md) answer to [`mod.vfs.read_action`](types/mod.vfs.read_action.md). The write operations [`vfs.write`](ops/vfs.write.md), [`vfs.mkdir`](ops/vfs.mkdir.md), [`vfs.move`](ops/vfs.move.md), [`vfs.remove`](ops/vfs.remove.md) and [`vfs.touch`](ops/vfs.touch.md) answer to [`mod.vfs.write_action`](types/mod.vfs.write_action.md). The manage operations [`vfs.volumes`](ops/vfs.volumes.md), [`vfs.create`](ops/vfs.create.md) and [`vfs.set_quota`](ops/vfs.set_quota.md) answer to [`mod.vfs.manage_action`](types/mod.vfs.manage_action.md). [`vfs.set_evaluator`](ops/vfs.set_evaluator.md) answers to the VFS identity, the node's user, the node and a holder of `mod.vfs.manage_action`. Every operation except `vfs.volumes` takes `vfs`, the VFS identity. It defaults to the caller, except in `vfs.create`, `vfs.set_quota` and `vfs.set_evaluator`, where it is required. A caller may read and change its own VFS, and the node's user and the node may read and change any VFS. Any other caller is allowed when the [evaluator](#evaluator) of the VFS answers yes, or holds a permit whose `Constraints` list the VFS identity. Write permission does not imply read permission. An operation checks authorization first, then whether the VFS exists, then the path. The node creates the VFS of an app when the app registers, and by default names the app the evaluator of that VFS. The `vfs` operations are not on the token-less list of the [apphost gate](../apphost/README.md#gate).

## Directories

The node database is the working store of a VFS. The node keeps the `Object ID` of each folder's directory with the entry, and a change in a folder clears the `Object ID` of that folder and of every folder above it, up to the root. A cleared `Object ID` is computed again from the entries, and the directory is then stored in the `local` repository group. A directory is stored before its folder keeps the new `Object ID`. Directory bytes do not count in the `Usage` of a VFS; the inode limit bounds them.

A VFS with a cleared root `Object ID` is pending. The node computes a pending VFS in the background, with one worker for the node, the most overdue VFS first:

* A VFS is due when it has not changed for the quiet time, or at the latest when it has been pending for the longest wait, even while it keeps changing.
* A background compute is charged one token per byte of each directory it stores, and at least the minimum charge per directory. Each VFS has a token bucket that refills at the refill rate up to the bucket size. A due VFS whose bucket cannot pay waits until it can. A compute larger than the bucket waits for a full bucket.
* Background computes of all VFSes together stay within the node rate: a compute starts no earlier than the end of the one before plus its charge at the node rate.
* A failed store keeps the VFS pending, and the node tries again after the longest wait.
* The pending state and the buckets live in memory. At start every VFS with a cleared root `Object ID` is pending, and every bucket is full.

A request that needs a cleared `Object ID`, through [`vfs.ls`](ops/vfs.ls.md), [`vfs.stat`](ops/vfs.stat.md), [`vfs.statfs`](ops/vfs.statfs.md), [`vfs.volumes`](ops/vfs.volumes.md), [`vfs.move`](ops/vfs.move.md) or [`vfs.touch`](ops/vfs.touch.md), computes and stores it at once. Such a request is not charged and never waits for tokens. It waits for a compute of the same VFS that runs, and answers its result. When the store fails, the request still answers the `Object ID`, and a later compute stores the directory. A request for an `Object ID` that is kept stores nothing.

A directory that a folder no longer has is replaced. The node notes a replaced directory when the change commits, and a sweeper deletes it once the grace time has passed since the note, unless a holder holds it: a folder whose directory it is again, a folder of another VFS, or any other holder of the objects module. The objects module checks the holders again under the lock of each repository, as `objects.purge` does, and keeps a directory that a repository committed after the note. A directory kept by that check is noted again, so its grace time starts over. A note made again after the sweeper read it keeps its own grace time. The sweeper runs every sweep interval, so a replaced directory that nothing holds is deleted within the grace time plus one sweep interval. A directory already gone counts as deleted. A directory the sweeper could not delete, and a directory stored but taken by no folder after a failure, stays until `objects.purge` deletes it. The node never deletes and stores the same directory at once.

The keys of the module configuration:

| Key | Default | Meaning |
|-----|---------|---------|
| `directory_quiet_time` | `5s` | The time without a change after which a pending VFS is due. |
| `directory_longest_wait` | `60s` | The longest time a VFS is pending before it is due; also the wait before a retry. |
| `directory_bucket_size` | `8388608` | The token bucket of one VFS, in bytes. |
| `directory_refill_rate` | `4096` | The refill of one bucket, in bytes per second. |
| `directory_min_charge` | `4096` | The least charge for one stored directory, in bytes. |
| `directory_node_rate` | `32768` | The bound on background computes of all VFSes together, in bytes per second. |
| `directory_sweep_interval` | `10m` | The time between two runs of the sweeper. |
| `directory_grace_time` | `1h` | The time a replaced directory stays before the sweeper deletes it. |

A value of `0` or below is replaced by its default. A `directory_min_charge` above `directory_bucket_size` sets both to their defaults.

## Evaluator

A VFS may name an evaluator: an endpoint of the form `astral://<identity-or-alias>:vfs.authorize` that decides, at the moment of access, who else may read or write the VFS. The field is empty by default, and an empty field asks no one. [`vfs.set_evaluator`](ops/vfs.set_evaluator.md) sets and clears it, and [`mod.vfs.info`](types/mod.vfs.info.md) reports it. [`apphost.register`](../apphost/ops/apphost.register.md) names the new app the evaluator of its own VFS, with the endpoint `astral://<app identity>:vfs.authorize`, unless the registration turns this off. A VFS created with [`vfs.create`](ops/vfs.create.md) starts with an empty evaluator. Any identity may be the evaluator. The op is always `vfs.authorize`; an endpoint with another op, query arguments or a caller part is refused when it is set, and a stored endpoint of another form refuses without a question.

The node asks the evaluator about [`mod.vfs.read_action`](types/mod.vfs.read_action.md) and [`mod.vfs.write_action`](types/mod.vfs.write_action.md) only, and only about the VFS that names it. It never asks about [`mod.vfs.manage_action`](types/mod.vfs.manage_action.md). The VFS identity, the node's user and the node are allowed without a question. For any other actor the node asks the evaluator before it checks stored contracts. Node-local grants may be checked before or after the evaluator; the outcome is the same. A yes allows the action. A no, or a question that fails, leaves the decision to grants and contracts. In a contract chain the evaluator is asked once per level, about the actor of that level. Every question is put again; the node remembers no answer.

The node puts the question as a query from the node identity to the evaluator's identity, on `vfs.authorize`, with no arguments. It sends the action as the channel's single input object, a `mod.vfs.read_action` or a `mod.vfs.write_action` whose `ActorID` is the identity asking for access and whose `VFSID` is the VFS. It reads one object back:

* An [`ack`](../../primitive-types/ack.md) allows the action.
* Any other object, such as an [`error_message`](../../primitive-types/error_message.md), refuses it.
* An evaluator that cannot be resolved or reached, rejects the query, closes the channel, or does not read the question or answers nothing within the timeout refuses it. The timeout bounds the whole question, sending the action and reading the answer. The timeout is the auth module's default for an external question, 250 milliseconds.
* An actor that is the evaluator's own identity is refused without a question, because an authority cannot decide its own access.

The node bounds by the timeout the routing of the question to the evaluator as well: an evaluator endpoint that takes the query and neither accepts nor rejects it refuses the question when the timeout ends. A read by `Object ID` through [`mod.auth.see_objects_action`](../auth/types/mod.auth.see_objects_action.md) is allowed without a question when the actor is the identity of any VFS that holds the object. For an actor that the built-in rules do not allow the node may ask the evaluator of each VFS that holds the object in turn, and each question is bounded by the timeout, so such a read waits up to the timeout once for each VFS that holds the object.

This is the form in which the `auth` module asks an external authority over `astral://`. An app that evaluates its VFS registers a handler for `vfs.authorize` with [`apphost.register_handler`](../apphost/ops/apphost.register_handler.md), reads the action, and answers `ack` or `error_message`. An app registered with the default fields that does not serve `vfs.authorize` refuses every question, so every actor the built-in rules refuse waits up to the timeout before stored contracts are checked (node-local grants may be checked before or after). Such an app registers with `Evaluator` false or clears the field.

The same exchange put by hand to an app that evaluates its VFS, which answers yes:

```shellsession
$ astral-query 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f:vfs.authorize -in json -out json
{"Type":"mod.vfs.read_action","Object":{"Nonce":"a1b2c3d4e5f60718","ActorID":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","VFSID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"}}
{"Type":"ack","Object":null}
```
