# mod.vfs.listing

The canonical form of a folder: its entries in a fixed order and encoding. The `Object ID` of a listing is the `ID` of a folder in a [`mod.vfs.entry`](mod.vfs.entry.md). The node only hashes a listing. No operation sends, answers or stores it, and no object of this type exists in a repository.

## Encoding

All integers are big-endian. The listing is a header followed by the entries.

* Stamp (4 bytes) – `41 44 43 30`.
* Type name (string8) – `mod.vfs.listing`.
* Count (uint32) – The number of entries.
* Entries – In strictly ascending byte order of `Name`.

Each entry is encoded as:

* Name (string8) – The name of the entry.
* ID (object_id.sha256) – The `Size` as 8 bytes, then the 32 bytes of the hash.
* Flags (uint16) – The flags of the entry.
* ModTime (8 bytes) – The modification time as nanoseconds since the Unix epoch, UTC.

An entry carries no type header and no presence byte, unlike the default encoding of [`mod.vfs.entry`](mod.vfs.entry.md).

* The `Object ID` of a folder is the length of these bytes and their SHA-256 hash.
* The `ID` of a file in a listing is the `Object ID` of its content. The `ID` of a sub-folder is the `Object ID` of its listing.
* Each state of a folder has exactly one listing. All empty folders have the listing with a count of 0 and share one `Object ID`.
* A listing with entries out of order, a repeated name, an invalid name, or a flag bit other than bit 0 set is invalid.
* The flags and the modification times of the entries are part of the hashed bytes, so a change of either changes the `Object ID` of the root. The VFS identity, the limits, the usage, the permits and the modification time of the root itself are not.

## Example

The listing of a folder with one file `a.txt` of the six bytes `hello` and a line feed, modified at `1700000000000000000` nanoseconds. The listing is 80 bytes and its SHA-256 hash is `5ab8b70ba82974c48df86f4bcf3525cabe79931cff16d52d9fbb7c281f381eae`. The line breaks are for reading only.

```text
414443300f6d6f642e7666732e6c697374696e6700000001
05 612e747874
0000000000000006
5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03
0000
17979cfe362a0000
```
