from typing import List, Dict, Any
import asyncpg
import json

class MemoryManager:
    def __init__(self, uri: str):
        self.uri = uri
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.uri)
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id SERIAL PRIMARY KEY,
                    channel_id BIGINT,
                    user_id BIGINT,
                    username TEXT,
                    content TEXT,
                    is_bot BOOLEAN,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Create index for faster lookups
            await conn.execute('CREATE INDEX IF NOT EXISTS idx_channel_timestamp ON memory(channel_id, timestamp DESC)')

    async def add_message(self, channel_id: int, user_id: int, username: str, content: str, is_bot: bool = False):
        if not self.pool:
            return
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO memory (channel_id, user_id, username, content, is_bot)
                VALUES ($1, $2, $3, $4, $5)
            ''', channel_id, user_id, username, content, is_bot)

    async def get_context(self, channel_id: int, limit: int = 40) -> str:
        if not self.pool:
            return ""
        async with self.pool.acquire() as conn:
            records = await conn.fetch('''
                SELECT username, content, is_bot 
                FROM memory 
                WHERE channel_id = $1 
                ORDER BY timestamp DESC 
                LIMIT $2
            ''', channel_id, limit)
            
            context = []
            # We fetch DESC (newest first), so we need to reverse to get chronological order
            for record in reversed(records):
                role = "Bot" if record['is_bot'] else record['username']
                context.append(f"{role}: {record['content']}")
                
            return "\n".join(context)

    async def clear_context(self, channel_id: int):
        if not self.pool:
            return
        async with self.pool.acquire() as conn:
            await conn.execute('DELETE FROM memory WHERE channel_id = $1', channel_id)
