import { startSession, fetchQuestion, submitAnswer, fetchResult } from './api.js?v=20251109L';

const appEl = document.getElementById('app');
console.log('Loaded app.js version 20251109L');
window._quiz_debug = { appLoaded: true };

const state = {
  loading: false,
  index: 0,
  total: 0,
  question: null,
  answered: false,
  lastCorrect: null,
  lastAnswerIndex: null,
  sessionId: null,
};

function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  let clickHandler = null;
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === 'class') el.className = v;
    else if (k === 'onClick' && typeof v === 'function') {
      clickHandler = v;
      console.log(`Storing click handler for <${tag}>`);
    }
    else if (k.startsWith('on') && typeof v === 'function') {
      const eventName = k.slice(2).toLowerCase();
      console.log(`Adding event handler for ${k} (${eventName}) to <${tag}>`);
      window._quiz_debug.lastHandler = { tag, event: k, eventName };
      el.addEventListener(eventName, v);
    }
    else if (v !== null && v !== undefined) el.setAttribute(k, v);
  }
  // Apply click handler after element is created
  if (clickHandler) {
    el.onclick = clickHandler;
    console.log(`Applied onclick to <${tag}>`);
  }
  for (const c of children) {
    if (Array.isArray(c)) c.forEach(x => el.appendChild(x instanceof Node ? x : document.createTextNode(x)));
    else el.appendChild(c instanceof Node ? c : document.createTextNode(c));
  }
  return el;
}

function renderStart() {
  console.log('renderStart called');
  window._quiz_debug.renderStart = true;
  appEl.innerHTML = '';
  const card = h('div', { class: 'card shadow quiz-card' },
    h('div', { class: 'card-body' },
      h('h3', { class: 'card-title mb-3' }, 'Welkom!'),
      h('p', { class: 'card-text' }, 'Klaar voor een korte quiz?'),
      h('button', { class: 'btn btn-primary', onClick: onStart }, 'Start quiz')
    )
  );
  appEl.appendChild(card);
  window._quiz_debug.startRendered = true;
}

function progressBar() {
  const percent = state.total > 0 ? Math.round((state.index / state.total) * 100) : 0;
  return h('div', { class: 'progress mb-3' },
    h('div', { class: 'progress-bar', role: 'progressbar', style: `width: ${percent}%` }, `${percent}%`)
  );
}

function renderQuestion() {
  console.log('renderQuestion called, state.answered:', state.answered);
  appEl.innerHTML = '';
  
  const q = state.question;
  
  const btns = q.choices.map((text, i) => {
    const classes = ['btn', 'btn-outline-secondary', 'w-100', 'choice-btn'];
    if (state.answered) {
      if (i === state.lastAnswerIndex) classes.push(state.lastCorrect ? 'correct' : 'incorrect');
    }
    console.log(`Creating button ${i}, disabled: ${state.answered}`);
    
    // Create button directly like test button
    const btn = document.createElement('button');
    btn.className = classes.join(' ');
    btn.textContent = text;
    btn.disabled = state.answered;
    btn.style.cssText = 'pointer-events: auto; cursor: pointer;';
    btn.onclick = () => {
      console.log(`Button ${i} clicked!`);
      onAnswer(i);
    };
    
    return btn;
  });

  const bodyChildren = [
    h('h5', { class: 'card-title' }, q.text),
    h('div', { class: 'vstack gap-2 my-3' }, btns),
    h('div', { class: 'footer-actions' },
      state.answered ? h('button', { class: 'btn btn-primary', onClick: onNext }, 'Volgende') : h('span', {})
    )
  ];

  const card = h('div', { class: 'card shadow quiz-card' },
    h('div', { class: 'card-body' },
      progressBar(),
      ...bodyChildren
    )
  );
  appEl.appendChild(card);
}

function renderResult(score, total) {
  appEl.innerHTML = '';
  const card = h('div', { class: 'card shadow quiz-card' },
    h('div', { class: 'card-body' },
      h('h3', { class: 'card-title mb-3' }, 'Resultaat'),
      h('p', {}, `Je score: ${score} / ${total}`),
      h('div', { class: 'd-flex gap-2' },
        h('button', { class: 'btn btn-outline-secondary', onClick: () => location.reload() }, 'Opnieuw'),
        h('button', { class: 'btn btn-primary', onClick: onStart }, 'Nieuwe sessie')
      )
    )
  );
  appEl.appendChild(card);
}

async function onStart() {
  console.log('onStart triggered');
  try {
    state.loading = true;
    const s = await startSession();
    state.sessionId = s && (s.session_id || s.sessionId || null);
    console.log('Session created:', state.sessionId);
    await loadQuestion();
  } catch (e) {
    showError(e);
  } finally {
    state.loading = false;
  }
}

async function loadQuestion() {
  console.log('Loading question with sessionId:', state.sessionId);
  const data = await fetchQuestion(state.sessionId).catch(err => { showError(err); return null; });
  if(!data) return;
  console.log('Question response:', data);
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

async function onAnswer(i) {
  console.log('onAnswer triggered for choice:', i);
  if (state.answered) return;
  try {
  const res = await submitAnswer(i, state.sessionId).catch(err => { showError(err); return null; });
  if(!res) return;
    state.answered = true;
    state.lastCorrect = !!res.correct;
    state.lastAnswerIndex = i;
    // If finished, jump to result; else show Next button
    if (res.finished) {
      renderResult(res.score, res.total);
    } else {
      renderQuestion();
    }
  } catch (e) {
    showError(e);
  }
}

async function onNext() {
  try {
    await loadQuestion();
  } catch (e) {
    showError(e);
  }
}

function showError(e) {
  appEl.innerHTML = '';
  const msg = (e && e.message) ? e.message : String(e);
  const card = h('div', { class: 'card shadow quiz-card' },
    h('div', { class: 'card-body' },
      h('h5', { class: 'card-title text-danger' }, 'Er is een fout opgetreden'),
      h('pre', { class: 'error' }, msg),
      h('div', { class: 'd-flex gap-2' },
        h('button', { class: 'btn btn-outline-secondary', onClick: () => location.reload() }, 'Herlaad'),
        h('button', { class: 'btn btn-primary', onClick: () => renderStart() }, 'Terug')
      )
    )
  );
  appEl.appendChild(card);
}

// Initialize
renderStart();
