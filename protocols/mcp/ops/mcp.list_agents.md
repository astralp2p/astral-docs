# mcp.list_agents

Stream every registered agent, access tokens included. Local-only — queries
from the network are rejected.

The token is streamed by design: `mcp.create_agent` returns a token once, and
this operation is the only way to recover one that was lost. The response is
therefore a credential-bearing enumeration of every tenant's agents on the
node, and its output must be treated as the tokens themselves are. A read that
does not need the tokens is `mcp.agent`, which answers per agent and withholds
them.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns a stream of `mcp.agent` objects, followed by an `eos`
object. An `error_message` object is returned instead if the records cannot be
read.

## Examples

```shellsession
$ astral-query mcp.list_agents -out json
{"Type":"mcp.agent","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","Token":"h4d8s2w6y1b9t3n7","ExpiresAt":"2027-08-20T12:00:00+02:00"}}
{"Type":"mcp.agent","Object":{"Identity":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","Alias":"","Token":"c5v1k8m4p7q2z6r3","ExpiresAt":"2027-08-20T12:00:00+02:00"}}
{"Type":"eos","Object":null}
```
