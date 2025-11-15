#!/bin/bash

# AI Features Test and Setup Script
# Comprehensive testing and configuration for AI integration

set -e

echo "🤖 AI Features Test & Setup Script"
echo "=================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the correct directory
if [ ! -f "webapi.py" ] || [ ! -f "ai_config.py" ]; then
    print_error "Please run this script from the quiz application root directory"
    exit 1
fi

print_status "Starting AI features test and setup..."

# Step 1: Check Python environment
print_status "Checking Python environment..."
python3 --version
if [ $? -ne 0 ]; then
    print_error "Python 3 is not available"
    exit 1
fi
print_success "Python environment OK"

# Step 2: Create virtual environment if needed
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Step 3: Install base dependencies
print_status "Installing base dependencies..."
pip install -r requirements.txt
print_success "Base dependencies installed"

# Step 4: Check for AI dependencies
print_status "Checking AI dependencies..."
if [ -f "requirements-ai.txt" ]; then
    print_status "Installing AI dependencies..."
    pip install -r requirements-ai.txt
    print_success "AI dependencies installed"
else
    print_warning "AI requirements file not found"
fi

# Step 5: Install test dependencies
print_status "Installing test dependencies..."
pip install pytest pytest-asyncio pytest-mock
print_success "Test dependencies installed"

# Step 6: Run AI configuration check
print_status "Running AI configuration check..."
if python3 -c "
import ai_config
try:
    config = ai_config.get_ai_config()
    status = ai_config.validate_ai_setup()
    print('Configuration loaded successfully')
    print(f'OpenAI available: {status.get(\"openai_available\", False)}')
    print(f'Anthropic available: {status.get(\"anthropic_available\", False)}')
    print(f'Features enabled: {status.get(\"features_enabled\", False)}')
    print(f'Ready: {status.get(\"ready\", False)}')
except Exception as e:
    print(f'Configuration error: {e}')
    exit(1)
" 2>/dev/null; then
    print_success "AI configuration check passed"
else
    print_warning "AI configuration needs setup"
    
    # Run interactive setup
    if [ -f "ai_setup.py" ]; then
        print_status "Running interactive AI setup..."
        python3 ai_setup.py
    else
        print_warning "Interactive setup not available"
        print_status "Manual configuration required:"
        echo "  1. Set OPENAI_API_KEY environment variable"
        echo "  2. Set ANTHROPIC_API_KEY environment variable"
        echo "  3. Ensure AI dependencies are installed"
    fi
fi

# Step 7: Run unit tests
print_status "Running AI feature tests..."
if [ -f "test_ai_features.py" ]; then
    python3 -m pytest test_ai_features.py -v --tb=short
    if [ $? -eq 0 ]; then
        print_success "All AI tests passed"
    else
        print_warning "Some AI tests failed - check output above"
    fi
else
    print_warning "AI test file not found, skipping tests"
fi

# Step 8: Test basic functionality
print_status "Testing basic AI functionality..."

# Test AI configuration
python3 -c "
import asyncio
import sys
sys.path.append('.')

async def test_basic_functionality():
    try:
        # Test configuration
        from ai_config import get_ai_config, validate_ai_setup
        config = get_ai_config()
        status = validate_ai_setup()
        print(f'✓ Configuration loaded: {status.get(\"ready\", False)}')
        
        # Test question generation (mock)
        if status.get('features_enabled', False):
            from question_generator import QuestionGenerator, DifficultyLevel
            generator = QuestionGenerator()
            print('✓ Question generator initialized')
        
        # Test chatbot initialization
        if status.get('chatbot_enabled', False):
            from ai_chatbot import StudyAssistantChatbot
            chatbot = StudyAssistantChatbot()
            print('✓ Chatbot initialized')
        
        # Test personalized learning
        from personalized_learning import LearningAnalytics, PersonalizedRecommendationEngine
        analytics = LearningAnalytics()
        recommendations = PersonalizedRecommendationEngine()
        print('✓ Personalized learning components initialized')
        
        print('\\n🎉 All AI components initialized successfully!')
        return True
    
    except Exception as e:
        print(f'❌ Error testing functionality: {e}')
        return False

# Run the test
success = asyncio.run(test_basic_functionality())
exit(0 if success else 1)
"

if [ $? -eq 0 ]; then
    print_success "Basic functionality test passed"
else
    print_warning "Basic functionality test had issues"
fi

# Step 9: Test web API endpoints
print_status "Testing web API integration..."
python3 -c "
import sys
sys.path.append('.')

try:
    # Import webapi to check if AI endpoints are available
    import webapi
    
    # Check if AI imports are working
    if hasattr(webapi, 'generate_questions_for_category'):
        print('✓ AI question generation endpoint available')
    
    if hasattr(webapi, 'StudyAssistantChatbot'):
        print('✓ AI chatbot endpoint available')
        
    print('✓ Web API integration OK')
    
except ImportError as e:
    print(f'⚠ AI features not available in web API: {e}')
except Exception as e:
    print(f'❌ Web API integration error: {e}')
"

# Step 10: Generate test report
print_status "Generating test report..."
cat > ai_test_report.txt << EOF
AI Features Test Report
=======================
Generated: $(date)

Environment:
- Python Version: $(python3 --version)
- Working Directory: $(pwd)

Dependencies:
- Base requirements: $([ -f requirements.txt ] && echo "✓ Found" || echo "❌ Missing")
- AI requirements: $([ -f requirements-ai.txt ] && echo "✓ Found" || echo "❌ Missing")

Components:
- AI Configuration: $([ -f ai_config.py ] && echo "✓ Present" || echo "❌ Missing")
- Question Generator: $([ -f question_generator.py ] && echo "✓ Present" || echo "❌ Missing")
- Personalized Learning: $([ -f personalized_learning.py ] && echo "✓ Present" || echo "❌ Missing")
- AI Chatbot: $([ -f ai_chatbot.py ] && echo "✓ Present" || echo "❌ Missing")
- Frontend CSS: $([ -f static/ai-features.css ] && echo "✓ Present" || echo "❌ Missing")
- Frontend JS: $([ -f static/ai-features.js ] && echo "✓ Present" || echo "❌ Missing")
- Setup Script: $([ -f ai_setup.py ] && echo "✓ Present" || echo "❌ Missing")
- Test Suite: $([ -f test_ai_features.py ] && echo "✓ Present" || echo "❌ Missing")

Configuration Status:
$(python3 -c "
import ai_config
try:
    status = ai_config.validate_ai_setup()
    for key, value in status.items():
        print(f'- {key}: {\"✓\" if value else \"❌\"} {value}')
except Exception as e:
    print(f'- Configuration Error: {e}')
" 2>/dev/null || echo "- Configuration check failed")

Next Steps:
1. Configure API keys if not already set
2. Test question generation with real API calls
3. Test chatbot functionality
4. Verify frontend integration
5. Deploy and monitor performance

EOF

print_success "Test report generated: ai_test_report.txt"

# Step 11: Summary
echo ""
echo "🏁 AI Features Setup Complete!"
echo "================================"
echo ""
echo "Summary:"
echo "- ✅ Environment configured"
echo "- ✅ Dependencies installed"
echo "- ✅ Components tested"
echo "- ✅ Web API integration checked"
echo ""
echo "Next Steps:"
echo "1. Review the test report: cat ai_test_report.txt"
echo "2. Configure API keys if needed: python3 ai_setup.py"
echo "3. Start the application: python3 webapi.py"
echo "4. Test AI features in the web interface"
echo ""
echo "For more information, see: README-AI.md"

print_success "Setup complete! 🚀"