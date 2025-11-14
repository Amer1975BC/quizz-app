import { startSession, fetchQuestion, submitAnswer, fetchResult } from './api.js?v=20251109L';

const quizContent = document.getElementById('quiz-content');
const scoreEl = document.getElementById('score');
const nextBtn = document.getElementById('next-btn');

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
};

function renderQuestion() {
  quizContent.innerHTML = '';
  nextBtn.style.display = 'none';

  const q = state.question;
  const questionDiv = document.createElement('div');
  questionDiv.className = 'question';
  questionDiv.textContent = q.text;

  const answersDiv = document.createElement('div');
  answersDiv.className = 'answers';

  q.choices.forEach((text, i) => {
    const btn = document.createElement('button');
    btn.textContent = text;
    btn.disabled = state.answered;
    btn.onclick = () => onAnswer(i, btn);
    if (state.answered) {
      if (i === state.lastAnswerIndex) {
        btn.classList.add(state.lastCorrect ? 'correct' : 'wrong');
      }
    }
    answersDiv.appendChild(btn);
  });

  quizContent.appendChild(questionDiv);
  quizContent.appendChild(answersDiv);
}

function renderResult(score, total) {
  quizContent.innerHTML = `
    <div class="question">Quiz afgerond!</div>
    <div class="score">Score: ${score} / ${total}</div>
    <button class="next-btn" onclick="location.reload()">Opnieuw</button>
  `;
  nextBtn.style.display = 'none';
}

async function onStart() {
  state.loading = true;
  const s = await startSession();
  state.sessionId = s && (s.session_id || s.sessionId || null);
  state.score = 0;
  scoreEl.textContent = `Score: ${state.score}`;
  await loadQuestion();
  state.loading = false;
}

async function loadQuestion() {
  const data = await fetchQuestion(state.sessionId).catch(err => { showError(err); return null; });
  if (!data) return;
  if (data.finished) {
    const res = await fetchResult(state.sessionId);
    renderResult(res.score, res.total);
    return;
  }
  state.index = data.index;
  state.total = data.total;
  state.question = data.question;
  state.answered = false;
  state.lastCorrect = null;
  state.lastAnswerIndex = null;
  renderQuestion();
}

async function onAnswer(i, btn) {
  if (state.answered) return;
  const res = await submitAnswer(i, state.sessionId).catch(err => { showError(err); return null; });
  if (!res) return;
  state.answered = true;
  state.lastCorrect = !!res.correct;
  state.lastAnswerIndex = i;
  if (res.correct) state.score++;
  scoreEl.textContent = `Score: ${state.score}`;
  // Mark buttons
  const buttons = document.querySelectorAll('.answers button');
  buttons.forEach((b, idx) => {
    b.disabled = true;
    if (idx === i) b.classList.add(res.correct ? 'correct' : 'wrong');
  });
  // Show next button
  if (res.finished) {
    renderResult(res.score, res.total);
  } else {
    nextBtn.style.display = '';
    nextBtn.onclick = onNext;
  }
}

async function onNext() {
  nextBtn.style.display = 'none';
  await loadQuestion();
}

function showError(e) {
  quizContent.innerHTML = `<div class="question" style="color:red;">Fout: ${e && e.message ? e.message : String(e)}</div>`;
  nextBtn.style.display = 'none';
}

// Start quiz direct
onStart();
