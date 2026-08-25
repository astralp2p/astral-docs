# mcp.create_agent

Mint a new agent: a fresh identity with a signed relay contract, an optional
alias, and the access token the agent presents to the MCP endpoint. The
returned object carries the token, and it is the only response that does —
`mcp.list_agents` is the sole way to recover it afterwards. Local-only —
queries from the network are rejected.

## Arguments

* alias (string) – Alias to bind to the new agent. No alias is bound when
  empty, and none is generated: an alias is node-global, so a name the caller
  did not choose contends in a namespace it does not own.
* duration (duration) – Lifetime of the access token. Defaults to the module's
  `token_duration`, itself 1 year.

## Returned objects

The operation returns one of:
* An `error_message` object if the identity cannot be minted, the alias is
  already taken (`alias already taken`), the token cannot be issued, or the
  record cannot be stored.
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
