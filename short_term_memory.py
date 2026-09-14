from config import MAX_RECENT_MESSAGES, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
import redis
import json

class ShortTermMemory:
    """
    Session-level memory.
    Keeps only the latest N raw messages.
    """

    def __init__(
        self,
        max_messages=MAX_RECENT_MESSAGES,
    ):
        self.max_messages = max_messages
        self.r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True
            )


    def add_message(self, session_key: str, role: str, content: str):
        message = json.dumps({"role": role, "content": content})
        self.r.rpush(session_key, message)
        self.r.ltrim(session_key, -self.max_messages, -1)


    def get_messages(self,session_key: str,):
        messages = self.r.lrange(session_key, 0, -1)
        return [
            json.loads(message)
            for message in messages
        ]

    def clear(self,session_key: str,):
        self.r.delete(session_key)


short_term_memory = ShortTermMemory()