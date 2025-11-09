const app = document.getElementById('admin-app');

function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  Object.entries(attrs || {}).forEach(([k, v]) => {
    if (k === 'class') el.className = v;
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (v !== null && v !== undefined) el.setAttribute(k, v);
  });
  children.flat().forEach(c => el.appendChild(c instanceof Node ? c : document.createTextNode(c)));
  return el;
}

async function api(path, opts) {
  const r = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...opts });
  if (!r.ok) throw new Error(await r.text());
  const ct = r.headers.get('content-type') || '';
  return ct.includes('application/json') ? r.json() : r.text();
}

async function listQuestions() {
  return api('/api/admin/questions');
}

async function createQuestion(payload) {
  return api('/api/admin/questions', { method: 'POST', body: JSON.stringify(payload) });
}

async function deleteQuestion(id) {
  return api(`/api/admin/questions/${id}`, { method: 'DELETE' });
}

function renderForm(onSubmit) {
  const text = h('input', { class: 'form-control', placeholder: 'Vraagtekst' });
  const choices = [0,1,2,3].map(() => h('input', { class: 'form-control', placeholder: 'Antwoord' }));
  const correct = h('select', { class: 'form-select' }, ...[0,1,2,3].map(i => h('option', { value: String(i) }, String(i))));
  const btn = h('button', { class: 'btn btn-primary', onClick: async (e) => {
    e.preventDefault();
    const payload = {
      text: text.value.trim(),
      choices: choices.map(c => c.value).filter(Boolean),
      correct_index: parseInt(correct.value || '0', 10) || 0,
    };
    await onSubmit(payload);
  }}, 'Toevoegen');

  return h('form', { class: 'card p-3 mb-3' },
    h('div', { class: 'mb-2' }, h('label', {}, 'Vraag'), text),
    h('div', { class: 'mb-2' }, h('label', {}, 'Antwoorden (4)'), ...choices.map(c => h('div', { class: 'mb-1' }, c))),
    h('div', { class: 'mb-3' }, h('label', {}, 'Correct index (0-3)'), correct),
    btn
  );
}

function renderTable(items, onDelete) {
  const rows = items.map(q => h('tr', {},
    h('td', {}, String(q.id ?? '')),
    h('td', {}, q.text || ''),
    h('td', {}, (q.choices || []).join(' | ')),
    h('td', {}, String(q.correct_index ?? q.correctIndex ?? '')),
    h('td', {}, h('button', { class: 'btn btn-sm btn-outline-danger', onClick: () => onDelete(q.id) }, 'Verwijderen'))
  ));
  return h('table', { class: 'table table-striped' },
    h('thead', {}, h('tr', {}, h('th', {}, 'ID'), h('th', {}, 'Vraag'), h('th', {}, 'Antwoorden'), h('th', {}, 'Correct'), h('th', {}))),
    h('tbody', {}, rows)
  );
}

async function render() {
  app.innerHTML = '';
  const title = h('h3', { class: 'mb-3' }, 'Vragenbeheer');
  const loading = h('div', { class: 'text-secondary' }, 'Laden...');
  app.append(title, loading);
  try {
    const items = await listQuestions();
    const refresh = async () => render();
    const form = renderForm(async (payload) => {
      await createQuestion(payload);
      await refresh();
    });
    const table = renderTable(items, async (id) => { await deleteQuestion(id); await refresh(); });
    app.innerHTML = '';
    app.append(title, form, table);
  } catch (e) {
    app.innerHTML = '';
    app.append(title, h('div', { class: 'alert alert-danger' }, String(e.message || e)));
  }
}

render();
