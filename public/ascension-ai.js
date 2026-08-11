(() => {
  'use strict';
  const ACCESS_KEY = 'ascension_ai_test_access';
  const SESSION_KEY = 'ascension_ai_test_sessions';
  const THEME_KEY = 'ascension_ai_test_theme';
  const state = { sessions: [], activeId: null, busy: false, health: null, shell: 'ap', tier: 'lifeos_infinite' };
  const $ = selector => document.querySelector(selector);
  const access = () => sessionStorage.getItem(ACCESS_KEY) || '';

  async function request(path, options = {}, timeout = 60000) {
    const controller = new AbortController(); const timer = setTimeout(() => controller.abort(), timeout);
    try {
      const response = await fetch(path, { ...options, signal: controller.signal, headers: { 'Content-Type': 'application/json', ...(access() ? { Authorization: `Bearer ${access()}` } : {}), ...(options.headers || {}) } });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.detail || 'Ascension AI request failed.');
      return payload;
    } finally { clearTimeout(timer); }
  }

  async function streamRequest(payload, onEvent, timeout = 180000) {
    const controller = new AbortController(); const timer = setTimeout(() => controller.abort(), timeout);
    try {
      const response = await fetch('/v1/stream', {
        method: 'POST', signal: controller.signal, body: JSON.stringify(payload),
        headers: { 'Content-Type': 'application/json', ...(access() ? { Authorization: `Bearer ${access()}` } : {}) }
      });
      if (!response.ok) { const error = await response.json().catch(() => ({})); throw new Error(error.detail || 'Ascension AI request failed.'); }
      if (!response.body) return null;
      const reader = response.body.getReader(); const decoder = new TextDecoder(); let buffer = '';
      while (true) {
        const { value, done } = await reader.read(); buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
        const blocks = buffer.split(/\r?\n\r?\n/); buffer = blocks.pop() || '';
        for (const block of blocks) {
          let event = 'message'; const data = [];
          block.split(/\r?\n/).forEach(line => { if (line.startsWith('event:')) event = line.slice(6).trim(); if (line.startsWith('data:')) data.push(line.slice(5).trimStart()); });
          if (!data.length) continue;
          let parsed; try { parsed = JSON.parse(data.join('\n')); } catch (_) { continue; }
          onEvent(event, parsed);
          if (event === 'error') throw new Error(parsed.message || 'Native model streaming failed.');
        }
        if (done) break;
      }
      return true;
    } finally { clearTimeout(timer); }
  }

  const makeId = () => `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  function save() { localStorage.setItem(SESSION_KEY, JSON.stringify(state.sessions.slice(0, 30))); }
  function load() { try { state.sessions = JSON.parse(localStorage.getItem(SESSION_KEY) || '[]').slice(0, 30); } catch (_) { state.sessions = []; } if (!state.sessions.length) createSession(); else state.activeId = state.sessions[0].id; }
  function current() { return state.sessions.find(item => item.id === state.activeId); }
  function createSession() { const item = { id: makeId(), title: 'New intelligence test', messages: [] }; state.sessions.unshift(item); state.activeId = item.id; save(); render(); }
  function removeSession(id) { state.sessions = state.sessions.filter(item => item.id !== id); if (!state.sessions.length) return createSession(); if (state.activeId === id) state.activeId = state.sessions[0].id; save(); render(); }

  function renderHistory() { const nav = $('#history'); nav.textContent = ''; state.sessions.forEach(session => { const wrap = document.createElement('div'); wrap.className = 'history-wrap'; const open = document.createElement('button'); open.type = 'button'; open.className = `history-item${session.id === state.activeId ? ' active' : ''}`; open.textContent = session.title; open.onclick = () => { state.activeId = session.id; render(); $('#sidebar').classList.remove('open'); }; const del = document.createElement('button'); del.type = 'button'; del.className = 'history-delete'; del.textContent = '×'; del.setAttribute('aria-label', `Delete ${session.title}`); del.onclick = event => { event.stopPropagation(); removeSession(session.id); }; wrap.append(open, del); nav.append(wrap); }); }
  function messageNode(message) { const article = document.createElement('article'); article.className = `message ${message.role}`; const avatar = document.createElement('div'); avatar.className = 'avatar'; avatar.textContent = message.role === 'assistant' ? 'A' : 'YOU'; const wrap = document.createElement('div'); const body = document.createElement('div'); body.className = 'message-body'; body.textContent = message.content; wrap.append(body); if (message.meta) { const meta = document.createElement('div'); meta.className = 'meta'; meta.textContent = message.meta; wrap.append(meta); } article.append(avatar, wrap); return article; }
  function renderMessages() { const session = current(); const messages = $('#messages'); messages.textContent = ''; const active = Boolean(session?.messages.length); $('#empty').hidden = active; messages.hidden = !active; if (!active) return; session.messages.forEach(message => messages.append(messageNode(message))); requestAnimationFrame(() => { $('#conversation').scrollTop = $('#conversation').scrollHeight; }); }
  function render() { renderHistory(); renderMessages(); }
  function resize() { const input = $('#prompt'); input.style.height = 'auto'; input.style.height = `${Math.min(input.scrollHeight, 180)}px`; }
  function toast(text) { const node = $('#toast'); node.textContent = text; node.classList.add('show'); clearTimeout(toast.timer); toast.timer = setTimeout(() => node.classList.remove('show'), 2800); }
  async function send(text) {
    const prompt = String(text || '').trim(); if (!prompt || state.busy) return;
    const session = current(); state.busy = true; session.messages.push({ role: 'user', content: prompt }); if (session.messages.length === 1) session.title = prompt.slice(0, 52); save(); render(); $('#prompt').value = ''; resize(); $('#send').disabled = true;
    const live = { role: 'assistant', content: '', meta: 'Ascension native is thinking…' }; const node = messageNode(live); $('#messages').append(node); const body = node.querySelector('.message-body'); const metaNode = node.querySelector('.meta'); let meta = {}; let done = {};
    const payload = { shell: state.shell, tier: state.tier, messages: session.messages.map(({ role, content }) => ({ role, content })), surface: 'standalone_lab', mode: 'conversation' };
    try {
      const streamed = await streamRequest(payload, (event, data) => {
        if (event === 'meta') { meta = data; metaNode.textContent = `${data.shell || state.shell} · ${data.tier || state.tier} · ${data.model || 'Ascension native'}`; }
        if (event === 'token') { body.textContent += data.token || ''; $('#conversation').scrollTop = $('#conversation').scrollHeight; }
        if (event === 'done') done = data;
      });
      if (streamed === null) {
        const result = await request('/chat', { method: 'POST', body: JSON.stringify(payload) }, 180000);
        body.textContent = result.content; meta = result; done = result;
      }
      if (!body.textContent.trim()) throw new Error('Ascension native returned an empty response.');
      live.content = body.textContent; live.meta = `${meta.shell || state.shell} shell · ${meta.tier || state.tier} · Ascension native · ${meta.model || 'model unknown'} · ${done.latency_ms || 0} ms`;
      metaNode.textContent = live.meta; session.messages.push(live); save();
    }
    catch (error) { node.remove(); const saved = { role: 'assistant', content: error.name === 'AbortError' ? 'The native model timed out before completing this response.' : error.message, meta: 'Candidate unavailable · no fallback or substitution occurred' }; session.messages.push(saved); save(); $('#messages').append(messageNode(saved)); if (/access code/i.test(error.message)) showGate(error.message); }
    finally { state.busy = false; $('#send').disabled = false; $('#prompt').focus(); $('#conversation').scrollTop = $('#conversation').scrollHeight; }
  }

  function showGate(error = '') { $('#shell').hidden = true; $('#access-gate').hidden = false; $('#access-error').textContent = error; setTimeout(() => $('#access-code').focus(), 0); }
  async function unlock(code) { sessionStorage.setItem(ACCESS_KEY, code); try { await request('/model/info', {}, 12000); $('#access-gate').hidden = true; $('#shell').hidden = false; render(); } catch (error) { sessionStorage.removeItem(ACCESS_KEY); showGate(error.message); } }
  async function readHealth() { try { state.health = await request('/health', {}, 12000); const node = $('#status'); node.classList.toggle('ready', state.health.candidate_ready); node.querySelector('span').textContent = state.health.candidate_ready ? `${state.health.model} ready` : 'Setup incomplete'; } catch (_) { $('#status span').textContent = 'Service unavailable'; } }

  function bind() { $('#new-chat').onclick = createSession; $('#menu').onclick = () => $('#sidebar').classList.toggle('open'); $('#shell-select').onchange = event => { state.shell = event.target.value; createSession(); toast(`Testing ${event.target.options[event.target.selectedIndex].text}`); }; $('#tier-select').onchange = event => { state.tier = event.target.value; createSession(); toast(`Testing ${event.target.options[event.target.selectedIndex].text}`); }; $('#lock-lab').onclick = () => { sessionStorage.removeItem(ACCESS_KEY); showGate(); }; $('#theme-toggle').onclick = () => { const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light'; document.documentElement.dataset.theme = next; localStorage.setItem(THEME_KEY, next); $('#theme-toggle').textContent = next === 'light' ? 'Dark mode' : 'Light mode'; }; $('#access-form').onsubmit = event => { event.preventDefault(); unlock($('#access-code').value); }; $('#composer').onsubmit = event => { event.preventDefault(); send($('#prompt').value); }; $('#prompt').addEventListener('input', resize); $('#prompt').addEventListener('keydown', event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); $('#composer').requestSubmit(); } }); document.querySelectorAll('[data-prompt]').forEach(button => button.onclick = () => send(button.dataset.prompt)); }
  async function boot() { document.documentElement.dataset.theme = localStorage.getItem(THEME_KEY) || 'dark'; load(); bind(); await readHealth(); if (access()) { try { await request('/model/info', {}, 12000); $('#shell').hidden = false; render(); } catch (_) { showGate(); } } else showGate(); }
  document.addEventListener('DOMContentLoaded', boot);
})();
