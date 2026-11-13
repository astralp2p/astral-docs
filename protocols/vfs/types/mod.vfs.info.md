# mod.vfs.info

The facts about one VFS: its identity, root, usage and limits.

## Fields

* VFS (identity) – The VFS identity.
* Root (object_id.sha256) – The `Object ID` of the root [`mod.vfs.directory`](mod.vfs.directory.md).
* Usage (uint64) – The bytes of file content the VFS holds. Each distinct file `Object ID` counts once, and a folder counts no bytes.
* Quota (uint64) – The byte limit. `0` means no limit.
* Inodes (uint64) – The number of inodes in use: one per entry. The root uses no inode.
* InodeLimit (uint64) – The inode limit. `0` means no limit.

The type reports no free space of the device. `Root`, `Usage` and `Inodes` describe one state of the VFS.

In JSON `Root` is the `data1` text form of the `Object ID`.

## Example

```json
{
  "Type": "mod.vfs.info",
  "Object": {
    "VFS": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Root": "data1fysiashf4okmwa1g9o54m3h41m1i6xgjt39as4ws39q5hfyxuo8iq",
    "Usage": 6,
    "Quota": 1073741824,
    "Inodes": 1,
    "InodeLimit": 1000000
  }
}
```
