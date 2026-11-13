# objects.purge

Delete the objects of a repository that no holder holds and that no caller has committed or read within a window. A group is purged once per leaf repository, and each leaf is purged in order of last touch, the least recently touched object first.

The caller must hold
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md).
The operation answers an `error_message` reading `not permitted` before the
repository is looked up when the caller is not authorized.

## Arguments

* repo (string8, required) – Repository to purge. A group is purged once per leaf repository below it.
* untouched (duration) – Delete only objects whose last touch is older than this window. A value below one hour, or no value, means one hour.
* dry (bool) – When `true`, the operation answers the ids it would delete and deletes nothing. Defaults to `false`.
* zone (zone) – Zone filter for the delete context. Defaults to all zones.
* out (string8) – Output format.

## Tracking and last touch

The node tracks each object committed to a leaf repository, a repository that stores objects itself. A group stores nothing and is not tracked. One row names the leaf repository and the object, and holds two times in whole seconds since the Unix epoch: the commit time, and the read time, which is `0` until the first counted read. The last touch of an object is the later of the two times. A row is removed when its object is deleted and when its repository is removed. An object written before tracking has no row and is never purged. The empty object is never stored and has no row.

An object is touched when it is committed, also when its content already existed, and when a caller reads it:

* A read counts on every route: [`objects.read`](objects.read.md), [`objects.load`](objects.load.md), [`vfs.read`](../../vfs/ops/vfs.read.md), the HTTP object handler, and a group read that ends in a leaf.
* A read counts for every tracked copy of the object, whichever repository served it.
* A read counts when its first byte is delivered. A read that can deliver no byte, such as a read of the empty object or with an `offset` equal to the object's `Size`, counts when it closes. A partial read counts like a full one, and a stream that keeps delivering bytes counts again once a minute.
* A read never creates a row. A read of an untracked object changes nothing.
* A read does not count when the node reads for itself: the follower of the [`auth`](../../auth/README.md) module and the follower of the [`crypto`](../../crypto/README.md) module that look for contracts and keys, and [`objects.probe`](objects.probe.md), whoever asks. A reader that is opened and closed without delivering a byte does not count, such as the losing readers of a concurrent group read.
* [`objects.contains`](objects.contains.md), [`objects.scan`](objects.scan.md), holder checks, deleting and purging do not touch an object.

The node keeps reads in memory and writes them to the database once a minute when there are any, before each purge decision and at shutdown. A write raises a read time and never lowers it. A node that stops without shutting down loses the reads of its last minute.

## Purge

An object is deleted only when no holder holds it and its last touch is older than the window. The window is `untouched`, raised to one hour when it is shorter, so an object committed or read within the last hour is never purged. A held object is never deleted, whatever its times say, and a held object is kept in every repository that has it. Its read time is still recorded.

The operation decides each object on current data. It writes the reads to the database, lists the objects whose last touch is older than the window, and for each one takes the lock of the leaf repository, writes the reads again, reads its row again, asks the holders, and only then deletes. An object read or committed after the listing and before its turn is kept. A commit takes the same lock, so a commit that has answered cannot lose to a purge.

With `dry`, the operation answers the ids of the objects a run without `dry` deletes, and it deletes nothing. An object that no longer exists in the leaf is answered by neither run.

## Schedule

The node purges the group `local` every 24 hours with the window `purge_untouched` of the configuration of the objects module, a duration such as `720h`. The default is 720 hours. A value of zero or below turns the schedule off. The first run comes 24 hours after the node starts. The scheduled run deletes, and its result is written to the log.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found or the purge fails mid-stream (sent after any ids already purged).
* A stream of `object_id.sha256` objects, one per purged object, or one per object a `dry` run would purge, followed by an `eos` object.

## Examples

```shellsession
$ astral-query objects.purge -repo local -out json
{"Type":"object_id.sha256","Object":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
{"Type":"object_id.sha256","Object":"data1bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}
{"Type":"eos","Object":null}
```

Listing what a purge of objects untouched for 30 days would delete:

```shellsession
$ astral-query objects.purge -repo local -untouched 720h -dry true -out json
{"Type":"object_id.sha256","Object":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
{"Type":"eos","Object":null}
```
