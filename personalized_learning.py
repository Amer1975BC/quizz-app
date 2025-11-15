"""
Personalized Learning Engine
Analyzes user performance and provides adaptive recommendations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
from sqlalchemy import text
# Database connection handled separately

logger = logging.getLogger(__name__)


def get_database_session():
    """Get database session - imported locally to avoid circular imports"""
    try:
        from webapi import SessionLocal
        return SessionLocal()
    except ImportError:
        # Return None if webapi is not available (testing, etc)
        return None


class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING = "reading"

class DifficultyPreference(Enum):
    GRADUAL = "gradual"      # Slow progression
    STANDARD = "standard"    # Normal progression  
    CHALLENGE = "challenge"  # Fast progression

@dataclass
class UserPerformance:
    """Represents user performance metrics"""
    user_id: str
    category: str
    total_questions: int
    correct_answers: int
    average_time: float
    recent_accuracy: float  # Last 10 questions
    difficulty_level: int   # 1-5 scale
    learning_velocity: float  # Rate of improvement
    weak_topics: List[str]
    strong_topics: List[str]
    recommended_difficulty: int
    confidence_score: float

@dataclass
class LearningRecommendation:
    """AI-generated learning recommendation"""
    user_id: str
    category: str
    action: str  # "practice_more", "advance", "review", "break"
    reason: str
    suggested_topics: List[str]
    difficulty_adjustment: int  # -2 to +2
    estimated_improvement_time: int  # minutes
    confidence: float

class LearningAnalytics:
    """Machine learning engine for personalized learning"""
    
    def __init__(self):
        self.db = get_database_session()
    
    def analyze_user_performance(self, user_id: str, category: str = None) -> Dict[str, UserPerformance]:
        """Analyze user performance across categories"""
        try:
            # Query user quiz history
            if category:
                categories = [category]
            else:
                categories = self._get_user_categories(user_id)
            
            performance_data = {}
            
            for cat in categories:
                perf = self._calculate_performance_metrics(user_id, cat)
                if perf:
                    performance_data[cat] = perf
            
            return performance_data
            
        except Exception as e:
            logger.error(f"Error analyzing user performance: {e}")
            return {}
    
    def _get_user_categories(self, user_id: str) -> List[str]:
        """Get categories the user has attempted"""
        try:
            # This would need to be adapted based on your session storage
            # For now, return default categories
            return ["general", "PSPO1", "Verpleegkundig Rekenen"]
        except Exception:
            return ["general"]
    
    def _calculate_performance_metrics(self, user_id: str, category: str) -> Optional[UserPerformance]:
        """Calculate detailed performance metrics for a user in a category"""
        try:
            # Simulate user performance data (in real implementation, this would come from database)
            # You would query actual user sessions and answers
            
            # For demonstration, we'll create sample data
            sample_data = self._generate_sample_performance(user_id, category)
            
            total_questions = sample_data.get("total_questions", 0)
            if total_questions == 0:
                return None
            
            correct_answers = sample_data.get("correct_answers", 0)
            accuracy = correct_answers / total_questions if total_questions > 0 else 0
            
            # Calculate recent performance (last 10 questions)
            recent_accuracy = sample_data.get("recent_accuracy", accuracy)
            
            # Estimate difficulty level based on performance
            difficulty_level = self._estimate_difficulty_level(accuracy, recent_accuracy)
            
            # Calculate learning velocity (improvement rate)
            learning_velocity = self._calculate_learning_velocity(sample_data.get("historical_scores", []))
            
            # Identify weak and strong topics
            weak_topics, strong_topics = self._identify_topic_strengths(user_id, category)
            
            # Recommend difficulty adjustment
            recommended_difficulty = self._recommend_difficulty(
                accuracy, recent_accuracy, difficulty_level, learning_velocity
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                total_questions, accuracy, learning_velocity
            )
            
            return UserPerformance(
                user_id=user_id,
                category=category,
                total_questions=total_questions,
                correct_answers=correct_answers,
                average_time=sample_data.get("average_time", 45.0),
                recent_accuracy=recent_accuracy,
                difficulty_level=difficulty_level,
                learning_velocity=learning_velocity,
                weak_topics=weak_topics,
                strong_topics=strong_topics,
                recommended_difficulty=recommended_difficulty,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return None
    
    def _generate_sample_performance(self, user_id: str, category: str) -> Dict[str, Any]:
        """Generate sample performance data (replace with real database queries)"""
        # This simulates user performance data
        # In real implementation, query from user_sessions, user_answers tables
        
        import random
        random.seed(hash(user_id + category) % 1000)  # Consistent "randomness" per user/category
        
        total_questions = random.randint(20, 100)
        accuracy_base = random.uniform(0.4, 0.9)
        
        return {
            "total_questions": total_questions,
            "correct_answers": int(total_questions * accuracy_base),
            "recent_accuracy": accuracy_base + random.uniform(-0.1, 0.1),
            "average_time": random.uniform(30, 60),
            "historical_scores": [accuracy_base + random.uniform(-0.2, 0.2) for _ in range(10)]
        }
    
    def _estimate_difficulty_level(self, accuracy: float, recent_accuracy: float) -> int:
        """Estimate current difficulty level based on performance"""
        avg_performance = (accuracy + recent_accuracy) / 2
        
        if avg_performance >= 0.9:
            return 5  # Expert
        elif avg_performance >= 0.8:
            return 4  # Advanced
        elif avg_performance >= 0.7:
            return 3  # Intermediate
        elif avg_performance >= 0.6:
            return 2  # Beginner+
        else:
            return 1  # Beginner
    
    def _calculate_learning_velocity(self, historical_scores: List[float]) -> float:
        """Calculate rate of learning improvement"""
        if len(historical_scores) < 3:
            return 0.0
        
        # Simple linear regression to find improvement trend
        x = np.array(range(len(historical_scores)))
        y = np.array(historical_scores)
        
        # Calculate slope (learning velocity)
        slope = np.polyfit(x, y, 1)[0]
        return float(slope)
    
    def _identify_topic_strengths(self, user_id: str, category: str) -> Tuple[List[str], List[str]]:
        """Identify weak and strong topics within a category"""
        # This would analyze topic-level performance
        # For demonstration, return sample topics
        
        if category == "PSPO1":
            weak_topics = ["Sprint Planning", "Product Backlog"]
            strong_topics = ["Scrum Events", "Scrum Team"]
        elif category == "Verpleegkundig Rekenen":
            weak_topics = ["Dosering berekeningen", "IV druppelsnelheid"]
            strong_topics = ["Eenheid conversies", "Percentage oplossingen"]
        else:
            weak_topics = ["Complex reasoning", "Technical concepts"]
            strong_topics = ["Basic knowledge", "Factual recall"]
        
        return weak_topics, strong_topics
    
    def _recommend_difficulty(
        self, 
        accuracy: float, 
        recent_accuracy: float, 
        current_level: int,
        learning_velocity: float
    ) -> int:
        """Recommend optimal difficulty level"""
        
        # If recent performance is much better than overall, increase difficulty
        if recent_accuracy > accuracy + 0.1 and accuracy > 0.8:
            return min(5, current_level + 1)
        
        # If recent performance is worse, decrease difficulty
        elif recent_accuracy < accuracy - 0.1 or accuracy < 0.6:
            return max(1, current_level - 1)
        
        # If learning velocity is high, can handle more challenge
        elif learning_velocity > 0.05 and accuracy > 0.75:
            return min(5, current_level + 1)
        
        # Otherwise, maintain current level
        else:
            return current_level
    
    def _calculate_confidence_score(
        self, 
        total_questions: int, 
        accuracy: float,
        learning_velocity: float
    ) -> float:
        """Calculate confidence in the performance assessment"""
        
        # Base confidence on sample size
        sample_confidence = min(1.0, total_questions / 50)
        
        # Adjust for consistency (stable vs volatile performance)
        stability_bonus = 0.2 if abs(learning_velocity) < 0.02 else 0.0
        
        # Adjust for accuracy level
        accuracy_bonus = 0.3 if accuracy > 0.7 else 0.0
        
        return min(1.0, sample_confidence + stability_bonus + accuracy_bonus)

class PersonalizedRecommendationEngine:
    """Generates personalized learning recommendations"""
    
    def __init__(self):
        self.analytics = LearningAnalytics()
    
    def get_learning_recommendations(
        self, 
        user_id: str,
        category: str = None
    ) -> List[LearningRecommendation]:
        """Generate personalized learning recommendations"""
        
        performance_data = self.analytics.analyze_user_performance(user_id, category)
        recommendations = []
        
        for cat, performance in performance_data.items():
            recommendation = self._generate_category_recommendation(performance)
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_category_recommendation(self, performance: UserPerformance) -> LearningRecommendation:
        """Generate recommendation for a specific category"""
        
        # Analyze performance patterns
        accuracy = performance.correct_answers / performance.total_questions
        is_improving = performance.learning_velocity > 0
        is_struggling = performance.recent_accuracy < 0.6
        is_excelling = performance.recent_accuracy > 0.85
        has_enough_data = performance.total_questions >= 20
        
        # Determine recommendation
        if is_struggling and has_enough_data:
            action = "review"
            reason = f"Recent accuracy ({performance.recent_accuracy:.1%}) suggests reviewing fundamentals"
            difficulty_adjustment = -1
            suggested_topics = performance.weak_topics[:3]
            estimated_time = 30
            
        elif is_excelling and is_improving:
            action = "advance"
            reason = f"Excellent performance ({accuracy:.1%}) with positive trend"
            difficulty_adjustment = 1
            suggested_topics = ["Advanced topics", "New challenges"]
            estimated_time = 25
            
        elif not has_enough_data:
            action = "practice_more"
            reason = "Need more data to provide accurate recommendations"
            difficulty_adjustment = 0
            suggested_topics = ["Continue current topics"]
            estimated_time = 20
            
        elif accuracy > 0.9 and performance.learning_velocity < 0.01:
            action = "break"
            reason = "High mastery achieved - consider taking a break or exploring new topics"
            difficulty_adjustment = 0
            suggested_topics = ["New categories", "Review challenging topics"]
            estimated_time = 15
            
        else:
            action = "practice_more"
            reason = f"Steady progress - continue practicing to improve from {accuracy:.1%}"
            difficulty_adjustment = 0
            suggested_topics = performance.weak_topics[:2] + ["General practice"]
            estimated_time = 25
        
        return LearningRecommendation(
            user_id=performance.user_id,
            category=performance.category,
            action=action,
            reason=reason,
            suggested_topics=suggested_topics,
            difficulty_adjustment=difficulty_adjustment,
            estimated_improvement_time=estimated_time,
            confidence=performance.confidence_score
        )
    
    def get_next_question_recommendation(
        self, 
        user_id: str,
        category: str,
        current_session_performance: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Recommend next question characteristics based on performance"""
        
        performance = self.analytics.analyze_user_performance(user_id, category)
        cat_performance = performance.get(category)
        
        if not cat_performance:
            # Default for new users
            return {
                "difficulty": 2,
                "topics": ["basics"],
                "question_type": "multiple_choice",
                "estimated_time": 45
            }
        
        # Adjust based on session performance
        session_accuracy = 1.0
        if current_session_performance:
            session_correct = current_session_performance.get("correct", 0)
            session_total = current_session_performance.get("total", 0)
            session_accuracy = session_correct / session_total if session_total > 0 else 1.0
        
        # Determine difficulty
        base_difficulty = cat_performance.recommended_difficulty
        
        if session_accuracy > 0.8:
            target_difficulty = min(5, base_difficulty + 1)
        elif session_accuracy < 0.5:
            target_difficulty = max(1, base_difficulty - 1)
        else:
            target_difficulty = base_difficulty
        
        # Suggest topics
        if session_accuracy < 0.6:
            topics = cat_performance.weak_topics[:2]
        else:
            topics = cat_performance.weak_topics[:1] + ["general"]
        
        return {
            "difficulty": target_difficulty,
            "topics": topics,
            "question_type": "multiple_choice",
            "estimated_time": int(cat_performance.average_time * 1.1)
        }

# Global instances
personalized_engine = PersonalizedRecommendationEngine()

def get_user_recommendations(user_id: str, category: str = None) -> List[Dict[str, Any]]:
    """Get personalized recommendations for a user"""
    recommendations = personalized_engine.get_learning_recommendations(user_id, category)
    return [asdict(rec) for rec in recommendations]

def get_adaptive_question_params(
    user_id: str,
    category: str,
    session_performance: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Get adaptive parameters for next question selection"""
    return personalized_engine.get_next_question_recommendation(
        user_id, category, session_performance
    )