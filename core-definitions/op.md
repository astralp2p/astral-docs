# Op (Operation)

* An `Op` is a single API method that has an `Op Name` and a
  set of `Op Parameters`.
* An `Op Name` consists of alphanumeric characters, periods and 
  underscores, starting with a letter. Period is conventionally used to for 
  namespacing.
* An `Op Parameter` has a `Parameter Name` and an [`Object Type`](object-type.md) it takes.
* Only `Object Types` that support type-specific [`Text Encoding`](../topics/text-encoding.md) can be used as
  `Op Parameters`.
* A `Query` that omits a required `Op Parameter` is accepted and answered with one
  `error_message` reading `argument required: <names>`. `<names>` lists every
  omitted required `Op Parameter` in declaration order, separated by `, `.
* When that `Query` also carries keys no `Op Parameter` declares, the
  `error_message` continues with `; unknown argument: <keys>`, sorted and
  separated by `, `. At most 8 keys are named; more end the list with `…`.
  `in` and `out` are never named unknown. Example:
  `argument required: identity; unknown argument: id`.
* A `Query` that omits no required `Op Parameter` skips the keys no
  `Op Parameter` declares.
* A `Query` whose `Op Parameter` value does not parse is accepted and answered with
  one `error_message` reading `invalid argument: <name>: <cause>`.
* An `Op` refuses a `Caller` by accepting the `Query` and answering one
  `error_message`: `not permitted` when the `Caller` lacks the permission the
  `Op` requires, and `origin not allowed: <origin>` when the `Op` does not admit
  the `Query`'s origin. An `Op` that streams raw bytes rejects the `Query`
  instead.
* An `Op` that closes its `Channel` closes both directions. A later write by
  the `Caller` fails.
* When run over an accepted [`Query`](query.md)'s [`Channel`](channel.md), an `Op`
  reads input [`Objects`](object.md) and writes result `Objects` back. It runs in
  single or batch mode, and single-mode `Ops` compose into pipelines — see
  [Op modes & composition](../topics/op-modes.md).
