"""
AI Chatbot Helper for Quiz Application
Provides intelligent study assistance and explanations
"""

import json
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio
import openai
import anthropic
from ai_config import get_ai_config, format_prompt, TEMPERATURE_SETTINGS
from personalized_learning import get_user_recommendations

logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Represents a chat message"""
    id: str
    user_id: str
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime
    context: Dict[str, Any] = None  # Quiz context, user performance, etc.

@dataclass 
class ChatSession:
    """Represents a chat session"""
    session_id: str
    user_id: str
    messages: List[ChatMessage]
    created_at: datetime
    last_activity: datetime
    context: Dict[str, Any] = None

class StudyAssistantChatbot:
    """AI-powered study assistant chatbot"""
    
    def __init__(self):
        self.config = get_ai_config()
        self.sessions: Dict[str, ChatSession] = {}  # In-memory storage (use Redis/DB in production)
        
        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None
        
        if self.config.openai_api_key:
            openai.api_key = self.config.openai_api_key
            self.openai_client = openai
            
        if self.config.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
    
    async def start_chat_session(
        self, 
        user_id: str,
        quiz_context: Dict[str, Any] = None
    ) -> str:
        """Start a new chat session"""
        
        session_id = f"chat_{user_id}_{int(datetime.now().timestamp())}"
        
        # Get user's learning context
        user_recommendations = get_user_recommendations(user_id)
        available_categories = ["General", "PSPO1", "Verpleegkundig Rekenen"]
        
        # Create system message with context
        system_context = {
            "categories": available_categories,
            "performance_summary": self._summarize_performance(user_recommendations),
            "quiz_context": quiz_context or {}
        }
        
        system_prompt = format_prompt("chatbot_system", **system_context)
        
        # Create session
        session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            messages=[
                ChatMessage(
                    id=f"msg_{session_id}_0",
                    user_id="system",
                    role="system",
                    content=system_prompt,
                    timestamp=datetime.now(),
                    context=system_context
                )
            ],
            created_at=datetime.now(),
            last_activity=datetime.now(),
            context=system_context
        )
        
        self.sessions[session_id] = session
        
        # Send welcome message
        welcome_msg = await self._generate_welcome_message(user_id, user_recommendations)
        await self.add_message(session_id, "assistant", welcome_msg)
        
        logger.info(f"Started chat session {session_id} for user {user_id}")
        return session_id
    
    async def add_message(
        self, 
        session_id: str,
        role: str, 
        content: str,
        context: Dict[str, Any] = None
    ) -> ChatMessage:
        """Add a message to the chat session"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Chat session {session_id} not found")
        
        session = self.sessions[session_id]
        
        message = ChatMessage(
            id=f"msg_{session_id}_{len(session.messages)}",
            user_id=session.user_id if role == "user" else "assistant",
            role=role,
            content=content,
            timestamp=datetime.now(),
            context=context
        )
        
        session.messages.append(message)
        session.last_activity = datetime.now()
        
        return message
    
    async def get_ai_response(
        self, 
        session_id: str,
        user_message: str,
        context: Dict[str, Any] = None
    ) -> str:
        """Get AI response to user message"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Chat session {session_id} not found")
        
        # Add user message
        await self.add_message(session_id, "user", user_message, context)
        
        session = self.sessions[session_id]
        
        try:
            # Prepare conversation history for AI
            conversation = self._prepare_conversation_history(session)
            
            # Generate response
            if self.openai_client:
                response = await self._get_openai_response(conversation)
            elif self.anthropic_client:
                response = await self._get_anthropic_response(conversation)
            else:
                response = "I'm sorry, but the AI assistant is currently unavailable. Please try again later."
            
            # Add assistant response
            await self.add_message(session_id, "assistant", response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            error_response = "I'm experiencing some technical difficulties. Could you please rephrase your question?"
            await self.add_message(session_id, "assistant", error_response)
            return error_response
    
    async def _get_openai_response(self, conversation: List[Dict[str, str]]) -> str:
        """Get response from OpenAI"""
        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model=self.config.chatbot_model,
            messages=conversation,
            temperature=TEMPERATURE_SETTINGS["chatbot"],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    
    async def _get_anthropic_response(self, conversation: List[Dict[str, str]]) -> str:
        """Get response from Anthropic"""
        # Separate system message from conversation
        system_message = ""
        messages = []
        
        for msg in conversation:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                messages.append(msg)
        
        response = await asyncio.to_thread(
            self.anthropic_client.messages.create,
            model=self.config.anthropic_model,
            system=system_message,
            messages=messages,
            temperature=TEMPERATURE_SETTINGS["chatbot"],
            max_tokens=500
        )
        return response.content[0].text.strip()
    
    def _prepare_conversation_history(self, session: ChatSession) -> List[Dict[str, str]]:
        """Prepare conversation history for AI model"""
        conversation = []
        
        # Limit conversation length to avoid token limits
        recent_messages = session.messages[-self.config.max_conversation_length:]
        
        for msg in recent_messages:
            conversation.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return conversation
    
    def _summarize_performance(self, recommendations: List[Dict[str, Any]]) -> str:
        """Create a summary of user performance for context"""
        if not recommendations:
            return "New user - no performance history available"
        
        summaries = []
        for rec in recommendations:
            category = rec.get("category", "Unknown")
            action = rec.get("action", "continue")
            summaries.append(f"{category}: {action}")
        
        return "; ".join(summaries)
    
    async def _generate_welcome_message(
        self, 
        user_id: str,
        recommendations: List[Dict[str, Any]]
    ) -> str:
        """Generate personalized welcome message"""
        
        if not recommendations:
            return """👋 Hallo! Ik ben je AI study assistent. Ik kan je helpen met:

🤔 Uitleg bij moeilijke vragen
📚 Studietips en strategieën  
🎯 Persoonlijke leeradvies
❓ Vragen over quiz onderwerpen

Waar kan ik je mee helpen?"""

        # Personalize based on performance
        strong_areas = []
        weak_areas = []
        
        for rec in recommendations:
            if rec.get("action") == "advance":
                strong_areas.append(rec.get("category"))
            elif rec.get("action") in ["review", "practice_more"]:
                weak_areas.append(rec.get("category"))
        
        welcome = "👋 Welkom terug! Op basis van je prestaties zie ik dat:\n\n"
        
        if strong_areas:
            welcome += f"💪 Je doet het goed in: {', '.join(strong_areas)}\n"
        
        if weak_areas:
            welcome += f"📈 Je kunt verbeteren in: {', '.join(weak_areas)}\n"
        
        welcome += "\n🤖 Ik kan je helpen met uitleg, studietips en persoonlijk advies. Waar wil je aan werken?"
        
        return welcome
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get chat session history"""
        if session_id not in self.sessions:
            return []
        
        session = self.sessions[session_id]
        
        # Return messages excluding system message
        return [
            asdict(msg) for msg in session.messages 
            if msg.role != "system"
        ]
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old chat sessions"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        sessions_to_remove = [
            session_id for session_id, session in self.sessions.items()
            if session.last_activity < cutoff_time
        ]
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
            logger.info(f"Cleaned up old session: {session_id}")

class QuizSpecificAssistant:
    """Specialized assistant for quiz-specific help"""
    
    def __init__(self):
        self.chatbot = StudyAssistantChatbot()
    
    async def explain_question(
        self,
        question: str,
        choices: List[str],
        correct_answer: str,
        user_answer: str,
        category: str
    ) -> str:
        """Provide explanation for a specific question"""
        
        from question_generator import enhance_question_with_ai
        
        try:
            enhancement = await enhance_question_with_ai(
                question, choices, correct_answer, category, user_answer
            )
            return enhancement.get("explanation", "Unable to generate explanation")
            
        except Exception as e:
            logger.error(f"Error explaining question: {e}")
            return "I'm having trouble generating an explanation right now. Please try asking me directly!"
    
    async def get_study_tips(
        self,
        user_id: str,
        category: str,
        weak_topics: List[str]
    ) -> str:
        """Get personalized study tips"""
        
        tips_prompt = f"""
        Provide 3-5 specific study tips for improving in {category}, focusing on these weak areas: {', '.join(weak_topics)}.
        
        Make the tips:
        - Actionable and practical
        - Specific to the subject matter
        - Encouraging and motivational
        - Suitable for self-study
        
        Format as a numbered list.
        """
        
        try:
            if self.chatbot.openai_client:
                response = await asyncio.to_thread(
                    openai.chat.completions.create,
                    model=self.chatbot.config.openai_model,
                    messages=[{"role": "user", "content": tips_prompt}],
                    temperature=0.7,
                    max_tokens=400
                )
                return response.choices[0].message.content.strip()
            else:
                return self._get_default_study_tips(category, weak_topics)
                
        except Exception as e:
            logger.error(f"Error generating study tips: {e}")
            return self._get_default_study_tips(category, weak_topics)
    
    def _get_default_study_tips(self, category: str, weak_topics: List[str]) -> str:
        """Fallback study tips when AI is unavailable"""
        
        tips = f"📚 Study tips for {category}:\n\n"
        tips += "1. 📖 Review fundamentals before tackling complex topics\n"
        tips += "2. 🔄 Practice regularly with short, focused sessions\n"
        tips += "3. ✏️ Take notes on concepts you find challenging\n"
        tips += "4. 🎯 Focus extra attention on: " + ", ".join(weak_topics[:3]) + "\n"
        tips += "5. 💡 Try explaining concepts out loud to test understanding"
        
        return tips

# Global instances
study_assistant = StudyAssistantChatbot()
quiz_assistant = QuizSpecificAssistant()

# Convenience functions for API endpoints
async def start_chat(user_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Start a chat session and return session info"""
    session_id = await study_assistant.start_chat_session(user_id, context)
    
    return {
        "session_id": session_id,
        "status": "started",
        "messages": study_assistant.get_session_history(session_id)
    }

async def chat_with_assistant(
    session_id: str,
    message: str,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Send message to assistant and get response"""
    
    response = await study_assistant.get_ai_response(session_id, message, context)
    
    return {
        "response": response,
        "session_id": session_id,
        "messages": study_assistant.get_session_history(session_id)[-2:]  # Last 2 messages
    }

async def get_question_explanation(
    question: str,
    choices: List[str],
    correct_answer: str,
    user_answer: str,
    category: str
) -> Dict[str, Any]:
    """Get explanation for a quiz question"""
    
    explanation = await quiz_assistant.explain_question(
        question, choices, correct_answer, user_answer, category
    )
    
    return {
        "explanation": explanation,
        "question": question,
        "correct_answer": correct_answer,
        "user_answer": user_answer
    }