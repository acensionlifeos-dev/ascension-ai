const summary = document.getElementById('summary');
const grid = document.getElementById('grid');
const filters = document.getElementById('filters');
const status = document.getElementById('status');

let data = [];
let categories = new Set();

async function load() {
  try {
    const res = await fetch('/static/capability_report.json');
    const report = await res.json();
    data = report.capabilities;
    categories = new Set(data.map(c => c.category));
    renderSummary(report);
    renderFilters();
    renderGrid(data);
    status.innerHTML = '<i></i><span>Report loaded</span>';
  } catch (err) {
    status.innerHTML = `<i></i><span>Failed to load report: ${err.message}</span>`;
  }
}

function renderSummary(report) {
  summary.innerHTML = `
    <div class="card ok"><strong>${report.per_capability_ready}</strong><label>Per-capability passed / ${report.total}</label></div>
    <div class="card ok"><strong>${(report.per_capability_rate * 100).toFixed(1)}%</strong><label>Per-capability rate</label></div>
    <div class="card ${report.execution_ready === report.total ? 'ok' : 'warn'}"><strong>${report.execution_ready}</strong><label>Execution passed / ${report.total}</label></div>
    <div class="card ${report.execution_ready === report.total ? 'ok' : 'warn'}"><strong>${(report.execution_rate * 100).toFixed(1)}%</strong><label>Execution rate</label></div>
  `;
}

function renderFilters() {
  const catOptions = ['<option value="">All categories</option>', ...Array.from(categories).sort().map(c => `<option value="${c}">${c}</option>`)].join('');
  filters.innerHTML = `
    <select id="category"><option value="">All categories</option></select>
    <select id="status"><option value="">All statuses</option><option value="pass">Pass both</option><option value="fail">Any fail</option></select>
    <input type="text" id="search" placeholder="Search capability…">
  `;
  filters.querySelector('#category').innerHTML = catOptions;
  filters.querySelector('#category').addEventListener('change', () => applyFilters());
  filters.querySelector('#status').addEventListener('change', () => applyFilters());
  filters.querySelector('#search').addEventListener('input', () => applyFilters());
}

function applyFilters() {
  const cat = filters.querySelector('#category').value;
  const stat = filters.querySelector('#status').value;
  const search = filters.querySelector('#search').value.toLowerCase();
  const filtered = data.filter(c => {
    if (cat && c.category !== cat) return false;
    if (stat === 'pass' && !(c.per_capability_passed && c.execution_passed)) return false;
    if (stat === 'fail' && (c.per_capability_passed && c.execution_passed)) return false;
    if (search && !c.name.toLowerCase().includes(search) && !c.id.toLowerCase().includes(search)) return false;
    return true;
  });
  renderGrid(filtered);
}

function renderGrid(items) {
  grid.innerHTML = items.map(c => `
    <div class="item ${c.execution_passed && c.per_capability_passed ? '' : 'fail'}">
      <div class="id">${c.id}</div>
      <h3>${c.name}</h3>
      <div class="tags">
        <span class="tag">${c.category}</span>
        <span class="tag">${c.shell}</span>
        <span class="tag ${c.per_capability_passed ? 'ok' : 'fail'}">${c.per_capability_passed ? 'cap ok' : 'cap fail'}</span>
        <span class="tag ${c.execution_passed ? 'ok' : 'fail'}">${c.execution_passed ? 'exec ok' : 'exec fail'}</span>
      </div>
    </div>
  `).join('');
}

load();
