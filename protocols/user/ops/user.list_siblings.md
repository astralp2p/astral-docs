# user.list_siblings

List identities of sibling nodes currently linked to this node — that is,
nodes in the same user swarm with a live link maintained by the sibling
linker. The caller must hold `mod.user.see_swarm_action`; rejected with code
`4` otherwise.

## Arguments

* zone (zone, optional) – Zone mask included in the context used to enumerate
  siblings (e.g. `n` for network).

## Returned objects

The operation streams one `identity` per linked sibling, then an `eos`. An
`error_message` is returned instead if encoding fails.

## Examples

```shellsession
$ astral-query user.list_siblings -out json
{"Type":"identity","Object":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"}
{"Type":"eos","Object":""}
```
