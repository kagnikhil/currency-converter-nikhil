/**
 * app.js - Minimal, clean currency converter logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const state = {
    currencies: {},
    presets: {},
    rates: {},
    multiTargets: ['EUR', 'GBP', 'INR', 'JPY', 'AUD', 'CAD']
  };

  // Theme
  const htmlDoc = document.documentElement;
  const btnTheme = document.getElementById('btnTheme');
  const themeLabel = document.getElementById('themeLabel');
  const savedTheme = localStorage.getItem('theme') || 'dark';
  applyTheme(savedTheme);

  btnTheme.addEventListener('click', () => {
    const isDark = htmlDoc.getAttribute('data-theme') === 'dark';
    applyTheme(isDark ? 'light' : 'dark');
  });

  function applyTheme(theme) {
    htmlDoc.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    themeLabel.textContent = theme === 'dark' ? 'Light' : 'Dark';
  }

  // Segmented Tabs
  const tabButtons = document.querySelectorAll('.segmented-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const targetId = btn.getAttribute('data-tab');
      document.getElementById(targetId).classList.add('active');

      if (targetId === 'tabRates') {
        loadRatesTable();
      }
    });
  });

  // Single Converter elements
  const amountInput = document.getElementById('amountInput');
  const fromCurrencySelect = document.getElementById('fromCurrencySelect');
  const toCurrencySelect = document.getElementById('toCurrencySelect');
  const convertedOutput = document.getElementById('convertedOutput');
  const rateSummary = document.getElementById('rateSummary');
  const btnSwap = document.getElementById('btnSwap');
  const btnCopy = document.getElementById('btnCopy');

  // Multi Converter elements
  const multiAmountInput = document.getElementById('multiAmountInput');
  const multiBaseSelect = document.getElementById('multiBaseSelect');
  const presetsBar = document.getElementById('presetsBar');
  const multiList = document.getElementById('multiList');
  const addCurrencySelect = document.getElementById('addCurrencySelect');

  // Rates elements
  const ratesBaseSelect = document.getElementById('ratesBaseSelect');
  const ratesFilterInput = document.getElementById('ratesFilterInput');
  const ratesTableBody = document.getElementById('ratesTableBody');

  // Status & Sync
  const statusLabel = document.getElementById('statusLabel');
  const btnSync = document.getElementById('btnSync');
  const syncSpin = document.getElementById('syncSpin');

  // Fetch initial data
  async function init() {
    try {
      const resp = await fetch('/api/currencies');
      const data = await resp.json();
      state.currencies = data.currencies;
      state.presets = data.presets;

      populateDropdowns();
      renderPresets();

      convertSingle();
      convertMulti();
      checkStatus();
    } catch (e) {
      console.error(e);
    }
  }

  function populateDropdowns() {
    const sorted = Object.keys(state.currencies).sort();

    fromCurrencySelect.innerHTML = '';
    toCurrencySelect.innerHTML = '';
    multiBaseSelect.innerHTML = '';
    ratesBaseSelect.innerHTML = '';
    addCurrencySelect.innerHTML = '<option value="">+ Add target currency...</option>';

    sorted.forEach(code => {
      const info = state.currencies[code] || {};
      const flag = info.flag || '';
      const name = info.name || code;
      const text = `${flag} ${code} (${name})`;

      fromCurrencySelect.add(new Option(text, code));
      toCurrencySelect.add(new Option(text, code));
      multiBaseSelect.add(new Option(text, code));
      ratesBaseSelect.add(new Option(text, code));
      addCurrencySelect.add(new Option(text, code));
    });

    fromCurrencySelect.value = 'USD';
    toCurrencySelect.value = 'INR';
    multiBaseSelect.value = 'USD';
    ratesBaseSelect.value = 'USD';
  }

  function renderPresets() {
    presetsBar.innerHTML = '<span style="font-size: 0.75rem; color: var(--text-muted); margin-right: 0.25rem;">Presets:</span>';
    Object.entries(state.presets).forEach(([name, list]) => {
      const btn = document.createElement('button');
      btn.className = 'preset-btn';
      btn.textContent = name;
      btn.addEventListener('click', () => {
        const base = multiBaseSelect.value;
        state.multiTargets = list.filter(c => c !== base);
        convertMulti();
      });
      presetsBar.appendChild(btn);
    });
  }

  async function checkStatus() {
    try {
      const resp = await fetch('/api/status');
      const data = await resp.json();
      if (data.is_offline) {
        statusLabel.textContent = `Offline (Cached: ${data.last_updated})`;
        document.querySelector('.dot-online').style.background = 'var(--text-muted)';
      } else {
        statusLabel.textContent = 'Live rates';
        document.querySelector('.dot-online').style.background = 'var(--success)';
      }
    } catch (e) {}
  }

  // Single conversion
  let debounceTimer;
  function onSingleInput() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(convertSingle, 200);
  }

  amountInput.addEventListener('input', onSingleInput);
  fromCurrencySelect.addEventListener('change', convertSingle);
  toCurrencySelect.addEventListener('change', convertSingle);

  btnSwap.addEventListener('click', () => {
    const temp = fromCurrencySelect.value;
    fromCurrencySelect.value = toCurrencySelect.value;
    toCurrencySelect.value = temp;
    convertSingle();
  });

  async function convertSingle() {
    const amount = parseFloat(amountInput.value);
    if (isNaN(amount) || amount < 0) {
      convertedOutput.value = '--';
      return;
    }

    const from = fromCurrencySelect.value;
    const to = toCurrencySelect.value;

    try {
      const resp = await fetch('/api/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, from, to })
      });
      const data = await resp.json();

      if (data.success) {
        convertedOutput.value = formatNumber(data.result);
        rateSummary.innerHTML = `1 <strong>${from}</strong> = ${formatRate(data.rate)} <strong>${to}</strong> <span style="color: var(--text-muted); font-size: 0.75rem; margin-left: 0.5rem;">(1 ${to} = ${formatRate(data.inverse_rate)} ${from})</span>`;
      }
    } catch (e) {
      convertedOutput.value = 'Error';
    }
  }

  btnCopy.addEventListener('click', () => {
    const text = `${amountInput.value} ${fromCurrencySelect.value} = ${convertedOutput.value} ${toCurrencySelect.value}`;
    navigator.clipboard.writeText(text).then(() => {
      btnCopy.textContent = 'Copied!';
      setTimeout(() => { btnCopy.textContent = 'Copy'; }, 1500);
    });
  });

  // Multi conversion
  multiAmountInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(convertMulti, 200);
  });

  multiBaseSelect.addEventListener('change', () => {
    state.multiTargets = state.multiTargets.filter(c => c !== multiBaseSelect.value);
    convertMulti();
  });

  addCurrencySelect.addEventListener('change', () => {
    const val = addCurrencySelect.value;
    if (val && val !== multiBaseSelect.value && !state.multiTargets.includes(val)) {
      state.multiTargets.push(val);
      convertMulti();
    }
    addCurrencySelect.value = '';
  });

  async function convertMulti() {
    const amount = parseFloat(multiAmountInput.value);
    if (isNaN(amount) || amount < 0) return;

    const base = multiBaseSelect.value;
    if (state.multiTargets.length === 0) {
      multiList.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: 1.5rem 0;">No target currencies added.</p>';
      return;
    }

    try {
      const resp = await fetch('/api/convert-multiple', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, base, targets: state.multiTargets })
      });
      const data = await resp.json();

      if (data.success) {
        renderMultiList(base, data.results);
      }
    } catch (e) {
      console.error(e);
    }
  }

  function renderMultiList(base, results) {
    multiList.innerHTML = '';
    results.forEach(item => {
      const code = item.to_curr;
      const info = state.currencies[code] || {};
      const flag = info.flag || '';
      const name = info.name || code;

      const row = document.createElement('div');
      row.className = 'multi-item';
      row.innerHTML = `
        <div class="multi-item-left">
          <span class="currency-flag">${flag}</span>
          <div>
            <div class="multi-code">${code}</div>
            <div class="multi-name">${name}</div>
          </div>
        </div>
        <div class="multi-item-right">
          <div>
            <div class="multi-val">${formatNumber(item.result)}</div>
            <div class="multi-unit-rate">1 ${base} = ${formatRate(item.rate)} ${code}</div>
          </div>
          <button class="btn-remove" title="Remove" aria-label="Remove">&times;</button>
        </div>
      `;

      row.querySelector('.btn-remove').addEventListener('click', () => {
        state.multiTargets = state.multiTargets.filter(c => c !== code);
        convertMulti();
      });

      multiList.appendChild(row);
    });
  }

  // Live Rates Table
  ratesBaseSelect.addEventListener('change', loadRatesTable);
  ratesFilterInput.addEventListener('input', renderRatesTable);

  async function loadRatesTable() {
    const base = ratesBaseSelect.value;
    ratesTableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 1rem;">Loading...</td></tr>';

    try {
      const resp = await fetch(`/api/rates?base=${base}`);
      const data = await resp.json();
      state.rates = data.rates || {};
      renderRatesTable();
    } catch (e) {
      ratesTableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--danger); padding: 1rem;">Error loading rates.</td></tr>';
    }
  }

  function renderRatesTable() {
    const base = ratesBaseSelect.value;
    const query = ratesFilterInput.value.toLowerCase().trim();
    ratesTableBody.innerHTML = '';

    const popular = ['USD', 'EUR', 'GBP', 'INR', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'AED', 'SGD', 'SAR', 'KRW'];
    const codes = Object.keys(state.rates).sort((a, b) => {
      const iA = popular.indexOf(a);
      const iB = popular.indexOf(b);
      if (iA !== -1 && iB !== -1) return iA - iB;
      if (iA !== -1) return -1;
      if (iB !== -1) return 1;
      return a.localeCompare(b);
    });

    let rendered = 0;
    codes.forEach(code => {
      if (code === base) return;
      const info = state.currencies[code] || {};
      const flag = info.flag || '';
      const name = info.name || code;
      const country = info.country || '';

      const searchStr = `${code} ${name} ${country}`.toLowerCase();
      if (query && !searchStr.includes(query)) return;

      rendered++;
      const rate = state.rates[code];
      const inv = rate > 0 ? (1.0 / rate) : 0;

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${flag} ${code}</strong> <span style="color: var(--text-muted); font-size: 0.8rem; margin-left: 0.3rem;">${name}</span></td>
        <td>${country}</td>
        <td style="text-align: right; font-weight: 600;">${formatRate(rate)}</td>
        <td style="text-align: right; color: var(--text-muted);">${formatRate(inv)}</td>
      `;
      ratesTableBody.appendChild(tr);
    });

    if (rendered === 0) {
      ratesTableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 1rem;">No matching currencies.</td></tr>';
    }
  }

  // Sync
  btnSync.addEventListener('click', async () => {
    btnSync.style.opacity = '0.6';
    try {
      await fetch('/api/refresh', { method: 'POST' });
      await convertSingle();
      await convertMulti();
      if (document.getElementById('tabRates').classList.contains('active')) {
        await loadRatesTable();
      }
      await checkStatus();
    } catch (e) {
    } finally {
      btnSync.style.opacity = '1';
    }
  });

  // Utilities
  function formatNumber(n) {
    return n.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: (n < 1 && n > 0) ? 6 : 4
    });
  }

  function formatRate(n) {
    if (n >= 1000) return n.toFixed(2);
    if (n >= 1) return n.toFixed(4);
    return n.toFixed(6);
  }

  init();
});
