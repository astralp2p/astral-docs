# mod.vfs.entry

One name in a folder of a VFS, a file or a folder.

## Fields

* Name (string8) – The name of the entry. The name of the root, as [`vfs.stat`](../ops/vfs.stat.md) answers it for `/`, is empty.
* ID (object_id.sha256) – For a file, the `Object ID` of its content. For a folder, the `Object ID` of its [`mod.vfs.directory`](mod.vfs.directory.md).
* Flags (uint16) – Bit 0 is set for a folder and clear for a file. Bits 1 to 15 are zero. The folder bit never changes after the entry is created.
* ModTime (time) – The modification time of the entry.
* CreationTime (time) – The creation time of the entry.

The size of a file is the `Size` of its `ID`. The `ID` of a file with no content has `Size` 0 and the SHA-256 hash of no bytes.

A new entry gets the node's time as `ModTime`. Adding an entry to a folder, removing one from it or renaming one in it sets the time of that folder to the node's time, the root included. Replacing the content of a file sets the time of the file and leaves the time of its folder alone. [`vfs.touch`](../ops/vfs.touch.md) sets a time the caller chooses. [`vfs.move`](../ops/vfs.move.md) keeps the `ModTime` of the moved entry.

An entry gets the node's time as `CreationTime` when it is created: by [`vfs.write`](../ops/vfs.write.md) to a path with no entry, by [`vfs.mkdir`](../ops/vfs.mkdir.md), or as a missing parent folder. A write over an existing file, `vfs.move` and `vfs.touch` keep the `CreationTime`. A name that is removed and created again gets a new `CreationTime`. No operation sets a `CreationTime` the caller chooses. The root is in no folder and has no `CreationTime`.

In JSON `ID` is the `data1` text form of the `Object ID`, `Flags` is a number, and `ModTime` and `CreationTime` are RFC 3339 strings.

## Example

```json
{
  "Type": "mod.vfs.entry",
  "Object": {
    "Name": "a.txt",
    "ID": "data1csrtss41fiq9bbso9hftnd77uwo5su68na7xgueefbin7bdxpxod",
    "Flags": 0,
    "ModTime": "2023-11-14T22:13:20Z",
    "CreationTime": "2023-11-14T21:13:20Z"
  }
}
```
