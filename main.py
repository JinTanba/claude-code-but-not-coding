import asyncio
import os
from claude_code_sdk import query, ClaudeCodeOptions
from claude_code_sdk.types import McpStdioServerConfig
from claude_code_sdk_client import ClaudeCodeClient
from hooks.basichooks import BasicHooks
from prompts.buzzPRTaskPrompt import create_buzz_pr_task_prompt
from prompts.append_system_prompt import append_system_prompt
from prompts.buzzVideoPrompt import create_buzz_video_prompt
from sdk_mcp_server.server import aitimes_db_mcp_server
last_session_id = None

playwrightMcpServer = McpStdioServerConfig(
    command="npx",
    args=["@playwright/mcp@latest"]
)


## playwright mcp tools
playwrightMcpTools = [
    'mcp__playwright-mcp__browser_navigate',
    'mcp__playwright-mcp__browser_navigate_back',
    'mcp__playwright-mcp__browser_navigate_forward',
    'mcp__playwright-mcp__browser_close',
    'mcp__playwright-mcp__browser_resize',
    'mcp__playwright-mcp__browser_snapshot',
    'mcp__playwright-mcp__browser_take_screenshot',
    'mcp__playwright-mcp__browser_console_messages',
    'mcp__playwright-mcp__browser_network_requests',
    'mcp__playwright-mcp__browser_click',
    'mcp__playwright-mcp__browser_hover',
    'mcp__playwright-mcp__browser_drag',
    'mcp__playwright-mcp__browser_type',
    'mcp__playwright-mcp__browser_press_key',
    'mcp__playwright-mcp__browser_select_option',
    'mcp__playwright-mcp__browser_tab_list',
    'mcp__playwright-mcp__browser_tab_new',
    'mcp__playwright-mcp__browser_tab_select',
    'mcp__playwright-mcp__browser_tab_close',
    'mcp__playwright-mcp__browser_evaluate',
    'mcp__playwright-mcp__browser_file_upload',
    'mcp__playwright-mcp__browser_handle_dialog',
    'mcp__playwright-mcp__browser_wait_for',
    'mcp__playwright-mcp__browser_install',
    'mcp__playwright-mcp__browser_parse_insight',
    'mcp__playwright-mcp__send_insight'
]
allowed_tools = [
    "Read",
    "Write",
    "Edit",
    "Bash",
    "Glob",
    "Grep",
    "WebSearch"
]

aitimes_db_mcp_tools = [
    "mcp__aitimes-db-mcp__create_article",
    "mcp__aitimes-db-mcp__get_article",
    "mcp__aitimes-db-mcp__update_article",
    "mcp__aitimes-db-mcp__list_articles",
    "mcp__aitimes-db-mcp__delete_article",
    "mcp__aitimes-db-mcp__upload_video"
]

basic_hooks = BasicHooks()
hooks = basic_hooks.get_hooks()

allowed_tools = allowed_tools + playwrightMcpTools + aitimes_db_mcp_tools

options = ClaudeCodeOptions(
    model="opus",
    allowed_tools=allowed_tools,
    permission_mode="acceptEdits",
    cwd=os.path.dirname(os.path.abspath(__file__)),
    mcp_servers={
        "playwright-mcp": playwrightMcpServer,
        "aitimes-db-mcp": aitimes_db_mcp_server
    },
    append_system_prompt=append_system_prompt,
    hooks=hooks
)

client = ClaudeCodeClient(options)

async def main():
    await client.start_task(create_buzz_pr_task_prompt)
    await client.start_task(create_buzz_video_prompt)
    await client.start()


if __name__ == "__main__":
    asyncio.run(main())