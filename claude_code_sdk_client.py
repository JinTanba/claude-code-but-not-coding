from typing import Any, Generator
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, AssistantMessage, TextBlock
import asyncio

class ClaudeCodeClient:
    """Claude との単一会話セッションを維持します。"""
    
    def __init__(self, options: ClaudeCodeOptions = None):
        self.client = ClaudeSDKClient(options)
        self.turn_count = 0
        self.created_session_id = None
    
    async def _receive_response(self, turn_count: int):
        """Claudeからのレスポンスを受信して処理します。"""
        print(f"[ターン {turn_count}] Claude: ", end="")
        async for message in self.client.receive_response():
            # 最初のメッセージはセッションIDを含むシステム初期化メッセージです
            if hasattr(message, 'subtype') and message.subtype == 'init':
                session_id = message.data.get('session_id')
                print(f"⚡️⚡️ Claude Working!!。ID: {session_id}")
                self.created_session_id = session_id
            # このIDを後で再開するために保存できます
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text, end="")
            
        print()  # レスポンス後の改行

    async def start_task(self, create_prompt_func):
        stream_prompt = create_prompt_func()
        await self.client.connect()
        print("⚡️ Claude Code SDK Session is started and Context is active!!")
        await self.client.query(stream_prompt())

        async for message in self.client.receive_response():
            # 最初のメッセージはセッションIDを含むシステム初期化メッセージです
            if hasattr(message, 'subtype') and message.subtype == 'init':
                session_id = message.data.get('session_id')
                print(f"⚡️⚡️ Claude Working!!。ID: {session_id}")
                self.created_session_id = session_id
            # このIDを後で再開するために保存できます
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print("🤖",block.text, end="")

    async def start(self):
        await self.client.connect()
        print("⚡️ Claude Code SDK Session is started and Context is active!!")
        print("コマンド: 終了するには 'exit'、現在のタスクを停止するには 'interrupt'、新しいセッションには 'new'")

        while True:
            user_input = input(f"\n[ターン {self.turn_count + 1}] あなた: ")
            
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'interrupt':
                await self.client.interrupt()
                print("タスクが割り込まれました！")
                continue
            elif user_input.lower() == 'new':
                # 新しいセッションのために切断して再接続
                await self.client.disconnect()
                await self.client.connect()
                self.turn_count = 0
                print("新しい会話セッションを開始しました（以前のコンテキストはクリアされました）")
                continue
            
            # メッセージを送信 - Claude はこのセッションの以前のメッセージをすべて記憶
            await self.client.query(user_input)
            self.turn_count += 1

            # レスポンスを処理
            await self._receive_response(self.turn_count)
        
        await self.client.disconnect()
        print(f"会話は {self.turn_count} ターン後に終了しました。")
        return self.created_session_id if self.created_session_id else None

