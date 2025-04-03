# membase mcp server

## Description

Unibase membase is the first decentralized memory layer for AI agents. It stores historical information, interaction records, and persistent data of agents, ensuring their continuity and traceability.

The membase mcp server enables seamless integration with the membase protocol for decentralized storage. It provides functionality to upload and download memory to/from the Unibase DA network.

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
- MEMBASE_ID: your instance id


## Configuration on Claude/Windsurf/Cursor/Cline

```json
{
  "mcpServers": {
    "membase": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/membase-mcp",
        "run", 
        "src/membase_mcp/server.py"
      ],
      "env": {
        "MEMBASE_ACCOUNT": "your account, 0x...",
        "MEMBASE_CONVERSATION_ID": "your conversation id, should be unique",
        "MEMBASE_ID": "your sub account, any string"
      }
    }
  }
}
```

## Usage

call functions in llm chat

+ get conversation id and switch conversation

![get conversation id and switch conversation](./asset/switch.png)

+ save message and get messages

![save message and get messages](./asset/save.png)
