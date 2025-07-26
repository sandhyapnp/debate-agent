from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse


class CritiqueAgent(BaseAgent):
    def __init__(self):
        super().__init__("Critique")
        self.user_score = 0
        self.agent_score = 0
        self.argument_analyses = []
        self.scoring_criteria = {
            "evidence_use": 20,
            "logical_structure": 25,
            "relevance": 20,
            "persuasiveness": 20,
            "clarity": 15
        }
        
    def analyze_exchange(self, user_argument: str, agent_argument: str, 
                        user_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        
        user_scores = self._score_argument(user_argument, is_user=True, analysis=user_analysis)
        agent_scores = self._score_argument(agent_argument, is_user=False)
        
        self.user_score += sum(user_scores.values())
        self.agent_score += sum(agent_scores.values())
        
        exchange_analysis = {
            "user_scores": user_scores,
            "agent_scores": agent_scores,
            "user_feedback": self._generate_feedback(user_scores, user_argument),
            "agent_feedback": self._generate_feedback(agent_scores, agent_argument),
            "winner": "user" if sum(user_scores.values()) > sum(agent_scores.values()) else "agent",
            "total_user_score": self.user_score,
            "total_agent_score": self.agent_score
        }
        
        self.argument_analyses.append(exchange_analysis)
        return exchange_analysis
    
    def _score_argument(self, argument: str, is_user: bool = True, analysis: Dict[str, Any] = None) -> Dict[str, int]:
        scores = {}
        arg_lower = argument.lower()
        
        if analysis and is_user:
            scores["evidence_use"] = 18 if analysis.get("evidence_provided") else 8
        else:
            scores["evidence_use"] = 15 if any(word in arg_lower for word in 
                ["study", "research", "data", "statistics", "evidence", "example"]) else 8
        
        logical_words = ["because", "therefore", "thus", "consequently", "as a result", 
                        "furthermore", "however", "moreover", "in addition"]
        logical_count = sum(1 for word in logical_words if word in arg_lower)
        scores["logical_structure"] = min(25, 10 + logical_count * 3)
        
        sentence_count = len([s for s in argument.split('.') if len(s.strip()) > 5])
        topic_relevance = 20 if sentence_count >= 2 else 12
        scores["relevance"] = topic_relevance
        
        persuasive_elements = ["consider", "perspective", "important", "crucial", "significant", 
                              "impact", "consequences", "benefits", "advantages", "disadvantages"]
        persuasive_count = sum(1 for word in persuasive_elements if word in arg_lower)
        scores["persuasiveness"] = min(20, 8 + persuasive_count * 2)
        
        word_count = len(argument.split())
        if 20 <= word_count <= 100:
            scores["clarity"] = 15
        elif 100 < word_count <= 150:
            scores["clarity"] = 12
        else:
            scores["clarity"] = 8
        
        if analysis and analysis.get("fallacies"):
            scores["logical_structure"] = max(5, scores["logical_structure"] - 8)
        
        return scores
    
    def _generate_feedback(self, scores: Dict[str, int], argument: str) -> str:
        feedback_parts = []
        
        if scores["evidence_use"] < 12:
            feedback_parts.append("Consider adding more evidence or examples to support your claims")
        elif scores["evidence_use"] >= 16:
            feedback_parts.append("Good use of evidence and supporting details")
        
        if scores["logical_structure"] < 15:
            feedback_parts.append("Work on connecting your ideas with clearer logical transitions")
        elif scores["logical_structure"] >= 20:
            feedback_parts.append("Strong logical flow and structure in your argument")
        
        if scores["persuasiveness"] < 12:
            feedback_parts.append("Try to make your argument more compelling and consider counterpoints")
        elif scores["persuasiveness"] >= 16:
            feedback_parts.append("Persuasive and well-articulated argument")
        
        if scores["clarity"] < 12:
            feedback_parts.append("Consider being more concise or breaking down complex ideas")
        elif scores["clarity"] >= 14:
            feedback_parts.append("Clear and well-structured presentation")
        
        if not feedback_parts:
            feedback_parts.append("Solid argument overall with room for minor improvements")
        
        return ". ".join(feedback_parts) + "."
    
    def get_debate_evaluation(self) -> Dict[str, Any]:
        if not self.argument_analyses:
            return {"error": "No arguments to evaluate"}
        
        avg_user_score = self.user_score / len(self.argument_analyses)
        avg_agent_score = self.agent_score / len(self.argument_analyses)
        
        user_wins = sum(1 for analysis in self.argument_analyses if analysis["winner"] == "user")
        agent_wins = len(self.argument_analyses) - user_wins
        
        overall_winner = "user" if user_wins > agent_wins else "agent" if agent_wins > user_wins else "tie"
        
        strengths = self._identify_strengths()
        areas_for_improvement = self._identify_improvements()
        
        return {
            "total_exchanges": len(self.argument_analyses),
            "user_wins": user_wins,
            "agent_wins": agent_wins,
            "overall_winner": overall_winner,
            "average_user_score": round(avg_user_score, 1),
            "average_agent_score": round(avg_agent_score, 1),
            "user_strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "final_grade": self._calculate_grade(avg_user_score)
        }
    
    def _identify_strengths(self) -> List[str]:
        strengths = []
        
        if not self.argument_analyses:
            return strengths
        
        avg_scores = {}
        for criterion in self.scoring_criteria:
            total = sum(analysis["user_scores"][criterion] for analysis in self.argument_analyses)
            avg_scores[criterion] = total / len(self.argument_analyses)
        
        threshold = 15
        if avg_scores["evidence_use"] >= threshold:
            strengths.append("Strong use of evidence and examples")
        if avg_scores["logical_structure"] >= threshold * 1.2:
            strengths.append("Excellent logical reasoning and structure")
        if avg_scores["persuasiveness"] >= threshold:
            strengths.append("Persuasive and compelling arguments")
        if avg_scores["clarity"] >= threshold * 0.9:
            strengths.append("Clear and articulate communication")
        
        return strengths if strengths else ["Consistent participation and engagement"]
    
    def _identify_improvements(self) -> List[str]:
        improvements = []
        
        if not self.argument_analyses:
            return improvements
        
        avg_scores = {}
        for criterion in self.scoring_criteria:
            total = sum(analysis["user_scores"][criterion] for analysis in self.argument_analyses)
            avg_scores[criterion] = total / len(self.argument_analyses)
        
        threshold = 12
        if avg_scores["evidence_use"] < threshold:
            improvements.append("Incorporate more evidence and concrete examples")
        if avg_scores["logical_structure"] < threshold * 1.2:
            improvements.append("Improve logical flow and argument structure")
        if avg_scores["persuasiveness"] < threshold:
            improvements.append("Work on making arguments more persuasive and impactful")
        if avg_scores["clarity"] < threshold:
            improvements.append("Focus on clearer and more concise communication")
        
        return improvements if improvements else ["Continue developing argumentation skills"]
    
    def _calculate_grade(self, avg_score: float) -> str:
        max_possible = sum(self.scoring_criteria.values())
        percentage = (avg_score / max_possible) * 100
        
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
    
    def reset_scores(self):
        self.user_score = 0
        self.agent_score = 0
        self.argument_analyses = []