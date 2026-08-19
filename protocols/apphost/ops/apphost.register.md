# apphost.register

Provision a fresh guest identity end-to-end: generate a new keypair, sign and
store an app contract between the new identity and the node, and issue an
access token. Used by apps/agents to bootstrap themselves on first run.

An app may ask for the actions it needs to hold. Asking is not receiving: the
node joins what the caller's origin is entitled to with what the app asked
for, and its register policy decides what the new identity actually holds.
Whatever is granted is written into a node→app contract; the answer carries
the token alone, so an app learns what it was granted by using it.

## Arguments

* permits (string8) – Actions the app asks to hold, comma-separated (e.g.
  `mod.user.see_swarm_action`). An action name carries no comma. Omitted asks for
  nothing.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if any step failed.
* An `apphost.access_token` object containing the new guest's token.

The operation is rejected outright if the node's register policy refuses the
registration.

## Examples

```shellsession
$ astral-query apphost.register -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Asking to hold an action:

```shellsession
$ astral-query apphost.register -permits mod.user.see_swarm_action -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```
