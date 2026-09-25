# mcp.create_agent

Mint a new agent: a fresh identity with a signed relay contract, a signed
hosting contract, an optional alias, and the access token the agent presents to
the MCP endpoint, with a mailbox this node hosts. The agent is minted through
the [`messaging`](../../messaging/README.md) module, as
[`messaging.create_identity`](../../messaging/ops/messaging.create_identity.md)
mints a participant, so the node signs, indexes and stores the hosting contract
the agent's identity issues to it. The returned object carries the token.
`mcp.agent` withholds it, and `mcp.list_agents` is the sole way to recover it
afterwards. Local-only — queries from the network are rejected.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before an identity is minted when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* alias (string) – Alias to bind to the new agent. No alias is bound when
  empty, and none is generated: an alias is node-global, so a name the caller
  did not choose contends in a namespace it does not own.
* duration (duration) – Lifetime of the access token. Defaults to the
  [`messaging`](../../messaging/README.md#configuration) module's
  `token_duration`, itself 1 year.

## Returned objects

The operation returns one of:
* An `error_message` object if the identity cannot be minted, the alias is
  already taken (`alias already taken`), the token cannot be issued, a
  contract cannot be signed, indexed or stored, the mailbox index entry cannot
  be stored, or the agent record cannot be stored. A participant minted for an
  agent record that cannot be stored is deleted again, as
  `messaging.delete_identity` deletes one.
* An `mcp.agent` object describing the new agent, including its token.

## Examples

```shellsession
$ astral-query mcp.create_agent -alias scout -out json
{"Type":"mcp.agent","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","Token":"h4d8s2w6y1b9t3n7","ExpiresAt":"2027-08-20T12:00:00+02:00"}}
```

```shellsession
$ astral-query mcp.create_agent -alias scout -out json
{"Type":"error_message","Object":"alias already taken"}
```
