from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}
    next_action: Optional[str] = None


class BaseAgent(ABC):
    def __init__(self, name: str, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.model = model
        self.conversation_history = []
    
    @abstractmethod
    def process(self, user_input: str, context: Dict[str, Any] = {}) -> AgentResponse:
        pass
    
    def add_to_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})
    
    def clear_history(self):
        self.conversation_history = []