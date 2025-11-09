async function apiRequest(path, options = {}) {
  const resp = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    credentials: 'same-origin',
    ...options,
  });
  if (!resp.ok) {
    let text = await resp.text().catch(() => '');
    throw new Error(text || ('HTTP ' + resp.status));
  }
  const ct = resp.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    return await resp.json();
  }
  return await resp.text();
}

export async function startSession() {
  // returns { session_id }
  return await apiRequest('/api/start', { method: 'POST' });
}

export async function fetchQuestion(sessionId) {
  // Try cookie first; if sid provided use explicit query param fallback.
  const path = sessionId ? `/api/question?sid=${encodeURIComponent(sessionId)}` : '/api/question';
  return await apiRequest(path);
}

export async function submitAnswer(choiceIndex, sessionId) {
  const path = sessionId ? `/api/answer?sid=${encodeURIComponent(sessionId)}` : '/api/answer';
  return await apiRequest(path, { method: 'POST', body: JSON.stringify({ choice: choiceIndex }) });
}

export async function fetchResult(sessionId) {
  const path = sessionId ? `/api/result?sid=${encodeURIComponent(sessionId)}` : '/api/result';
  return await apiRequest(path);
}
