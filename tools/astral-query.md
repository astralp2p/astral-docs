# astral-query

The `astral-query` tool can be used to send queries to nodes on the Astral 
Network from the command line.

The syntax is:

`astral-query [target:]<operation> [-<param> <val>] ... [<val>]`

The target can be the hex string of the target identity or its alias.

A `target:` that names another node needs the [`Network` zone](../core-definitions/zone.md),
which only an authenticated caller has. Export an access token first:

`export ASTRALD_APPHOST_TOKEN=<token>`

Without it the call is anonymous, the `Network` zone is stripped, and the query
fails locally with `route_not_found` before reaching the target — exporting the
token, not changing the query, is the fix. An anonymous call reaches only the
operations of the node's anonymous allowlist
([apphost, Sessions without a token](../protocols/apphost/README.md#sessions-without-a-token));
any other operation answers `denied`. A token issued to a
[`User`](../core-definitions/user.md) also routes the query as that user, which
the target may require in order to accept it.

## Arguments

Each `-<param> <val>` pair sets the query argument `<param>` to `<val>`. The
`<val>` token is taken as is, even when it starts with `-` or contains `=`.

One more token after the pairs, without a leading `-`, sets the argument `arg`,
the positional argument. `astral-query nat.set_enabled false` and
`astral-query nat.set_enabled -arg false` send the same query.

`astral-query` exits with status `1`, before it resolves the target or routes
the query, when a token is one of:

* `<key>=<val>` without a leading `-`. `key=value` is not an argument syntax.
  The error names the `-<key> <val>` form:
  `error: unexpected argument user=X: pass it as -user X`.
* `-<param>` as the last token, with no `<val>`:
  `error: argument -user has no value`.
* Any other token without a leading `-` in place of a `-<param>`, other than
  the last token: `error: unexpected argument <token>`.

A positional value that contains `=` is passed as `-arg <val>`.

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
  | astral-query bip137sig.derive_key -in json -out json -path "m/1791'/0'/0'/0/0"
```

See [Op modes & composition](../topics/op-modes.md) for the composition rule and
its limits.

## Ending input

`astral-query` copies stdin to the query's `Channel`. The end of stdin does not
close the `Channel`. An `Op` in batch mode reads until an
[`eos`](../primitive-types/eos.md) or EOF, so the `Op` keeps waiting after stdin
ends, and `astral-query` does not exit.
[`objects.store`](../protocols/objects/ops/objects.store.md),
[`crypto.public_key`](../protocols/crypto/ops/crypto.public_key.md) and
[`auth.sign_contract`](../protocols/auth/ops/auth.sign_contract.md) read their
input in batch mode.

`-eos` makes `astral-query` send an `eos` after stdin ends. A batch-mode `Op`
answers the `eos` with a final `eos` and returns, and `astral-query` exits.
`-eos` is a flag of `astral-query` itself and precedes the operation. After the
operation, `-eos` is read as a `-<param>`.

```shellsession
$ echo '{"Type":"string8","Object":"hello"}' | astral-query -eos objects.store -in json -out json
{"Type":"object_id.sha256","Object":"data1brwgb65sy54z9imojxaaof9btx3nujt1rxqyozt9ahxm189hi36e1"}
{"Type":"eos","Object":null}
```

Without `-eos`, the same command prints the `object_id.sha256` and does not
exit. Complete output followed by no exit is the symptom of a missing `-eos`.

`-eos` takes effect only when the query has an input format. The `eos` is
encoded in that format. A piped or redirected stdin has no input format unless
`-in <enc>` sets one. A terminal stdin defaults to `text`, or to the format in
`ASTRAL_DEFAULT_INPUT_FORMAT` when that variable is set.
