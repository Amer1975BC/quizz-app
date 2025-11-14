// Safari compatible version - load API functions globally
// API functions will be loaded via separate script tag

const quizContent = document.getElementById('quiz-content');
const scoreEl = document.getElementById('score');
const nextBtn = document.getElementById('next-btn');
const backBtn = document.getElementById('back-btn');
const quizSelector = document.getElementById('quiz-selector');

const state = {
  loading: false,
  index: 0,
  total: 0,
  question: null,
  answered: false,
  lastCorrect: null,
  lastAnswerIndex: null,
  sessionId: null,
  score: 0,
  quizType: null
};

// Quiz selector functions
window.startQuiz = function(type) {
  state.quizType = type;
  quizSelector.style.display = 'none';
  quizContent.style.display = 'block';
  scoreEl.style.display = 'block';
  backBtn.style.display = 'block';
  
  // Start appropriate quiz
  onStart(type);
}

window.showQuizSelector = function() {
  quizSelector.style.display = 'block';
  quizContent.style.display = 'none';
  scoreEl.style.display = 'none';
  nextBtn.style.display = 'none';
  backBtn.style.display = 'none';
  
  // Reset state
  state.sessionId = null;
  state.score = 0;
  state.index = 0;
}

function renderQuestion() {
  quizContent.innerHTML = '';
  nextBtn.style.display = 'none';

  const q = state.question;
  const questionDiv = document.createElement('div');
  questionDiv.className = 'question';
  questionDiv.textContent = q.text;

  const answersDiv = document.createElement('div');
  answersDiv.className = 'answers';

  for (var i = 0; i < q.choices.length; i++) {
    var text = q.choices[i];
    const btn = document.createElement('button');
    btn.textContent = text;
    btn.disabled = state.answered;
    (function(index) {
      btn.onclick = function() { onAnswer(index, btn); };
    })(i);
    if (state.answered) {
      if (i === state.lastAnswerIndex) {
        btn.classList.add(state.lastCorrect ? 'correct' : 'wrong');
      }
      // Show all correct answers
      if (state.correctAnswers && state.correctAnswers.indexOf(i) !== -1) {
        btn.classList.add('correct');
      }
    }
    answersDiv.appendChild(btn);
  }

  quizContent.appendChild(questionDiv);
  quizContent.appendChild(answersDiv);
}

function renderResult(score, total) {
  const percentage = Math.round((score / total) * 100);
  let message = '';
  
  if (state.quizType === 'pspo1') {
    if (percentage >= 85) {
      message = '🎉 Excellent! Je bent klaar voor het PSPO I examen!';
    } else if (percentage >= 70) {
      message = '👍 Goed! Nog wat extra studeren en je bent er klaar voor.';
    } else {
      message = '📚 Blijf oefenen. Je hebt meer voorbereiding nodig.';
    }
  } else {
    if (percentage >= 80) {
      message = '🎉 Geweldig resultaat!';
    } else if (percentage >= 60) {
      message = '👍 Goed gedaan!';
    } else {
      message = '💪 Blijf oefenen!';
    }
  }

  quizContent.innerHTML = 
    '<div class="question">Quiz afgerond!</div>' +
    '<div class="score">Score: ' + score + ' / ' + total + ' (' + percentage + '%)</div>' +
    '<div class="question" style="font-size: 1.2em; margin-top: 20px;">' + message + '</div>' +
    '<button class="next-btn" onclick="startQuiz(\'' + state.quizType + '\')">🔄 Opnieuw</button>';
  nextBtn.style.display = 'none';
}

function onStart(quizType) {
  if (typeof quizType === 'undefined') quizType = 'general';
  state.loading = true;
  
  // Start session with quiz type parameter
  const params = quizType === 'pspo1' ? '?category=PSPO1' : '';
  const url = '/api/start' + params;
  
  fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin' })
    .then(function(resp) {
      if (!resp.ok) {
        throw new Error('HTTP ' + resp.status);
      }
      return resp.json();
    })
    .then(function(s) {
      state.sessionId = s && (s.session_id || s.sessionId || null);
      state.score = 0;
      scoreEl.textContent = 'Score: ' + state.score;
      return loadQuestion();
    })
    .then(function() {
      state.loading = false;
    })
    .catch(function(err) {
      showError(err);
      state.loading = false;
    });
}

function loadQuestion() {
  const path = state.sessionId ? '/api/question?sid=' + encodeURIComponent(state.sessionId) : '/api/question';
  
  return fetch(path, { headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin' })
    .then(function(resp) {
      if (!resp.ok) {
        throw new Error('HTTP ' + resp.status);
      }
      return resp.json();
    })
    .then(function(data) {
      if (data.finished) {
        const resultPath = state.sessionId ? '/api/result?sid=' + encodeURIComponent(state.sessionId) : '/api/result';
        return fetch(resultPath, { headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin' })
          .then(function(resp) { return resp.json(); })
          .then(function(res) {
            renderResult(res.score, res.total);
          });
      }
      state.index = data.index;
      state.total = data.total;
      state.question = data.question;
      state.answered = false;
      state.lastCorrect = null;
      state.lastAnswerIndex = null;
      state.correctAnswers = null;
      renderQuestion();
    })
    .catch(function(err) {
      showError(err);
    });
}

function onAnswer(i, btn) {
  if (state.answered) return;
  
  const path = state.sessionId ? '/api/answer?sid=' + encodeURIComponent(state.sessionId) : '/api/answer';
  const body = JSON.stringify({ choice: i });
  
  fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: body })
    .then(function(resp) {
      if (!resp.ok) {
        throw new Error('HTTP ' + resp.status);
      }
      return resp.json();
    })
    .then(function(res) {
      state.answered = true;
      state.lastCorrect = !!res.correct;
      state.lastAnswerIndex = i;
      state.correctAnswers = res.correct_answers || [];
      
      if (res.correct) state.score++;
      scoreEl.textContent = 'Score: ' + state.score;
      
      // Mark buttons
      const buttons = document.querySelectorAll('.answers button');
      for (var idx = 0; idx < buttons.length; idx++) {
        var b = buttons[idx];
        b.disabled = true;
        if (idx === i) {
          b.classList.add(res.correct ? 'correct' : 'wrong');
        }
        // Highlight all correct answers
        if (state.correctAnswers.indexOf(idx) !== -1) {
          b.classList.add('correct');
        }
      }
      
      // Show next button
      if (res.finished) {
        renderResult(res.score, res.total);
      } else {
        nextBtn.style.display = '';
        nextBtn.onclick = onNext;
      }
    })
    .catch(function(err) {
      showError(err);
    });
}

function onNext() {
  nextBtn.style.display = 'none';
  loadQuestion();
}

function showError(e) {
  quizContent.innerHTML = '<div class="question" style="color:red;">Fout: ' + (e && e.message ? e.message : String(e)) + '</div>';
  nextBtn.style.display = 'none';
}

// Show quiz selector on load instead of starting directly
showQuizSelector();