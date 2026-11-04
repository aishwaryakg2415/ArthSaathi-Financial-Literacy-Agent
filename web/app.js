/* ============================================================
   ArthSaathi – app.js
   Vanilla JavaScript – no frameworks, no build step
   ============================================================ */

(function () {
  'use strict';

  // ── Config ────────────────────────────────────────────────
  const cfg = (typeof window.ARTHSAATHI_CONFIG === 'object' && window.ARTHSAATHI_CONFIG) || {};
  const LANGFLOW_URL = cfg.LANGFLOW_URL || '';
  const LANGFLOW_API_KEY = cfg.LANGFLOW_API_KEY || '';

  // Stable session id for this browser tab
  const SESSION_ID = 'as_' + Math.random().toString(36).slice(2) + Date.now().toString(36);

  // ── DOM refs ──────────────────────────────────────────────
  const chatWindow     = document.getElementById('chat-window');
  const msgInput       = document.getElementById('msg-input');
  const sendBtn        = document.getElementById('send-btn');
  const warnBar        = document.getElementById('warn-bar');
  const langSelect     = document.getElementById('lang-select');
  const scamToggleBtn  = document.getElementById('scam-toggle-btn');
  const scamPanel      = document.getElementById('scam-panel');
  const scamTextarea   = document.getElementById('scam-textarea');
  const scamSendBtn    = document.getElementById('scam-send-btn');

  // ── Sensitive-data guard ──────────────────────────────────
  // Matches: 4-6 digit number near PIN/OTP/CVV  OR  12-16 digit card number
  const SENSITIVE_RE = /\b(?:pin|otp|cvv)\b[^0-9]{0,20}[0-9]{4,6}|[0-9]{4,6}[^0-9]{0,20}\b(?:pin|otp|cvv)\b|\b[0-9]{12,16}\b/i;

  function containsSensitiveData(text) {
    return SENSITIVE_RE.test(text);
  }

  // ── HTML escaping ─────────────────────────────────────────
  function escapeHTML(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // ── Simple markdown → HTML ────────────────────────────────
  // Operates on already-escaped text to stay XSS-safe.
  function renderMarkdown(escaped) {
    const lines = escaped.split('\n');
    const out   = [];
    let inUl    = false;
    let inOl    = false;

    function closeList() {
      if (inUl) { out.push('</ul>'); inUl = false; }
      if (inOl) { out.push('</ol>'); inOl = false; }
    }

    let table   = null;

    function flushTable() {
      if (!table) return;
      out.push('<div class="table-wrap"><table>' + table.join('') + '</table></div>');
      table = null;
    }

    lines.forEach(function (line) {
      // Table row: "| a | b |"  (separator rows like "|---|---|" are skipped)
      if (/^\s*\|.*\|\s*$/.test(line)) {
        closeList();
        if (/^\s*\|[\s:|-]+\|\s*$/.test(line)) return;
        const cells = line.trim().slice(1, -1).split('|').map(function (c) { return applyInline(c.trim()); });
        const tag = table ? 'td' : 'th';
        table = table || [];
        table.push('<tr>' + cells.map(function (c) { return '<' + tag + '>' + c + '</' + tag + '>'; }).join('') + '</tr>');
        return;
      }
      flushTable();
      if (line.trim() === '') return;

      // Heading: "# ", "## ", "### "
      const hMatch = line.match(/^#{1,6}\s+(.*)/);
      if (hMatch) {
        closeList();
        out.push('<h4>' + applyInline(hMatch[1]) + '</h4>');
        return;
      }
      // Horizontal rule
      if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) {
        closeList();
        out.push('<hr>');
        return;
      }

      // Numbered list:  "1. " or "1) "
      const olMatch = line.match(/^(\d+)[.)]\s+(.*)/);
      // Bullet list:    "- " or "* " (may be indented)
      const ulMatch = line.match(/^\s*[-*•]\s+(.*)/);

      if (ulMatch) {
        if (inOl) { out.push('</ol>'); inOl = false; }
        if (!inUl) { out.push('<ul>'); inUl = true; }
        out.push('<li>' + applyInline(ulMatch[1]) + '</li>');
      } else if (olMatch) {
        if (inUl) { out.push('</ul>'); inUl = false; }
        if (!inOl) { out.push('<ol>'); inOl = true; }
        out.push('<li>' + applyInline(olMatch[2]) + '</li>');
      } else {
        closeList();
        if (line.trim() === '') {
          // blank line – skip or keep as paragraph break
          out.push('');
        } else {
          out.push('<p>' + applyInline(line) + '</p>');
        }
      }
    });
    closeList();
    flushTable();
    return out.join('\n');
  }

  // Apply inline: **bold**, *italic*, `code`, <br>
  function applyInline(text) {
    return text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*])\*([^*\s][^*]*?)\*(?!\*)/g, '$1<em>$2</em>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/&lt;br\s*\/?&gt;/gi, '<br>');
  }

  // ── Append a message bubble ───────────────────────────────
  function appendMessage(role, htmlContent) {
    const row    = document.createElement('div');
    row.className = 'msg-row ' + role;

    const avatar  = document.createElement('div');
    avatar.className = 'avatar ' + role;
    avatar.textContent = role === 'user' ? 'You' : 'AS';
    avatar.setAttribute('aria-hidden', 'true');

    const bubble  = document.createElement('div');
    bubble.className = 'bubble';

    if (role === 'user') {
      // user messages: plain escaped text, preserve line breaks
      bubble.innerHTML = htmlContent.replace(/\n/g, '<br>');
    } else {
      // agent messages: render simple markdown
      bubble.innerHTML = htmlContent;
    }

    if (role === 'user') {
      row.appendChild(bubble);
      row.appendChild(avatar);
    } else {
      row.appendChild(avatar);
      row.appendChild(bubble);
    }

    chatWindow.appendChild(row);
    scrollToBottom();
    return bubble;
  }

  // ── Typing indicator ──────────────────────────────────────
  let typingRow = null;

  function showTyping() {
    if (typingRow) return;
    typingRow = document.createElement('div');
    typingRow.className = 'msg-row agent';

    const avatar = document.createElement('div');
    avatar.className = 'avatar agent';
    avatar.textContent = 'AS';
    avatar.setAttribute('aria-hidden', 'true');

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerHTML =
      '<div class="typing-indicator" aria-label="ArthSaathi is typing">' +
      '<div class="dot"></div><div class="dot"></div><div class="dot"></div>' +
      '</div>';

    typingRow.appendChild(avatar);
    typingRow.appendChild(bubble);
    chatWindow.appendChild(typingRow);
    scrollToBottom();
  }

  function hideTyping() {
    if (typingRow) {
      typingRow.remove();
      typingRow = null;
    }
  }

  // ── Scroll chat to bottom ─────────────────────────────────
  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // ── Sensitive-data warning ────────────────────────────────
  function showWarn() {
    warnBar.classList.add('visible');
    setTimeout(function () { warnBar.classList.remove('visible'); }, 6000);
  }

  // ── Send a message to Langflow ────────────────────────────
  async function sendMessage(userText) {
    userText = userText.trim();
    if (!userText) return;

    // Sensitive-data guard
    if (containsSensitiveData(userText)) {
      showWarn();
      return;
    }

    // Language prefix
    const lang = langSelect.value;
    const payload = lang
      ? 'Please reply in ' + lang + '.\n\n' + userText
      : userText;

    // Show user bubble (unmodified text, no language prefix)
    appendMessage('user', escapeHTML(userText));

    // Lock input
    sendBtn.disabled = true;
    msgInput.disabled = true;
    showTyping();

    // No URL configured → helpful error
    if (!LANGFLOW_URL || LANGFLOW_URL.includes('<FLOW_ID>')) {
      hideTyping();
      appendMessage('agent',
        renderMarkdown(escapeHTML(
          'ArthSaathi is not connected yet.\n' +
          'Please copy config.example.js to config.js and fill in your LANGFLOW_URL.'
        ))
      );
      unlock();
      return;
    }

    const headers = { 'Content-Type': 'application/json' };
    if (LANGFLOW_API_KEY) headers['x-api-key'] = LANGFLOW_API_KEY;

    const body = JSON.stringify({
      input_value:  payload,
      input_type:   'chat',
      output_type:  'chat',
      session_id:   SESSION_ID
    });

    try {
      const resp = await fetch(LANGFLOW_URL, { method: 'POST', headers: headers, body: body });

      if (!resp.ok) {
        throw new Error('Server returned ' + resp.status + ' ' + resp.statusText);
      }

      const data = await resp.json();

      // Extract reply text: data.outputs[0].outputs[0].results.message.text
      let replyText;
      try {
        replyText = data.outputs[0].outputs[0].results.message.text;
        if (typeof replyText !== 'string' || !replyText) throw new Error('empty');
      } catch (_) {
        // Fallback: show raw JSON
        replyText = '_(Raw response)_\n```\n' + JSON.stringify(data, null, 2) + '\n```';
        hideTyping();
        appendMessage('agent', '<pre style="white-space:pre-wrap;font-size:0.8rem">' + escapeHTML(JSON.stringify(data, null, 2)) + '</pre>');
        unlock();
        return;
      }

      hideTyping();
      appendMessage('agent', renderMarkdown(escapeHTML(replyText)));

    } catch (err) {
      hideTyping();
      appendMessage('agent',
        renderMarkdown(escapeHTML(
          'Sorry, I could not reach the server right now. Please check your connection and try again.\n\n' +
          'Error: ' + err.message
        ))
      );
    }

    unlock();
  }

  function unlock() {
    sendBtn.disabled  = false;
    msgInput.disabled = false;
    msgInput.focus();
  }

  // ── Event: send button ────────────────────────────────────
  sendBtn.addEventListener('click', function () {
    const text = msgInput.value;
    msgInput.value = '';
    autoResize();
    sendMessage(text);
  });

  // ── Event: Enter key (Shift+Enter = new line) ─────────────
  msgInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const text = msgInput.value;
      msgInput.value = '';
      autoResize();
      sendMessage(text);
    }
  });

  // ── Auto-resize textarea ──────────────────────────────────
  function autoResize() {
    msgInput.style.height = 'auto';
    msgInput.style.height = Math.min(msgInput.scrollHeight, 130) + 'px';
  }
  msgInput.addEventListener('input', autoResize);

  // ── Event: quick chips ────────────────────────────────────
  document.querySelectorAll('.chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      sendMessage(chip.dataset.q);
    });
  });

  // ── Event: scam checker toggle ────────────────────────────
  scamToggleBtn.addEventListener('click', function () {
    const isOpen = scamPanel.classList.toggle('open');
    scamToggleBtn.setAttribute('aria-expanded', String(isOpen));
    scamPanel.setAttribute('aria-hidden',       String(!isOpen));
    if (isOpen) scamTextarea.focus();
  });

  // ── Event: scam send ─────────────────────────────────────
  scamSendBtn.addEventListener('click', function () {
    const txt = scamTextarea.value.trim();
    if (!txt) return;
    scamTextarea.value = '';
    scamPanel.classList.remove('open');
    scamToggleBtn.setAttribute('aria-expanded', 'false');
    scamPanel.setAttribute('aria-hidden', 'true');
    sendMessage('Check this message for scam red flags: ' + txt);
  });

  // ── Welcome message ───────────────────────────────────────
  appendMessage('agent',
    renderMarkdown(escapeHTML(
      'Namaste! 🙏 I am **ArthSaathi**, your digital financial literacy guide.\n\n' +
      'I can help you with:\n' +
      '- UPI & mobile payments\n' +
      '- Spotting scams and fraud\n' +
      '- Savings and government schemes\n' +
      '- Budgeting and loan EMIs\n\n' +
      'Type your question below, or tap one of the quick buttons above.\n' +
      'Choose your preferred language from the dropdown. 🌐'
    ))
  );

})();
