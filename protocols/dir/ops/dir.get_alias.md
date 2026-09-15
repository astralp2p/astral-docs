# dir.get_alias

Get the alias of an `Identity`.

## Arguments

* identity (string8, required) – The identity to get the alias of, given as a
  hex public key or a name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if `identity` does not resolve.
* An `error_message` object reading `missing identity` if `identity` resolves to
  the anonymous identity.
* An `error_message` object if there was an error.
* A `string8` object containing the alias of the identity.

## Examples

```shellsession
$ astral-query dir.get_alias -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"string8","Object":"somealias"}
```