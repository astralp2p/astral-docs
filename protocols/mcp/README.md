# mcp

The `mcp` protocol registers AI agents and serves tools over the Model Context
Protocol. Each agent has a [`messaging`](../messaging/README.md) mailbox and an
[`apphost`](../apphost/README.md) access token.

The HTTP endpoint authenticates the token and runs tools as its identity. Five
built-in tools send, list, read, wait for, and archive mail. A deployment can
add tools backed by fixed Astral queries; the target service decides whether
the caller may use them.

## Operations

* [`mcp.create_agent`](ops/mcp.create_agent.md) – create an agent, mailbox, and token.
* [`mcp.agent`](ops/mcp.agent.md) – read one agent without its token.
* [`mcp.list_agents`](ops/mcp.list_agents.md) – list agents with their valid tokens.
* [`mcp.delete_agent`](ops/mcp.delete_agent.md) – remove an agent and its mailbox.

These management operations reject network queries and require the action
documented on each operation. The endpoint accepts any valid apphost token;
an agent record is not required.

[MCP Endpoint](../../topics/mcp-endpoint.md) covers authentication, mail-tool
JSON, declared tools, activity reports, and configuration.
