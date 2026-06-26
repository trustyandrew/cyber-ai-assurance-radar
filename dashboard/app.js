/* Renders window.DASHBOARD_DATA (from dashboard-data.js) into the mock-up layout.
   Vanilla JS, no dependencies. */
(function () {
  "use strict";
  var D = window.DASHBOARD_DATA;
  var app = document.getElementById("app");
  var metaBox = document.getElementById("meta-box");
  if (!D) return;

  var CTA = "If your organisation is preparing for ISO/IEC 27001, ISO/IEC 42001, " +
    "cyber assurance or responsible AI governance, I can help you separate what " +
    "matters from what is noise — and build an evidence-based path forward.";
  var PRI_CLASS = { Critical: "critical", High: "high", Medium: "medium", Watch: "watch", Low: "low" };
  var state = { filter: "All" };
  var votes = D.feedback || {};  // {id: {vote, at, item}} — overridden by live GET if served
  var itemsById = {};

  function indexItems() {
    (D.current_signals || []).forEach(function (it) { itemsById[it.id] = it; });
    Object.keys(D.sections || {}).forEach(function (k) {
      (D.sections[k] || []).forEach(function (it) { itemsById[it.id] = it; });
    });
  }

  function voteOf(id) {
    var v = votes[id];
    return v && typeof v === "object" ? (v.vote || "") : (v || "");
  }

  function pickedItems() {
    return Object.keys(votes)
      .filter(function (id) { return voteOf(id) === "up"; })
      .map(function (id) { return itemsById[id] || (votes[id] && votes[id].item); })
      .filter(Boolean);
  }

  function postVote(id, vote) {
    var item = itemsById[id] || (votes[id] && votes[id].item);
    if (vote === "none") { delete votes[id]; }
    else { votes[id] = { vote: vote, item: item }; }
    fetch("/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, vote: vote, item: vote === "up" ? item : null })
    }).catch(function () {});  // file:// has no server — UI still updates for the session
    render();
  }

  function buildNewsletter(range) {
    var status = document.getElementById("nl-status");
    var out = document.getElementById("nl-out");
    if (status) status.textContent = "Building…";
    fetch("/newsletter", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ range: range })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (out) out.value = d.md || "";
        if (status) status.textContent = d.count + " pick(s) · " + d.range + " · theme: " + (d.theme || "");
      })
      .catch(function () { if (status) status.textContent = "Build failed — is the local server running?"; });
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function passes(it) {
    if (voteOf(it.id) === "down") return false;
    if (state.filter === "All") return true;
    if (state.filter === "New") return !!it.is_new;
    return it.priority === state.filter;
  }

  function allMaterial() {
    var out = [], seen = {};
    Object.keys(D.sections || {}).forEach(function (k) {
      (D.sections[k] || []).forEach(function (it) {
        if (!seen[it.id]) { seen[it.id] = 1; out.push(it); }
      });
    });
    return out;
  }

  function signalCard(it) {
    var tags = (it.tags || []).slice(0, 4).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("");
    var newBadge = it.is_new ? '<span class="badge new">New</span>' : "";
    var why = it.why_it_matters
      ? '<div class="why"><strong>Why it matters:</strong> ' + esc(it.why_it_matters) + "</div>" : "";
    var action = it.suggested_action
      ? '<div class="action"><strong>Suggested action:</strong> ' + esc(it.suggested_action) + "</div>" : "";
    return (
      '<article class="card">' +
        '<div class="card-top">' +
          '<span class="badge ' + (PRI_CLASS[it.priority] || "watch") + '">' + esc(it.priority) + "</span>" +
          '<span class="lens">' + newBadge + " " + esc(it.lens) + " · " + it.relevance_score + "/5</span>" +
        "</div>" +
        "<h3>" + esc(it.title) + "</h3>" +
        (it.summary ? "<p>" + esc(it.summary) + "</p>" : "") +
        why + action +
        '<div class="card-meta"><span>' + esc(it.source) + "</span><span>" + esc(it.published_date || "—") + "</span></div>" +
        '<div class="tags">' + tags + "</div>" +
        '<div class="card-actions">' +
          '<a href="' + esc(it.url) + '" target="_blank" rel="noopener">Open source →</a>' +
          '<span class="votes">' +
            '<button class="vote up' + (voteOf(it.id) === "up" ? " active" : "") + '" data-id="' + esc(it.id) +
              '" data-vote="up" title="Mark as newsletter candidate" aria-label="Thumbs up">👍</button>' +
            '<button class="vote down" data-id="' + esc(it.id) +
              '" data-vote="down" title="Dismiss and exclude" aria-label="Thumbs down">👎</button>' +
          "</span>" +
        "</div>" +
      "</article>"
    );
  }

  function hero() {
    var c = D.counts || {};
    var kpis = [
      [c.items_material || 0, "Current signals in radar"],
      [c.newsletter_candidates || 0, "Newsletter candidates"],
      [c.standards_tracked || 0, "Standards tracked"],
      [(c.sources_ok || 0) + "/" + (c.sources_checked || 0), "Source families OK"],
    ];
    return (
      '<section class="hero">' +
        '<div class="hero-card">' +
          '<div class="eyebrow">Standards-led assurance radar</div>' +
          "<h1>Cyber, privacy and AI assurance are converging.</h1>" +
          "<p>A daily, standards-led scan across ASD/ACSC, ISO/IEC SC 27 and the 27000 family, " +
          "ISO/IEC SC 42 and the 42000 family, AI testing, data quality, impact and conformity " +
          "assessment, privacy and Australian Government AI obligations — ranked for assurance value, not noise.</p>" +
        "</div>" +
        '<div class="kpi-grid">' +
          kpis.map(function (k) {
            return '<div class="kpi"><div class="num">' + esc(k[0]) + '</div><div class="label">' + esc(k[1]) + "</div></div>";
          }).join("") +
        "</div>" +
      "</section>"
    );
  }

  function signalsSection() {
    var opts = ["All", "New", "Critical", "High", "Medium", "Watch"];
    var pills = opts.map(function (o) {
      return '<button data-p="' + o + '" aria-pressed="' + (state.filter === o) + '">' + o + "</button>";
    }).join("");
    var source = state.filter === "New" ? allMaterial() : (D.current_signals || []);
    var items = source.filter(passes).sort(function (a, b) {
      return (b.relevance_score || 0) - (a.relevance_score || 0);
    });
    var cards = items.length
      ? items.map(signalCard).join("")
      : '<p class="empty">' +
        (state.filter === "New" ? "Nothing new since the last run." : "No signals at this priority.") +
        "</p>";
    return (
      '<section id="signals">' +
        '<div class="section-head">' +
          "<div><h2>Current signals</h2><p>Ranked items likely to produce advisory, newsletter or assurance value.</p></div>" +
          '<div class="controls">' + pills + "</div>" +
        "</div>" +
        '<div class="cards">' + cards + "</div>" +
      "</section>"
    );
  }

  function standardsTable(id, title, sub, rows) {
    rows = rows || [];
    var body = rows.map(function (r) {
      var chg = r.change === "new" ? '<span class="chg new">NEW</span> '
              : (r.change === "updated" ? '<span class="chg upd">UPDATED</span> ' : "");
      return "<tr><td>" + chg + "<a href='" + esc(r.url) + "' target='_blank' rel='noopener'>" +
        esc(r.designation) + "</a></td>" +
        "<td>" + esc(r.area) + "</td>" +
        "<td><span class='state " + esc(r.status_class) + "'>" + esc(r.status) + "</span></td>" +
        "<td>" + esc(r.why) + "</td></tr>";
    }).join("");
    return (
      '<section id="' + id + '">' +
        '<div class="section-head"><div><h2>' + esc(title) + "</h2><p>" + esc(sub) + "</p></div></div>" +
        '<div class="table-panel"><table><thead><tr>' +
          "<th>Standard / work item</th><th>Area</th><th>Status</th><th>Why watch it</th>" +
        "</tr></thead><tbody>" + body + "</tbody></table>" +
        '<p class="disclaimer">Curated register — confirm current edition / stage at the source.</p></div>' +
      "</section>"
    );
  }

  function sourceQueue() {
    var rows = (D.source_queue || []).map(function (s) {
      return "<tr><td><strong>" + esc(s.family) + "</strong></td><td>" + esc(s.terms) +
        "</td><td><span class='mini-badge " + esc((s.priority || "").toLowerCase()) + "'>" + esc(s.priority) + "</span></td></tr>";
    }).join("");
    return (
      '<section id="sources">' +
        '<div class="section-head"><div><h2>Source queue &amp; search strategy</h2>' +
        "<p>The configuration the daily 8am job and Friday newsletter roll-up work from.</p></div></div>" +
        '<div class="table-panel"><table><thead><tr><th>Source family</th><th>Search / watch terms</th><th>Priority</th></tr></thead>' +
        "<tbody>" + rows + "</tbody></table></div>" +
      "</section>"
    );
  }

  function sourceHealth() {
    var rows = ((D.source_health || {}).sources || []).map(function (s) {
      return "<tr><td><strong>" + esc(s.name) + "</strong></td>" +
        "<td><span class='state " + esc(s.status) + "'>" + esc(s.status) + "</span></td>" +
        "<td>" + esc(s.detail) + "</td></tr>";
    }).join("");
    return (
      '<section id="health">' +
        '<div class="section-head"><div><h2>Source health</h2><p>What was checked, what failed, and what needs manual review.</p></div></div>' +
        '<div class="table-panel"><table><thead><tr><th>Source</th><th>Status</th><th>Detail</th></tr></thead>' +
        "<tbody>" + rows + "</tbody></table></div>" +
      "</section>"
    );
  }

  function newsletterSection() {
    var picks = pickedItems();
    var pickList = picks.length
      ? picks.map(function (it) {
          return "<li><a href='" + esc(it.url) + "' target='_blank' rel='noopener'>" +
            esc(it.title) + "</a> — " + esc(it.source) + "</li>";
        }).join("")
      : "<li>No picks yet — give signals a 👍 above to add them.</li>";
    var ranges = [["since_last", "Since last"], ["week", "Last week"],
                  ["month", "Last month"], ["quarter", "Last quarter"]];
    var buttons = ranges.map(function (r) {
      return '<button class="nl-range" data-range="' + r[0] + '">' + r[1] + "</button>";
    }).join("");
    return (
      '<section id="newsletter">' +
        '<div class="section-head"><div><h2>Newsletter</h2>' +
        "<p>Build a copy/paste brief from your 👍 picks.</p></div></div>" +
        '<div class="twocol">' +
          '<div class="callout"><h3>Your picks (👍) — ' + picks.length + "</h3>" +
            '<ul id="picks">' + pickList + "</ul></div>" +
          '<div class="callout"><h3>Build newsletter</h3>' +
            '<div class="nl-controls">' + buttons + "</div>" +
            '<p class="nl-status" id="nl-status">Pick a range to generate.</p>' +
            '<textarea id="nl-out" class="nl-out" readonly placeholder="Newsletter markdown appears here…"></textarea>' +
            '<button id="nl-copy" class="button" style="margin-top:10px">Copy to clipboard</button>' +
          "</div>" +
        "</div>" +
      "</section>"
    );
  }

  function footer() {
    return '<section class="footer"><div><h3>Signal, not noise.</h3><p>' + esc(CTA) +
      '</p></div><a class="button" href="#signals">Back to signals</a></section>';
  }

  function renderMeta() {
    var c = D.counts || {};
    metaBox.innerHTML =
      "<strong>Last run:</strong><br>" + esc(D.generated_at || "") + "<br>" + esc(D.timezone || "") + "<br><br>" +
      "Source families: " + (c.sources_ok || 0) + "/" + (c.sources_checked || 0) + " ok, " + (c.sources_failed || 0) + " failed<br>" +
      "Current signals: " + (c.items_material || 0) + " (" + (c.items_new || 0) + " new)<br>" +
      "Standards in radar: " + (c.standards_tracked || 0) + "<br>" +
      "Newsletter candidates: " + (c.newsletter_candidates || 0);
  }

  function render() {
    var s = D.standards || {};
    app.innerHTML =
      hero() +
      signalsSection() +
      standardsTable("sc27", "SC 27 / 27000 family radar",
        "Information security, cyber and privacy-protection standards to monitor.", s.sc27) +
      standardsTable("sc42", "SC 42 / 42000 and AI assurance radar",
        "AI management systems, impact assessment, testing, data quality, transparency and incident reporting.", s.sc42) +
      standardsTable("frameworks", "Global & national frameworks",
        "NIST CSF & AI RMF, EU AI Act, ASD ISM/Essential Eight, PSPF and others — aligned with the reference vault.", s.frameworks) +
      sourceQueue() + sourceHealth() + newsletterSection() + footer();
    app.querySelectorAll(".controls button").forEach(function (b) {
      b.addEventListener("click", function () { state.filter = b.dataset.p; render(); });
    });
    app.querySelectorAll(".vote").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.dataset.id, vote = b.dataset.vote;
        if (vote === "up" && voteOf(id) === "up") vote = "none";  // click 👍 again to clear
        postVote(id, vote);
      });
    });
    app.querySelectorAll(".nl-range").forEach(function (b) {
      b.addEventListener("click", function () { buildNewsletter(b.dataset.range); });
    });
    var copyBtn = document.getElementById("nl-copy");
    if (copyBtn) copyBtn.addEventListener("click", function () {
      var out = document.getElementById("nl-out");
      if (out && out.value && navigator.clipboard) {
        navigator.clipboard.writeText(out.value);
        copyBtn.textContent = "Copied ✓";
        setTimeout(function () { copyBtn.textContent = "Copy to clipboard"; }, 1500);
      }
    });
  }

  function init() { indexItems(); renderMeta(); render(); }
  init();  // render immediately from baked feedback — never block render on the network
  // then refresh live votes from the local server (best-effort) and re-render if changed
  fetch("/feedback.json", { cache: "no-store" })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (live) { if (live && typeof live === "object") { votes = live; render(); } })
    .catch(function () {});
})();
