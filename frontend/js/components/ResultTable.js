// js/components/ResultTable.js
// Renders a dynamic, sortable, searchable, paginated table from an array of
// row objects with automatic column detection. No hardcoded columns.

function humanizeColumn(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .split(' ')
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

function formatCell(value) {
  if (value === null || value === undefined) return '—';
  if (typeof value === 'boolean') return value ? 'True' : 'False';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function toCSV(columns, rows) {
  const escape = (val) => {
    const s = formatCell(val);
    if (/[",\n]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
    return s;
  };
  const header = columns.map((c) => escape(humanizeColumn(c))).join(',');
  const lines = rows.map((row) => columns.map((c) => escape(row[c])).join(','));
  return [header, ...lines].join('\n');
}

/**
 * Mounts a fully interactive result table into `container` using the
 * `#tpl-result-table` template. Returns nothing — it's a fire-and-forget
 * render, matching the rest of the app's simple DOM-templating approach.
 *
 * @param {HTMLElement} container - element to append the table card into
 * @param {Array<Record<string, any>>} data
 * @param {number} rowCount
 */
export function renderResultTable(container, data, rowCount) {
  const tpl = document.getElementById('tpl-result-table');
  const node = tpl.content.cloneNode(true);
  const card = node.querySelector('.result-card');

  const columns = data.length > 0 ? Object.keys(data[0]) : [];

  const state = {
    sortKey: null,
    sortDir: 'asc', // 'asc' | 'desc'
    search: '',
    page: 1,
    pageSize: 10,
  };

  const rowCountEl = card.querySelector('.row-count-num');
  rowCountEl.textContent = rowCount ?? data.length;

  const thead = card.querySelector('thead');
  const tbody = card.querySelector('tbody');
  const tableEmpty = card.querySelector('.table-empty');
  const tableScroll = card.querySelector('.table-scroll');
  const searchInput = card.querySelector('.search-input');
  const rowsSelect = card.querySelector('.rows-select');
  const pageStatus = card.querySelector('.page-status');
  const pagePrev = card.querySelector('.page-prev');
  const pageNext = card.querySelector('.page-next');
  const copyTableBtn = card.querySelector('.copy-table-btn');
  const downloadBtn = card.querySelector('.download-csv-btn');

  if (columns.length === 0) {
    tableScroll.style.display = 'none';
    card.querySelector('.table-footer').style.display = 'none';
    tableEmpty.style.display = 'block';
    tableEmpty.textContent = 'No matching records found.';
    container.appendChild(node);
    return;
  }

  // --- Header ---
  const headerRow = document.createElement('tr');
  columns.forEach((col) => {
    const th = document.createElement('th');
    th.dataset.col = col;
    th.innerHTML = `<span class="th-inner">${humanizeColumn(col)}<span class="sort-icon">↕</span></span>`;
    th.addEventListener('click', () => {
      if (state.sortKey === col) {
        state.sortDir = state.sortDir === 'asc' ? 'desc' : 'asc';
      } else {
        state.sortKey = col;
        state.sortDir = 'asc';
      }
      state.page = 1;
      render();
    });
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);

  function getFilteredSortedRows() {
    let rows = data;

    if (state.search.trim()) {
      const q = state.search.trim().toLowerCase();
      rows = rows.filter((row) =>
        columns.some((col) => formatCell(row[col]).toLowerCase().includes(q))
      );
    }

    if (state.sortKey) {
      const key = state.sortKey;
      const dir = state.sortDir === 'asc' ? 1 : -1;
      rows = [...rows].sort((a, b) => {
        const av = a[key];
        const bv = b[key];
        if (av === null || av === undefined) return 1;
        if (bv === null || bv === undefined) return -1;
        if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * dir;
        return String(av).localeCompare(String(bv), undefined, { numeric: true }) * dir;
      });
    }

    return rows;
  }

  function render() {
    // header sort indicators
    headerRow.querySelectorAll('th').forEach((th) => {
      const col = th.dataset.col;
      const icon = th.querySelector('.sort-icon');
      if (col === state.sortKey) {
        th.classList.add('is-sorted');
        icon.textContent = state.sortDir === 'asc' ? '↑' : '↓';
      } else {
        th.classList.remove('is-sorted');
        icon.textContent = '↕';
      }
    });

    const filtered = getFilteredSortedRows();
    const totalPages = Math.max(1, Math.ceil(filtered.length / state.pageSize));
    state.page = Math.min(state.page, totalPages);

    const start = (state.page - 1) * state.pageSize;
    const pageRows = filtered.slice(start, start + state.pageSize);

    tbody.innerHTML = '';

    if (filtered.length === 0) {
      tableScroll.style.display = 'none';
      tableEmpty.style.display = 'block';
    } else {
      tableScroll.style.display = 'block';
      tableEmpty.style.display = 'none';
      pageRows.forEach((row) => {
        const tr = document.createElement('tr');
        columns.forEach((col) => {
          const td = document.createElement('td');
          td.textContent = formatCell(row[col]);
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }

    pageStatus.textContent = `Page ${state.page} of ${totalPages}`;
    pagePrev.disabled = state.page <= 1;
    pageNext.disabled = state.page >= totalPages;
  }

  searchInput.addEventListener('input', (e) => {
    state.search = e.target.value;
    state.page = 1;
    render();
  });

  rowsSelect.addEventListener('change', (e) => {
    state.pageSize = Number(e.target.value);
    state.page = 1;
    render();
  });

  pagePrev.addEventListener('click', () => {
    state.page = Math.max(1, state.page - 1);
    render();
  });

  pageNext.addEventListener('click', () => {
    state.page += 1;
    render();
  });

  copyTableBtn.addEventListener('click', async () => {
    const filtered = getFilteredSortedRows();
    const csv = toCSV(columns, filtered);
    try {
      await navigator.clipboard.writeText(csv);
      const original = copyTableBtn.innerHTML;
      copyTableBtn.textContent = 'Copied!';
      copyTableBtn.classList.add('is-copied');
      setTimeout(() => {
        copyTableBtn.innerHTML = original;
        copyTableBtn.classList.remove('is-copied');
      }, 1500);
    } catch {
      /* clipboard unavailable — silently ignore */
    }
  });

  downloadBtn.addEventListener('click', () => {
    const filtered = getFilteredSortedRows();
    const csv = toCSV(columns, filtered);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'insightiq-results.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  render();
  container.appendChild(node);
}
