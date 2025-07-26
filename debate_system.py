from typing import Dict, Any
from agents.topic_selector import TopicSelectorAgent
from agents.debator import DebatorAgent
from agents.critique import CritiqueAgent


class DebateSystem:
    def __init__(self):
        self.topic_selector = TopicSelectorAgent()
        self.debator = DebatorAgent()
        self.critique = CritiqueAgent()
        self.state = "topic_selection"
        self.debate_setup = None
        
    def process_input(self, user_input: str) -> str:
        if self.state == "topic_selection":
            response = self.topic_selector.process(user_input)
            
            if response.next_action == "exit":
                return response.content
            elif response.next_action == "start_debate":
                self.debate_setup = response.metadata
                self.debator.setup_debate(
                    self.debate_setup["topic"],
                    self.debate_setup["agent_stance"],
                    self.debate_setup["user_stance"]
                )
                self.state = "debating"
                return response.content
            else:
                return response.content
                
        elif self.state == "debating":
            if user_input.lower() in ["exit", "quit", "stop", "end debate"]:
                self.state = "evaluation"
                return self._generate_final_evaluation()
            
            debator_response = self.debator.process(user_input)
            
            if debator_response.next_action == "end_debate":
                self.state = "evaluation" 
                return self._generate_final_evaluation()
            
            user_analysis = debator_response.metadata.get("user_argument_analysis", {})
            critique_analysis = self.critique.analyze_exchange(
                user_input, 
                debator_response.content,
                user_analysis
            )
            
            feedback = f"\n--- Round {critique_analysis['total_user_score']//100 + 1} Feedback ---\n"
            feedback += f"Your argument score: {sum(critique_analysis['user_scores'].values())}/100\n"
            feedback += f"Feedback: {critique_analysis['user_feedback']}\n"
            feedback += f"Current total: You {critique_analysis['total_user_score']} - Agent {critique_analysis['total_agent_score']}\n"
            feedback += "=" * 50 + "\n\n"
            
            return debator_response.content + "\n\n" + feedback
            
        elif self.state == "evaluation":
            return "The debate has ended. Type 'restart' to begin a new debate or 'exit' to quit."
            
        else:
            return "Something went wrong. Please restart the system."
    
    def _generate_final_evaluation(self) -> str:
        evaluation = self.critique.get_debate_evaluation()
        
        if "error" in evaluation:
            return "The debate ended before any arguments were made. Thank you for your time!"
        
        result = "\n" + "="*60 + "\n"
        result += "                    DEBATE EVALUATION\n"
        result += "="*60 + "\n\n"
        
        result += f"Topic: {self.debate_setup['topic']}\n"
        result += f"Your stance: {self.debate_setup['user_stance'].upper()}\n"
        result += f"Agent stance: {self.debate_setup['agent_stance'].upper()}\n\n"
        
        result += f"Total exchanges: {evaluation['total_exchanges']}\n"
        result += f"Rounds won by you: {evaluation['user_wins']}\n"
        result += f"Rounds won by agent: {evaluation['agent_wins']}\n"
        result += f"Overall winner: {evaluation['overall_winner'].upper()}\n\n"
        
        result += f"Your average score: {evaluation['average_user_score']}/100\n"
        result += f"Final grade: {evaluation['final_grade']}\n\n"
        
        if evaluation['user_strengths']:
            result += "Your strengths:\n"
            for strength in evaluation['user_strengths']:
                result += f"  • {strength}\n"
            result += "\n"
        
        if evaluation['areas_for_improvement']:
            result += "Areas for improvement:\n"
            for improvement in evaluation['areas_for_improvement']:
                result += f"  • {improvement}\n"
            result += "\n"
        
        result += "Thank you for the engaging debate! Type 'restart' for a new topic or 'exit' to quit.\n"
        result += "="*60
        
        return result
    
    def restart(self):
        self.topic_selector = TopicSelectorAgent()
        self.debator = DebatorAgent()
        self.critique = CritiqueAgent()
        self.state = "topic_selection"
        self.debate_setup = None
        return "Welcome back! Let's start a new debate. What topic interests you?"
    
    def get_state(self) -> str:
        return self.state