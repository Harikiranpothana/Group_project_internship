// js/components/ChatBubble.js
// Small DOM-templating helpers for the conversation thread.

import { renderResultTable } from './ResultTable.js';

function formatTime(date = new Date()) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/**
 * Appends a right-aligned user bubble to the conversation.
 * @returns {HTMLElement} the mounted message node
 */
export function addUserMessage(conversationEl, text) {
  const tpl = document.getElementById('tpl-user-message');
  const node = tpl.content.cloneNode(true);
  node.querySelector('.msg__text').textContent = text;
  node.querySelector('.msg__time').textContent = formatTime();
  const el = node.querySelector('.msg');
  conversationEl.appendChild(node);
  return el;
}

/**
 * Appends an animated "thinking" bubble with rotating status text.
 * @returns {{ el: HTMLElement, stop: () => void }}
 */
export function addLoadingMessage(conversationEl) {
  const tpl = document.getElementById('tpl-loading');
  const node = tpl.content.cloneNode(true);
  const el = node.querySelector('.msg');
  const textEl = node.querySelector('.loading-text');

  const messages = [
    'Generating SQL...',
    'Validating Query...',
    'Running Query...',
    'Fetching Data...',
    'Almost Done...',
  ];
  let i = 0;
  textEl.textContent = messages[0];
  const interval = setInterval(() => {
    i = (i + 1) % messages.length;
    textEl.textContent = messages[i];
  }, 1800);

  conversationEl.appendChild(node);

  return {
    el,
    stop: () => clearInterval(interval),
  };
}

/**
 * Appends a left-aligned assistant bubble with the AI explanation, and,
 * if rows are present, a result table beneath it. Hides the explanation
 * entirely when `answer` is empty, per spec.
 */
export function addAssistantMessage(conversationEl, { answer, data, row_count }) {
  const tpl = document.getElementById('tpl-assistant-message');
  const node = tpl.content.cloneNode(true);
  const bodyEl = node.querySelector('.msg__body');
  const bubbleEl = node.querySelector('.msg__bubble--assistant');
  const timeEl = node.querySelector('.msg__time');
  const copyBtn = node.querySelector('.copy-answer-btn');
  const colEl = node.querySelector('.msg__col');

  timeEl.textContent = formatTime();

  const hasAnswer = typeof answer === 'string' && answer.trim().length > 0;

  if (hasAnswer) {
    bodyEl.textContent = answer;
    copyBtn.style.display = 'inline-flex';
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(answer);
        const original = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.classList.add('is-copied');
        setTimeout(() => {
          copyBtn.textContent = original;
          copyBtn.classList.remove('is-copied');
        }, 1500);
      } catch {
        /* clipboard unavailable */
      }
    });
  } else {
    // Hide the explanation section completely when there's no answer text.
    bubbleEl.style.display = 'none';
  }

  const el = node.querySelector('.msg');
  conversationEl.appendChild(node);

  if (Array.isArray(data) && data.length > 0) {
    renderResultTable(colEl, data, row_count);
  } else if (hasAnswer === false) {
    // No answer and no rows — still let the user know nothing came back.
    bodyEl.textContent = 'No matching records found.';
    bubbleEl.style.display = '';
  }

  return el;
}

/** Appends a red rounded error alert with the backend's message. */
export function addErrorMessage(conversationEl, message) {
  const tpl = document.getElementById('tpl-error');
  const node = tpl.content.cloneNode(true);
  node.querySelector('.error-alert__message').textContent = message;
  const el = node.querySelector('.error-alert');
  conversationEl.appendChild(node);
  return el;
}
