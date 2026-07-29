# astral-query

The `astral-query` tool can be used to send queries to nodes on the Astral 
Network from the command line.

The syntax is:

`astral-query [target:]<operation> [-<param> <val>] ...`

The target can be the hex string of the target identity or its alias.

A `target:` that names another node needs the [`Network` zone](../core-definitions/zone.md),
which only an authenticated caller has. Export an access token first:

`export ASTRALD_APPHOST_TOKEN=<token>`

Without it the call is anonymous, the `Network` zone is stripped, and the query
fails locally with `route_not_found` before reaching the target — exporting the
token, not changing the query, is the fix. A token issued to a
[`User`](../core-definitions/user.md) also routes the query as that user, which
the target may require in order to accept it.

## Encodings and chaining

Each query runs an [`Op`](../core-definitions/op.md) over a
[`Channel`](../core-definitions/channel.md); `astral-query` maps that `Channel`
onto the process's standard streams:

* `-in <enc>` decodes input [`Objects`](../core-definitions/object.md) from stdin.
* `-out <enc>` encodes result `Objects` to stdout.

`<enc>` is a channel format token: `bin`, `json`, `text` or `canonical` in
either direction, plus `base64` and `render` for `-out` only. The full table is
in [`Channel`](../core-definitions/channel.md). Tokens are case-sensitive, and
an unrecognised one produces no output and exits successfully — an empty result
with no error message is the symptom of a typo. Because the streams carry typed
`Objects`, single-mode ops chain with shell pipes when the upstream result's
`Object Type` is the type the next op reads and both sides use the same encoding:

```shellsession
$ astral-query bip137sig.new_entropy -bits 256 -out json \
  | astral-query bip137sig.mnemonic   -in json -out json \
  | astral-query bip137sig.seed       -in json -out json \
  | astral-query bip137sig.derive_key -in json -out json -path "m/44'/0'/0'/0/0"
```

See [Op modes & composition](../topics/op-modes.md) for the composition rule and
its limits.