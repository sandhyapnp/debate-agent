from typing import Dict, Any, List
import json
from .base_agent import BaseAgent, AgentResponse


class TopicSelectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("TopicSelector")
        self.state = "initial"
        self.selected_topic = None
        self.selected_stance = None
        
    def process(self, user_input: str, context: Dict[str, Any] = {}) -> AgentResponse:
        if self.state == "initial":
            return self._handle_initial_state(user_input)
        elif self.state == "topic_discovery":
            return self._handle_topic_discovery(user_input)
        elif self.state == "topic_confirmation":
            return self._handle_topic_confirmation(user_input)
        elif self.state == "stance_selection":
            return self._handle_stance_selection(user_input)
        else:
            return AgentResponse(
                content="Something went wrong. Let's start over.",
                next_action="restart"
            )
    
    def _handle_initial_state(self, user_input: str) -> AgentResponse:
        if user_input.lower() in ["exit", "quit", "stop"]:
            return AgentResponse(
                content="Goodbye! Feel free to come back anytime for a debate.",
                next_action="exit"
            )
        
        self.add_to_history("user", user_input)
        
        if "topic" in user_input.lower() and len(user_input.split()) > 3:
            self.selected_topic = user_input
            self.state = "topic_confirmation"
            return AgentResponse(
                content=f"Great! I see you want to debate about: '{user_input}'\n\nIs this correct? (yes/no)\n\nOr type 'exit' to quit.",
                metadata={"topic": user_input}
            )
        else:
            self.state = "topic_discovery"
            return AgentResponse(
                content="Welcome to the Debate Agent! I'll help you find an interesting topic to debate.\n\nWhat are you interested in? Some popular areas include:\n- Technology and AI\n- Environmental issues\n- Social media and privacy\n- Education and learning\n- Health and wellness\n- Politics and governance\n\nOr tell me about your background/interests, or type 'exit' to quit."
            )
    
    def _handle_topic_discovery(self, user_input: str) -> AgentResponse:
        if user_input.lower() in ["exit", "quit", "stop"]:
            return AgentResponse(
                content="Goodbye! Feel free to come back anytime for a debate.",
                next_action="exit"
            )
        
        self.add_to_history("user", user_input)
        
        suggested_topics = self._suggest_topics_based_on_input(user_input)
        
        self.state = "topic_confirmation"
        return AgentResponse(
            content=f"Based on your interests, here are some debate topics:\n\n" +
                   "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(suggested_topics)]) +
                   "\n\nPick a number (1-3), suggest your own topic, or type 'exit' to quit.",
            metadata={"suggested_topics": suggested_topics}
        )
    
    def _handle_topic_confirmation(self, user_input: str) -> AgentResponse:
        if user_input.lower() in ["exit", "quit", "stop"]:
            return AgentResponse(
                content="Goodbye! Feel free to come back anytime for a debate.",
                next_action="exit"
            )
        
        if user_input.lower() in ["yes", "y"]:
            self.state = "stance_selection"
            return AgentResponse(
                content=f"Perfect! We'll debate: '{self.selected_topic}'\n\nWould you like to argue FOR or AGAINST this topic? (for/against)\n\nOr type 'exit' to quit."
            )
        elif user_input.lower() in ["no", "n"]:
            self.state = "topic_discovery"
            return AgentResponse(
                content="No problem! Let's find a better topic. What interests you?"
            )
        elif user_input.isdigit():
            topic_index = int(user_input) - 1
            suggested_topics = self.conversation_history[-1].get("metadata", {}).get("suggested_topics", [])
            if 0 <= topic_index < len(suggested_topics):
                self.selected_topic = suggested_topics[topic_index]
                self.state = "stance_selection"
                return AgentResponse(
                    content=f"Great choice! We'll debate: '{self.selected_topic}'\n\nWould you like to argue FOR or AGAINST this topic? (for/against)\n\nOr type 'exit' to quit."
                )
        else:
            self.selected_topic = user_input
            self.state = "stance_selection"
            return AgentResponse(
                content=f"Interesting topic! We'll debate: '{user_input}'\n\nWould you like to argue FOR or AGAINST this topic? (for/against)\n\nOr type 'exit' to quit."
            )
    
    def _handle_stance_selection(self, user_input: str) -> AgentResponse:
        if user_input.lower() in ["exit", "quit", "stop"]:
            return AgentResponse(
                content="Goodbye! Feel free to come back anytime for a debate.",
                next_action="exit"
            )
        
        if user_input.lower() in ["for", "pro", "support"]:
            self.selected_stance = "for"
        elif user_input.lower() in ["against", "con", "oppose"]:
            self.selected_stance = "against"
        else:
            return AgentResponse(
                content="Please choose 'for' or 'against', or type 'exit' to quit."
            )
        
        return AgentResponse(
            content=f"Excellent! You'll argue {self.selected_stance.upper()} the topic: '{self.selected_topic}'\n\nLet's begin the debate! Make your opening argument.",
            metadata={
                "topic": self.selected_topic,
                "user_stance": self.selected_stance,
                "agent_stance": "against" if self.selected_stance == "for" else "for"
            },
            next_action="start_debate"
        )
    
    def _suggest_topics_based_on_input(self, user_input: str) -> List[str]:
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["tech", "ai", "artificial", "computer", "software"]):
            return [
                "Artificial Intelligence should replace human decision-making in healthcare",
                "Social media platforms should be held responsible for misinformation",
                "Remote work is more productive than office work"
            ]
        elif any(word in user_lower for word in ["environment", "climate", "green", "nature"]):
            return [
                "Nuclear energy is the best solution to climate change",
                "Individual actions matter more than corporate responsibility for environment",
                "Economic growth should be prioritized over environmental protection"
            ]
        elif any(word in user_lower for word in ["education", "school", "learning", "student"]):
            return [
                "Standardized testing accurately measures student ability",
                "College education is worth the debt",
                "Online learning is as effective as in-person education"
            ]
        else:
            return [
                "Social media does more harm than good",
                "Universal basic income would solve poverty",
                "Space exploration funding should be redirected to Earth problems"
            ]
    
    def get_debate_setup(self) -> Dict[str, str]:
        return {
            "topic": self.selected_topic,
            "user_stance": self.selected_stance,
            "agent_stance": "against" if self.selected_stance == "for" else "for"
        }