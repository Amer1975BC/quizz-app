"""
AI-Powered Question Generator
Generates new quiz questions using various AI models
"""

import json
import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
import anthropic
from ai_config import get_ai_config, format_prompt, AIProvider, TEMPERATURE_SETTINGS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class GeneratedQuestion:
    """Represents a generated quiz question"""
    text: str
    choices: List[str]
    correct_answer: str
    explanation: str
    difficulty: str
    category: str
    topic: str
    confidence: float = 0.0

class QuestionGenerator:
    """AI-powered question generator using multiple LLM providers"""
    
    def __init__(self):
        self.config = get_ai_config()
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize clients if API keys are available
        if self.config.openai_api_key:
            openai.api_key = self.config.openai_api_key
            self.openai_client = openai
            logger.info("OpenAI client initialized")
            
        if self.config.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
            logger.info("Anthropic client initialized")
    
    async def generate_questions(
        self, 
        category: str,
        count: int = 5,
        difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE,
        existing_topics: List[str] = None,
        target_audience: str = "general learners"
    ) -> List[GeneratedQuestion]:
        """Generate quiz questions for a specific category"""
        
        if not self._is_available():
            raise ValueError("No AI providers available. Please configure API keys.")
        
        existing_topics = existing_topics or []
        
        # Prepare prompt
        prompt_kwargs = {
            "category": category,
            "count": count,
            "difficulty": difficulty.value,
            "existing_topics": ", ".join(existing_topics) if existing_topics else "None",
            "target_audience": target_audience
        }
        
        prompt = format_prompt("question_generation", **prompt_kwargs)
        
        try:
            # Try primary provider first
            if self.config.default_provider == AIProvider.OPENAI and self.openai_client:
                response_text = await self._generate_with_openai(prompt)
            elif self.config.default_provider == AIProvider.ANTHROPIC and self.anthropic_client:
                response_text = await self._generate_with_anthropic(prompt)
            else:
                # Fallback to any available provider
                if self.openai_client:
                    response_text = await self._generate_with_openai(prompt)
                elif self.anthropic_client:
                    response_text = await self._generate_with_anthropic(prompt)
                else:
                    raise ValueError("No AI providers configured")
            
            # Parse and validate response
            questions = self._parse_response(response_text, category, difficulty.value)
            logger.info(f"Generated {len(questions)} questions for category: {category}")
            return questions
            
        except Exception as e:
            logger.error(f"Error generating questions: {e}")
            raise
    
    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate questions using OpenAI"""
        try:
            response = await asyncio.to_thread(
                openai.chat.completions.create,
                model=self.config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE_SETTINGS["question_generation"],
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise
    
    async def _generate_with_anthropic(self, prompt: str) -> str:
        """Generate questions using Anthropic Claude"""
        try:
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=self.config.anthropic_model,
                max_tokens=2000,
                temperature=TEMPERATURE_SETTINGS["question_generation"],
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation error: {e}")
            raise
    
    def _parse_response(self, response_text: str, category: str, difficulty: str) -> List[GeneratedQuestion]:
        """Parse AI response into GeneratedQuestion objects"""
        try:
            # Extract JSON from response (handle cases where AI adds extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_text = response_text[json_start:json_end]
            data = json.loads(json_text)
            
            questions = []
            for q_data in data.get("questions", []):
                question = GeneratedQuestion(
                    text=q_data["text"],
                    choices=q_data["choices"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation", ""),
                    difficulty=q_data.get("difficulty", difficulty),
                    category=q_data.get("category", category),
                    topic=q_data.get("topic", "General"),
                    confidence=self._calculate_confidence(q_data)
                )
                
                # Validate question
                if self._validate_question(question):
                    questions.append(question)
                else:
                    logger.warning(f"Invalid question skipped: {question.text[:50]}...")
            
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"Failed to parse AI response as JSON: {e}")
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise
    
    def _validate_question(self, question: GeneratedQuestion) -> bool:
        """Validate a generated question"""
        # Check required fields
        if not question.text or not question.choices or not question.correct_answer:
            return False
        
        # Check minimum choices
        if len(question.choices) < 2:
            return False
        
        # Check correct answer format
        valid_answers = ['A', 'B', 'C', 'D', '1', '2', '3', '4']
        if question.correct_answer not in valid_answers:
            return False
        
        # Check question length
        if len(question.text) < 10 or len(question.text) > 500:
            return False
        
        return True
    
    def _calculate_confidence(self, q_data: Dict) -> float:
        """Calculate confidence score for generated question"""
        score = 0.5  # Base score
        
        # Bonus for having explanation
        if q_data.get("explanation"):
            score += 0.2
        
        # Bonus for appropriate number of choices
        choices_count = len(q_data.get("choices", []))
        if choices_count == 4:
            score += 0.2
        elif choices_count >= 3:
            score += 0.1
        
        # Bonus for topic specification
        if q_data.get("topic") and q_data["topic"] != "General":
            score += 0.1
        
        return min(1.0, score)
    
    def _is_available(self) -> bool:
        """Check if any AI provider is available"""
        return bool(self.openai_client or self.anthropic_client)

class QuestionEnhancer:
    """Enhances existing questions with AI-generated explanations and difficulty assessment"""
    
    def __init__(self):
        self.generator = QuestionGenerator()
    
    async def generate_explanation(
        self, 
        question: str, 
        choices: List[str], 
        correct_answer: str,
        user_answer: str = None
    ) -> str:
        """Generate explanation for why an answer is correct"""
        
        prompt_kwargs = {
            "question": question,
            "choices": choices,
            "correct_answer": correct_answer,
            "user_answer": user_answer or "Not provided"
        }
        
        prompt = format_prompt("explanation_generation", **prompt_kwargs)
        
        try:
            if self.generator.openai_client:
                response = await asyncio.to_thread(
                    openai.chat.completions.create,
                    model=self.generator.config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURE_SETTINGS["explanation"],
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            elif self.generator.anthropic_client:
                response = await asyncio.to_thread(
                    self.generator.anthropic_client.messages.create,
                    model=self.generator.config.anthropic_model,
                    max_tokens=500,
                    temperature=TEMPERATURE_SETTINGS["explanation"],
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            else:
                return "AI explanation not available - no providers configured."
                
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Unable to generate explanation at this time."
    
    async def assess_difficulty(
        self, 
        question: str, 
        choices: List[str],
        category: str
    ) -> Tuple[int, str]:
        """Assess difficulty level of a question (1-5 scale)"""
        
        prompt_kwargs = {
            "question": question,
            "choices": choices,
            "category": category
        }
        
        prompt = format_prompt("difficulty_assessment", **prompt_kwargs)
        
        try:
            if self.generator.openai_client:
                response = await asyncio.to_thread(
                    openai.chat.completions.create,
                    model=self.generator.config.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=TEMPERATURE_SETTINGS["content_moderation"],
                    max_tokens=300
                )
                response_text = response.choices[0].message.content
            else:
                return 3, "Default difficulty - AI assessment not available"
            
            # Parse JSON response
            try:
                data = json.loads(response_text)
                difficulty = int(data.get("difficulty", 3))
                reasoning = data.get("reasoning", "AI assessment completed")
                return max(1, min(5, difficulty)), reasoning
            except (json.JSONDecodeError, ValueError):
                return 3, "Unable to parse difficulty assessment"
                
        except Exception as e:
            logger.error(f"Error assessing difficulty: {e}")
            return 3, "Error during difficulty assessment"

# Global instances
question_generator = QuestionGenerator()
question_enhancer = QuestionEnhancer()

async def generate_questions_for_category(
    category: str,
    count: int = 5,
    difficulty: str = "intermediate"
) -> List[Dict[str, Any]]:
    """Convenient function to generate questions and return as dictionaries"""
    
    difficulty_level = DifficultyLevel(difficulty.lower())
    questions = await question_generator.generate_questions(
        category=category,
        count=count,
        difficulty=difficulty_level
    )
    
    # Convert to dictionaries for easy JSON serialization
    return [
        {
            "text": q.text,
            "choices": q.choices,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "category": q.category,
            "topic": q.topic,
            "confidence": q.confidence,
            "generated_by_ai": True
        }
        for q in questions
    ]

async def enhance_question_with_ai(
    question_text: str,
    choices: List[str],
    correct_answer: str,
    category: str,
    user_answer: str = None
) -> Dict[str, Any]:
    """Enhance existing question with AI-generated explanation and difficulty"""
    
    enhancer = QuestionEnhancer()
    
    # Generate explanation and assess difficulty in parallel
    explanation_task = enhancer.generate_explanation(
        question_text, choices, correct_answer, user_answer
    )
    difficulty_task = enhancer.assess_difficulty(
        question_text, choices, category
    )
    
    explanation, (difficulty_score, difficulty_reasoning) = await asyncio.gather(
        explanation_task, difficulty_task
    )
    
    return {
        "explanation": explanation,
        "difficulty_score": difficulty_score,
        "difficulty_reasoning": difficulty_reasoning
    }