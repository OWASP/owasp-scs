---
hide:
  - toc
  - nav
search:
  exclude: true
---

# Interactive SCS Checklist

<div class="scs-checklist-hero scs-glass-card" id="scs-checklist-hero">
  <div class="scs-hero-gradient"></div>
  <div class="scs-hero-inner">
    <div class="scs-hero-header">
      <div class="scs-hero-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      </div>
      <div class="scs-hero-text">
        <h1>OWASP SCS Checklist</h1>
        <p class="scs-checklist-subtitle">Interactive security checklist for smart contract auditing</p>
      </div>
      <div class="scs-hero-progress-ring" role="img" aria-label="Progress">
        <svg viewBox="0 0 36 36">
          <defs>
            <linearGradient id="scs-ring-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="hsl(243, 75%, 59%)"/>
              <stop offset="100%" stop-color="hsl(280, 70%, 55%)"/>
            </linearGradient>
          </defs>
          <path class="scs-ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
          <path class="scs-ring-fill" id="scs-hero-progress-fill" stroke="url(#scs-ring-gradient)" stroke-dasharray="0, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
        </svg>
        <span class="scs-ring-text" id="scs-hero-progress-pct">0%</span>
      </div>
      <div class="scs-hero-actions">
        <button type="button" class="scs-btn scs-btn-export" id="scs-hero-export-json">Export JSON</button>
        <button type="button" class="scs-btn scs-btn-export" id="scs-hero-export-csv">Export CSV</button>
        <a href="/SCSVS/" class="scs-hero-link">View SCSVS</a>
      </div>
    </div>
    <div class="scs-hero-progress-wrap">
      <div class="scs-hero-progress-bar"><span class="scs-hero-progress-fill" id="scs-hero-linear-fill" style="width:0%"></span></div>
      <div class="scs-hero-stats"><span id="scs-hero-stats">0 of 231 checklist items verified</span></div>
    </div>
  </div>
</div>

<div id="scs-interactive-checklist">
  <div class="scs-checklist-loading" aria-live="polite">
    <span class="scs-spinner" aria-hidden="true"></span>
    <p>Loading checklist...</p>
  </div>
</div>

<noscript>
  <div class="scs-checklist-noscript admonition warning">
    <p class="admonition-title">JavaScript required</p>
    <p>This interactive checklist requires JavaScript. Please enable it or use the <a href="../">static checklists</a> instead.</p>
  </div>
</noscript>

---

## Security Levels & Priorities

---

## Related Resources

- [SCSVS Controls](../SCSVS/index.md) – Full verification standard
- [SCSTG Tests](../SCSTG/tests/index.md) – Testing guide
- [SCWE Weaknesses](../SCWE/index.md) – Weakness enumerations
