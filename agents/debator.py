from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse


class DebatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Debator")
        self.topic = None
        self.my_stance = None
        self.opponent_stance = None
        self.argument_count = 0
        self.key_points_made = []
        
    def setup_debate(self, topic: str, agent_stance: str, user_stance: str):
        self.topic = topic
        self.my_stance = agent_stance
        self.opponent_stance = user_stance
        self.argument_count = 0
        self.key_points_made = []
        
    def process(self, user_input: str, context: Dict[str, Any] = {}) -> AgentResponse:
        if user_input.lower() in ["exit", "quit", "stop", "end debate"]:
            return AgentResponse(
                content="The debate has ended. Thank you for the engaging discussion!",
                next_action="end_debate"
            )
        
        self.add_to_history("user", user_input)
        
        user_argument = self._analyze_user_argument(user_input)
        counter_argument = self._generate_counter_argument(user_argument)
        
        self.argument_count += 1
        
        return AgentResponse(
            content=counter_argument,
            metadata={
                "argument_number": self.argument_count,
                "user_argument_analysis": user_argument,
                "agent_stance": self.my_stance
            }
        )
    
    def _analyze_user_argument(self, user_input: str) -> Dict[str, Any]:
        analysis = {
            "main_points": [],
            "evidence_provided": False,
            "logical_structure": "unclear",
            "emotional_appeals": False,
            "fallacies": []
        }
        
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["study", "research", "data", "statistics", "evidence"]):
            analysis["evidence_provided"] = True
        
        if any(word in user_lower for word in ["because", "therefore", "thus", "consequently", "as a result"]):
            analysis["logical_structure"] = "clear"
        
        if any(word in user_lower for word in ["feel", "believe", "think", "everyone knows", "obviously"]):
            analysis["emotional_appeals"] = True
            
        if "everyone" in user_lower or "no one" in user_lower or "always" in user_lower or "never" in user_lower:
            analysis["fallacies"].append("overgeneralization")
        
        sentences = user_input.split('.')
        analysis["main_points"] = [s.strip() for s in sentences if len(s.strip()) > 10][:3]
        
        return analysis
    
    def _generate_counter_argument(self, user_analysis: Dict[str, Any]) -> str:
        stance_templates = {
            "for": {
                "ai_healthcare": [
                    "While I understand your concerns, consider that AI can process vast amounts of medical data faster than humans, potentially saving lives through quicker diagnoses.",
                    "You raise valid points, but AI systems can reduce human error and provide consistent, unbiased medical recommendations based on comprehensive data analysis.",
                    "That's an interesting perspective, however AI in healthcare could democratize access to quality medical advice, especially in underserved areas."
                ],
                "social_media_responsibility": [
                    "I see your argument, but platforms have the infrastructure and reach to combat misinformation at scale in ways individuals cannot.",
                    "While you make valid points, social media companies profit from user engagement and should bear responsibility for the content they amplify.",
                    "Your perspective is noted, yet these platforms shape public discourse and have a duty to ensure information accuracy."
                ]
            },
            "against": {
                "ai_healthcare": [
                    "I appreciate your argument, but human judgment involves empathy and contextual understanding that AI cannot replicate in medical care.",
                    "You make some points, however AI systems can perpetuate biases present in training data, potentially harming vulnerable populations.",
                    "While technology has benefits, medical decisions require human intuition and the ability to handle unique, unprecedented cases."
                ],
                "social_media_responsibility": [
                    "I understand your position, but platforms cannot effectively determine truth without becoming censors of legitimate discourse.",
                    "Your points have merit, yet holding platforms responsible could lead to over-censorship and suppression of diverse viewpoints.",
                    "That's a fair argument, however the sheer volume of content makes comprehensive fact-checking practically impossible."
                ]
            }
        }
        
        response_starters = [
            f"I hear your argument about {user_analysis['main_points'][0] if user_analysis['main_points'] else 'this topic'}, but let me present a different perspective.",
            f"You raise some interesting points, particularly about {user_analysis['main_points'][0] if user_analysis['main_points'] else 'this issue'}. However, consider this:",
            f"I appreciate the thought you've put into this, especially regarding {user_analysis['main_points'][0] if user_analysis['main_points'] else 'your position'}. Let me offer a counterpoint:",
        ]
        
        if not user_analysis["evidence_provided"]:
            evidence_challenge = " Furthermore, I notice your argument would be stronger with supporting evidence or examples."
        else:
            evidence_challenge = ""
        
        if user_analysis["fallacies"]:
            fallacy_note = f" I also notice some overgeneralization in your reasoning that we should address."
        else:
            fallacy_note = ""
        
        topic_lower = self.topic.lower() if self.topic else ""
        
        if "ai" in topic_lower or "artificial intelligence" in topic_lower:
            topic_key = "ai_healthcare"
        elif "social media" in topic_lower:
            topic_key = "social_media_responsibility"
        else:
            topic_key = "ai_healthcare"
        
        stance_responses = stance_templates.get(self.my_stance, {}).get(topic_key, [
            f"I understand your position, but from the {self.my_stance} perspective, we must consider the broader implications.",
            f"You make some valid points, however arguing {self.my_stance} this topic reveals important considerations you may have overlooked.",
            f"While I respect your viewpoint, taking the {self.my_stance} stance shows us a different angle on this issue."
        ])
        
        import random
        starter = random.choice(response_starters)
        main_argument = random.choice(stance_responses)
        
        key_point = f"One crucial point to consider is that {'this approach' if self.my_stance == 'for' else 'this position'} {'addresses' if self.my_stance == 'for' else 'overlooks'} the long-term consequences for society."
        
        self.key_points_made.append(key_point)
        
        return f"{starter} {main_argument} {key_point}{evidence_challenge}{fallacy_note}\n\nWhat's your response to this perspective?"
    
    def get_debate_summary(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "agent_stance": self.my_stance,
            "total_arguments": self.argument_count,
            "key_points_made": self.key_points_made
        }