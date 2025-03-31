# membase mcp server

## Description

Membase is a core component of the Unibase ecosystem. It stores historical information, interaction records, and persistent data of Agents, ensuring their continuity and traceability.

The membase mcp server enables seamless integration with the membase protocol for decentralized storage. It provides functionality to upload memory to the Unibase DA network.


## Functions

Messages or memoiries can be visit at: https://testnet.hub.membase.io/

- **get_conversation_id**: Get the current conversation id.
- **switch_conversation**: Switch to a different conversation.
- **save_message**: Save a message/memory into the current conversation.
- **get_messages**: Get the last n messages from the current conversation.

## Installation


```shell
git clone https://github.com/unibaseio/membase-mcp.git
cd membase-mcp
uv run src/membase_mcp/server.py
```


## Environment variables

- MEMBASE_ACCOUNT: your account to upload
- MEMBASE_CONVERSATION_ID: your conversation id, should be unique, will preload its history
- MEMBASE_ID: your sub account


## Configuration on Claude/Windsurf/Cursor/Cline

```json
{
  "mcpServers": {
    "membase": {
      "command": "uv",
      "args": ["run", "path/to/membase_mcp"],
      "env": {
        "MEMBASE_ACCOUNT": "your account, 0x...",
        "MEMBASE_CONVERSATION_ID": "your conversation id, should be unique",
        "MEMBASE_ID": "your sub account, any string"
      }
    }
  }
}
```



