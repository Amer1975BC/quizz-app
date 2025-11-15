"""
Test Suite for AI Features
Comprehensive tests for question generation, personalized learning, and chatbot
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock dependencies for testing
class MockOpenAI:
    def __init__(self):
        self.chat = Mock()
        self.chat.completions = Mock()
        self.chat.completions.create = Mock(return_value=Mock(
            choices=[Mock(message=Mock(content="Test response"))]
        ))

class MockAnthropic:
    def __init__(self):
        self.messages = Mock()
        self.messages.create = Mock(return_value=Mock(
            content=[Mock(text="Test response")]
        ))

# Test Configuration
@pytest.fixture
def mock_ai_config():
    """Mock AI configuration for testing"""
    with patch('ai_config.get_ai_config') as mock_config:
        config = Mock()
        config.openai_api_key = "test_key"
        config.anthropic_api_key = "test_key"
        config.openai_model = "gpt-3.5-turbo"
        config.anthropic_model = "claude-3-sonnet"
        config.enable_question_generation = True
        config.enable_personalized_learning = True
        config.chatbot_enabled = True
        config.default_provider = Mock()
        config.default_provider.value = "openai"
        mock_config.return_value = config
        yield config

@pytest.fixture
def mock_openai():
    """Mock OpenAI client"""
    with patch('openai.chat.completions.create') as mock_create:
        response_content = json.dumps({
            "questions": [{
                "text": "What is 2+2?",
                "choices": ["A. 3", "B. 4", "C. 5", "D. 6"],
                "correct_answer": "B",
                "explanation": "Basic arithmetic",
                "difficulty": "beginner", 
                "category": "math",
                "topic": "Addition"
            }]
        })
        mock_create.return_value = Mock(
            choices=[Mock(message=Mock(content=response_content))]
        )
        yield mock_create

class TestQuestionGenerator:
    """Test AI question generation"""
    
    @pytest.mark.asyncio
    async def test_generate_questions(self, mock_ai_config, mock_openai):
        """Test basic question generation"""
        from question_generator import QuestionGenerator, DifficultyLevel
        
        generator = QuestionGenerator()
        
        questions = await generator.generate_questions(
            category="math",
            count=1,
            difficulty=DifficultyLevel.BEGINNER
        )
        
        assert len(questions) == 1
        assert questions[0].text == "What is 2+2?"
        assert len(questions[0].choices) == 4
        assert questions[0].correct_answer == "B"
        assert questions[0].category == "math"
    
    @pytest.mark.asyncio
    async def test_invalid_response_handling(self, mock_ai_config):
        """Test handling of invalid AI responses"""
        from question_generator import QuestionGenerator, DifficultyLevel
        
        with patch('openai.chat.completions.create') as mock_create:
            mock_create.return_value = Mock(
                choices=[Mock(message=Mock(content="Invalid JSON response"))]
            )
            
            generator = QuestionGenerator()
            
            with pytest.raises(ValueError, match="Failed to parse AI response"):
                await generator.generate_questions(
                    category="test",
                    count=1,
                    difficulty=DifficultyLevel.BEGINNER
                )
    
    def test_question_validation(self, mock_ai_config):
        """Test question validation logic"""
        from question_generator import QuestionGenerator, GeneratedQuestion
        
        generator = QuestionGenerator()
        
        # Valid question
        valid_q = GeneratedQuestion(
            text="Test question?",
            choices=["A. Option 1", "B. Option 2"],
            correct_answer="A",
            explanation="Test explanation",
            difficulty="beginner",
            category="test",
            topic="testing"
        )
        assert generator._validate_question(valid_q) == True
        
        # Invalid question (no choices)
        invalid_q = GeneratedQuestion(
            text="Test question?",
            choices=[],
            correct_answer="A",
            explanation="Test explanation",
            difficulty="beginner",
            category="test",
            topic="testing"
        )
        assert generator._validate_question(invalid_q) == False

class TestPersonalizedLearning:
    """Test personalized learning engine"""
    
    def test_performance_analysis(self):
        """Test user performance analysis"""
        from personalized_learning import LearningAnalytics
        
        analytics = LearningAnalytics()
        performance = analytics.analyze_user_performance("test_user", "general")
        
        assert "general" in performance
        assert performance["general"].user_id == "test_user"
        assert performance["general"].category == "general"
        assert performance["general"].total_questions > 0
    
    def test_difficulty_estimation(self):
        """Test difficulty level estimation"""
        from personalized_learning import LearningAnalytics
        
        analytics = LearningAnalytics()
        
        # Test different accuracy levels
        assert analytics._estimate_difficulty_level(0.95, 0.95) == 5  # Expert
        assert analytics._estimate_difficulty_level(0.85, 0.85) == 4  # Advanced
        assert analytics._estimate_difficulty_level(0.75, 0.75) == 3  # Intermediate
        assert analytics._estimate_difficulty_level(0.65, 0.65) == 2  # Beginner+
        assert analytics._estimate_difficulty_level(0.45, 0.45) == 1  # Beginner
    
    def test_learning_velocity_calculation(self):
        """Test learning velocity calculation"""
        from personalized_learning import LearningAnalytics
        
        analytics = LearningAnalytics()
        
        # Improving scores
        improving_scores = [0.6, 0.65, 0.7, 0.75, 0.8]
        velocity = analytics._calculate_learning_velocity(improving_scores)
        assert velocity > 0  # Positive trend
        
        # Declining scores
        declining_scores = [0.8, 0.75, 0.7, 0.65, 0.6]
        velocity = analytics._calculate_learning_velocity(declining_scores)
        assert velocity < 0  # Negative trend
    
    def test_recommendations_generation(self):
        """Test learning recommendations"""
        from personalized_learning import PersonalizedRecommendationEngine
        
        engine = PersonalizedRecommendationEngine()
        recommendations = engine.get_learning_recommendations("test_user")
        
        assert len(recommendations) > 0
        assert all(rec.user_id == "test_user" for rec in recommendations)
        assert all(rec.action in ["review", "practice_more", "advance", "break"] for rec in recommendations)

class TestAIChatbot:
    """Test AI chatbot functionality"""
    
    @pytest.mark.asyncio
    async def test_start_chat_session(self, mock_ai_config):
        """Test starting a chat session"""
        from ai_chatbot import StudyAssistantChatbot
        
        chatbot = StudyAssistantChatbot()
        
        with patch.object(chatbot, '_generate_welcome_message', return_value="Welcome!"):
            session_id = await chatbot.start_chat_session("test_user")
            
            assert session_id.startswith("chat_test_user_")
            assert session_id in chatbot.sessions
            assert len(chatbot.sessions[session_id].messages) >= 1
    
    @pytest.mark.asyncio
    async def test_ai_response_generation(self, mock_ai_config):
        """Test AI response generation"""
        from ai_chatbot import StudyAssistantChatbot
        
        chatbot = StudyAssistantChatbot()
        
        # Start session
        session_id = await chatbot.start_chat_session("test_user")
        
        # Mock AI response
        with patch.object(chatbot, '_get_openai_response', return_value="Test AI response"):
            response = await chatbot.get_ai_response(session_id, "Test message")
            
            assert response == "Test AI response"
            assert len(chatbot.sessions[session_id].messages) >= 2  # System + welcome + user + assistant
    
    def test_conversation_history_limiting(self, mock_ai_config):
        """Test conversation history limiting"""
        from ai_chatbot import StudyAssistantChatbot, ChatSession, ChatMessage
        from datetime import datetime
        
        chatbot = StudyAssistantChatbot()
        chatbot.config.max_conversation_length = 3
        
        # Create session with many messages
        session = ChatSession(
            session_id="test_session",
            user_id="test_user",
            messages=[
                ChatMessage("1", "test_user", "user", f"Message {i}", datetime.now())
                for i in range(10)
            ],
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        conversation = chatbot._prepare_conversation_history(session)
        assert len(conversation) <= 3

class TestQuestionEnhancement:
    """Test question enhancement features"""
    
    @pytest.mark.asyncio
    async def test_explanation_generation(self, mock_ai_config, mock_openai):
        """Test AI explanation generation"""
        from question_generator import QuestionEnhancer
        
        enhancer = QuestionEnhancer()
        
        explanation = await enhancer.generate_explanation(
            question="What is 2+2?",
            choices=["A. 3", "B. 4", "C. 5", "D. 6"],
            correct_answer="B",
            user_answer="A"
        )
        
        assert isinstance(explanation, str)
        assert len(explanation) > 0
    
    @pytest.mark.asyncio
    async def test_difficulty_assessment(self, mock_ai_config):
        """Test AI difficulty assessment"""
        from question_generator import QuestionEnhancer
        
        with patch('openai.chat.completions.create') as mock_create:
            mock_create.return_value = Mock(
                choices=[Mock(message=Mock(content=json.dumps({
                    "difficulty": 3,
                    "reasoning": "Medium complexity question",
                    "concepts": ["arithmetic", "basic math"],
                    "prerequisites": ["number sense"]
                })))]
            )
            
            enhancer = QuestionEnhancer()
            
            difficulty, reasoning = await enhancer.assess_difficulty(
                question="What is 2+2?",
                choices=["A. 3", "B. 4", "C. 5", "D. 6"],
                category="math"
            )
            
            assert difficulty == 3
            assert "Medium complexity" in reasoning

class TestAIIntegration:
    """Test AI integration with main application"""
    
    def test_ai_availability_check(self):
        """Test AI availability detection"""
        from ai_config import validate_ai_setup
        
        # Mock environment variables
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test_key',
            'ANTHROPIC_API_KEY': 'test_key'
        }):
            status = validate_ai_setup()
            
            assert 'openai_available' in status
            assert 'anthropic_available' in status
            assert 'features_enabled' in status
            assert 'ready' in status
    
    @pytest.mark.asyncio
    async def test_convenience_functions(self, mock_ai_config, mock_openai):
        """Test convenience functions for API endpoints"""
        from question_generator import generate_questions_for_category
        
        questions = await generate_questions_for_category("math", 1, "beginner")
        
        assert len(questions) == 1
        assert questions[0]['generated_by_ai'] == True
        assert 'confidence' in questions[0]

class TestErrorHandling:
    """Test error handling in AI features"""
    
    @pytest.mark.asyncio
    async def test_openai_api_error_handling(self, mock_ai_config):
        """Test handling of OpenAI API errors"""
        from question_generator import QuestionGenerator, DifficultyLevel
        
        with patch('openai.chat.completions.create', side_effect=Exception("API Error")):
            generator = QuestionGenerator()
            
            with pytest.raises(Exception):
                await generator.generate_questions(
                    category="test",
                    count=1,
                    difficulty=DifficultyLevel.BEGINNER
                )
    
    @pytest.mark.asyncio
    async def test_chatbot_error_recovery(self, mock_ai_config):
        """Test chatbot error recovery"""
        from ai_chatbot import StudyAssistantChatbot
        
        chatbot = StudyAssistantChatbot()
        session_id = await chatbot.start_chat_session("test_user")
        
        # Mock API error
        with patch.object(chatbot, '_get_openai_response', side_effect=Exception("API Error")):
            response = await chatbot.get_ai_response(session_id, "Test message")
            
            assert "technical difficulties" in response.lower()

class TestPerformanceAndScaling:
    """Test performance and scaling aspects"""
    
    def test_large_conversation_handling(self, mock_ai_config):
        """Test handling of large conversation histories"""
        from ai_chatbot import StudyAssistantChatbot, ChatSession, ChatMessage
        from datetime import datetime
        
        chatbot = StudyAssistantChatbot()
        
        # Create session with maximum messages
        large_session = ChatSession(
            session_id="large_session",
            user_id="test_user", 
            messages=[
                ChatMessage(str(i), "test_user", "user", f"Message {i}", datetime.now())
                for i in range(100)  # Large conversation
            ],
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        conversation = chatbot._prepare_conversation_history(large_session)
        
        # Should limit to max_conversation_length
        assert len(conversation) <= chatbot.config.max_conversation_length
    
    @pytest.mark.asyncio
    async def test_concurrent_question_generation(self, mock_ai_config, mock_openai):
        """Test concurrent question generation"""
        from question_generator import generate_questions_for_category
        
        # Generate questions concurrently
        tasks = [
            generate_questions_for_category("math", 2, "beginner")
            for _ in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        assert all(len(questions) == 2 for questions in results)

# Performance benchmarks
class TestPerformanceBenchmarks:
    """Performance benchmarks for AI features"""
    
    @pytest.mark.asyncio
    async def test_question_generation_speed(self, mock_ai_config, mock_openai):
        """Benchmark question generation speed"""
        from question_generator import generate_questions_for_category
        import time
        
        start_time = time.time()
        questions = await generate_questions_for_category("math", 5, "beginner")
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within reasonable time (mocked, so should be very fast)
        assert generation_time < 1.0  # 1 second for mocked responses
        assert len(questions) == 5

# Integration tests
class TestEndToEndIntegration:
    """End-to-end integration tests"""
    
    @pytest.mark.asyncio
    async def test_complete_ai_workflow(self, mock_ai_config, mock_openai):
        """Test complete AI workflow from generation to explanation"""
        from question_generator import generate_questions_for_category, enhance_question_with_ai
        
        # 1. Generate questions
        questions = await generate_questions_for_category("math", 1, "beginner")
        assert len(questions) == 1
        
        question = questions[0]
        
        # 2. Enhance with explanation
        enhancement = await enhance_question_with_ai(
            question['text'],
            question['choices'],
            question['correct_answer'],
            "math"
        )
        
        assert 'explanation' in enhancement
        assert 'difficulty_score' in enhancement

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])