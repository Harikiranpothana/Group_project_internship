// js/app.js
import { askQuestion } from './services/api.js';
import { addUserMessage, addLoadingMessage, addAssistantMessage, addErrorMessage } from './components/ChatBubble.js';

const emptyState = document.getElementById('emptyState');
const conversation = document.getElementById('conversation');
const promptForm = document.getElementById('promptForm');
const promptInput = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const darkModeToggle = document.getElementById('darkModeToggle');
const iconSun = document.getElementById('iconSun');
const iconMoon = document.getElementById('iconMoon');
const examples = document.getElementById('examples');

let isSending = false;

/* ---------------------------------------------------------
   Dark mode
--------------------------------------------------------- */
function applyTheme(theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark');
  iconSun.style.display = theme === 'dark' ? 'none' : 'block';
  iconMoon.style.display = theme === 'dark' ? 'block' : 'none';
  localStorage.setItem('insightiq-theme', theme);
}

(function initTheme() {
  const saved = localStorage.getItem('insightiq-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? 'dark' : 'light'));
})();

darkModeToggle.addEventListener('click', () => {
  const isDark = document.documentElement.classList.contains('dark');
  applyTheme(isDark ? 'light' : 'dark');
});

/* ---------------------------------------------------------
   Composer: autosize, enable/disable, enter-to-send
--------------------------------------------------------- */
function autosizeTextarea() {
  promptInput.style.height = 'auto';
  promptInput.style.height = Math.min(promptInput.scrollHeight, 160) + 'px';
}

function updateSendState() {
  sendBtn.disabled = isSending || promptInput.value.trim().length === 0;
}

promptInput.addEventListener('input', () => {
  autosizeTextarea();
  updateSendState();
});

promptInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    promptForm.requestSubmit();
  }
});

promptInput.focus();

/* ---------------------------------------------------------
   New chat
--------------------------------------------------------- */
newChatBtn.addEventListener('click', () => {
  conversation.innerHTML = '';
  conversation.classList.remove('is-active');
  emptyState.style.display = 'flex';
  promptInput.value = '';
  autosizeTextarea();
  updateSendState();
  promptInput.focus();
});

/* ---------------------------------------------------------
   Example chips
--------------------------------------------------------- */
examples.addEventListener('click', (e) => {
  const chip = e.target.closest('.example-chip');
  if (!chip) return;
  promptInput.value = chip.dataset.question;
  autosizeTextarea();
  updateSendState();
  promptForm.requestSubmit();
});

/* ---------------------------------------------------------
   Submit flow
--------------------------------------------------------- */
promptForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const question = promptInput.value.trim();
  if (!question || isSending) return;

  // Reveal the conversation, hide the welcome screen on first send.
  emptyState.style.display = 'none';
  conversation.classList.add('is-active');

  addUserMessage(conversation, question);

  promptInput.value = '';
  autosizeTextarea();

  isSending = true;
  promptInput.disabled = true;
  updateSendState();

  const loading = addLoadingMessage(conversation);
  scrollToBottom();

  try {
    const result = await askQuestion(question);
    loading.stop();
    loading.el.remove();

    if (result.success === false) {
      addErrorMessage(conversation, result.message || 'The backend could not process this question.');
    } else {
      addAssistantMessage(conversation, result);
    }
  } catch (err) {
    loading.stop();
    loading.el.remove();
    addErrorMessage(conversation, err.message || 'Something went wrong while sending your question.');
  } finally {
    isSending = false;
    promptInput.disabled = false;
    updateSendState();
    promptInput.focus();
    scrollToBottom();
  }
});

function scrollToBottom() {
  requestAnimationFrame(() => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  });
}

updateSendState();
