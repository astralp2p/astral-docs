# dir.set_alias

Set or remove an alias for an identity.

## Arguments

* id (identity, required) – The identity to set the alias for
* alias (string8, required) – The alias to set. To remove the existing alias,
  pass the argument with an empty value; omitting it is not the same and fails.

## Returned objects

The operation returns one of:
* An `error_message` object if there was an error.
* An `ack` object if the operation was successful.

A missing required argument is not reported this way. The check runs before the
query is accepted, so the caller sees a bare rejection rather than an
`error_message` naming the argument.

## Examples

Set an alias:

```shellsession
$ astral-query dir.set_alias -id 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -alias somealias -out text
#[ack] 
```

Remove it — the argument is present, its value empty:

```shellsession
$ astral-query dir.set_alias -id 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -alias "" -out text
#[ack] 
```
