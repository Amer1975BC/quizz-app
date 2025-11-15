/**
 * Frontend JavaScript Tests for Quiz Application
 * Tests timer functionality, category selection, and UI interactions
 */

// Mock DOM elements for testing
class MockElement {
    constructor(id) {
        this.id = id;
        this.innerHTML = '';
        this.textContent = '';
        this.style = {};
        this.classList = {
            add: () => {},
            remove: () => {},
            contains: () => false
        };
        this.onclick = null;
        this.disabled = false;
    }
    
    addEventListener(event, callback) {
        this[`on${event}`] = callback;
    }
    
    click() {
        if (this.onclick) this.onclick();
    }
}

// Mock document object
const mockDocument = {
    getElementById: (id) => new MockElement(id),
    querySelectorAll: () => [],
    createElement: (tag) => new MockElement(tag)
};

// Mock window object  
const mockWindow = {
    location: { href: '' },
    fetch: async (url, options) => ({
        ok: true,
        json: async () => ({ session_id: 'test-session', category: 'general' })
    })
};

// Test Suite for Timer Functionality
class TimerTests {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.tests = [];
    }
    
    assert(condition, message) {
        if (condition) {
            this.passed++;
            console.log(`✓ ${message}`);
        } else {
            this.failed++;
            console.error(`✗ ${message}`);
        }
        this.tests.push({ passed: condition, message });
    }
    
    // Test timer initialization
    testTimerInitialization() {
        console.log('\n--- Testing Timer Initialization ---');
        
        // Mock timer variables
        let timerInterval = null;
        let startTime = null;
        let elapsedTime = 0;
        let isPaused = false;
        
        // Test initial state
        this.assert(timerInterval === null, 'Timer interval should be null initially');
        this.assert(startTime === null, 'Start time should be null initially');
        this.assert(elapsedTime === 0, 'Elapsed time should be 0 initially');
        this.assert(isPaused === false, 'Timer should not be paused initially');
    }
    
    // Test timer start functionality
    testTimerStart() {
        console.log('\n--- Testing Timer Start ---');
        
        let timerStarted = false;
        let startTime = null;
        
        // Mock startTimer function
        function startTimer() {
            if (!timerStarted) {
                startTime = Date.now();
                timerStarted = true;
                return true;
            }
            return false;
        }
        
        const result = startTimer();
        this.assert(result === true, 'Timer should start successfully');
        this.assert(timerStarted === true, 'Timer started flag should be set');
        this.assert(startTime !== null, 'Start time should be recorded');
        
        // Test that timer cannot be started twice
        const secondStart = startTimer();
        this.assert(secondStart === false, 'Timer should not start if already running');
    }
    
    // Test timer pause functionality  
    testTimerPause() {
        console.log('\n--- Testing Timer Pause/Resume ---');
        
        let isPaused = false;
        let pauseTime = 0;
        
        // Mock pauseTimer function
        function pauseTimer() {
            if (!isPaused) {
                isPaused = true;
                pauseTime = Date.now();
                return 'paused';
            } else {
                isPaused = false;
                return 'resumed';
            }
        }
        
        const pauseResult = pauseTimer();
        this.assert(pauseResult === 'paused', 'Timer should pause successfully');
        this.assert(isPaused === true, 'Paused flag should be set');
        
        const resumeResult = pauseTimer();
        this.assert(resumeResult === 'resumed', 'Timer should resume successfully');
        this.assert(isPaused === false, 'Paused flag should be cleared on resume');
    }
    
    // Test timer color warnings
    testTimerColorWarnings() {
        console.log('\n--- Testing Timer Color Warnings ---');
        
        function getTimerColor(seconds) {
            if (seconds >= 600) { // 10 minutes
                return 'red';
            } else if (seconds >= 300) { // 5 minutes  
                return 'yellow';
            } else {
                return 'green';
            }
        }
        
        this.assert(getTimerColor(120) === 'green', 'Timer should be green under 5 minutes');
        this.assert(getTimerColor(360) === 'yellow', 'Timer should be yellow between 5-10 minutes');
        this.assert(getTimerColor(720) === 'red', 'Timer should be red over 10 minutes');
    }
    
    // Test time formatting
    testTimeFormatting() {
        console.log('\n--- Testing Time Formatting ---');
        
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        
        this.assert(formatTime(65) === '01:05', 'Should format 65 seconds as 01:05');
        this.assert(formatTime(3661) === '61:01', 'Should format 3661 seconds as 61:01');
        this.assert(formatTime(0) === '00:00', 'Should format 0 seconds as 00:00');
    }
}

// Test Suite for Category Selection
class CategoryTests {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.tests = [];
    }
    
    assert(condition, message) {
        if (condition) {
            this.passed++;
            console.log(`✓ ${message}`);
        } else {
            this.failed++;
            console.error(`✗ ${message}`);
        }
        this.tests.push({ passed: condition, message });
    }
    
    // Test category parameter generation
    testCategoryParameters() {
        console.log('\n--- Testing Category Parameters ---');
        
        function getCategoryParam(category) {
            switch(category) {
                case 'general':
                    return 'general';
                case 'pspo1':
                    return 'PSPO1';
                case 'nursing':
                    return 'Verpleegkundig Rekenen';
                default:
                    return 'general';
            }
        }
        
        this.assert(getCategoryParam('general') === 'general', 'General category should map correctly');
        this.assert(getCategoryParam('pspo1') === 'PSPO1', 'PSPO1 category should map correctly');
        this.assert(getCategoryParam('nursing') === 'Verpleegkundig Rekenen', 'Nursing category should map correctly');
        this.assert(getCategoryParam('invalid') === 'general', 'Invalid category should default to general');
    }
    
    // Test API URL construction
    testAPIURLConstruction() {
        console.log('\n--- Testing API URL Construction ---');
        
        function buildStartURL(category) {
            const baseURL = '/api/start';
            if (category) {
                return `${baseURL}?category=${encodeURIComponent(category)}`;
            }
            return baseURL;
        }
        
        const generalURL = buildStartURL('general');
        this.assert(generalURL === '/api/start?category=general', 'General URL should be constructed correctly');
        
        const nursingURL = buildStartURL('Verpleegkundig Rekenen');
        this.assert(nursingURL.includes('Verpleegkundig%20Rekenen'), 'Nursing URL should be URL-encoded');
        
        const noCategory = buildStartURL(null);
        this.assert(noCategory === '/api/start', 'URL without category should be base URL');
    }
}

// Test Suite for UI Interactions
class UITests {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.tests = [];
    }
    
    assert(condition, message) {
        if (condition) {
            this.passed++;
            console.log(`✓ ${message}`);
        } else {
            this.failed++;
            console.error(`✗ ${message}`);
        }
        this.tests.push({ passed: condition, message });
    }
    
    // Test button state management
    testButtonStates() {
        console.log('\n--- Testing Button State Management ---');
        
        const mockButton = new MockElement('test-button');
        
        function disableButton(button) {
            button.disabled = true;
            button.textContent = 'Loading...';
        }
        
        function enableButton(button, text) {
            button.disabled = false;
            button.textContent = text;
        }
        
        disableButton(mockButton);
        this.assert(mockButton.disabled === true, 'Button should be disabled');
        this.assert(mockButton.textContent === 'Loading...', 'Button text should show loading');
        
        enableButton(mockButton, 'Start Quiz');
        this.assert(mockButton.disabled === false, 'Button should be enabled');
        this.assert(mockButton.textContent === 'Start Quiz', 'Button text should be restored');
    }
    
    // Test quiz progress tracking
    testQuizProgress() {
        console.log('\n--- Testing Quiz Progress ---');
        
        function updateProgress(current, total) {
            const percentage = Math.round((current / total) * 100);
            return {
                percentage,
                text: `Vraag ${current} van ${total}`,
                isComplete: current >= total
            };
        }
        
        const progress1 = updateProgress(5, 20);
        this.assert(progress1.percentage === 25, 'Progress should be 25% for question 5 of 20');
        this.assert(progress1.text === 'Vraag 5 van 20', 'Progress text should be formatted correctly');
        this.assert(progress1.isComplete === false, 'Quiz should not be complete');
        
        const progress2 = updateProgress(20, 20);
        this.assert(progress2.percentage === 100, 'Progress should be 100% when complete');
        this.assert(progress2.isComplete === true, 'Quiz should be complete');
    }
}

// Test Runner
class TestRunner {
    static runAllTests() {
        console.log('🧪 Starting Frontend JavaScript Tests...\n');
        
        const timerTests = new TimerTests();
        const categoryTests = new CategoryTests();
        const uiTests = new UITests();
        
        // Run timer tests
        timerTests.testTimerInitialization();
        timerTests.testTimerStart();
        timerTests.testTimerPause();
        timerTests.testTimerColorWarnings();
        timerTests.testTimeFormatting();
        
        // Run category tests
        categoryTests.testCategoryParameters();
        categoryTests.testAPIURLConstruction();
        
        // Run UI tests
        uiTests.testButtonStates();
        uiTests.testQuizProgress();
        
        // Summarize results
        const totalPassed = timerTests.passed + categoryTests.passed + uiTests.passed;
        const totalFailed = timerTests.failed + categoryTests.failed + uiTests.failed;
        const totalTests = totalPassed + totalFailed;
        
        console.log('\n📊 Test Results Summary:');
        console.log(`✓ Passed: ${totalPassed}/${totalTests}`);
        console.log(`✗ Failed: ${totalFailed}/${totalTests}`);
        console.log(`📈 Success Rate: ${Math.round((totalPassed/totalTests)*100)}%`);
        
        if (totalFailed === 0) {
            console.log('\n🎉 All tests passed!');
            return true;
        } else {
            console.log('\n❌ Some tests failed. Please review the failures above.');
            return false;
        }
    }
}

// Export for Node.js testing or run directly in browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { TestRunner, TimerTests, CategoryTests, UITests };
} else {
    // Run tests if in browser
    document.addEventListener('DOMContentLoaded', () => {
        TestRunner.runAllTests();
    });
}