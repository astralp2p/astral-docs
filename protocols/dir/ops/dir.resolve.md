# dir.resolve

Resolve an `identity` from the string. The node tries these forms in order, and
the first match resolves the string:
* An empty string or `anyone` resolves to the anonymous identity
* `localnode` resolves to the node's own identity
* The pubkey hex string of the `identity`
* The alias of the `identity`
* A name a registered resolver claims (e.g. `localuser`, the user identity)

## Arguments

* identity (string8, required) – The name to be resolved.

## Returned objects

The operation returns one of:
* An `error_message` object if there was an error.
* An `identity` object if the name was resolved.

## Examples

```shellsession
$ astral-query dir.resolve -identity somealias -out json
{"Type":"identity","Object":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"}
```