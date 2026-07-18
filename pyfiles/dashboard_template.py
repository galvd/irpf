"""
Template do dashboard (HTML/CSS/JS completos) como string Python — fonte de
verdade do design, sem depender de nenhum arquivo .html no repositorio.

Editar o design (CSS, JS, layout) = editar o TEMPLATE_HTML abaixo diretamente.
dashboard_builder.py injeta os dados desta string (nunca a modifica) e grava o
resultado em index.html na raiz do projeto.

O placeholder <script type="application/json" id="irpf-data">{}</script> e
substituido em tempo de build pelo JSON real (ver dashboard_builder.render_html).
"""

TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Observatório de Empresas do ES: Monitor de Emprego e Renda</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg-page:#FFFFFF;
    --bg-panel:#BBDEFB;
    --bg-panel-soft:#E3F2FD;
    --bg-card:#FFFFFF;
    --blue-dark:#1565C0;
    --blue-mid:#2196F3;
    --blue-border:#90CAF9;
    --blue-muted:#5C84AC;
    --magenta:#F06292;
    --magenta-text:#C2185B;
    --magenta-soft:#FCE4EC;
    --font-display:"Baloo 2", "Nunito", sans-serif;
    --font-body:"Nunito", -apple-system, sans-serif;
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{
    margin:0;
    background:var(--bg-page);
    color:var(--blue-dark);
    font-family:var(--font-body);
    line-height:1.5;
    -webkit-font-smoothing:antialiased;
  }
  @media (prefers-reduced-motion: reduce){
    *{transition:none !important; animation:none !important;}
  }
  a{color:var(--magenta-text);}
  ::selection{background:var(--magenta); color:#fff;}

  .wrap{max-width:1440px; margin:0 auto; padding:0 24px 56px;}

  header.top{
    text-align:center;
    padding:36px 0 28px;
  }
  header.top h1{
    font-family:var(--font-display); font-weight:800; font-size:28px;
    margin:0 0 6px; color:var(--blue-dark); letter-spacing:0.2px; line-height:1.2;
  }
  @media (max-width:640px){ header.top h1{font-size:22px;} }
  header.top p{
    margin:0; color:var(--blue-mid); font-size:18px; font-weight:600;
  }
  .badge-exercicio{
    display:inline-block; margin-top:14px;
    font-family:var(--font-body); font-weight:700; font-size:12.5px;
    color:var(--magenta-text); background:#fff; border:1.5px solid var(--magenta);
    padding:6px 16px; border-radius:20px;
  }

  .mega-panel{
    background:var(--bg-panel); border-radius:24px; padding:28px 28px 32px;
  }
  .mega-panel.municipios-panel{margin-top:18px;}

  .section-label{
    font-size:12px; text-transform:uppercase; letter-spacing:1.2px;
    color:var(--blue-dark); margin:0 0 12px; font-weight:700;
    font-family:var(--font-body);
  }

  .cards-grid{
    display:grid; grid-template-columns:repeat(6, minmax(0, 1fr)); gap:12px;
  }
  @media (max-width:960px){ .cards-grid{grid-template-columns:repeat(3, minmax(0, 1fr));} }
  @media (max-width:560px){ .cards-grid{grid-template-columns:repeat(2, minmax(0, 1fr));} }
  .card{
    background:var(--bg-card); border-radius:16px; padding:14px 16px;
    height:82px; display:flex; flex-direction:column; justify-content:center;
    overflow:hidden;
  }
  .card .lbl{
    font-size:11.5px; color:var(--blue-mid); margin:0 0 6px; font-weight:700;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }
  .card .val{
    font-family:var(--font-display); font-weight:700; font-size:22px;
    font-variant-numeric:tabular-nums; margin:0; color:var(--blue-dark);
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }

  .main-grid{
    display:grid; grid-template-columns:400px 1fr; gap:20px; margin-top:24px;
    align-items:start;
  }
  @media (max-width:860px){ .main-grid{grid-template-columns:1fr;} }

  .search-input{
    width:100%; background:var(--bg-card); border:none;
    color:var(--blue-dark); font-family:var(--font-body); font-weight:600; font-size:14px;
    padding:11px 16px; border-radius:24px; margin-bottom:12px;
  }
  .search-input:focus{outline:2px solid var(--magenta); outline-offset:1px;}
  .search-input::placeholder{color:var(--blue-muted); font-weight:500;}

  .list-card{background:var(--bg-card); border-radius:18px; padding:6px 4px;}

  table.mun-table{width:100%; border-collapse:collapse; font-size:12.5px;}
  table.mun-table th{
    text-align:right; font-weight:700; color:var(--blue-mid); font-size:10.5px;
    text-transform:uppercase; letter-spacing:0.5px; padding:10px 10px 8px; cursor:pointer;
    user-select:none; white-space:nowrap; position:sticky; top:0; background:var(--bg-card);
  }
  table.mun-table th:first-child, table.mun-table td:first-child{text-align:left;}
  table.mun-table th:hover{color:var(--magenta-text);}
  table.mun-table th.active{color:var(--magenta-text);}
  table.mun-table td{
    padding:8px 10px; text-align:right; font-family:var(--font-body); font-weight:600;
    color:var(--blue-dark); font-variant-numeric:tabular-nums; white-space:nowrap;
  }
  table.mun-table td:first-child{ text-align:left; white-space:normal; font-weight:600;}
  table.mun-table tbody tr{cursor:pointer; border-radius:10px;}
  table.mun-table tbody tr:hover td{background:var(--bg-panel-soft);}
  table.mun-table tbody tr.selected td{background:var(--magenta-soft);}
  table.mun-table tbody tr.selected td:first-child{color:var(--magenta-text); font-weight:800;}

  tr.state-row td{background:var(--bg-panel-soft); font-weight:800; border-bottom:2px solid var(--blue-border);}
  tr.state-row td:first-child{font-family:var(--font-display); font-size:14px; color:var(--blue-dark);}
  tr.state-row:hover td{background:#D6EAFB;}
  tr.state-row.selected td{background:var(--magenta-soft) !important;}
  tr.state-row.selected td:first-child{color:var(--magenta-text) !important;}

  .table-scroll{max-height:560px; overflow-y:auto; margin-top:2px;}
  .table-scroll::-webkit-scrollbar{width:8px;}
  .table-scroll::-webkit-scrollbar-thumb{background:var(--blue-border); border-radius:4px;}

  .detail-head{display:flex; align-items:flex-start; gap:14px; margin-bottom:18px;}
  .detail-head h2{
    font-family:var(--font-display); font-weight:700; font-size:24px; margin:0 0 2px;
    color:var(--blue-dark);
  }
  .detail-head .sub{color:var(--blue-dark); font-size:13.5px; margin:0; font-weight:700;}

  .detail-cards{
    display:grid; grid-template-columns:repeat(6, minmax(0, 1fr)); gap:10px; margin-bottom:24px;
  }
  @media (max-width:760px){ .detail-cards{grid-template-columns:repeat(2, minmax(0, 1fr));} }

  .chart-controls{
    display:flex; align-items:center; gap:10px; margin-bottom:14px; flex-wrap:wrap;
  }
  .chart-controls span{font-size:11px; color:var(--blue-dark); text-transform:uppercase; letter-spacing:0.6px; font-weight:700;}
  .metric-btn{
    background:var(--bg-card); border:1.5px solid transparent; color:var(--blue-mid);
    font-family:var(--font-body); font-weight:700; font-size:12px; padding:6px 14px; border-radius:20px;
    cursor:pointer;
  }
  .metric-btn.active{border-color:var(--magenta); color:var(--magenta-text);}
  .metric-btn:hover{color:var(--blue-dark);}

  .bar-row{display:grid; grid-template-columns:220px 1fr 130px; align-items:center; gap:10px; margin-bottom:9px;}
  .bar-label{
    font-size:12px; color:var(--blue-dark); text-align:right; font-weight:600;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }
  .bar-track{
    background:var(--bg-card); border:1px solid var(--blue-border); border-radius:10px;
    height:20px; position:relative; overflow:hidden;
  }
  .bar-fill{height:100%; background:var(--magenta); border-radius:10px;}
  .bar-fill-overlay{
    position:absolute; left:0; top:0;
    height:100%; background:var(--blue-dark); border-radius:0;
  }
  .chart-legend{
    display:flex; align-items:center; gap:8px; font-size:13px; color:var(--blue-mid);
    font-weight:600; margin:14px 0 0;
  }
  .chart-legend .legend-swatch{width:24px; height:9px; border-radius:5px; display:inline-block; margin-right:4px; vertical-align:middle;}
  .chart-legend .legend-swatch-tax{background:var(--blue-dark);}
  .chart-legend .legend-swatch-rest{background:var(--magenta); margin-left:12px;}
  .bar-value{
    white-space:nowrap; text-align:right;
    font-family:var(--font-body); font-weight:700; font-size:11.5px; color:var(--blue-dark);
  }
  @media (max-width:640px){ .bar-row{grid-template-columns:120px 1fr 105px;} .bar-label{font-size:11px;} }

  footer{
    margin-top:32px; color:var(--blue-muted); font-size:11.5px; line-height:1.7; text-align:center;
  }
  footer a{color:var(--blue-muted); text-decoration:underline;}
  footer .footer-links{
    margin:14px 0 0; padding-top:14px; border-top:1px solid var(--blue-border);
    font-size:12px;
  }
  footer .footer-links a{color:var(--magenta-text); text-decoration:underline; font-weight:600;}

  .empty-hint{color:var(--blue-muted); font-size:12.5px; padding:20px 4px;}
</style>
</head>
<body>
<div class="wrap">

  <header class="top">
    <h1>Observatório de Empresas do ES: Monitor de Emprego e Renda</h1>
    <p>Perfil dos declarantes de IRPF por município</p>
    <span class="badge-exercicio">Exercício 2026 · Receita Federal</span>
  </header>

  <div class="mega-panel state-panel">
    <div class="section-label">Estado · Espírito Santo (agregado)</div>
    <div class="cards-grid" id="stateCards"></div>
  </div>

  <div class="mega-panel municipios-panel">
    <div class="main-grid">
      <div>
        <input type="text" class="search-input" id="searchBox" placeholder="Buscar município…">
        <div class="list-card">
          <div class="table-scroll">
            <table class="mun-table">
              <thead>
                <tr>
                  <th data-key="name">Município</th>
                  <th data-key="tq">Declar.</th>
                  <th data-key="i">Idade</th>
                  <th data-key="rt">Rend.</th>
                  <th data-key="f">Fem.</th>
                </tr>
              </thead>
              <tbody id="munTableBody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div id="detailPanel"></div>
    </div>

  </div>

  <footer>
    Dados agregados extraídos do painel público "Perfil do Declarante IRPF" da Receita Federal (Power BI publish-to-web).
    Grupos município × profissão com menos de 10 declarantes são omitidos pela própria fonte (regra de sigilo estatístico);
    por isso, a soma dos declarantes por profissão fica cerca de 1,5% abaixo do total oficial do estado.
    Valores monetários em reais correntes do exercício 2026.
    <p class="footer-links">
      Construído por <strong>Daniel Galvêas</strong> ·
      <a href="https://github.com/galvd" target="_blank" rel="noopener">github.com/galvd</a> ·
      Projeto irmão: <a href="https://github.com/galvd/RAIS_information_loss" target="_blank" rel="noopener">Monitor de Emprego e Renda</a>
      (<a href="https://galvd.github.io/RAIS_information_loss/" target="_blank" rel="noopener">mapas</a>)
    </p>
  </footer>

</div>

<script type="application/json" id="irpf-data">{}</script>
<script>
(function(){
  const DATA = JSON.parse(document.getElementById('irpf-data').textContent);
  const names = Object.keys(DATA);
  const STATE_ID = '__ESTADO__';

  if (names.length === 0){
    document.querySelector('.mega-panel').innerHTML =
      '<p style="padding:48px 24px;text-align:center;color:var(--blue-mid);font-weight:600;">' +
      'Nenhum dado carregado neste arquivo — isto é o template de design.<br>' +
      'Rode <code>python main.py build-dashboard</code> para gerar o index.html com os dados atuais.</p>';
    return;
  }

  const fmtInt = n => n == null ? '—' : n.toLocaleString('pt-BR');
  const fmtPct = n => n == null ? '—' : (n*100).toLocaleString('pt-BR',{maximumFractionDigits:1}) + '%';
  const fmtIdade = n => n == null ? '—' : n.toLocaleString('pt-BR',{maximumFractionDigits:1});
  const fmtR$compact = n => {
    if (n == null) return '—';
    if (n >= 1000) return 'R$ ' + (n/1000).toLocaleString('pt-BR',{maximumFractionDigits:1}) + 'K';
    return 'R$ ' + n.toLocaleString('pt-BR',{maximumFractionDigits:0});
  };
  // Padrao de 2 casas decimais para os valores que identificam as barras do grafico
  // (declarantes fica com fmtInt, sem casas decimais, por ser contagem de pessoas)
  const fmtR$bar = n => {
    if (n == null) return '—';
    if (n >= 1000) return 'R$ ' + (n/1000).toLocaleString('pt-BR',{minimumFractionDigits:2, maximumFractionDigits:2}) + 'K';
    return 'R$ ' + n.toLocaleString('pt-BR',{minimumFractionDigits:2, maximumFractionDigits:2});
  };

  function weightedState(key){
    let num = 0, den = 0;
    names.forEach(n => {
      const d = DATA[n];
      if (d[key] != null){ num += d[key]*d.tq; den += d.tq; }
    });
    return den ? num/den : null;
  }
  const stateTotal = names.reduce((s,n)=>s+DATA[n].tq,0);
  const stateAgg = {
    tq: stateTotal, f: weightedState('f'), i: weightedState('i'),
    rt: weightedState('rt'), rb: weightedState('rb'), pt: weightedState('pt'),
  };

  const stateProfsMap = {};
  names.forEach(n => {
    DATA[n].profs.forEach(([p, q, f, i, rt, rb, pt, pFull]) => {
      if (!stateProfsMap[p]) stateProfsMap[p] = {q:0, fw:0, iw:0, rtw:0, rbw:0, ptw:0, full:pFull};
      const acc = stateProfsMap[p];
      acc.q += q;
      if (f  != null){ acc.fw  += f*q;  }
      if (i  != null){ acc.iw  += i*q;  }
      if (rt != null){ acc.rtw += rt*q; }
      if (rb != null){ acc.rbw += rb*q; }
      if (pt != null){ acc.ptw += pt*q; }
    });
  });
  const STATE_PROFS = Object.entries(stateProfsMap).map(([p, a]) => [
    p, a.q,
    a.q ? a.fw/a.q : null, a.q ? a.iw/a.q : null,
    a.q ? a.rtw/a.q : null, a.q ? a.rbw/a.q : null, a.q ? a.ptw/a.q : null,
    a.full,
  ]);

  function renderMetricCards(d){
    return `
      <div class="card"><p class="lbl" title="Feminino">Feminino</p><p class="val">${fmtPct(d.f)}</p></div>
      <div class="card"><p class="lbl" title="Idade média">Idade média</p><p class="val">${fmtIdade(d.i)}</p></div>
      <div class="card"><p class="lbl" title="Rend. tributável médio">Rend. tributável médio</p><p class="val">${fmtR$compact(d.rb)}</p></div>
      <div class="card"><p class="lbl" title="Renda anual média">Renda anual média</p><p class="val">${fmtR$compact(d.rt)}</p></div>
      <div class="card"><p class="lbl" title="Patrimônio médio">Patrimônio médio</p><p class="val">${fmtR$compact(d.pt)}</p></div>
      <div class="card"><p class="lbl" title="N de declarantes">N de declarantes</p><p class="val">${fmtInt(d.tq)}</p></div>
    `;
  }

  document.getElementById('stateCards').innerHTML = renderMetricCards(stateAgg);

  let sortKey = 'name', sortDir = 1, filterText = '', selected = STATE_ID;
  let profMetric = 'rt';

  const rankByTq = [...names].sort((a,b)=>DATA[b].tq - DATA[a].tq);
  const rankIndex = {}; rankByTq.forEach((n,i)=>rankIndex[n]=i+1);

  function renderTable(){
    let list = names.filter(n => DATA[n].disp.toLowerCase().includes(filterText.toLowerCase()));
    list.sort((a,b) => {
      if (sortKey === 'name'){
        return DATA[a].disp.localeCompare(DATA[b].disp, 'pt-BR', {sensitivity:'base'}) * sortDir;
      }
      const va = DATA[a][sortKey], vb = DATA[b][sortKey];
      if (va == null) return 1; if (vb == null) return -1;
      if (va < vb) return -1*sortDir; if (va > vb) return 1*sortDir;
      return 0;
    });

    const stateRow = `<tr class="state-row ${selected===STATE_ID?'selected':''}" data-name="${STATE_ID}">
      <td>Espírito Santo · todos os municípios</td>
      <td>${fmtInt(stateAgg.tq)}</td>
      <td>${fmtIdade(stateAgg.i)}</td>
      <td>${fmtR$compact(stateAgg.rt)}</td>
      <td>${fmtPct(stateAgg.f)}</td>
    </tr>`;

    const body = document.getElementById('munTableBody');
    if (!list.length){
      body.innerHTML = stateRow + `<tr><td colspan="5" class="empty-hint">Nenhum município encontrado.</td></tr>`;
    } else {
      body.innerHTML = stateRow + list.map(n => {
        const d = DATA[n];
        return `<tr data-name="${n}" class="${n===selected?'selected':''}">
          <td>${d.disp}</td>
          <td>${fmtInt(d.tq)}</td>
          <td>${fmtIdade(d.i)}</td>
          <td>${fmtR$compact(d.rt)}</td>
          <td>${fmtPct(d.f)}</td>
        </tr>`;
      }).join('');
    }
    body.querySelectorAll('tr[data-name]').forEach(tr => {
      tr.addEventListener('click', () => selectMunicipio(tr.getAttribute('data-name')));
    });
  }

  document.querySelectorAll('table.mun-table th').forEach(th => {
    if (th.getAttribute('data-key') === 'name') th.classList.add('active');
    th.addEventListener('click', () => {
      const key = th.getAttribute('data-key');
      if (sortKey === key) sortDir *= -1; else { sortKey = key; sortDir = key==='name' ? 1 : -1; }
      document.querySelectorAll('table.mun-table th').forEach(t=>t.classList.remove('active'));
      th.classList.add('active');
      renderTable();
    });
  });

  document.getElementById('searchBox').addEventListener('input', e => {
    filterText = e.target.value; renderTable();
  });

  function renderDetail(){
    const panel = document.getElementById('detailPanel');
    const isState = selected === STATE_ID;
    const d = isState ? stateAgg : DATA[selected];

    const metricLabels = {rt:'Renda anual média', pt:'Patrimônio médio', rb:'Renda anual tributável', q:'Nº de declarantes'};
    const metrics = Object.keys(metricLabels);
    const idx = {q:1, rt:4, rb:5, pt:6}[profMetric];
    const sourceProfs = isState ? STATE_PROFS : d.profs;
    const profs = [...sourceProfs].sort((a,b) => (b[idx]||0) - (a[idx]||0)).slice(0, 12);
    const maxVal = Math.max(...profs.map(p => p[idx] || 0), 1);
    const fmtBar = profMetric === 'q' ? fmtInt : fmtR$bar;
    const isRendaAnual = profMetric === 'rt';

    const headHtml = isState
      ? `<div>
           <h2>Espírito Santo</h2>
           <p class="sub">Agregado dos 78 municípios · todas as profissões</p>
         </div>`
      : `<div>
           <h2>${d.disp}</h2>
           <p class="sub">${rankIndex[selected]}º maior município do ES em nº de declarantes</p>
         </div>`;

    panel.innerHTML = `
      <div class="detail-head">${headHtml}</div>
      <div class="detail-cards">${renderMetricCards(d)}</div>
      <div class="section-label" style="margin-top:0;">Profissões · top 12 ${isState ? '(estado inteiro)' : ''}</div>
      <div class="chart-controls">
        <span>Ordenar por</span>
        ${metrics.map(m => `<button class="metric-btn ${m===profMetric?'active':''}" data-metric="${m}">${metricLabels[m]}</button>`).join('')}
      </div>
      <div id="profChart"></div>
      ${isRendaAnual ? '<div class="chart-legend"><span class="legend-swatch legend-swatch-rest"></span>Renda anual total &nbsp; <span class="legend-swatch legend-swatch-tax"></span>Renda tributável (sobreposta, mesma escala)</div>' : ''}
    `;

    const chart = document.getElementById('profChart');
    chart.innerHTML = profs.map(p => {
      const val = p[idx] || 0;
      const pct = Math.max((val / maxVal) * 100, 2);

      if (isRendaAnual){
        const rendTotal = p[4] || 0;
        const rendTrib = p[5] || 0;
        const pctTrib = rendTotal ? Math.round((rendTrib / rendTotal) * 100) : 0;
        const totalPct = Math.max((rendTotal / maxVal) * 100, 2);
        const tribPct = Math.max((rendTrib / maxVal) * 100, 0);
        return `<div class="bar-row">
          <div class="bar-label" title="${p[7] || p[0]}">${p[0]}</div>
          <div class="bar-track">
            <div class="bar-fill" style="width:${totalPct}%"></div>
            <div class="bar-fill-overlay" style="width:${tribPct}%"></div>
          </div>
          <div class="bar-value">(${pctTrib}%) ${fmtBar(val)}</div>
        </div>`;
      }

      return `<div class="bar-row">
        <div class="bar-label" title="${p[7] || p[0]}">${p[0]}</div>
        <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
        <div class="bar-value">${fmtBar(val)}</div>
      </div>`;
    }).join('');

    panel.querySelectorAll('.metric-btn').forEach(btn => {
      btn.addEventListener('click', () => { profMetric = btn.getAttribute('data-metric'); renderDetail(); });
    });
  }

  function selectMunicipio(name){
    selected = name;
    renderTable();
    renderDetail();
    if (window.innerWidth <= 860){
      document.getElementById('detailPanel').scrollIntoView({behavior:'smooth', block:'start'});
    }
  }

  renderTable();
  renderDetail();
})();
</script>
</body>
</html>
"""
