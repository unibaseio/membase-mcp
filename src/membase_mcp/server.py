"""
Membase MCP Server Documentation

This module implements a FastMCP server that provides tools for managing conversations and messages
using the Membase memory system. The server offers the following main functionalities:

1. Conversation Management:
   - Get current conversation ID
   - Switch between different conversations
   - Save messages to conversations
   - Retrieve recent messages from conversations

2. Configuration:
   - Uses environment variables for configuration:
     * MEMBASE_ACCOUNT: Membase account identifier
     * MEMBASE_ID: Unique identifier for the current instance
     * MEMBASE_CONVERSATION_ID: Default conversation ID

3. Tools:
   - get_conversation_id(): Returns the current conversation ID
   - switch_conversation(conversation_id): Switches to a specified conversation
   - save_message(content, msg_type): Saves a message to the current conversation
   - get_messages(recent_n): Retrieves the last n messages from the current conversation

4. Memory Management:
   - Uses MultiMemory for handling conversations
   - Supports automatic upload to hub
   - Maintains conversation history
"""

import argparse
import json
import logging
import os
from typing import Literal
import uuid


from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from membase.memory.message import Message
from membase.memory.multi_memory import MultiMemory

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--transport", type=str, default="stdio", choices=["stdio", "sse"])
parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
args = parser.parse_args()

mcp = FastMCP(
    "Membase MCP Server", port=args.port, debug=True, log_level=args.log_level,
)

membase_account = os.getenv("MEMBASE_ACCOUNT")
if not membase_account or membase_account == "":
    raise ValueError("MEMBASE_ACCOUNT is not set")

logging.info(f"membase_account: {membase_account}")

membase_id = os.getenv("MEMBASE_ID")
if not membase_id or membase_id == "":
    membase_id = str(uuid.uuid4())

logging.info(f"membase_id: {membase_id}")

# Initialize default_conversation_id
default_conversation_id = os.getenv("MEMBASE_CONVERSATION_ID")
if not default_conversation_id:
    default_conversation_id = str(uuid.uuid4())

logging.info(f"default_conversation_id: {default_conversation_id}")

# Initialize MultiMemory
mm = MultiMemory(
    membase_account=membase_account,
    auto_upload_to_hub=True,
    default_conversation_id=default_conversation_id,
)
mm.load_from_hub(default_conversation_id)

@mcp.tool()
def get_conversation_id():
    '''
    Get the current conversation id.
    '''
    global default_conversation_id
    return default_conversation_id

@mcp.tool()
def switch_conversation(conversation_id: str):
    '''
    Switch to a different conversation.
    '''
    global default_conversation_id, mm
    default_conversation_id = conversation_id
    mm.load_from_hub(conversation_id)
    return f"Switched to conversation {conversation_id}."

@mcp.tool()
def save_message(content: str, msg_type: Literal["user", "assistant"] = "assistant"):
    '''
    Save a message/memory into the current conversation.
    '''
    msg = Message(
        name=membase_id,
        role=msg_type,
        content=content,
    )
    global default_conversation_id, mm
    mm.add(msg, default_conversation_id)
    return f"Message saved to conversation: {default_conversation_id}."

@mcp.tool()
def get_messages(recent_n: int = 8):
    '''
    Get the last n messages from the current conversation.
    '''
    global default_conversation_id, mm
    res = mm.get(default_conversation_id, recent_n)
    result = []
    for msg in res:
        result.append(msg.content)
    return json.dumps(result)


def main():
    logging.info("Starting Membase MCP Server")
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()
