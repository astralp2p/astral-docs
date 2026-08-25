# mcp.agent

Return one agent's record without its access token. Local-only — queries from
the network are rejected.

## Arguments

* id (string, required) – The agent, given as a hex public key or alias
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `id` resolves to no
  identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it. A caller distinguishes a mistyped name
  from an identity that is not an agent.
* An `mcp.agent_info` object describing the agent.

## Examples

```shellsession
$ astral-query mcp.agent -id scout -out json
{"Type":"mcp.agent_info","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","ExpiresAt":"2027-08-20T12:00:00+02:00"}}
```

```shellsession
$ astral-query mcp.agent -id 026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2 -out json
{"Type":"error_message","Object":"agent not found"}
```
