const DATA_URL = "data/autoteakg_frontend_data.json";

const TYPE_COLORS = {
  Paper: "#8f6435",
  EvidenceRecord: "#20383b",
  TeaType: "#6f9276",
  MaterialForm: "#a0a97a",
  ComponentGroup: "#e0ac4f",
  ActivityCategory: "#cd654b",
  StudyType: "#7b91b2",
  EvidenceLevel: "#8f7ab8",
  EffectDirection: "#b88a7a",
  Mechanism: "#546e7a",
  MicrobiotaFeature: "#3a8f7b",
  MicrobialMetabolite: "#b37a2f",
  HostPhenotype: "#b25c5c",
  UncertaintyFlag: "#787878",
  ProcessingStep: "#506c3f",
  ExtractionMethod: "#5b7a91",
};

const fmt = new Intl.NumberFormat("en-US");
let state = {};
let graphRuntime = null;

function el(tag, className = "", text = "") {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function topEntries(obj, n = 10) {
  return Object.entries(obj || {})
    .filter(([k]) => k)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n);
}

function renderMetrics(metrics) {
  const items = [
    ["证据记录", metrics.records],
    ["图谱节点", metrics.nodes],
    ["图谱关系", metrics.edges],
    ["微生物相关记录", metrics.microbiome_records],
    ["缺少上下文记录", metrics.missing_context_after_methods || 303],
  ];
  const root = document.getElementById("metrics");
  root.innerHTML = "";
  for (const [label, value] of items) {
    const card = el("div", "metric-card");
    card.appendChild(el("strong", "", fmt.format(value)));
    card.appendChild(el("span", "", label));
    root.appendChild(card);
  }
}

function drawBarChart(canvas, entries, options = {}) {
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = Math.floor(rect.width * dpr);
  canvas.height = Math.floor(rect.height * dpr);
  ctx.scale(dpr, dpr);
  const w = rect.width;
  const h = rect.height;
  ctx.clearRect(0, 0, w, h);
  const left = 155;
  const right = 38;
  const top = 16;
  const rowH = Math.max(22, (h - 40) / entries.length);
  const max = Math.max(...entries.map(([, v]) => v), 1);
  ctx.font = "13px Arial";
  ctx.textBaseline = "middle";
  entries.forEach(([label, value], i) => {
    const y = top + i * rowH + rowH / 2;
    const barW = ((w - left - right) * value) / max;
    ctx.fillStyle = "#20383b";
    ctx.fillText(label, 10, y);
    ctx.fillStyle = options.color || "#6f9276";
    ctx.fillRect(left, y - 8, barW, 16);
    ctx.fillStyle = "#20383b";
    ctx.fillText(value, left + barW + 8, y);
  });
}

function populateSelect(id, values, label) {
  const sel = document.getElementById(id);
  sel.innerHTML = "";
  sel.appendChild(new Option(label, ""));
  values.forEach((v) => sel.appendChild(new Option(v, v)));
}

function renderFilters(data) {
  populateSelect("activityFilter", data.filters.activity_categories, "全部");
  populateSelect("evidenceFilter", data.filters.evidence_levels, "全部");
  populateSelect("uncertaintyFilter", data.filters.uncertainty_classes, "全部");
  populateSelect("componentFilter", data.filters.component_groups, "全部");
  ["activityFilter", "evidenceFilter", "uncertaintyFilter", "componentFilter", "searchBox"].forEach((id) => {
    document.getElementById(id).addEventListener("input", renderRecords);
  });
  document.getElementById("resetFilters").addEventListener("click", () => {
    ["activityFilter", "evidenceFilter", "uncertaintyFilter", "componentFilter"].forEach((id) => (document.getElementById(id).value = ""));
    document.getElementById("searchBox").value = "";
    renderRecords();
  });
}

function recordMatches(record) {
  const activity = document.getElementById("activityFilter").value;
  const evidence = document.getElementById("evidenceFilter").value;
  const uncertainty = document.getElementById("uncertaintyFilter").value;
  const component = document.getElementById("componentFilter").value;
  const query = document.getElementById("searchBox").value.toLowerCase().trim();
  if (activity && record.activity_category !== activity) return false;
  if (evidence && record.evidence_level !== evidence) return false;
  if (uncertainty && record.uncertainty_class !== uncertainty) return false;
  if (component && record.component_group !== component) return false;
  if (query) {
    const haystack = Object.values(record).join(" ").toLowerCase();
    if (!haystack.includes(query)) return false;
  }
  return true;
}

function renderRecords() {
  const tbody = document.getElementById("recordsTable");
  tbody.innerHTML = "";
  const rows = state.data.records.filter(recordMatches).slice(0, 80);
  for (const record of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${record.record_id}</strong><br><small>${record.paper_id} · ${record.year || ""}</small></td>
      <td>${record.tea_type || "—"}<br><small>${record.component_group || "—"}</small></td>
      <td>${record.activity_category || "—"}</td>
      <td>${record.evidence_level || "—"}<br><small>${record.study_type || ""}</small></td>
      <td>${record.mechanism_label || record.host_phenotype || "—"}<br><small>${record.microbial_metabolite || record.microbiota_taxon || ""}</small></td>
      <td><span class="pill">${record.uncertainty_class || "—"}</span><br><small>${record.uncertainty_flags || ""}</small></td>
    `;
    tr.addEventListener("click", () => showRecord(record));
    tbody.appendChild(tr);
  }
}

function showRecord(record) {
  const inspector = document.getElementById("inspector");
  inspector.innerHTML = `
    <h3>${record.record_id}</h3>
    <p><strong>${record.title || record.paper_id}</strong></p>
    <span class="pill">${record.activity_category}</span>
    <span class="pill">${record.evidence_level}</span>
    <span class="pill">${record.uncertainty_class}</span>
    <p><b>Tea / Component</b><br>${record.tea_type || "—"} / ${record.component_group || "—"}</p>
    <p><b>Mechanism</b><br>${record.mechanism_label || "—"}</p>
    <p><b>Metabolite / Phenotype</b><br>${record.microbial_metabolite || "—"} / ${record.host_phenotype || "—"}</p>
    <p><b>Claim</b><br>${record.claim_text_raw || "—"}</p>
  `;
}

function renderLegend(nodes) {
  const types = [...new Set(nodes.map((n) => n.type))].sort();
  const root = document.getElementById("legend");
  root.innerHTML = "";
  types.forEach((type) => {
    const item = el("span", "legend-item");
    const dot = el("span", "dot");
    dot.style.background = TYPE_COLORS[type] || "#999";
    item.appendChild(dot);
    item.appendChild(document.createTextNode(type));
    root.appendChild(item);
  });
}

function initGraph(data) {
  const canvas = document.getElementById("graphCanvas");
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const nodes = data.graph.nodes.map((n, i) => ({
    ...n,
    x: rect.width / 2 + Math.cos(i) * rect.width * 0.2 + (Math.random() - 0.5) * 80,
    y: rect.height / 2 + Math.sin(i) * rect.height * 0.2 + (Math.random() - 0.5) * 80,
    vx: 0,
    vy: 0,
  }));
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const edges = data.graph.edges
    .map((e) => ({ ...e, s: byId.get(e.source), t: byId.get(e.target) }))
    .filter((e) => e.s && e.t);
  graphRuntime = { canvas, ctx, nodes, edges, hover: null, selected: null };
  renderLegend(nodes);
  canvas.addEventListener("click", (event) => {
    const hit = hitTest(event);
    if (hit) showGraphItem(hit);
  });
  requestAnimationFrame(tickGraph);
}

function hitTest(event) {
  const { canvas, nodes, edges } = graphRuntime;
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;
  for (const node of nodes) {
    const r = node.type === "EvidenceRecord" ? 7 : 5;
    if (Math.hypot(node.x - x, node.y - y) < r + 5) return { kind: "node", item: node };
  }
  for (const edge of edges) {
    const d = pointLineDistance(x, y, edge.s.x, edge.s.y, edge.t.x, edge.t.y);
    if (d < 4) return { kind: "edge", item: edge };
  }
  return null;
}

function pointLineDistance(px, py, x1, y1, x2, y2) {
  const A = px - x1;
  const B = py - y1;
  const C = x2 - x1;
  const D = y2 - y1;
  const dot = A * C + B * D;
  const len = C * C + D * D;
  const t = Math.max(0, Math.min(1, dot / len));
  return Math.hypot(px - (x1 + t * C), py - (y1 + t * D));
}

function showGraphItem(hit) {
  const inspector = document.getElementById("inspector");
  if (hit.kind === "node") {
    const n = hit.item;
    inspector.innerHTML = `
      <h3>${n.label || n.id}</h3>
      <span class="pill">${n.type}</span>
      ${n.uncertainty_class ? `<span class="pill">${n.uncertainty_class}</span>` : ""}
      <p><b>ID</b><br>${n.id}</p>
      ${n.title ? `<p><b>Title</b><br>${n.title}</p>` : ""}
      ${n.claim_text_raw ? `<p><b>Claim</b><br>${n.claim_text_raw}</p>` : ""}
      ${n.uncertainty_flags ? `<p><b>Flags</b><br>${n.uncertainty_flags}</p>` : ""}
    `;
  } else {
    const e = hit.item;
    inspector.innerHTML = `
      <h3>${e.type}</h3>
      <p><b>Record</b><br>${e.record_id || "—"}</p>
      <p><b>PMID</b><br>${e.paper_id || "—"}</p>
      <span class="pill">${e.evidence_level || "no evidence"}</span>
      <span class="pill">${e.uncertainty_class || "no uncertainty"}</span>
      <p><b>Source -> Target</b><br>${e.source}<br>→ ${e.target}</p>
    `;
  }
}

function tickGraph() {
  const g = graphRuntime;
  if (!g) return;
  const rect = g.canvas.getBoundingClientRect();
  const w = rect.width;
  const h = rect.height;
  const cx = w / 2;
  const cy = h / 2;
  for (let iter = 0; iter < 2; iter++) {
    for (let i = 0; i < g.nodes.length; i++) {
      const a = g.nodes[i];
      for (let j = i + 1; j < g.nodes.length; j++) {
        const b = g.nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist2 = dx * dx + dy * dy + 0.01;
        const force = Math.min(1200 / dist2, 1.5);
        a.vx += dx * force * 0.01;
        a.vy += dy * force * 0.01;
        b.vx -= dx * force * 0.01;
        b.vy -= dy * force * 0.01;
      }
    }
    for (const e of g.edges) {
      const dx = e.t.x - e.s.x;
      const dy = e.t.y - e.s.y;
      e.s.vx += dx * 0.002;
      e.s.vy += dy * 0.002;
      e.t.vx -= dx * 0.002;
      e.t.vy -= dy * 0.002;
    }
    for (const n of g.nodes) {
      n.vx += (cx - n.x) * 0.0009;
      n.vy += (cy - n.y) * 0.0009;
      n.vx *= 0.86;
      n.vy *= 0.86;
      n.x = Math.max(18, Math.min(w - 18, n.x + n.vx));
      n.y = Math.max(18, Math.min(h - 18, n.y + n.vy));
    }
  }
  drawGraph();
  requestAnimationFrame(tickGraph);
}

function drawGraph() {
  const { canvas, ctx, nodes, edges } = graphRuntime;
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.floor(rect.width * dpr);
  canvas.height = Math.floor(rect.height * dpr);
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, rect.width, rect.height);
  ctx.lineWidth = 0.8;
  ctx.strokeStyle = "rgba(32,56,59,0.13)";
  for (const e of edges) {
    ctx.beginPath();
    ctx.moveTo(e.s.x, e.s.y);
    ctx.lineTo(e.t.x, e.t.y);
    ctx.stroke();
  }
  for (const n of nodes) {
    const r = n.type === "EvidenceRecord" ? 6.5 : n.type === "Paper" ? 5 : 4.6;
    ctx.beginPath();
    ctx.fillStyle = TYPE_COLORS[n.type] || "#999";
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fill();
    if (n.type === "EvidenceRecord") {
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  }
}

function initCharts(data) {
  drawBarChart(document.getElementById("activityChart"), topEntries(data.metrics.activity_counts, 9), { color: "#cd654b" });
  drawBarChart(document.getElementById("uncertaintyChart"), topEntries(data.metrics.uncertainty_counts, 5), { color: "#e0ac4f" });
}

fetch(DATA_URL)
  .then((res) => res.json())
  .then((data) => {
    state.data = data;
    data.metrics.missing_context_after_methods = 303;
    renderMetrics(data.metrics);
    initCharts(data);
    renderFilters(data);
    renderRecords();
    initGraph(data);
  })
  .catch((err) => {
    document.body.innerHTML = `<main class="panel"><h1>数据加载失败</h1><p>${err}</p><p>请在 frontend 目录运行 <code>python -m http.server</code> 后访问。</p></main>`;
  });
