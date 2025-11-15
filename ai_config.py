"""
AI/ML Configuration for Quiz Application
Provides centralized configuration for all AI services and models
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"

@dataclass
class AIConfig:
    """Configuration for AI/ML services"""
    
    # API Keys (should be set via environment variables)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    
    # Model configurations
    openai_model: str = "gpt-3.5-turbo"
    anthropic_model: str = "claude-3-sonnet-20240229"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Question generation settings
    default_provider: AIProvider = AIProvider.OPENAI
    max_questions_per_request: int = 5
    question_temperature: float = 0.7
    
    # Learning analytics
    enable_learning_analytics: bool = True
    min_attempts_for_analysis: int = 10
    difficulty_adjustment_threshold: float = 0.7
    
    # Chatbot settings
    chatbot_enabled: bool = True
    chatbot_model: str = "gpt-3.5-turbo"
    max_conversation_length: int = 10
    
    # Performance settings
    use_caching: bool = True
    cache_ttl_seconds: int = 3600
    batch_size: int = 32
    
    # Feature flags
    enable_question_generation: bool = True
    enable_personalized_learning: bool = True
    enable_ai_explanations: bool = True
    enable_content_moderation: bool = True
    
    def __post_init__(self):
        """Load configuration from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # Override defaults from environment
        self.openai_model = os.getenv("OPENAI_MODEL", self.openai_model)
        self.enable_learning_analytics = os.getenv("ENABLE_LEARNING_ANALYTICS", "true").lower() == "true"
        self.chatbot_enabled = os.getenv("CHATBOT_ENABLED", "true").lower() == "true"

# Global configuration instance
ai_config = AIConfig()

def get_ai_config() -> AIConfig:
    """Get the global AI configuration"""
    return ai_config

def validate_ai_setup() -> Dict[str, Any]:
    """Validate AI setup and return status"""
    status = {
        "openai_available": bool(ai_config.openai_api_key),
        "anthropic_available": bool(ai_config.anthropic_api_key),
        "features_enabled": {
            "question_generation": ai_config.enable_question_generation,
            "personalized_learning": ai_config.enable_personalized_learning,
            "chatbot": ai_config.chatbot_enabled,
            "analytics": ai_config.enable_learning_analytics
        },
        "ready": False
    }
    
    # Check if at least one AI provider is available
    status["ready"] = status["openai_available"] or status["anthropic_available"]
    
    return status

# Model temperature settings for different tasks
TEMPERATURE_SETTINGS = {
    "question_generation": 0.8,  # More creative for variety
    "explanation": 0.3,          # More focused for accuracy
    "chatbot": 0.7,              # Balanced for conversation
    "content_moderation": 0.1    # Very focused for consistency
}

# Prompt templates
PROMPT_TEMPLATES = {
    "question_generation": """
Generate {count} multiple choice quiz questions for the category: {category}

Requirements:
- Questions should be at {difficulty} level
- Each question should have 4 answer choices (A, B, C, D)
- Mark the correct answer clearly
- Questions should be educational and accurate
- Vary the question types and topics within the category
- Make questions relevant for {target_audience}

Category: {category}
Difficulty: {difficulty}
Target Audience: {target_audience}
Existing Topics: {existing_topics}

Format your response as JSON with this structure:
{{
  "questions": [
    {{
      "text": "Question text here?",
      "choices": ["A. Choice 1", "B. Choice 2", "C. Choice 3", "D. Choice 4"],
      "correct_answer": "A",
      "explanation": "Why this answer is correct",
      "difficulty": "{difficulty}",
      "category": "{category}",
      "topic": "Specific topic within category"
    }}
  ]
}}
""",

    "explanation_generation": """
Provide a clear, educational explanation for why the correct answer to this quiz question is right, and why the other options are incorrect.

Question: {question}
Correct Answer: {correct_answer}
User's Answer: {user_answer}
All Choices: {choices}

Please provide:
1. A brief explanation of why the correct answer is right
2. Why the user's answer (if different) is incorrect
3. Any additional learning tips or context

Keep the explanation clear, encouraging, and educational.
""",

    "chatbot_system": """
You are a helpful AI study assistant for a quiz application. Your role is to:
1. Help users understand quiz concepts and topics
2. Provide explanations for questions they find difficult
3. Offer study tips and learning strategies
4. Motivate and encourage learning

Guidelines:
- Be encouraging and supportive
- Provide clear, accurate explanations
- Suggest study strategies when appropriate
- Keep responses concise but helpful
- If you don't know something, admit it and suggest alternatives

Current quiz context:
- Available categories: {categories}
- User's recent performance: {performance_summary}
""",

    "difficulty_assessment": """
Analyze this quiz question and assess its difficulty level on a scale of 1-5:
1 = Very Easy (basic recall)
2 = Easy (simple understanding)
3 = Medium (application of knowledge)
4 = Hard (analysis and synthesis)
5 = Very Hard (complex problem solving)

Question: {question}
Choices: {choices}
Category: {category}

Provide a JSON response with:
{{
  "difficulty": 1-5,
  "reasoning": "Brief explanation of difficulty assessment",
  "concepts": ["list", "of", "key", "concepts"],
  "prerequisites": ["required", "knowledge", "areas"]
}}
"""
}

def get_prompt_template(template_name: str) -> str:
    """Get a prompt template by name"""
    return PROMPT_TEMPLATES.get(template_name, "")

def format_prompt(template_name: str, **kwargs) -> str:
    """Format a prompt template with provided arguments"""
    template = get_prompt_template(template_name)
    return template.format(**kwargs)