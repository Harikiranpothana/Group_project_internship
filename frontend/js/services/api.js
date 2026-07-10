// js/services/api.js
// Handles all communication with the FastAPI backend.

const BASE_URL = 'http://localhost:8000/api';

/**
 * Sends a natural-language business question to the backend and
 * returns a normalized result object.
 *
 * @param {string} question
 * @returns {Promise<{
 *   success: boolean,
 *   message: string,
 *   question: string,
 *   answer: string,
 *   row_count: number,
 *   data: Array<Record<string, any>>
 * }>}
 */
export async function askQuestion(question) {
  let response;

  try {
    response = await fetch(`${BASE_URL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
  } catch (networkError) {
    // fetch() only throws for network-level failures (offline, DNS, CORS, etc.)
    const err = new Error(`Network error — could not reach the InsightIQ backend at ${BASE_URL}.`);
    err.status = 0;
    throw err;
  }

  let payload = {};
  try {
    payload = await response.json();
  } catch {
    payload = {};
  }

  if (!response.ok) {
    const backendMessage =
      payload.message ||
      payload.detail ||
      payload.answer ||
      `The backend returned an error (${response.status}) while processing this question.`;
    const err = new Error(backendMessage);
    err.status = response.status;
    throw err;
  }

  return {
    success: payload.success ?? true,
    message: payload.message ?? 'Query executed successfully.',
    question: payload.question ?? question,
    answer: payload.answer ?? '',
    row_count: payload.row_count ?? (Array.isArray(payload.data) ? payload.data.length : 0),
    data: Array.isArray(payload.data) ? payload.data : [],
  };
}
