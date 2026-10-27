/* Horus website behaviour. No scroll-jacking, no timers that hide content, nothing moves while you read.
   Four instruments: the gaze, the engagement ledger, the consultation replay, the receipt. Two forms that send a scope of work. */
(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- the gaze: the focus point follows the pointer within a small radius ---------- */
  (function gaze() {
    var pupil = document.getElementById('pupil'); var ring = document.getElementById('iris');
    if (!pupil || reduced) return;
    var svg = pupil.ownerSVGElement, cx = 50, cy = 50, tx = 50, ty = 50, rx = 50, ry = 50, raf = null;
    function step() {
      cx += (tx - cx) * 0.1; cy += (ty - cy) * 0.1; rx += (tx - rx) * 0.06; ry += (ty - ry) * 0.06;
      pupil.setAttribute('cx', cx.toFixed(2)); pupil.setAttribute('cy', cy.toFixed(2));
      if (ring) { ring.setAttribute('cx', (50 + (rx - 50) * 0.35).toFixed(2)); ring.setAttribute('cy', (50 + (ry - 50) * 0.35).toFixed(2)); }
      if (Math.abs(tx - cx) > 0.03 || Math.abs(ty - cy) > 0.03 || Math.abs(tx - rx) > 0.03) raf = requestAnimationFrame(step); else raf = null;
    }
    function aim(e) {
      var r = svg.getBoundingClientRect(); var dx = (e.clientX - (r.left + r.width / 2)) / Math.max(r.width, 1); var dy = (e.clientY - (r.top + r.height / 2)) / Math.max(r.height, 1);
      var len = Math.hypot(dx, dy) || 1; var k = Math.min(len, 0.9) / len; tx = 50 + dx * k * 9; ty = 50 + dy * k * 7;
      if (!raf) raf = requestAnimationFrame(step);
    }
    window.addEventListener('pointermove', aim, { passive: true });
    window.addEventListener('pointerleave', function () { tx = 50; ty = 50; if (!raf) raf = requestAnimationFrame(step); });
  })();

  /* ---------- the engagement ledger: an illustrative six-week run ---------- */
  var PHASES = [
    { n: '01', name: 'Scope to plan', when: 'Week 1', title: 'Horus reads the scope and returns the plan',
      does: 'Reads the scope of work and every document behind it. Maps the stakeholders, the questions and the option space. Sets the milestones. Sends you the engagement plan, then writes and schedules the meeting requests to your stakeholders.',
      you: 'The engagement plan within one working day. Meeting invitations for your stakeholders, written and scheduled by Horus.',
      records: [['PLN-001', 'Engagement plan · six weeks · four milestones'], ['STK-001…018', 'Eighteen stakeholders mapped, internal and external'], ['MTG-001…012', 'Twelve consultations scheduled'], ['MSG-001', 'Kickoff note sent to the client lead']],
      counts: [['Stakeholders', 18], ['Sources', 22], ['Evidence', 0], ['Options', 0]] },
    { n: '02', name: 'Research', when: 'Weeks 1 to 2', title: 'Horus reads the whole record, not a sample',
      does: 'Statutes, budgets, evaluations, datasets and every comparator jurisdiction, in every language they were published in. A source behind every fact, snapshotted the day it was read. Facts that cannot be sourced are listed as gaps for the consultations to close.',
      you: 'A weekly steering note: what the evidence says so far, what is still open, what changed in the plan.',
      records: [['SRC-061', 'Comparative tax-administration review, 2025 · snapshot stored'], ['SRC-074', 'Decree-Law of 2023, consolidated text'], ['EVD-0142', 'Adoption within two years of a phased mandate, three jurisdictions'], ['GAP-003', 'Open: compliance cost for micro-enterprises']],
      counts: [['Stakeholders', 18], ['Sources', 74], ['Evidence', 187], ['Options', 0]] },
    { n: '03', name: 'Consultation', when: 'Weeks 2 to 4', title: 'Horus conducts every meeting itself',
      does: 'Joins each call, leads the conversation from the plan, follows up on what it hears and reconciles positions across meetings. Ministries, agencies, regulators, industry, experts: internal and external stakeholders alike. Every statement is attributed and recorded before the call ends.',
      you: 'The record of each consultation the same day. The consultation synthesis the morning after the last meeting: who holds which position, where they agree, where they do not.',
      records: [['MTG-003', 'Merchants Association · 41 min · record written'], ['EVD-0210…0231', 'Twenty-two statements, attributed'], ['OQ-007', 'Positions differ on cost against support · to resolve in MTG-008'], ['ACT-012', 'Follow-up: the Association sends its 2024 survey']],
      counts: [['Stakeholders', 18], ['Sources', 88], ['Evidence', 243], ['Options', 0]] },
    { n: '04', name: 'Options and appraisal', when: 'Week 4', title: 'Every option, one method, every number tested',
      does: 'Develops the full option space, not the two there was time for. Appraises each option by the same method from one assumptions register: costs, benefits, who bears them, risk, and a sensitivity on every number.',
      you: 'The options paper and the assumptions register. A steering meeting where Horus presents the interim findings and takes your direction on priorities.',
      records: [['OPT-001…005', 'Five options developed'], ['APL-003', 'Appraisal: net present value, distribution, sensitivity'], ['ASM-019', 'Assumption: micro-enterprise compliance cost, bounded'], ['MTG-013', 'Steering meeting · interim findings presented']],
      counts: [['Stakeholders', 18], ['Sources', 96], ['Evidence', 268], ['Options', 5]] },
    { n: '05', name: 'Recommendation', when: 'Week 5', title: 'Horus decides, and writes down why',
      does: 'Weighs every option against the whole record and writes the recommendation with the reasoning that produced it: why this option, why not the others, what it rests on, what would change it. Then argues against its own draft in a full adversarial review and fixes what fails.',
      you: 'The draft policy document and the decision record behind it.',
      records: [['DEC-001', 'Recommendation: phased mandate over three years, with support line'], ['REV-002', 'Adversarial review: fourteen challenges, three revisions'], ['RSK-005', 'Risk: free tool not ready by year one · mitigation set'], ['DEL-003', 'Draft policy document, version 1']],
      counts: [['Stakeholders', 18], ['Sources', 96], ['Evidence', 268], ['Options', 5]] },
    { n: '06', name: 'Seal and handover', when: 'Week 6', title: 'The document is sealed when every check passes',
      does: 'Runs the seal checks: every claim traced, every option appraised, every stakeholder in scope consulted, the review passed, every number reproducible from the register. Seals the document. Presents it to your leadership and hands over the full engagement record.',
      you: 'The sealed policy document, the presentation and the complete evidence ledger. Every follow-up action tracked to its close.',
      records: [['CHK-001…005', 'Five seal checks passed'], ['DEL-004', 'Policy document · sealed · version 3'], ['MTG-014', 'Presentation to the Minister\'s office'], ['EXP-001', 'Full export: evidence ledger, assumptions register, every version']],
      counts: [['Stakeholders', 18], ['Sources', 96], ['Evidence', 268], ['Options', 5]] }
  ];
  (function ledger() {
    var list = document.getElementById('phases'); var out = document.getElementById('console'); if (!list || !out) return;
    function render(i) {
      var p = PHASES[i];
      list.querySelectorAll('.phase').forEach(function (b, j) { b.setAttribute('aria-selected', String(i === j)); });
      out.innerHTML = '<div class="bar"><span>DCT-2026-001 · ' + p.when.toLowerCase() + ' · ' + p.name.toLowerCase() + '</span><span class="live"><i></i>ledger</span></div>' +
        '<div class="body"><h3>' + p.title + '</h3><div class="does"><div><h4>Horus does</h4>' + p.does + '</div><div><h4>You receive</h4>' + p.you + '</div></div>' +
        '<div class="records">' + p.records.map(function (r, k) { return '<div style="animation-delay:' + (k * 90) + 'ms"><b>' + r[0] + '</b><span>' + r[1] + '</span></div>'; }).join('') + '</div>' +
        '<div class="counts">' + p.counts.map(function (c) { return '<div><b>' + c[1] + '</b>' + c[0] + '</div>'; }).join('') + '</div></div>';
    }
    PHASES.forEach(function (p, i) {
      var b = document.createElement('button'); b.className = 'phase'; b.type = 'button'; b.setAttribute('role', 'tab'); b.id = 'phase-' + p.n;
      b.innerHTML = '<span class="n">' + p.n + '</span><span>' + p.name + '</span><span class="gate">' + p.when + '</span>';
      b.addEventListener('click', function () { render(i); }); list.appendChild(b);
    });
    render(0);
  })();

  /* ---------- the consultation replay: an illustrative exchange, played on request ---------- */
  var SCRIPT = [
    { who: 'Horus', cls: 'horus', text: 'Good morning, Chairwoman, and thank you for the time. I am Horus. The Ministry has asked me to design the electronic invoicing mandate for small merchants, and your members will carry most of its compliance cost, so I want to understand adoption from their side. What is the single biggest obstacle today?' },
    { who: 'Chairwoman', cls: 'human', text: 'Cost, mostly. The software vendors price it for mid-sized firms. A corner shop with two staff will not pay that, and they are not sure the tax office will even read the invoices.' },
    { who: 'Horus', cls: 'horus', text: 'Two obstacles, then: the price, and whether filing changes anything for them. On price, the free zone ran a pilot in 2024 with a free invoicing tool. Did any of your members take part?' },
    { who: 'Chairwoman', cls: 'human', text: 'About forty did. The tool was fine; the problem was that nobody told them what happens when it fails on a Friday night. Support matters more than the price.' },
    { who: 'Horus', cls: 'horus', text: 'That is a different obstacle from the one most of the written submissions raise, and it changes the option design: a free tool without a support line would not solve it. May I record the Association\'s position as support before price in the consultation synthesis?' },
    { who: 'Chairwoman', cls: 'human', text: 'Yes. And we ran a member survey on exactly this in 2024.' },
    { who: 'Horus', cls: 'horus', text: 'I would like it. I will send a written request for the survey today, and I will come back to you with the Authority\'s pilot figures once I have reconciled them with yours. Is there anyone among your members I should hear directly?' },
    { who: 'Chairwoman', cls: 'human', text: 'Two or three. I will send you names this afternoon.' },
    { who: 'Ledger', cls: 'ledger', text: 'MTG-003 record written · EVD-0214 position: support before price, attributed · ACT-012 survey requested · three stakeholders added to the plan · OQ-007 opened: cost against support, to test in MTG-008' }
  ];
  (function consultation() {
    var box = document.getElementById('transcript'); var play = document.getElementById('replay'); var call = document.getElementById('call');
    var tiles = { horus: document.getElementById('tile-horus'), human: document.getElementById('tile-human') }; if (!box || !play) return;
    var timer = null, idx = 0, waves = [];
    function speak(cls, on) { Object.keys(tiles).forEach(function (k) { tiles[k].classList.toggle('speaking', on && k === cls); }); }
    function wave(tile, on) { var w = tile.querySelector('.wave'); if (!w) return; w.querySelectorAll('i').forEach(function (i) { i.style.height = on ? (4 + Math.random() * 12).toFixed(0) + 'px' : '4px'; }); }
    function row(s, still) { var u = document.createElement('div'); u.className = 'u ' + s.cls; if (still) { u.style.animation = 'none'; u.style.opacity = '1'; } u.innerHTML = '<span class="who">' + s.who + '</span><span>' + s.text + '</span>'; return u; }
    function stop() { if (timer) clearTimeout(timer); timer = null; waves.forEach(clearInterval); waves = []; speak(null, false); Object.keys(tiles).forEach(function (k) { wave(tiles[k], false); }); play.disabled = false; play.textContent = 'Replay the exchange'; if (call) call.classList.remove('playing'); }
    function line(i) {
      var s = SCRIPT[i]; box.appendChild(row(s, false)); box.scrollTop = box.scrollHeight;
      if (s.cls !== 'ledger') { speak(s.cls, true); var t = tiles[s.cls]; var w = setInterval(function () { wave(t, true); }, 140); waves.push(w); }
      var dur = reduced ? 400 : Math.min(5600, 1400 + s.text.length * 26);
      timer = setTimeout(function () { waves.forEach(clearInterval); waves = []; Object.keys(tiles).forEach(function (k) { wave(tiles[k], false); }); speak(null, false); idx++; if (idx < SCRIPT.length) line(idx); else stop(); }, dur);
    }
    play.addEventListener('click', function () { stop(); box.innerHTML = ''; idx = 0; play.disabled = true; play.textContent = 'Playing'; if (call) call.classList.add('playing'); line(0); });
    // at rest the panel already shows the whole exchange, so nothing is hidden behind the button
    SCRIPT.forEach(function (s) { box.appendChild(row(s, true)); });
  })();

  /* ---------- the receipt: what each sentence of a sealed document rests on ---------- */
  var SOURCES = {
    c1: { id: 'SRC-061 · snapshot 2026-10-14', title: 'Comparative tax-administration review, 2025', type: 'Official publication · primary', captured: '14 October 2026 · snapshot stored', corroboration: 'Agrees with the national adoption series of two jurisdictions (SRC-063, SRC-064)', carries: 'The eighty percent threshold at which the benefit is realised' },
    c2: { id: 'SRC-063 · SRC-064 · SRC-071', title: 'National adoption series, three comparator jurisdictions, 2019 to 2025', type: 'Official statistics · primary', captured: '15 October 2026 · three snapshots stored', corroboration: 'Each series reconciled against the jurisdiction\'s own evaluation report', carries: 'Time to threshold under a phased mandate and under a voluntary scheme' },
    c3: { id: 'MTG-003 · EVD-0214', title: 'Consultation record, Merchants Association, 21 October 2026', type: 'Stakeholder position · attributed and dated', captured: '21 October 2026 · transcript and record stored', corroboration: 'Held independently in two further consultations (MTG-005, MTG-009)', carries: 'Support, not price, as the binding constraint' },
    c4: { id: 'SRC-088 · snapshot 2026-10-16', title: 'Evaluation of the 2024 free-zone invoicing pilot', type: 'Official report · primary', captured: '16 October 2026 · snapshot stored', corroboration: 'Participant figures reproduced from table 4; the retention rate recomputed from them', carries: 'A third of participants lost in the first quarter' },
    gap: { id: 'ASM-019 · the gap', title: 'No source holds this figure', type: 'Assumption · bounded and flagged', captured: 'Written into the assumptions register on 22 October 2026', corroboration: 'Bounded between the two nearest comparators; a sensitivity on it sits in the appraisal (APL-003)', carries: 'Horus writes down what it could not verify instead of papering over it' }
  };
  (function receipt() {
    var claims = document.getElementById('claims'); var out = document.getElementById('source'); if (!claims || !out) return;
    function show(k) {
      var s = SOURCES[k]; if (!s) return;
      claims.querySelectorAll('.claim').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.c === k)); });
      out.className = 'source' + (k === 'gap' ? ' is-gap' : '');
      out.innerHTML = '<span class="data">' + s.id + '</span><h3>' + s.title + '</h3><dl><dt>Type</dt><dd>' + s.type + '</dd><dt>Captured</dt><dd>' + s.captured + '</dd><dt>Corroboration</dt><dd>' + s.corroboration + '</dd><dt>Carries</dt><dd>' + s.carries + '</dd></dl>';
    }
    claims.querySelectorAll('.claim').forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.c); }); });
    show('c1');
  })();

  /* ---------- requests: stored in the page's database when it is available, otherwise posted to the configured endpoint, otherwise shown to copy ---------- */
  var FORM_ENDPOINT = ''; // set to your form service URL (one that accepts multipart form posts with a file) when the site is hosted on its own domain
  var CONTACT = ''; // set to the company's address once it exists; shown as text, never as a mailto link
  var MAX_STORED_FILE = 160 * 1024; // the page database holds a document of up to 256 KiB; larger files travel through the endpoint instead
  function human(n) { return n < 1024 ? n + ' B' : n < 1048576 ? (n / 1024).toFixed(0) + ' KB' : (n / 1048576).toFixed(1) + ' MB'; }
  function asBase64(file) { return new Promise(function (res, rej) { var r = new FileReader(); r.onload = function () { res(String(r.result).split(',')[1] || ''); }; r.onerror = function () { rej(r.error); }; r.readAsDataURL(file); }); }
  function wireFile(box) {
    var input = box.querySelector('input[type=file]'); var name = box.querySelector('.file-name'); if (!input || !name) return;
    function show() { var f = input.files && input.files[0]; box.classList.toggle('has', !!f); name.textContent = f ? f.name + ' · ' + human(f.size) : ''; }
    input.addEventListener('change', show);
    ['dragenter', 'dragover'].forEach(function (ev) { box.addEventListener(ev, function (e) { e.preventDefault(); box.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { box.addEventListener(ev, function (e) { e.preventDefault(); box.classList.remove('over'); }); });
    box.addEventListener('drop', function (e) { var fs = e.dataTransfer && e.dataTransfer.files; if (fs && fs.length) { try { input.files = fs; } catch (x) { /* older engines: the user chooses the file instead */ } show(); } });
    box.reset = function () { box.classList.remove('has'); name.textContent = ''; };
  }
  document.querySelectorAll('.file').forEach(wireFile);

  function labelOf(form, el) { var l = el.id ? form.querySelector('label[for="' + el.id + '"]') : null; return (l ? l.textContent : el.name).toLowerCase(); }
  function wire(formId, statusId, copyId, kind, okText) {
    var form = document.getElementById(formId); var status = document.getElementById(statusId); var copy = document.getElementById(copyId); if (!form) return;
    form.addEventListener('input', function (e) { if (e.target && e.target.classList) e.target.classList.remove('invalid'); });
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var fileInput = form.querySelector('input[type=file]'); var file = fileInput && fileInput.files && fileInput.files[0] ? fileInput.files[0] : null;
      var scope = form.querySelector('[name=scope_text]'); var missing = [];
      if (scope && kind === 'engagement' && !file && !scope.value.trim()) { missing.push('the scope of work, attached or pasted'); scope.classList.add('invalid'); }
      form.querySelectorAll('[required]').forEach(function (el) { var empty = !String(el.value || '').trim(); el.classList.toggle('invalid', empty); if (empty) missing.push(labelOf(form, el)); });
      var email = form.querySelector('[name=email]');
      if (email && email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { email.classList.add('invalid'); missing.push('a valid work email'); }
      if (missing.length) { status.className = 'status err'; status.textContent = 'Please add ' + missing.join(', ') + '.'; var first = form.querySelector('.invalid'); if (first && first.focus) first.focus(); return; }

      var data = {}; new FormData(form).forEach(function (v, k) { if (typeof v === 'string') data[k] = v.trim(); });
      data.kind = kind; data.submitted_at = new Date().toISOString(); data.page = location.href.split('#')[0];
      if (file) data.attachment = { name: file.name, size: file.size, type: file.type };
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true; status.className = 'status'; status.textContent = 'Sending'; copy.classList.remove('show'); copy.textContent = '';
      var sent = false;
      try {
        var db = (window.claude && window.claude.use) ? await window.claude.use('db') : null;
        if (db) {
          var doc = Object.assign({}, data);
          if (file) doc.attachment = Object.assign({}, data.attachment, file.size <= MAX_STORED_FILE ? { content_base64: await asBase64(file) } : { stored: false, note: 'larger than the page database holds; ask for the file by email' });
          var id = 'req-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 7);
          await db.collection('requests').doc(id).set(doc); sent = true;
        }
      } catch (err) { sent = false; }
      if (!sent && FORM_ENDPOINT) {
        try {
          var fd = new FormData(form); fd.append('kind', kind); fd.append('submitted_at', data.submitted_at); fd.append('page', data.page);
          var r = await fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Accept': 'application/json' }, body: fd });
          if (!r.ok) throw new Error('endpoint ' + r.status); sent = true;
        } catch (err) { sent = false; }
      }
      if (sent) {
        status.className = 'status ok'; status.textContent = okText; form.reset(); form.querySelectorAll('.file').forEach(function (b) { if (b.reset) b.reset(); }); btn.disabled = false; return;
      }
      status.className = 'status err';
      status.textContent = (CONTACT ? 'This page could not send the request. Copy the text below and send it to ' + CONTACT : 'This page could not send the request. Copy the text below and send it by email') + (file ? ', with the scope document attached.' : '.');
      copy.textContent = Object.keys(data).filter(function (k) { return k !== 'page' && k !== 'attachment'; }).map(function (k) { return k + ': ' + data[k]; }).join('\n') + (file ? '\nattached: ' + file.name : '');
      copy.classList.add('show');
      var cb = document.createElement('button'); cb.type = 'button'; cb.className = 'btn'; cb.textContent = 'Copy';
      cb.addEventListener('click', function () { try { navigator.clipboard.writeText(copy.textContent.replace(/\n?Copy$/, '')).then(function () { cb.textContent = 'Copied'; }, function () { cb.textContent = 'Select and copy'; }); } catch (x) { cb.textContent = 'Select and copy'; } });
      copy.appendChild(cb); btn.disabled = false;
    });
  }
  wire('ask-form', 'ask-status', 'ask-copy', 'engagement', 'Received. Horus is reading the scope and will reply with the engagement plan within one working day.');
  wire('demo-form', 'demo-status', 'demo-copy', 'demo', 'Received. Horus will propose two times within one working day.');

  /* ---------- reveals: content is visible at rest; a gentle rise only as it enters ---------- */
  if (!reduced && 'IntersectionObserver' in window) {
    var els = document.querySelectorAll('.reveal'); var io = new IntersectionObserver(function (entries) { entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.remove('pending'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -5% 0px' });
    els.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top > window.innerHeight) { el.classList.add('pending'); io.observe(el); } });
  }
})();
