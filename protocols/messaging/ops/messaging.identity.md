# messaging.identity

Return one participant's record without any credential. Local-only — queries
from the network are rejected, and so are queries carrying the `mcp` origin.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any participant record is read when the caller is
not authorized, and a refused caller receives no bytes. A query from the network
or carrying the `mcp` origin is rejected before the action is submitted.

The record is read from this node's mailbox index and never asks the hosting
check: an entry still pending, and one whose hosting contract has expired or no
longer authorizes, is answered as any other. See [Hosting](../README.md#hosting).

## Arguments

* identity (string8, required) – The participant, given as a hex public key or a
  name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `identity` resolves to
  no identity.
* An `error_message` object reading `identity not found` if the identity
  resolves but this node's mailbox index has no entry for it. A caller
  distinguishes a mistyped name from an identity whose mailbox this node does
  not index.
* An `error_message` object if the index cannot be read.
* A `messaging.identity_info` object describing the participant.

## Examples

```shellsession
$ astral-query messaging.identity -identity scout -out json
{"Type":"messaging.identity_info","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout"}}
```

```shellsession
$ astral-query messaging.identity -identity 026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2 -out json
{"Type":"error_message","Object":"identity not found"}
```
