// Safari compatible API functions - no modules

function apiRequest(path, options) {
  options = options || {};
  var headers = { 'Content-Type': 'application/json' };
  if (options.headers) {
    for (var key in options.headers) {
      headers[key] = options.headers[key];
    }
  }
  
  var fetchOptions = {
    headers: headers,
    credentials: 'same-origin'
  };
  
  for (var key in options) {
    if (key !== 'headers') {
      fetchOptions[key] = options[key];
    }
  }
  
  return fetch(path, fetchOptions)
    .then(function(resp) {
      if (!resp.ok) {
        return resp.text().then(function(text) {
          throw new Error(text || ('HTTP ' + resp.status));
        }).catch(function() {
          throw new Error('HTTP ' + resp.status);
        });
      }
      var ct = resp.headers.get('content-type') || '';
      if (ct.indexOf('application/json') !== -1) {
        return resp.json();
      }
      return resp.text();
    });
}

// Global functions for Safari compatibility
window.startSession = function(params) {
  params = params || '';
  var url = '/api/start' + params;
  return apiRequest(url, { method: 'POST' });
};

window.fetchQuestion = function(sessionId) {
  var path = sessionId ? '/api/question?sid=' + encodeURIComponent(sessionId) : '/api/question';
  return apiRequest(path);
};

window.submitAnswer = function(choiceIndex, sessionId) {
  var path = sessionId ? '/api/answer?sid=' + encodeURIComponent(sessionId) : '/api/answer';
  return apiRequest(path, { method: 'POST', body: JSON.stringify({ choice: choiceIndex }) });
};

window.fetchResult = function(sessionId) {
  var path = sessionId ? '/api/result?sid=' + encodeURIComponent(sessionId) : '/api/result';
  return apiRequest(path);
};
