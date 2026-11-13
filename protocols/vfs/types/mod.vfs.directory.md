# mod.vfs.directory

The canonical form of a folder: its entries in a fixed order and encoding. The `Object ID` of a directory is the `ID` of a folder in a [`mod.vfs.entry`](mod.vfs.entry.md). No `vfs` operation sends or answers it.

The node stores the directory of a folder in the `local` repository group when it computes the folder's `Object ID` (see [storage of directories](../README.md#directories)). After an operation answers the `Object ID` of a folder, [`objects.probe`](../../objects/ops/objects.probe.md) on it answers the type `mod.vfs.directory`, and [`objects.read`](../../objects/ops/objects.read.md) answers the bytes below. A directory is read by `Object ID` under the rule of a file of the VFS: the VFS identity and an actor allowed [`mod.vfs.read_action`](mod.vfs.read_action.md) for the VFS read the current directory of each of its folders (see [`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md)). The node never reads a directory back: paths, listings and moves work from the entries.

## Encoding

All integers are big-endian. The directory is a header followed by the entries.

* Stamp (4 bytes) – `41 44 43 30`.
* Type name (string8) – `mod.vfs.directory`.
* Count (uint32) – The number of entries.
* Entries – In strictly ascending byte order of `Name`.

Each entry is encoded as:

* Name (string8) – The name of the entry.
* ID (object_id.sha256) – The `Size` as 8 bytes, then the 32 bytes of the hash.
* Flags (uint16) – The flags of the entry.
* ModTime (8 bytes) – The modification time as nanoseconds since the Unix epoch, UTC.
* CreationTime (8 bytes) – The creation time as nanoseconds since the Unix epoch, UTC.

An entry is 59 bytes plus the bytes of its name. It carries no type header and no presence byte, unlike the default encoding of [`mod.vfs.entry`](mod.vfs.entry.md).

* The `Object ID` of a folder is the length of these bytes and their SHA-256 hash.
* The `ID` of a file in a directory is the `Object ID` of its content. The `ID` of a sub-folder is the `Object ID` of its directory.
* Each state of a folder has exactly one directory. All empty folders have the directory with a count of 0 and share one `Object ID`.
* A directory with entries out of order, a repeated name, an invalid name, or a flag bit other than bit 0 set is invalid.
* The flags, the modification times and the creation times of the entries are part of the hashed bytes, so a change of any of them changes the `Object ID` of the root. Two folders with the same files have different `Object ID`s when their entries were created at different times. The VFS identity, the limits, the usage, the permits and the modification time of the root itself are not hashed.

## Examples

The directory of an empty folder is 26 bytes and its SHA-256 hash is `5bda020d3782b67b601ab110d94f3a3d64396438e5b4c4a7c2cbf3d9ff565382`.

```text
41444330116d6f642e7666732e6469726563746f727900000000
```

The directory of a folder with one file `a.txt` of the six bytes `hello` and a line feed, modified at `1700000000000000000` and created at `1699996400000000000` nanoseconds. The directory is 90 bytes and its SHA-256 hash is `d7702ed2ff919b922b0b391123f977fe466455a7afcaba17f0528e66f0bc3982`. The line breaks are for reading only.

```text
41444330116d6f642e7666732e6469726563746f727900000001
05 612e747874
0000000000000006
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03
0000
17979cfe362a0000
179799b805716000
```
