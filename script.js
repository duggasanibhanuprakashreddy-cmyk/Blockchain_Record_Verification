/**
 * BlockVerify - Core Blockchain Engine and UI Controller
 * Cryptographically identical to blockchain.py and app.py
 */

// Initial Seed Data (from data/blockchain.json)
const INITIAL_BLOCKCHAIN = [
  {
    "index": 0,
    "timestamp": "2026-10-07T16:38:27.342248",
    "record_id": "GENESIS",
    "record_hash": "0",
    "previous_hash": "0",
    "current_hash": "c2056aff109804eab157c4934b7453a6e40b686136e0f24a25119ec0e52ceceb"
  },
  {
    "index": 1,
    "timestamp": "2026-10-07T16:38:27.342266",
    "record_id": "R25EH043",
    "student_name": "Bhanuprakash Reddy",
    "course": "B.Tech AI & DS",
    "cgpa": "8.3",
    "record_hash": "2a74d1bf493e01cead65bfeb7b3f8a30fc172abe15b7a4c5b1d536907a25d21a",
    "previous_hash": "c2056aff109804eab157c4934b7453a6e40b686136e0f24a25119ec0e52ceceb",
    "current_hash": "a13f23727786820934a137260cefddcb51303fd169136e57dcb523c6c51ad509"
  },
  {
    "index": 2,
    "timestamp": "2026-10-07T16:38:27.342277",
    "record_id": "R25EH158",
    "student_name": "Jagadeesh K",
    "course": "B.Tech CSE",
    "cgpa": "8.7",
    "record_hash": "7ba2e0eaebc5f472135a60a8c86078c7374177560d11e61acaed6cee75137da1",
    "previous_hash": "a13f23727786820934a137260cefddcb51303fd169136e57dcb523c6c51ad509",
    "current_hash": "c39b3f7af118ef89af2efffe49396f0509b3a6de8415374fc6fb5774dae5893c"
  },
  {
    "index": 3,
    "timestamp": "2026-10-07T16:38:27.342284",
    "record_id": "R25EA073",
    "student_name": "Rahul Verma",
    "course": "B.Tech Data Science",
    "cgpa": "9.1",
    "record_hash": "771df9b231af9f4163dcf5e182d509277870ac94238990f0188f0e7be8988af3",
    "previous_hash": "c39b3f7af118ef89af2efffe49396f0509b3a6de8415374fc6fb5774dae5893c",
    "current_hash": "d90359392939d43a9dc1f26fac7b8ac7b3fe34595295dbd6f7510beb0bd564b6"
  },
  {
    "index": 4,
    "timestamp": "2026-10-07T16:42:29.340766",
    "record_id": "R25EH044",
    "student_name": "Siddharth Rao",
    "course": "B.Tech Cybersecurity",
    "cgpa": "8.5",
    "record_hash": "5655bd5666b271d1acef5360bbbac6b05345b489400a8e7ba88e9c8c4d9fb989",
    "previous_hash": "d90359392939d43a9dc1f26fac7b8ac7b3fe34595295dbd6f7510beb0bd564b6",
    "current_hash": "1b4a8be1fba5652a5086295add7b1c227b4e379d105d691ac26c44e0c5cc3aae"
  }
];

class BlockchainApp {
  constructor() {
    this.storageKey = 'blockverify_ledger_v2';
    this.themeKey = 'blockverify_theme_v2';
    this.chain = [];
    this.initTheme();
    this.initLedger();
    this.bindEvents();
    this.render();
  }

  // --- HASHING UTILITY (SHA-256) ---
  async sha256(text) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // Calculate block hash exactly matching Block.calculate_hash() in blockchain.py
  async calculateBlockHash(block) {
    const blockData = String(block.index) + block.timestamp + block.record_id + block.record_hash + block.previous_hash;
    return await this.sha256(blockData);
  }

  // --- LEDGER STORAGE & SYNC ---
  initLedger() {
    const saved = localStorage.getItem(this.storageKey);
    if (saved) {
      try {
        this.chain = JSON.parse(saved);
        if (Array.isArray(this.chain) && this.chain.length > 0) return;
      } catch (e) {
        console.warn('Failed to parse localStorage, resetting to seed data', e);
      }
    }
    this.chain = JSON.parse(JSON.stringify(INITIAL_BLOCKCHAIN));
    this.saveLedger();
  }

  saveLedger() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.chain));
  }

  resetToInitial() {
    this.chain = JSON.parse(JSON.stringify(INITIAL_BLOCKCHAIN));
    this.saveLedger();
    this.render();
  }

  // --- INTEGRITY CHECK ---
  async isChainValid() {
    for (let i = 1; i < this.chain.length; i++) {
      const currentBlock = this.chain[i];
      const prevBlock = this.chain[i - 1];

      const expectedHash = await this.calculateBlockHash(currentBlock);
      if (currentBlock.current_hash !== expectedHash) {
        return false;
      }

      if (currentBlock.previous_hash !== prevBlock.current_hash) {
        return false;
      }
    }
    return true;
  }

  // --- THEME ---
  initTheme() {
    const saved = localStorage.getItem(this.themeKey) || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    this.updateThemeButton(saved);
  }

  toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem(this.themeKey, next);
    this.updateThemeButton(next);
  }

  updateThemeButton(theme) {
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) {
      btn.innerHTML = theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
    }
  }

  // --- TAB NAVIGATION ---
  switchPage(pageId) {
    document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    const targetPage = document.getElementById(`page-${pageId}`);
    const targetNav = document.getElementById(`nav-${pageId}`);

    if (targetPage) targetPage.classList.add('active');
    if (targetNav) targetNav.classList.add('active');

    // Close mobile drawer if open
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) sidebar.classList.remove('mobile-open');

    this.render();
  }

  // --- EVENT BINDING ---
  bindEvents() {
    // Navigation items
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', () => {
        const page = item.getAttribute('data-page');
        if (page) this.switchPage(page);
      });
    });

    // Theme toggle
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => this.toggleTheme());
    }

    // Mobile nav toggle
    const mobileBtn = document.getElementById('mobile-nav-toggle');
    if (mobileBtn) {
      mobileBtn.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('mobile-open');
      });
    }

    // Add Record Form
    const addForm = document.getElementById('add-record-form');
    if (addForm) {
      addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleAddRecord();
      });
    }

    // Verify Record Form
    const verifyForm = document.getElementById('verify-record-form');
    if (verifyForm) {
      verifyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await this.handleVerifyRecord();
      });
    }

    // Quick fill chips for Add Record
    document.querySelectorAll('[data-fill-add]').forEach(btn => {
      btn.addEventListener('click', () => {
        const type = btn.getAttribute('data-fill-add');
        if (type === 'sample1') {
          document.getElementById('add-record-id').value = 'R25EH045';
          document.getElementById('add-student-name').value = 'Ananya Sharma';
          document.getElementById('add-course').value = 'B.Tech AI & DS';
          document.getElementById('add-cgpa').value = '9.4';
        } else if (type === 'sample2') {
          document.getElementById('add-record-id').value = 'R25CS102';
          document.getElementById('add-student-name').value = 'Kiran Kumar';
          document.getElementById('add-course').value = 'B.Tech CSE';
          document.getElementById('add-cgpa').value = '8.9';
        }
      });
    });

    // Quick fill chips for Verify Record
    document.querySelectorAll('[data-fill-verify]').forEach(btn => {
      btn.addEventListener('click', () => {
        const type = btn.getAttribute('data-fill-verify');
        if (type === 'genuine') {
          // Pre-populate with matching Bhanuprakash record
          document.getElementById('verify-record-id').value = 'R25EH043';
          document.getElementById('verify-student-name').value = 'Bhanuprakash Reddy';
          document.getElementById('verify-course').value = 'B.Tech AI & DS';
          document.getElementById('verify-cgpa').value = '8.3';
          this.handleVerifyRecord();
        } else if (type === 'tampered') {
          // Alter CGPA from 8.3 to 9.9
          document.getElementById('verify-record-id').value = 'R25EH043';
          document.getElementById('verify-student-name').value = 'Bhanuprakash Reddy';
          document.getElementById('verify-course').value = 'B.Tech AI & DS';
          document.getElementById('verify-cgpa').value = '9.9';
          this.handleVerifyRecord();
        }
      });
    });

    // Integrity Tamper Simulation Lab
    const tamperBtn = document.getElementById('simulate-tamper-btn');
    if (tamperBtn) {
      tamperBtn.addEventListener('click', () => this.simulateTampering());
    }

    const restoreBtn = document.getElementById('restore-chain-btn');
    if (restoreBtn) {
      restoreBtn.addEventListener('click', () => this.resetToInitial());
    }
  }

  // --- ACTIONS ---

  async handleAddRecord() {
    const recordId = document.getElementById('add-record-id').value.trim();
    const studentName = document.getElementById('add-student-name').value.trim();
    const course = document.getElementById('add-course').value.trim();
    const cgpa = document.getElementById('add-cgpa').value.trim();
    const resultBox = document.getElementById('add-result-box');

    if (!recordId || !studentName || !course || !cgpa) {
      alert('⚠️ Please fill in all fields.');
      return;
    }

    // Duplicate check
    const exists = this.chain.some(b => b.record_id.toLowerCase() === recordId.toLowerCase());
    if (exists) {
      alert(`⚠️ Record ID "${recordId}" already exists in the blockchain.`);
      return;
    }

    const recordData = `${studentName}|${course}|${cgpa}`;
    const recordHash = await this.sha256(recordData);
    const prevBlock = this.chain[this.chain.length - 1];

    const newBlock = {
      index: this.chain.length,
      timestamp: new Date().toISOString(),
      record_id: recordId,
      student_name: studentName,
      course: course,
      cgpa: cgpa,
      record_hash: recordHash,
      previous_hash: prevBlock.current_hash,
      current_hash: ''
    };

    newBlock.current_hash = await this.calculateBlockHash(newBlock);

    this.chain.push(newBlock);
    this.saveLedger();

    // Display result
    if (resultBox) {
      resultBox.style.display = 'block';
      resultBox.innerHTML = `
        <div class="status-banner" style="margin-top: 16px;">
          <span>✅</span> Record securely added to blockchain!
        </div>
        <div style="margin-top: 14px;">
          <h4 style="font-size: 15px; margin-bottom: 6px;">🔐 Record Fingerprint (SHA-256)</h4>
          <div class="code-box">
            <code>${recordHash}</code>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('${recordHash}')">Copy</button>
          </div>
        </div>
        <div class="metrics-grid" style="margin-top: 16px;">
          <div class="metric-card">
            <div class="metric-label">Block Number</div>
            <div class="metric-value">${newBlock.index}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Hash Algorithm</div>
            <div class="metric-value" style="font-size: 22px;">SHA-256</div>
          </div>
        </div>
      `;
    }

    // Reset form inputs
    document.getElementById('add-record-id').value = '';
    document.getElementById('add-student-name').value = '';
    document.getElementById('add-course').value = '';
    document.getElementById('add-cgpa').value = '';

    this.render();
  }

  async handleVerifyRecord() {
    const recordId = document.getElementById('verify-record-id').value.trim();
    const studentName = document.getElementById('verify-student-name').value.trim();
    const course = document.getElementById('verify-course').value.trim();
    const cgpa = document.getElementById('verify-cgpa').value.trim();
    const resultBox = document.getElementById('verify-result-box');

    if (!recordId || !studentName || !course || !cgpa) {
      alert('⚠️ Please fill in all fields.');
      return;
    }

    const recordData = `${studentName}|${course}|${cgpa}`;
    const generatedHash = await this.sha256(recordData);

    const foundBlock = this.chain.find(b => b.record_id.toLowerCase() === recordId.toLowerCase());

    if (!resultBox) return;
    resultBox.style.display = 'block';

    if (!foundBlock) {
      resultBox.innerHTML = `
        <div class="status-banner" style="background-color: var(--status-amber-bg); border-color: var(--status-amber-border); color: var(--status-amber);">
          <span>⚠️</span> Record not found in blockchain.
        </div>
      `;
      return;
    }

    const storedHash = foundBlock.record_hash;
    const isMatch = storedHash === generatedHash;

    resultBox.innerHTML = `
      <h3 style="font-size: 18px; margin-bottom: 12px; font-weight: 700;">🔐 Cryptographic Hash Comparison</h3>
      <div class="comparison-grid">
        <div class="hash-card">
          <h4>🔒 Stored Hash (On-Chain)</h4>
          <code>${storedHash}</code>
        </div>
        <div class="hash-card">
          <h4>🧪 Generated Hash (Input Data)</h4>
          <code>${generatedHash}</code>
        </div>
      </div>
      <div class="divider"></div>
      ${isMatch ? `
        <div class="status-banner" style="margin-top: 14px;">
          <span>🟢</span>
          <div>
            <strong>RECORD VERIFIED</strong><br>
            <span style="font-size: 13.5px; opacity: 0.9;">HASH MATCH — The record appears authentic and completely unchanged.</span>
          </div>
        </div>
      ` : `
        <div class="status-banner danger" style="margin-top: 14px;">
          <span>🔴</span>
          <div>
            <strong>RECORD TAMPERED</strong><br>
            <span style="font-size: 13.5px; opacity: 0.9;">HASH MISMATCH — The record data has been altered after notarization!</span>
          </div>
        </div>
      `}
    `;
  }

  simulateTampering() {
    if (this.chain.length > 1) {
      // Modify Block 1's record hash
      this.chain[1].record_hash = '9999999999999999999999999999999999999999999999999999999999999999';
      this.render();
      alert('⚠️ Simulated unauthorized alteration on Block 1! Check the Integrity tab to see the system detection.');
    }
  }

  // --- RENDER ALL VIEWS ---
  async render() {
    const totalBlocks = this.chain.length;
    const totalRecords = Math.max(0, totalBlocks - 1);
    const isValid = await this.isChainValid();

    // 1. Sidebar Updates
    const sidebarStored = document.getElementById('sidebar-stored-records');
    if (sidebarStored) sidebarStored.textContent = totalRecords;

    const sidebarStatusPill = document.getElementById('sidebar-status-pill');
    if (sidebarStatusPill) {
      if (isValid) {
        sidebarStatusPill.className = 'status-pill';
        sidebarStatusPill.innerHTML = '<span class="pulse-circle"></span> 🟢 SYSTEM SECURE';
      } else {
        sidebarStatusPill.className = 'status-pill danger';
        sidebarStatusPill.innerHTML = '<span class="pulse-circle"></span> 🔴 SYSTEM COMPROMISED';
      }
    }

    // 2. Dashboard Status Banner
    const dashBanner = document.getElementById('dash-status-banner');
    if (dashBanner) {
      if (isValid) {
        dashBanner.className = 'status-banner';
        dashBanner.innerHTML = '<span>🟢</span> SYSTEM SECURE — Blockchain integrity has been verified successfully.';
      } else {
        dashBanner.className = 'status-banner danger';
        dashBanner.innerHTML = '<span>🔴</span> SECURITY ALERT — Blockchain integrity may be compromised.';
      }
    }

    // 3. Dashboard Top Metrics
    const metricBlocks = document.getElementById('metric-total-blocks');
    const metricRecords = document.getElementById('metric-total-records');
    const metricStatus = document.getElementById('metric-status');

    if (metricBlocks) metricBlocks.textContent = totalBlocks;
    if (metricRecords) metricRecords.textContent = totalRecords;
    if (metricStatus) {
      metricStatus.textContent = isValid ? 'VALID' : 'INVALID';
      metricStatus.style.color = isValid ? 'var(--status-green)' : 'var(--status-red)';
    }

    // 4. Dashboard Blockchain Flow
    const flowContainer = document.getElementById('dash-flow-container');
    if (flowContainer) {
      flowContainer.innerHTML = '';
      const displayBlocks = this.chain.slice(0, 6);
      displayBlocks.forEach(b => {
        const div = document.createElement('div');
        div.className = 'flow-block';
        div.onclick = () => this.switchPage('blockchain');
        div.innerHTML = `
          <div class="flow-block-index">BLOCK ${b.index}</div>
          <div class="flow-block-id">${b.record_id}</div>
        `;
        flowContainer.appendChild(div);
      });
      if (this.chain.length > 6) {
        const moreDiv = document.createElement('div');
        moreDiv.className = 'flow-block';
        moreDiv.style.display = 'flex';
        moreDiv.style.alignItems = 'center';
        moreDiv.style.justifyContent = 'center';
        moreDiv.onclick = () => this.switchPage('blockchain');
        moreDiv.innerHTML = `<span style="font-size: 13px; color: var(--text-muted);">+ ${this.chain.length - 6} more blocks</span>`;
        flowContainer.appendChild(moreDiv);
      }
    }

    // 5. Records Page List
    const recordsList = document.getElementById('records-list-container');
    if (recordsList) {
      const nonGenesis = this.chain.filter(b => b.record_id !== 'GENESIS');
      if (nonGenesis.length === 0) {
        recordsList.innerHTML = `<p style="color: var(--text-muted);">No records have been added yet.</p>`;
      } else {
        recordsList.innerHTML = '';
        nonGenesis.forEach(b => {
          const card = document.createElement('div');
          card.className = 'expander-card';
          card.innerHTML = `
            <div class="expander-header" onclick="this.parentElement.classList.toggle('open')">
              <span class="expander-title">📄 ${b.record_id} &nbsp;•&nbsp; Block ${b.index}</span>
              <span class="expander-arrow">▼</span>
            </div>
            <div class="expander-body">
              <div class="detail-grid-2">
                <div class="detail-item">
                  <strong>Block:</strong> ${b.index}
                  <strong style="margin-top: 8px;">Timestamp:</strong> ${b.timestamp}
                </div>
                <div class="detail-item">
                  <strong>Record Hash:</strong>
                  <div class="code-box">
                    <code>${b.record_hash}</code>
                    <button class="copy-btn" onclick="navigator.clipboard.writeText('${b.record_hash}')">Copy</button>
                  </div>
                </div>
              </div>
            </div>
          `;
          recordsList.appendChild(card);
        });
      }
    }

    // 6. Blockchain Explorer Page List
    const explorerList = document.getElementById('explorer-list-container');
    if (explorerList) {
      explorerList.innerHTML = '';
      this.chain.forEach(b => {
        const card = document.createElement('div');
        card.className = 'expander-card';
        card.innerHTML = `
          <div class="expander-header" onclick="this.parentElement.classList.toggle('open')">
            <span class="expander-title">🔗 Block ${b.index} | Record: ${b.record_id}</span>
            <span class="expander-arrow">▼</span>
          </div>
          <div class="expander-body">
            <div class="detail-grid-2">
              <div class="detail-item">
                <strong>Block Index:</strong> ${b.index}
                <strong style="margin-top: 8px;">Record ID:</strong> ${b.record_id}
                <strong style="margin-top: 8px;">Timestamp:</strong> ${b.timestamp}
                <strong style="margin-top: 8px;">Record Hash:</strong>
                <div class="code-box">
                  <code>${b.record_hash}</code>
                </div>
              </div>
              <div class="detail-item">
                <strong>Previous Block Hash:</strong>
                <div class="code-box">
                  <code>${b.previous_hash}</code>
                </div>
                <strong style="margin-top: 8px;">Current Block Hash:</strong>
                <div class="code-box">
                  <code>${b.current_hash}</code>
                </div>
              </div>
            </div>
          </div>
        `;
        explorerList.appendChild(card);
      });
    }

    // 7. Integrity Page
    const integrityBanner = document.getElementById('integrity-status-banner');
    const integrityMetricStatus = document.getElementById('integrity-metric-status');
    const integrityMetricChecked = document.getElementById('integrity-metric-checked');

    if (integrityBanner) {
      if (isValid) {
        integrityBanner.className = 'status-banner';
        integrityBanner.innerHTML = '<span>🟢</span> <div><strong>BLOCKCHAIN IS VALID</strong><br><span style="font-size: 13.5px; opacity: 0.9;">All blocks passed the cryptographic integrity check.</span></div>';
      } else {
        integrityBanner.className = 'status-banner danger';
        integrityBanner.innerHTML = '<span>🔴</span> <div><strong>BLOCKCHAIN INTEGRITY COMPROMISED</strong><br><span style="font-size: 13.5px; opacity: 0.9;">One or more blocks fail the cryptographic hash continuity check!</span></div>';
      }
    }

    if (integrityMetricStatus) {
      integrityMetricStatus.textContent = isValid ? 'SECURE' : 'COMPROMISED';
      integrityMetricStatus.style.color = isValid ? 'var(--status-green)' : 'var(--status-red)';
    }

    if (integrityMetricChecked) {
      integrityMetricChecked.textContent = totalBlocks;
    }
  }
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.blockVerifyApp = new BlockchainApp();
});
