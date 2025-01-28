

class Conversation:
    def __init__(self, system_msg):
        self._system_msg = system_msg
        self._messages = []

    def _register_msg(self, role: str, msg: str):
        self._messages.append(
            {
                "role": role,
                "content": msg
            }
        )

    def register_assistant_msg(self, msg: str):
        self._register_msg("assistant", msg)

    def register_user_msg(self, msg: str):
        self._register_msg("user", msg)

    def flush_all_msgs(self):
        self._messages = []
    
    def rollback_msgs(self, rollback_amount: int):
        if rollback_amount >= len(self._messages):
            self.flush_all_msgs()
        else:
            self._messages = self._messages[:-rollback_amount]

    def dump_all_msgs(self) -> list:
        """Return all messages included System"""
        return [{"role": "system", "content": self._system_msg}]+self._messages
    
    def dump_conversation(self) -> list:
        """Return user and assistant messages"""
        return self._messages