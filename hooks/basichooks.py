import json
from claude_code_sdk import query, ClaudeCodeOptions, HookMatcher, HookContext
from typing import Any
from datetime import datetime

class BasicHooks:
    def __init__(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"logs/log_{timestamp}.txt"

    def write_log(self, log: str):
        with open(self.log_file, "a") as f:
            f.write(log + "\n")
    async def log_tool_use(self, input_data: dict[str, Any], tool_use_id: str | None, context: HookContext):
        print(f"🛠️ Tool use: {input_data.get('tool_name')}")
        try:
            # HookContextを直接JSONに変換せず、基本的な情報だけログに記録
            context_info = f"tool_use_id: {tool_use_id}, input_keys: {list(input_data.keys()) if input_data else 'None'}"
            self.write_log(f"Tool use: {input_data.get('tool_name')}, Context: {context_info}")
        except Exception as e:
            self.write_log(f"?Tool use: {input_data.get('tool_name')}")
        return {}
    
    def get_hooks(self) -> dict[str, list[HookMatcher]]:
        return {
            'PreToolUse': [
                HookMatcher(hooks=[self.log_tool_use])
            ],
            'PostToolUse': [
                HookMatcher(hooks=[self.log_tool_use])
            ]
        }

