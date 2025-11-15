/**
 * AI Features JavaScript Module
 * Handles all AI-powered features including chatbot, question generation, and explanations
 */

class AIFeatures {
    constructor() {
        this.chatSession = null;
        this.isAIAvailable = false;
        this.init();
    }

    async init() {
        console.log('🤖 Initializing AI Features...');
        
        // Check AI availability
        await this.checkAIStatus();
        
        // Initialize chat interface
        this.initChatInterface();
        
        // Add AI features to quiz interface
        this.enhanceQuizWithAI();
        
        // Initialize question generator
        this.initQuestionGenerator();
    }

    async checkAIStatus() {
        try {
            const response = await fetch('/api/ai/status');
            const status = await response.json();
            this.isAIAvailable = status.ready;
            
            console.log('🤖 AI Status:', status);
            
            // Update UI based on status
            this.updateAIStatusIndicator(status);
            
        } catch (error) {
            console.warn('⚠️ AI features unavailable:', error);
            this.isAIAvailable = false;
        }
    }

    updateAIStatusIndicator(status) {
        let indicator = document.getElementById('ai-status-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'ai-status-indicator';
            indicator.className = 'ai-status';
            document.querySelector('.quiz-header')?.appendChild(indicator);
        }

        if (status.ready) {
            indicator.className = 'ai-status enabled';
            indicator.innerHTML = '🤖 AI Enabled';
        } else {
            indicator.className = 'ai-status disabled';
            indicator.innerHTML = '🤖 AI Disabled';
        }
    }

    initChatInterface() {
        // Create chat toggle button
        const toggleButton = document.createElement('button');
        toggleButton.className = 'ai-chat-toggle';
        toggleButton.innerHTML = '🤖';
        toggleButton.title = 'Open AI Study Assistant';
        toggleButton.onclick = () => this.toggleChat();
        document.body.appendChild(toggleButton);

        // Create chat container
        const chatContainer = document.createElement('div');
        chatContainer.className = 'ai-chat-container';
        chatContainer.innerHTML = this.createChatHTML();
        document.body.appendChild(chatContainer);

        // Add event listeners
        this.setupChatEventListeners();
    }

    createChatHTML() {
        return `
            <div class="ai-chat-header">
                <div class="ai-chat-title">🤖 AI Study Assistant</div>
                <button class="ai-chat-close" onclick="aiFeatures.toggleChat()">&times;</button>
            </div>
            <div class="ai-chat-messages" id="ai-chat-messages"></div>
            <div class="ai-chat-input-container">
                <textarea 
                    class="ai-chat-input" 
                    id="ai-chat-input" 
                    placeholder="Ask me anything about the quiz..."
                    rows="1"
                    ${!this.isAIAvailable ? 'disabled' : ''}
                ></textarea>
                <button 
                    class="ai-chat-send" 
                    id="ai-chat-send"
                    ${!this.isAIAvailable ? 'disabled' : ''}
                >
                    →
                </button>
            </div>
        `;
    }

    setupChatEventListeners() {
        const chatInput = document.getElementById('ai-chat-input');
        const sendButton = document.getElementById('ai-chat-send');

        if (chatInput && sendButton && this.isAIAvailable) {
            // Send message on Enter (but not Shift+Enter)
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // Auto-resize textarea
            chatInput.addEventListener('input', (e) => {
                e.target.style.height = 'auto';
                e.target.style.height = Math.min(e.target.scrollHeight, 80) + 'px';
            });

            sendButton.addEventListener('click', () => this.sendMessage());
        }
    }

    async toggleChat() {
        const chatContainer = document.querySelector('.ai-chat-container');
        const toggleButton = document.querySelector('.ai-chat-toggle');
        
        if (chatContainer.style.display === 'flex') {
            chatContainer.style.display = 'none';
            toggleButton.innerHTML = '🤖';
        } else {
            chatContainer.style.display = 'flex';
            toggleButton.innerHTML = '✕';
            
            // Start chat session if needed
            if (!this.chatSession && this.isAIAvailable) {
                await this.startChatSession();
            }
        }
    }

    async startChatSession() {
        try {
            this.addMessage('assistant', 'Starting AI assistant...', true);
            
            const response = await fetch('/api/ai/chat/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: this.getCurrentUserId(),
                    context: this.getQuizContext()
                })
            });

            const result = await response.json();
            this.chatSession = result.session_id;

            // Clear loading message and show welcome
            const messagesContainer = document.getElementById('ai-chat-messages');
            messagesContainer.innerHTML = '';
            
            // Display chat history
            if (result.messages && result.messages.length > 0) {
                result.messages.forEach(msg => {
                    if (msg.role !== 'system') {
                        this.addMessage(msg.role, msg.content);
                    }
                });
            }

        } catch (error) {
            console.error('Error starting chat:', error);
            this.addMessage('assistant', 'Sorry, I\'m having trouble connecting. Please try again later.');
        }
    }

    async sendMessage() {
        const input = document.getElementById('ai-chat-input');
        const message = input.value.trim();
        
        if (!message || !this.chatSession) return;

        // Add user message to chat
        this.addMessage('user', message);
        input.value = '';
        input.style.height = 'auto';

        // Show typing indicator
        const typingId = this.addMessage('assistant', 'AI is thinking...', true);

        try {
            const response = await fetch('/api/ai/chat/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.chatSession,
                    message: message,
                    context: this.getQuizContext()
                })
            });

            const result = await response.json();
            
            // Remove typing indicator
            document.getElementById(typingId)?.remove();
            
            // Add AI response
            this.addMessage('assistant', result.response);

        } catch (error) {
            console.error('Error sending message:', error);
            document.getElementById(typingId)?.remove();
            this.addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
        }
    }

    addMessage(role, content, isLoading = false) {
        const messagesContainer = document.getElementById('ai-chat-messages');
        const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${role}`;
        messageDiv.id = messageId;
        
        const avatar = document.createElement('div');
        avatar.className = 'ai-message-avatar';
        avatar.innerHTML = role === 'user' ? '👤' : '🤖';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'ai-message-content';
        
        if (isLoading) {
            contentDiv.innerHTML = `<span class="ai-loading">${content} <div class="ai-loading-spinner"></div></span>`;
        } else {
            contentDiv.innerHTML = content;
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return messageId;
    }

    enhanceQuizWithAI() {
        if (!this.isAIAvailable) return;

        // Add AI explanation button to quiz interface
        this.addAIExplanationFeature();
        
        // Add personalized recommendations
        this.addPersonalizedRecommendations();
    }

    addAIExplanationFeature() {
        // This will be called after a user answers a question
        const originalShowResult = window.showResult;
        
        window.showResult = (data) => {
            // Call original function
            if (originalShowResult) {
                originalShowResult(data);
            }

            // Add AI explanation button
            const resultContainer = document.querySelector('.result-container') || 
                                  document.querySelector('#result') ||
                                  document.querySelector('.quiz-container');
            
            if (resultContainer && this.isAIAvailable) {
                this.addExplanationButton(resultContainer, data);
            }
        };
    }

    addExplanationButton(container, questionData) {
        // Remove existing explanation button
        const existingButton = container.querySelector('.ai-explain-button');
        if (existingButton) existingButton.remove();

        const button = document.createElement('button');
        button.className = 'ai-explain-button ai-feature-button';
        button.innerHTML = '🤖 Get AI Explanation';
        button.onclick = () => this.explainQuestion(questionData);

        container.appendChild(button);
    }

    async explainQuestion(questionData) {
        try {
            const button = document.querySelector('.ai-explain-button');
            if (button) {
                button.disabled = true;
                button.innerHTML = '🤖 Generating explanation...';
            }

            const response = await fetch('/api/ai/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: questionData.question || questionData.text,
                    choices: questionData.choices || [],
                    correct_answer: questionData.correct_answer,
                    user_answer: questionData.user_answer,
                    category: this.getCurrentCategory()
                })
            });

            const result = await response.json();
            this.displayExplanation(result.explanation);

        } catch (error) {
            console.error('Error getting explanation:', error);
            this.displayExplanation('Sorry, I couldn\'t generate an explanation right now.');
        } finally {
            const button = document.querySelector('.ai-explain-button');
            if (button) {
                button.disabled = false;
                button.innerHTML = '🤖 Get AI Explanation';
            }
        }
    }

    displayExplanation(explanation) {
        // Remove existing explanation
        const existingExplanation = document.querySelector('.ai-explanation-container');
        if (existingExplanation) existingExplanation.remove();

        const explanationDiv = document.createElement('div');
        explanationDiv.className = 'ai-explanation-container';
        explanationDiv.innerHTML = `
            <div class="ai-explanation-header">
                🤖 AI Explanation
            </div>
            <div class="ai-explanation-text">${explanation}</div>
        `;

        // Add after result or in main container
        const resultContainer = document.querySelector('.result-container') || 
                              document.querySelector('#result') ||
                              document.querySelector('.quiz-container');
        
        if (resultContainer) {
            resultContainer.appendChild(explanationDiv);
        }
    }

    async addPersonalizedRecommendations() {
        // This would show recommendations based on user performance
        // For now, we'll add it to the main quiz interface
        if (!this.isAIAvailable) return;

        const userId = this.getCurrentUserId();
        const category = this.getCurrentCategory();

        try {
            const response = await fetch(`/api/ai/recommendations/${userId}?category=${category}`);
            const result = await response.json();
            
            if (result.recommendations && result.recommendations.length > 0) {
                this.displayRecommendations(result.recommendations);
            }

        } catch (error) {
            console.error('Error getting recommendations:', error);
        }
    }

    displayRecommendations(recommendations) {
        const container = document.querySelector('.quiz-header') || 
                         document.querySelector('.quiz-container');
        
        if (!container) return;

        // Remove existing recommendations
        const existing = container.querySelector('.ai-recommendations');
        if (existing) existing.remove();

        const recommendationsDiv = document.createElement('div');
        recommendationsDiv.className = 'ai-recommendations';
        recommendationsDiv.innerHTML = `
            <h4>🎯 Personalized Learning Recommendations</h4>
            ${recommendations.map(rec => `
                <div class="ai-recommendation-item">
                    <div class="ai-recommendation-action">${rec.action.replace('_', ' ')}</div>
                    <div class="ai-recommendation-reason">${rec.reason}</div>
                    <div class="ai-recommendation-topics">
                        ${rec.suggested_topics.map(topic => 
                            `<span class="ai-topic-tag">${topic}</span>`
                        ).join('')}
                    </div>
                </div>
            `).join('')}
        `;

        container.appendChild(recommendationsDiv);
    }

    initQuestionGenerator() {
        // Add question generator to admin or main interface
        if (!this.isAIAvailable) return;

        this.addQuestionGeneratorUI();
    }

    addQuestionGeneratorUI() {
        // Check if we're on admin page or main page
        const targetContainer = document.querySelector('.admin-container') || 
                               document.querySelector('.quiz-container');
        
        if (!targetContainer) return;

        const generatorDiv = document.createElement('div');
        generatorDiv.className = 'ai-question-generator';
        generatorDiv.innerHTML = `
            <h3>🤖 AI Question Generator</h3>
            <div class="ai-generator-form">
                <div class="ai-form-group">
                    <label class="ai-form-label">Category:</label>
                    <select class="ai-form-select" id="ai-gen-category">
                        <option value="general">General Knowledge</option>
                        <option value="PSPO1">PSPO1 Scrum</option>
                        <option value="Verpleegkundig Rekenen">Nursing Calculations</option>
                    </select>
                </div>
                <div class="ai-form-group">
                    <label class="ai-form-label">Difficulty:</label>
                    <select class="ai-form-select" id="ai-gen-difficulty">
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                        <option value="expert">Expert</option>
                    </select>
                </div>
                <div class="ai-form-group">
                    <label class="ai-form-label">Number of Questions:</label>
                    <input type="number" class="ai-form-input" id="ai-gen-count" min="1" max="10" value="5">
                </div>
                <button class="ai-generate-button" onclick="aiFeatures.generateQuestions()">
                    🤖 Generate Questions
                </button>
            </div>
            <div id="ai-generated-questions"></div>
        `;

        targetContainer.appendChild(generatorDiv);
    }

    async generateQuestions() {
        const category = document.getElementById('ai-gen-category').value;
        const difficulty = document.getElementById('ai-gen-difficulty').value;
        const count = parseInt(document.getElementById('ai-gen-count').value);
        
        const button = document.querySelector('.ai-generate-button');
        const resultsDiv = document.getElementById('ai-generated-questions');
        
        try {
            button.disabled = true;
            button.innerHTML = '🤖 Generating...';
            resultsDiv.innerHTML = '<div class="ai-loading">Generating questions... <div class="ai-loading-spinner"></div></div>';

            const response = await fetch('/api/ai/generate-questions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category, difficulty, count })
            });

            const result = await response.json();
            
            if (result.success) {
                this.displayGeneratedQuestions(result.questions);
            } else {
                resultsDiv.innerHTML = '<div class="error">Failed to generate questions</div>';
            }

        } catch (error) {
            console.error('Error generating questions:', error);
            resultsDiv.innerHTML = '<div class="error">Error generating questions</div>';
        } finally {
            button.disabled = false;
            button.innerHTML = '🤖 Generate Questions';
        }
    }

    displayGeneratedQuestions(questions) {
        const resultsDiv = document.getElementById('ai-generated-questions');
        
        resultsDiv.innerHTML = `
            <h4>Generated Questions (${questions.length})</h4>
            <div class="generated-questions-list">
                ${questions.map((q, index) => `
                    <div class="ai-feature-card">
                        <div class="ai-feature-title">Question ${index + 1}</div>
                        <div><strong>Q:</strong> ${q.text}</div>
                        <div><strong>Choices:</strong> ${q.choices.join(', ')}</div>
                        <div><strong>Answer:</strong> ${q.correct_answer}</div>
                        <div><strong>Difficulty:</strong> ${q.difficulty}</div>
                        <div><strong>Topic:</strong> ${q.topic}</div>
                        ${q.explanation ? `<div><strong>Explanation:</strong> ${q.explanation}</div>` : ''}
                        <div><strong>Confidence:</strong> ${(q.confidence * 100).toFixed(1)}%</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Utility functions
    getCurrentUserId() {
        // In a real app, get from session/auth
        return localStorage.getItem('quiz_user_id') || 'anonymous_' + Date.now();
    }

    getCurrentCategory() {
        // Try to detect current category from URL or quiz state
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('category') || 'general';
    }

    getQuizContext() {
        return {
            current_category: this.getCurrentCategory(),
            user_id: this.getCurrentUserId(),
            page: window.location.pathname
        };
    }
}

// Initialize AI features when page loads
let aiFeatures;

document.addEventListener('DOMContentLoaded', () => {
    aiFeatures = new AIFeatures();
    console.log('🤖 AI Features initialized');
});

// Expose for global access
window.aiFeatures = aiFeatures;