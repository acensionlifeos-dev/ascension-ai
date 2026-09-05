(() => {
  'use strict';

  const LEGACY_SESSION_KEY = 'ascension_ai_test_sessions';
  const LEGACY_THEME_KEY = 'ascension_ai_test_theme';
  const LEGACY_VOICE_KEY = 'ascension_ai_test_voice';
  const SESSION_KEY = 'ascension_ai_sessions';
  const THEME_KEY = 'ascension_ai_theme';
  const VOICE_KEY = 'ascension_ai_voice';

  const state = {
    sessions: [],
    activeId: null,
    busy: false,
    health: null,
    talents: null,
    shell: 'ap',
    tier: 'lifeos_infinite',
    voiceOn: false,
    currentAbort: null,
  };
  const $ = selector => document.querySelector(selector);

  function buildData(cognition) {
    if (!cognition) return null;
    return {
      domains: cognition.domains || [],
      surfaces: cognition.surface_recommendations || [],
      retrieval: cognition.retrieval || [],
      actions: cognition.action_proposals || [],
      panels: cognition.data_panels || []
    };
  }

  function buildDataPanel(data) {
    if (!data) return null;
    const panel = document.createElement('div');
    panel.className = 'data-panel';
    if (data.panels?.length) panel.append(panelCards(data.panels));
    if (data.domains?.length) panel.append(dataChips('Domains', data.domains));
    if (data.surfaces?.length) panel.append(dataChips('Surfaces', data.surfaces));
    if (data.retrieval?.length) panel.append(retrievalList(data.retrieval));
    if (data.actions?.length) panel.append(actionCards(data.actions));
    return panel.childNodes.length ? panel : null;
  }

  function panelCards(panels) {
    const wrap = document.createElement('div');
    wrap.className = 'data-section data-panels';
    panels.forEach(panel => {
      const card = document.createElement('div');
      card.className = 'data-panel-card';
      const title = document.createElement('div');
      title.className = 'data-panel-card-title';
      title.textContent = panel.title || panel.id;
      if (panel.count != null) title.textContent += ` (${panel.count})`;
      card.append(title);
      const ul = document.createElement('ul');
      ul.className = 'data-list';
      (panel.items || []).slice(0, 3).forEach(item => {
        const li = document.createElement('li');
        li.textContent = String(item).slice(0, 160);
        ul.append(li);
      });
      card.append(ul);
      wrap.append(card);
    });
    return wrap;
  }

  function appendDataPanel(data, wrap) {
    if (!data || !wrap) return;
    // Remove any previously appended data panel to avoid duplicates on updates.
    wrap.querySelector('.data-panel')?.remove();
    const panel = buildDataPanel(data);
    if (panel) {
      const meta = wrap.querySelector('.meta');
      if (meta) wrap.insertBefore(panel, meta);
      else wrap.append(panel);
    }
  }

  function shellContext() {
    // Family shells inject per-user provider keys and permissioned context here.
    // This object is never persisted to localStorage.
    return (typeof window !== 'undefined' && window.ASCENSION_SHELL_CONTEXT) || {};
  }

  function migrateStorage(newKey, legacyKey) {
    const current = localStorage.getItem(newKey);
    if (current !== null) return current;
    const legacy = localStorage.getItem(legacyKey);
    if (legacy !== null) {
      localStorage.setItem(newKey, legacy);
      localStorage.removeItem(legacyKey);
    }
    return legacy;
  }

  function withTimeout(timeoutMs, externalSignal) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    if (externalSignal) {
      if (externalSignal.aborted) {
        clearTimeout(timer);
        controller.abort();
      } else {
        externalSignal.addEventListener('abort', () => {
          clearTimeout(timer);
          controller.abort();
        }, { once: true });
      }
    }
    return { signal: controller.signal, clear: () => clearTimeout(timer) };
  }

  async function request(path, options = {}, timeout = 60000, externalSignal = null) {
    const { signal, clear } = withTimeout(timeout, externalSignal);
    try {
      const response = await fetch(path, {
        ...options,
        signal,
        headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.detail || 'Aerynza AI request failed.');
      return payload;
    } finally { clear(); }
  }

  function parseSseBlock(block) {
    let event = 'message';
    const data = [];
    block.split(/\r?\n/).forEach(line => {
      if (line.startsWith('event:')) event = line.slice(6).trim();
      if (line.startsWith('data:')) data.push(line.slice(5).trimStart());
    });
    if (!data.length) return null;
    try { return { event, data: JSON.parse(data.join('\n')) }; } catch (_) { return null; }
  }

  async function streamRequest(payload, onEvent, timeout = 180000, externalSignal = null) {
    const { signal, clear } = withTimeout(timeout, externalSignal);
    try {
      const response = await fetch('/v1/stream', {
        method: 'POST',
        signal,
        body: JSON.stringify(payload),
        headers: { 'Content-Type': 'application/json' }
      });
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Aerynza AI request failed.');
      }
      if (!response.body) return null;
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      while (true) {
        const { value, done } = await reader.read();
        buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
        const blocks = buffer.split(/\r?\n\r?\n/);
        buffer = blocks.pop() || '';
        for (const block of blocks) {
          const parsed = parseSseBlock(block);
          if (!parsed) continue;
          onEvent(parsed.event, parsed.data);
          if (parsed.event === 'error') throw new Error(parsed.data.message || 'Native model streaming failed.');
        }
        if (done) break;
      }
      // Flush any final block that lacks a trailing blank line.
      if (buffer.trim()) {
        const parsed = parseSseBlock(buffer.trim());
        if (parsed) {
          onEvent(parsed.event, parsed.data);
          if (parsed.event === 'error') throw new Error(parsed.data.message || 'Native model streaming failed.');
        }
      }
      return true;
    } finally { clear(); }
  }

  const makeId = () => `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

  function save() { localStorage.setItem(SESSION_KEY, JSON.stringify(state.sessions.slice(0, 30))); }
  function load() {
    try { state.sessions = JSON.parse(localStorage.getItem(SESSION_KEY) || '[]').slice(0, 30); } catch (_) { state.sessions = []; }
    if (!state.sessions.length) createSession(); else state.activeId = state.sessions[0].id;
  }
  function current() { return state.sessions.find(item => item.id === state.activeId); }
  function createSession() {
    const item = { id: makeId(), title: 'New chat', messages: [] };
    state.sessions.unshift(item);
    state.activeId = item.id;
    save();
    render();
  }
  function removeSession(id) {
    state.sessions = state.sessions.filter(item => item.id !== id);
    if (!state.sessions.length) return createSession();
    if (state.activeId === id) state.activeId = state.sessions[0].id;
    save();
    render();
  }

  function messageNode(message) {
    const article = document.createElement('article');
    article.className = `message ${message.role}`;
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = message.role === 'assistant' ? 'A' : 'YOU';
    const wrap = document.createElement('div');
    wrap.className = 'message-wrap';
    const body = document.createElement('div');
    body.className = 'message-body';
    if (message.imageUrl) {
      const p = document.createElement('p');
      p.textContent = message.imageCaption || 'Screenshot:';
      body.append(p);
      const img = document.createElement('img');
      img.src = message.imageUrl;
      img.alt = message.imageAlt || 'screenshot';
      img.style.maxWidth = '100%';
      img.style.borderRadius = '8px';
      body.append(img);
    } else {
      body.textContent = message.content;
    }
    wrap.append(body);
    if (message.data) {
      const panel = buildDataPanel(message.data);
      if (panel) wrap.append(panel);
    }
    if (message.meta) {
      const meta = document.createElement('div');
      meta.className = 'meta';
      meta.textContent = message.meta;
      wrap.append(meta);
    }
    article.append(avatar, wrap);
    return article;
  }

  function dataChips(label, items) {
    const wrap = document.createElement('div');
    wrap.className = 'data-section';
    const title = document.createElement('span');
    title.className = 'data-label';
    title.textContent = label;
    wrap.append(title);
    items.forEach(item => {
      const chip = document.createElement('span');
      chip.className = 'data-chip';
      chip.textContent = String(item);
      wrap.append(chip);
    });
    return wrap;
  }

  function retrievalList(items) {
    const wrap = document.createElement('div');
    wrap.className = 'data-section';
    const title = document.createElement('span');
    title.className = 'data-label';
    title.textContent = 'Evidence';
    wrap.append(title);
    const list = document.createElement('ul');
    list.className = 'data-list';
    items.slice(0, 3).forEach(item => {
      const li = document.createElement('li');
      li.textContent = String(item.text || item.document || item.metadata?.source || JSON.stringify(item)).slice(0, 220);
      list.append(li);
    });
    wrap.append(list);
    return wrap;
  }

  function actionCards(items) {
    const wrap = document.createElement('div');
    wrap.className = 'data-section';
    const title = document.createElement('span');
    title.className = 'data-label';
    title.textContent = 'Proposed actions';
    wrap.append(title);
    items.slice(0, 6).forEach(action => {
      const card = document.createElement('div');
      card.className = 'action-card';
      const header = document.createElement('div');
      header.className = 'action-card-title';
      header.textContent = action.action || 'action';
      const meta = document.createElement('div');
      meta.className = 'action-card-meta';
      meta.textContent = `${action.domain || ''} · ${action.approval || ''}`.replace(/^\s*·\s*|\s*·\s*$/g, '');
      card.append(header, meta);
      wrap.append(card);
    });
    return wrap;
  }

  function renderHistory() {
    const nav = $('#history');
    nav.textContent = '';
    state.sessions.forEach(session => {
      const wrap = document.createElement('div');
      wrap.className = 'history-wrap';
      const open = document.createElement('button');
      open.type = 'button';
      open.className = `history-item${session.id === state.activeId ? ' active' : ''}`;
      open.textContent = session.title;
      open.onclick = () => { state.activeId = session.id; render(); $('#sidebar').classList.remove('open'); };
      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'history-delete';
      del.textContent = '×';
      del.setAttribute('aria-label', `Delete ${session.title}`);
      del.onclick = event => { event.stopPropagation(); removeSession(session.id); };
      wrap.append(open, del);
      nav.append(wrap);
    });
  }

  function renderMessages() {
    const session = current();
    const messages = $('#messages');
    messages.textContent = '';
    const active = Boolean(session?.messages.length);
    $('#empty').hidden = active;
    messages.hidden = !active;
    if (!active) return;
    session.messages.forEach(message => messages.append(messageNode(message)));
    requestAnimationFrame(() => { $('#conversation').scrollTop = $('#conversation').scrollHeight; });
  }

  function render() { renderHistory(); renderMessages(); }

  function resize() {
    const input = $('#prompt');
    input.style.height = 'auto';
    input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
  }

  function toast(text) {
    const node = $('#toast');
    node.textContent = text;
    node.classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => node.classList.remove('show'), 2800);
  }

  function speak(text) {
    if (!state.voiceOn || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(u);
  }

  function setBusy(text) {
    const status = $('#status');
    status.classList.add('busy');
    const icon = status.querySelector('i');
    if (icon) icon.className = 'spinner';
    const span = status.querySelector('span');
    if (span) span.textContent = text;
  }

  function setReady(text) {
    const status = $('#status');
    status.classList.remove('busy');
    const icon = status.querySelector('i');
    if (icon) icon.className = '';
    const span = status.querySelector('span');
    if (span) span.textContent = text;
  }

  function safeImageUrl(url) {
    try {
      const u = new URL(url, window.location.origin);
      if (u.origin === window.location.origin) return u.pathname + u.search;
      if (u.protocol === 'https:') return u.href;
      return null;
    } catch (_) { return null; }
  }

  function parseCommand(text) {
    const line = text.trim();
    const parts = line.split(/\s+/);
    const action = parts[0].toLowerCase();
    const tail = parts.slice(1).join(' ').trim();
    let apiAction = action;
    let params = {};
    if (action === 'open' || action === 'start') { apiAction = 'open_app'; params = { app: tail || 'notepad' }; }
    else if (action === 'type') { apiAction = 'type_text'; params = { text: tail }; }
    else if (action === 'press' || action === 'key') { apiAction = 'press_key'; params = { key: tail }; }
    else if (action === 'click') {
      const coords = tail.split(/[,\s]+/).filter(Boolean);
      params = { x: parseInt(coords[0], 10) || 0, y: parseInt(coords[1], 10) || 0 };
    }
    else if (action === 'screenshot' || action === 'capture') { apiAction = 'screenshot'; }
    else if (action === 'list' || action === 'windows') { apiAction = 'list_windows'; }
    else if (action === 'search') { apiAction = 'search'; params = { query: tail }; }
    else if (action === 'wait') { apiAction = 'wait'; params = { ms: parseInt(tail, 10) || 500 }; }
    else if (action === 'chain' || action === 'do') {
      apiAction = 'chain';
      params = { commands: tail.split(';').filter(Boolean).map(s => parseCommand(s)) };
    }
    else { throw new Error(`Unknown !command: ${action}`); }
    return { action: apiAction, params };
  }

  function parseAndroidCommand(text) {
    const line = text.trim();
    const parts = line.split(/\s+/);
    const sub = parts[0] ? parts[0].toLowerCase() : 'list';
    const rest = parts.slice(1).join(' ').trim();
    let action = sub;
    let params = {};
    if (sub === 'list') { action = 'list_devices'; }
    else if (sub === 'apps') { action = 'list_apps'; }
    else if (sub === 'screenshot') { action = 'screenshot'; }
    else if (sub === 'tap') {
      const c = rest.split(/[,\s]+/).filter(Boolean);
      params = { x: parseInt(c[0], 10) || 0, y: parseInt(c[1], 10) || 0 };
    }
    else if (sub === 'swipe') {
      const c = rest.split(/[,\s]+/).filter(Boolean);
      params = { x1: parseInt(c[0], 10) || 0, y1: parseInt(c[1], 10) || 0, x2: parseInt(c[2], 10) || 0, y2: parseInt(c[3], 10) || 0, ms: parseInt(c[4], 10) || 300 };
    }
    else if (sub === 'type') { action = 'type_text'; params = { text: rest }; }
    else if (sub === 'press' || sub === 'key') { action = 'press_key'; params = { key: rest }; }
    else if (['home', 'back', 'recent', 'enter', 'volume_up', 'volume_down'].includes(sub)) {
      action = 'press_key'; params = { key: sub };
    }
    else if (sub === 'launch') { action = 'launch_app'; params = { package: rest }; }
    return { action, params };
  }

  function parseiPhoneCommand(text) {
    const line = text.trim();
    const parts = line.split(/\s+/);
    const sub = parts[0] ? parts[0].toLowerCase() : 'list';
    const rest = parts.slice(1).join(' ').trim();
    if (sub === 'send') { return { action: 'send', params: { message: rest } }; }
    if (sub === 'test') { return { action: 'send', params: { message: 'Test from Aerynza AI on Windows.' } }; }
    if (sub === 'list' || sub === 'get') { return { action: 'list', params: {} }; }
    return { action: 'send', params: { message: text.trim() } };
  }

  function appendUserMessage(prompt) {
    const session = current();
    session.messages.push({ role: 'user', content: prompt });
    if (session.messages.length === 1) session.title = prompt.slice(0, 52);
    save();
    render();
    $('#prompt').value = '';
    resize();
    $('#send').disabled = true;
    setBusy('Working…');
  }

  function appendAssistantPlaceholder(metaLabel) {
    const live = { role: 'assistant', content: '', meta: metaLabel, data: null };
    const node = messageNode(live);
    $('#messages').append(node);
    const wrap = node.querySelector('.message-wrap');
    return { live, node, wrap, body: node.querySelector('.message-body'), metaNode: node.querySelector('.meta') };
  }

  function finalizeAction(node, live, result, metaPrefix, caption) {
    if ((result.status === 'screenshot' || result.status === 'image') && result.url) {
      const url = safeImageUrl(result.url);
      if (url) {
        live.imageUrl = url;
        live.imageCaption = caption;
        live.imageAlt = `${metaPrefix.toLowerCase()} image`;
      } else {
        live.content = `${metaPrefix} received an unsafe URL: ${result.url}`;
      }
    } else {
      live.content = result.message ? `${result.status}: ${result.message}` : JSON.stringify(result, null, 2);
    }
    live.meta = `${metaPrefix} · ${result.status}`;
    // Re-render the body safely
    const body = node.querySelector('.message-body');
    body.textContent = '';
    if (live.imageUrl) {
      const p = document.createElement('p');
      p.textContent = live.imageCaption;
      body.append(p);
      const img = document.createElement('img');
      img.src = live.imageUrl;
      img.alt = live.imageAlt;
      img.style.maxWidth = '100%';
      img.style.borderRadius = '8px';
      body.append(img);
    } else {
      body.textContent = live.content;
    }
    node.querySelector('.meta').textContent = live.meta;
  }

  async function runAndroid(tail) {
    const session = current();
    const prompt = '!android ' + tail;
    state.busy = true;
    appendUserMessage(prompt);
    setBusy('Running Android action…');
    const { live, node } = appendAssistantPlaceholder('Android shell');
    try {
      const command = parseAndroidCommand(tail);
      const result = await request('/v1/android/execute', { method: 'POST', body: JSON.stringify(command) }, 12000);
      finalizeAction(node, live, result, 'Android', 'Android screenshot:');
      session.messages.push(live);
      save();
      if (state.voiceOn && !live.imageUrl) speak(live.content);
    } catch (error) {
      node.remove();
      const saved = { role: 'assistant', content: error.name === 'AbortError' ? 'The action timed out.' : error.message, meta: 'Android action failed' };
      session.messages.push(saved); save(); $('#messages').append(messageNode(saved));
    } finally {
      state.busy = false;
      $('#send').disabled = false;
      $('#prompt').focus();
      $('#conversation').scrollTop = $('#conversation').scrollHeight;
      setReady(state.health?.candidate_ready ? `${state.health.model} ready` : 'Setup incomplete');
    }
  }

  async function runiPhone(tail) {
    const session = current();
    const prompt = '!iphone ' + tail;
    state.busy = true;
    appendUserMessage(prompt);
    setBusy('Running iPhone action…');
    const { live, node } = appendAssistantPlaceholder('iPhone shell');
    try {
      const command = parseiPhoneCommand(tail);
      const result = await request('/v1/iphone/execute', { method: 'POST', body: JSON.stringify({ ...command, context: shellContext() }) }, 12000);
      finalizeAction(node, live, result, 'iPhone', 'iPhone screenshot:');
      session.messages.push(live);
      save();
      if (state.voiceOn && !live.imageUrl) speak(live.content);
    } catch (error) {
      node.remove();
      const saved = { role: 'assistant', content: error.name === 'AbortError' ? 'The action timed out.' : error.message, meta: 'iPhone action failed' };
      session.messages.push(saved); save(); $('#messages').append(messageNode(saved));
    } finally {
      state.busy = false;
      $('#send').disabled = false;
      $('#prompt').focus();
      $('#conversation').scrollTop = $('#conversation').scrollHeight;
      setReady(state.health?.candidate_ready ? `${state.health.model} ready` : 'Setup incomplete');
    }
  }

  async function runDalle(tail) {
    const session = current();
    const prompt = '!dalle ' + tail;
    state.busy = true;
    appendUserMessage(prompt);
    setBusy('Running DALL-E 3…');
    const { live, node } = appendAssistantPlaceholder('DALL-E 3');
    try {
      const result = await request('/v1/media/generate', { method: 'POST', body: JSON.stringify({ prompt: tail, provider: 'dall-e-3', context: shellContext() }) }, 90000);
      finalizeAction(node, live, result, 'DALL-E 3', 'DALL-E 3 image:');
      session.messages.push(live);
      save();
      if (state.voiceOn && !live.imageUrl) speak(live.content);
    } catch (error) {
      node.remove();
      const saved = { role: 'assistant', content: error.name === 'AbortError' ? 'The DALL-E 3 request timed out.' : error.message, meta: 'DALL-E 3 action failed' };
      session.messages.push(saved); save(); $('#messages').append(messageNode(saved));
    } finally {
      state.busy = false;
      $('#send').disabled = false;
      $('#prompt').focus();
      $('#conversation').scrollTop = $('#conversation').scrollHeight;
      setReady(state.health?.candidate_ready ? `${state.health.model} ready` : 'Setup incomplete');
    }
  }

  async function runAction(prompt) {
    const first = prompt.slice(1).trim().split(/\s+/)[0].toLowerCase();
    const tail = prompt.slice(1).trim().split(/\s+/).slice(1).join(' ');
    if (first === 'android') { return runAndroid(tail); }
    if (first === 'iphone') { return runiPhone(tail); }
    if (first === 'dalle') { return runDalle(tail); }
    const session = current();
    state.busy = true;
    appendUserMessage(prompt);
    setBusy('Running Windows action…');
    const { live, node } = appendAssistantPlaceholder('Windows shell');
    try {
      const command = parseCommand(prompt.slice(1).trim());
      const result = await request('/v1/windows/execute', { method: 'POST', body: JSON.stringify(command) }, 12000);
      finalizeAction(node, live, result, 'Windows', 'Screenshot captured:');
      session.messages.push(live);
      save();
      if (state.voiceOn && !live.imageUrl) speak(live.content);
    } catch (error) {
      node.remove();
      const saved = { role: 'assistant', content: error.name === 'AbortError' ? 'The action timed out.' : error.message, meta: 'Windows action failed' };
      session.messages.push(saved); save(); $('#messages').append(messageNode(saved));
    } finally {
      state.busy = false;
      $('#send').disabled = false;
      $('#prompt').focus();
      $('#conversation').scrollTop = $('#conversation').scrollHeight;
      setReady(state.health?.candidate_ready ? `${state.health.model} ready` : 'Setup incomplete');
    }
  }

  async function send(text) {
    const prompt = String(text || '').trim();
    if (!prompt || state.busy) return;
    if (prompt.startsWith('!')) return runAction(prompt);

    const session = current();
    state.busy = true;
    appendUserMessage(prompt);
    setBusy('Aerynza native is thinking…');
    const { live, node, wrap, body, metaNode } = appendAssistantPlaceholder('Aerynza native is thinking…');
    let meta = {};
    let done = {};
    const payload = {
      shell: state.shell,
      tier: state.tier,
      messages: session.messages.map(({ role, content }) => ({ role, content })),
      surface: 'standalone_lab',
      mode: 'conversation',
      context: shellContext()
    };

    const abortController = new AbortController();
    state.currentAbort = abortController;
    $('#stop').hidden = false;

    function renderImageBody(caption, url) {
      body.textContent = '';
      const p = document.createElement('p');
      p.textContent = caption || 'Generated image:';
      body.append(p);
      const img = document.createElement('img');
      img.src = safeImageUrl(url) || url;
      img.alt = 'DALL-E 3 image';
      img.style.maxWidth = '100%';
      img.style.borderRadius = '8px';
      body.append(img);
      $('#conversation').scrollTop = $('#conversation').scrollHeight;
    }

    function onEvent(event, data) {
      if (event === 'meta') {
        meta = data;
        live.data = buildData(data.cognition);
        appendDataPanel(live.data, wrap);
        const talentCount = data.cognition?.talents?.length || 0;
        metaNode.textContent = `${data.shell || state.shell} · ${data.tier || state.tier} · ${talentCount} relevant talents · ${data.model || 'Aerynza native'}`;
      }
      if (event === 'token') {
        body.textContent += data.token || '';
        $('#conversation').scrollTop = $('#conversation').scrollHeight;
      }
      if (event === 'media') {
        live.content = data.message || '';
        live.imageUrl = safeImageUrl(data.url);
        renderImageBody(data.message, data.url);
      }
      if (event === 'done') done = data;
    }

    try {
      const streamed = await streamRequest(payload, onEvent, 180000, abortController.signal);
      if (streamed === null) {
        const result = await request('/chat', { method: 'POST', body: JSON.stringify(payload) }, 180000, abortController.signal);
        if (result.imageUrl) {
          live.content = result.content || '';
          live.imageUrl = safeImageUrl(result.imageUrl);
          renderImageBody(result.content, result.imageUrl);
        } else {
          body.textContent = result.content;
        }
        meta = result;
        done = result;
        live.data = buildData(result.cognition);
        appendDataPanel(live.data, wrap);
      }
      if (!body.textContent.trim() && !live.imageUrl) throw new Error('Aerynza native returned an empty response.');
      live.content = body.textContent || live.content || '';
      live.meta = `${meta.shell || state.shell} shell · ${meta.tier || state.tier} · ${meta.provider || 'Aerynza native'} · ${meta.model || 'model unknown'} · ${done.latency_ms || 0} ms`;
      metaNode.textContent = live.meta;
      session.messages.push(live);
      save();
      speak(live.content);
    } catch (error) {
      if (error.name === 'AbortError' && abortController.signal.aborted) {
        live.content = body.textContent.trim() || 'Stopped before any response.';
        live.meta = `${meta.shell || state.shell} · stopped`;
        metaNode.textContent = live.meta;
        session.messages.push(live);
        save();
      } else {
        node.remove();
        const saved = {
          role: 'assistant',
          content: error.name === 'AbortError' ? 'The native model timed out before completing this response.' : error.message,
          meta: 'Candidate unavailable · no fallback or substitution occurred'
        };
        session.messages.push(saved);
        save();
        $('#messages').append(messageNode(saved));
      }
    } finally {
      state.busy = false;
      state.currentAbort = null;
      $('#stop').hidden = true;
      $('#send').disabled = false;
      $('#prompt').focus();
      $('#conversation').scrollTop = $('#conversation').scrollHeight;
      setReady(state.health?.candidate_ready ? `${state.health.model} ready` : 'Setup incomplete');
    }
  }

  async function readHealth() {
    try {
      state.health = await request('/health', {}, 12000);
      const node = $('#status');
      node.classList.toggle('ready', state.health.candidate_ready);
      const talents = state.talents?.counts?.active;
      node.querySelector('span').textContent = state.health.candidate_ready
        ? `${state.health.model} ready${talents ? ` · ${talents} talents` : ''}`
        : 'Setup incomplete';
    } catch (_) {
      $('#status span').textContent = 'Service unavailable';
    }
  }

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(THEME_KEY, theme);
    $('#theme-toggle').textContent = theme === 'light' ? 'Dark mode' : 'Light mode';
  }

  function bindHistory() {
    $('#new-chat').onclick = createSession;
    $('#menu').onclick = () => $('#sidebar').classList.toggle('open');
  }

  function bindSelectors() {
    $('#shell-select').onchange = event => {
      state.shell = event.target.value;
      renderStarters();
      createSession();
      toast(`Switched to ${event.target.options[event.target.selectedIndex].text}`);
    };
    $('#tier-select').onchange = event => {
      state.tier = event.target.value;
      createSession();
      toast(`Switched to ${event.target.options[event.target.selectedIndex].text}`);
    };
  }

  function bindTheme() {
    $('#theme-toggle').onclick = () => {
      const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      applyTheme(next);
    };
  }

  function bindComposer() {
    $('#composer').onsubmit = event => {
      event.preventDefault();
      send($('#prompt').value);
    };
    $('#prompt').addEventListener('input', resize);
    $('#prompt').addEventListener('keydown', event => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        $('#composer').requestSubmit();
      }
    });
    $('#stop').onclick = () => {
      if (state.currentAbort) {
        state.currentAbort.abort();
        state.currentAbort = null;
      }
    };
  }

  function renderStarters() {
    const container = $('#starters');
    if (!container) return;
    container.querySelectorAll('[data-shell]').forEach(button => {
      button.hidden = button.dataset.shell !== state.shell;
    });
  }

  function bindStarters() {
    const container = $('#starters');
    if (!container) return;
    container.addEventListener('click', event => {
      const button = event.target.closest('[data-prompt]');
      if (!button) return;
      if (button.dataset.shell) {
        state.shell = button.dataset.shell;
        $('#shell-select').value = state.shell;
      }
      send(button.dataset.prompt);
    });
  }

  function bindVoice() {
    $('#voice-toggle').onclick = () => {
      state.voiceOn = !state.voiceOn;
      localStorage.setItem(VOICE_KEY, state.voiceOn ? '1' : '');
      $('#voice-toggle').textContent = state.voiceOn ? 'Voice on' : 'Voice';
      $('#voice-toggle').classList.toggle('on', state.voiceOn);
      if (!state.voiceOn) window.speechSynthesis?.cancel();
    };
  }

  function bindFileUpload() {
    $('#attach').onclick = () => $('#file-upload').click();
    $('#file-upload').onchange = event => {
      const file = event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        const current = $('#prompt').value;
        const snippet = String(reader.result).slice(0, 10000);
        $('#prompt').value = current ? `${current}\n\n--- file: ${file.name} ---\n${snippet}` : `--- file: ${file.name} ---\n${snippet}`;
        resize();
        toast(`Loaded ${file.name}`);
      };
      reader.onerror = () => toast('Could not read file.');
      reader.readAsText(file);
    };
  }

  function bindMic() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';
      recognition.onresult = event => {
        const transcript = event.results[0][0].transcript;
        $('#prompt').value = transcript;
        resize();
      };
      recognition.onerror = () => toast('Voice input failed. Try again.');
      $('#mic').onclick = () => {
        try { recognition.start(); toast('Listening…'); } catch (_) { toast('Mic already active.'); }
      };
    } else {
      $('#mic').onclick = () => toast('Voice input not supported in this browser.');
    }
  }

  function bindHelp() {
    const panel = $('#command-help');
    const toggle = show => { panel.hidden = !show; };
    $('#help').onclick = () => toggle(panel.hidden);
    $('#help-link').onclick = event => { event.preventDefault(); toggle(true); };
    $('#close-help').onclick = () => toggle(false);
  }

  function bind() {
    bindHistory();
    bindSelectors();
    bindTheme();
    bindComposer();
    bindStarters();
    bindVoice();
    bindFileUpload();
    bindMic();
    bindHelp();
    renderStarters();
  }

  async function boot() {
    migrateStorage(THEME_KEY, LEGACY_THEME_KEY);
    migrateStorage(VOICE_KEY, LEGACY_VOICE_KEY);
    migrateStorage(SESSION_KEY, LEGACY_SESSION_KEY);

    const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
    applyTheme(savedTheme);
    state.voiceOn = localStorage.getItem(VOICE_KEY) === '1';
    $('#voice-toggle').textContent = state.voiceOn ? 'Voice on' : 'Voice';
    $('#voice-toggle').classList.toggle('on', state.voiceOn);

    load();
    bind();
    await readHealth();
    try { state.talents = await request('/v1/talents', {}, 12000); } catch (_) { state.talents = []; }
    $('#shell').hidden = false;
    render();
    readHealth();
  }

  document.addEventListener('DOMContentLoaded', boot);
})();
