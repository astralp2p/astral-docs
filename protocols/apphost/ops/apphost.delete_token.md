# apphost.delete_token

Delete an access token so it no longer authenticates. Local-only — queries
from the network are rejected.

## Arguments

* token (string8, required) – The token to delete.

## Returned objects

The operation returns one of:
* An `error_message` object if the token is missing, unknown, or the database call failed. An unknown token returns `token not found` — a caller can distinguish an already-deleted token from a mistyped one.
* An `ack` object if the token was deleted.

## Examples

```shellsession
$ astral-query apphost.delete_token -token k7m2q5x9r3v4n8p1 -out json
{"Type":"ack","Object":null}
$ astral-query apphost.delete_token -token k7m2q5x9r3v4n8p1 -out json
{"Type":"error_message","Object":"token not found"}
```
