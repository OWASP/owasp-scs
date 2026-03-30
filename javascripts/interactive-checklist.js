/**
 * OWASP SCS Interactive Checklist
 * Vanilla JS – works with MkDocs Material, no framework dependencies.
 * Inspired by personal-security-checklist and digibastion patterns.
 */
(function () {
  'use strict';

  const STORAGE_PROGRESS = 'SCS_CHECKLIST_PROGRESS';
  const STORAGE_IGNORED = 'SCS_CHECKLIST_IGNORED';
  const YAML_URL = '/assets/data/scs-checklist.yaml';

  function loadState(key, defaultValue) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : (defaultValue || {});
    } catch {
      return defaultValue || {};
    }
  }

  function saveState(key, data) {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
      console.warn('SCS Checklist: Could not save to localStorage', e);
    }
  }

  function parseYaml(text) {
    if (typeof jsyaml !== 'undefined') {
      return jsyaml.load(text);
    }
    console.warn('SCS Checklist: js-yaml not loaded, using fallback');
    try {
      return JSON.parse(text.replace(/\n/g, '\\n'));
    } catch {
      return null;
    }
  }

  function init() {
    const container = document.getElementById('scs-interactive-checklist');
    if (!container) return;

    const loadingEl = container.querySelector('.scs-checklist-loading');
    if (!loadingEl) return;

    let checklistData = null;
    let completed = loadState(STORAGE_PROGRESS, {});
    let ignored = loadState(STORAGE_IGNORED, {});

    function persist() {
      saveState(STORAGE_PROGRESS, completed);
      saveState(STORAGE_IGNORED, ignored);
    }

    function getProgress(category) {
      const items = category?.items || [];
      let done = 0;
      let skipped = 0;
      let total = items.length;
      items.forEach((it) => {
        if (ignored[it.id]) skipped++;
        else if (completed[it.id]) done++;
      });
      const active = total - skipped;
      const pct = active > 0 ? Math.round((done / active) * 100) : 0;
      return { done, total, skipped, active, pct };
    }

    function getOverallProgress() {
      if (!checklistData?.categories) return { done: 0, total: 0, active: 0, pct: 0 };
      let done = 0;
      let active = 0;
      checklistData.categories.forEach((cat) => {
        cat.items.forEach((it) => {
          if (ignored[it.id]) return;
          active++;
          if (completed[it.id]) done++;
        });
      });
      const pct = active > 0 ? Math.round((done / active) * 100) : 0;
      return { done, total: active, active, pct };
    }

    function render() {
      if (!checklistData) return;

      const filterShow = container.dataset.filterShow || 'all';
      const filterSeverity = container.dataset.filterSeverity || 'all';
      const currentCategory = container.dataset.currentCategory || '';

      const categories = checklistData.categories || [];
      const cat = currentCategory ? categories.find((c) => c.id === currentCategory) : null;
      const items = cat ? cat.items : categories.flatMap((c) => c.items);

      let filtered = items.filter((it) => {
        if (filterShow === 'remaining' && (completed[it.id] || ignored[it.id])) return false;
        if (filterShow === 'completed' && !completed[it.id]) return false;
        if (filterShow === 'skipped' && !ignored[it.id]) return false;
        if (filterSeverity !== 'all') {
          const sev = getSeverity(it);
          if (sev !== filterSeverity) return false;
        }
        return true;
      });

      function getSeverity(it) {
        if (it.severity) return it.severity;
        const p = (it.priority || '').toLowerCase();
        const l = (it.level || '').toUpperCase();
        if (p === 'essential' && l === 'L1') return 'Critical';
        if (p === 'essential' && l === 'L2') return 'High';
        if (p === 'essential') return 'Critical';
        if (p === 'optional' && l === 'L1') return 'Medium';
        if (p === 'optional' && l === 'L2') return 'Low';
        if (p === 'optional') return 'Medium';
        if (p === 'advanced') return 'Best Practice';
        return null;
      }

      function parseQuestionItems(detailsStr) {
        if (!detailsStr || typeof detailsStr !== 'string') return [];
        const s = detailsStr.replace(/^['"]|['"]$/g, '').trim();
        const lines = s.split(/\n/);
        const items = [];
        let current = null;
        for (const line of lines) {
          const m = line.match(/^\s*[-–—]\s+(.+)/);
          if (m) {
            if (current) items.push(current);
            current = m[1].trim();
          } else if (current && line.trim()) {
            current += ' ' + line.trim();
          }
        }
        if (current) items.push(current);
        return items;
      }
      const overall = getOverallProgress();
      const controlBase = '/SCSVS/controls/';

      let html = '';

      const catColors = { 'SCSVS-ARCH': 'arch', 'SCSVS-CODE': 'code', 'SCSVS-GOV': 'gov', 'SCSVS-AUTH': 'auth', 'SCSVS-COMM': 'comm', 'SCSVS-CRYPTO': 'crypto', 'SCSVS-ORACLE': 'oracle', 'SCSVS-BLOCK': 'block', 'SCSVS-BRIDGE': 'bridge', 'SCSVS-DEFI': 'defi', 'SCSVS-COMP': 'comp' };
      html += '<div class="scs-category-nav">';
      html += '<button type="button" class="scs-cat-btn scs-cat-all' + (!currentCategory ? ' active' : '') + '" data-cat="">View All</button>';
      categories.forEach((c) => {
        const prog = getProgress(c);
        const colorClass = 'scs-cat-' + (catColors[c.id] || 'default');
        html += '<button type="button" class="scs-cat-btn ' + colorClass + (currentCategory === c.id ? ' active' : '') + '" data-cat="' + (c.id || '') + '">';
        html += '<span class="scs-cat-title">' + escapeHtml(c.title || c.id) + '</span>';
        html += '<span class="scs-cat-progress-bar"><span class="scs-cat-progress-fill" style="width:' + prog.pct + '%"></span></span>';
        html += '<span class="scs-cat-count">' + prog.done + '/' + (prog.active || prog.total) + '</span>';
        html += '</button>';
      });
      html += '</div>';

      const currentCatObj = currentCategory ? categories.find((c) => c.id === currentCategory) : null;
      const viewTitle = currentCatObj ? (currentCatObj.title || currentCatObj.id) : 'All Categories';
      const viewColorClass = currentCategory ? ('scs-view-title--' + (catColors[currentCategory] || 'default')) : 'scs-view-title--all';
      html += '<h3 class="scs-view-title ' + viewColorClass + '">' + escapeHtml(viewTitle) + '</h3>';

      html += '<div class="scs-filters">';
      html += '<div class="scs-filter-group"><label>Show:</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-show" value="all"' + (filterShow === 'all' ? ' checked' : '') + '> All</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-show" value="remaining"' + (filterShow === 'remaining' ? ' checked' : '') + '> Remaining</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-show" value="completed"' + (filterShow === 'completed' ? ' checked' : '') + '> Completed</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-show" value="skipped"' + (filterShow === 'skipped' ? ' checked' : '') + '> Skipped (Not Applicable)</label>';
      html += '</div>';
      html += '<div class="scs-filter-group"><label>Priority:</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-severity" value="all"' + (filterSeverity === 'all' ? ' checked' : '') + '> All</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-severity" value="Critical"' + (filterSeverity === 'Critical' ? ' checked' : '') + '> Critical</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-severity" value="High"' + (filterSeverity === 'High' ? ' checked' : '') + '> High</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-severity" value="Medium"' + (filterSeverity === 'Medium' ? ' checked' : '') + '> Medium</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-severity" value="Low"' + (filterSeverity === 'Low' ? ' checked' : '') + '> Low</label>';
      html += '<label class="scs-radio"><input type="radio" name="filter-severity" value="Best Practice"' + (filterSeverity === 'Best Practice' ? ' checked' : '') + '> Best Practice</label>';
      html += '</div>';
      html += '<button type="button" class="scs-btn scs-btn-sm" data-action="reset-filters">Reset filters</button>';
      html += '</div>';

      html += '<div class="scs-checklist-items">';
      filtered.forEach((it) => {
        const isDone = completed[it.id];
        const isSkip = ignored[it.id];
        const questionItems = parseQuestionItems(it.details);
        const severity = getSeverity(it);
        const cardClass = 'scs-item-card group' + (isDone ? ' scs-item-done' : '') + (isSkip ? ' scs-item-skipped' : '');
        html += '<div class="' + cardClass + '" data-id="' + it.id + '">';
        html += '<div class="scs-item-main" data-toggle-id="' + it.id + '">';
        html += '<div class="scs-item-checkbox-wrap">';
        html += '<div class="scs-item-checkbox' + (isDone ? ' scs-checkbox-done' : '') + (isSkip ? ' scs-checkbox-skipped' : '') + '">';
        if (isDone) {
          html += '<svg class="scs-check-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>';
        } else if (!isSkip) {
          html += '<svg class="scs-circle-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/></svg>';
        } else {
          html += '<span class="scs-skip-dot">−</span>';
        }
        html += '</div></div>';
        html += '<div class="scs-item-content">';
        html += '<div class="scs-item-header">';
        html += '<h4 class="scs-item-title">' + escapeHtml(it.point || '') + '</h4>';
        html += '<div class="scs-item-tags">';
        if (it.rid) html += '<span class="scs-tag-rid">' + escapeHtml(it.rid) + '</span>';
        if (severity) html += '<span class="scs-badge scs-severity-' + severity.toLowerCase().replace(/ /g, '-') + '">' + escapeHtml(severity) + '</span>';
        html += '</div></div>';
        if (questionItems.length) {
          html += '<ul class="scs-checklist-questions">';
          questionItems.forEach((q) => { html += '<li>' + escapeHtml(q) + '</li>'; });
          html += '</ul>';
        }
        html += '<div class="scs-item-footer">';
        if (it.control) html += '<a href="' + controlBase + it.control + '/" class="scs-item-link">' + escapeHtml(it.control) + '</a>';
        html += '<label class="scs-skip-label"><input type="checkbox" class="scs-checkbox-skip" data-id="' + it.id + '"' + (isSkip ? ' checked' : '') + '> Skip</label>';
        html += '</div></div></div>';
        html += '</div>';
      });
      html += '</div>';

      container.innerHTML = html;
      container.dataset.currentCategory = currentCategory;
      container.dataset.filterSeverity = filterSeverity;

      /* Sync hero progress circle */
      const heroFill = document.getElementById('scs-hero-progress-fill');
      const heroPct = document.getElementById('scs-hero-progress-pct');
      if (heroFill) heroFill.setAttribute('stroke-dasharray', overall.pct + ', 100');
      if (heroPct) heroPct.textContent = overall.pct + '%';

      /* Sync hero linear bar and item counts */
      const heroLinearFill = document.getElementById('scs-hero-linear-fill');
      const heroStats = document.getElementById('scs-hero-stats');
      if (heroLinearFill) heroLinearFill.style.width = overall.pct + '%';
      if (heroStats) heroStats.textContent = overall.done + ' of ' + overall.total + ' checklist items verified';
      container.dataset.filterShow = filterShow;

      container.querySelectorAll('.scs-cat-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          container.dataset.currentCategory = btn.dataset.cat || '';
          render();
        });
      });

      container.querySelectorAll('input[name="filter-show"]').forEach((radio) => {
        radio.addEventListener('change', () => {
          container.dataset.filterShow = radio.value;
          render();
        });
      });

      container.querySelectorAll('input[name="filter-severity"]').forEach((radio) => {
        radio.addEventListener('change', () => {
          container.dataset.filterSeverity = radio.value;
          render();
        });
      });

      container.querySelectorAll('.scs-skip-label').forEach((lbl) => {
        lbl.addEventListener('click', (e) => e.stopPropagation());
      });

      container.querySelectorAll('.scs-item-main').forEach((el) => {
        el.addEventListener('click', (e) => {
          if (e.target.closest('.scs-skip-label') || e.target.closest('a')) return;
          const id = el.dataset.toggleId;
          if (!id || ignored[id]) return;
          completed[id] = !completed[id];
          persist();
          render();
        });
      });

      container.querySelectorAll('.scs-checkbox-skip').forEach((cb) => {
        cb.addEventListener('change', () => {
          const id = cb.dataset.id;
          ignored[id] = !!cb.checked;
          if (ignored[id]) completed[id] = false;
          persist();
          render();
        });
      });

      container.querySelector('[data-action="reset-filters"]')?.addEventListener('click', () => {
        container.dataset.filterShow = 'all';
        container.dataset.filterSeverity = 'all';
        render();
      });

      function escapeCsv(val) {
        const s = String(val == null ? '' : val);
        if (s.indexOf(',') >= 0 || s.indexOf('"') >= 0 || s.indexOf('\n') >= 0) {
          return '"' + s.replace(/"/g, '""') + '"';
        }
        return s;
      }

      if (!container.dataset.exportListenersAttached) {
        container.dataset.exportListenersAttached = '1';
        document.getElementById('scs-hero-export-json')?.addEventListener('click', () => {
          const payload = { completed, ignored, metadata: checklistData.metadata, exportedAt: new Date().toISOString() };
          const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'scs-checklist-progress.json';
          a.click();
          URL.revokeObjectURL(a.href);
        });
        document.getElementById('scs-hero-export-csv')?.addEventListener('click', () => {
          const rows = [['VR ID', 'Control Item', 'Category', 'Status', 'Level', 'Priority']];
          checklistData.categories.forEach((cat) => {
            cat.items.forEach((it) => {
              let status = 'Unchecked';
              if (ignored[it.id]) status = 'Skipped';
              else if (completed[it.id]) status = 'Checked';
              rows.push([it.rid || it.id || '', it.point || '', cat.title || cat.id || '', status, it.level || '', it.priority || '']);
            });
          });
          const csv = rows.map((r) => r.map(escapeCsv).join(',')).join('\n');
          const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
          const a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'scs-checklist-progress.csv';
          a.click();
          URL.revokeObjectURL(a.href);
        });
      }
    }

    function escapeHtml(s) {
      const d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    }

    fetch(YAML_URL)
      .then((r) => r.text())
      .then((text) => {
        checklistData = parseYaml(text);
        if (!checklistData?.categories) {
          throw new Error('Invalid checklist data');
        }
        loadingEl.remove();
        container.dataset.filterShow = 'all';
        container.dataset.currentCategory = '';
        render();
      })
      .catch((err) => {
        loadingEl.innerHTML = '<p class="scs-checklist-error">Failed to load checklist. <a href="' + YAML_URL + '">Check data</a>.</p>';
        console.error('SCS Checklist load error:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(init);
  }
})();
