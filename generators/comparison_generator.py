#!/usr/bin/env python3
"""格安SIM比較表HTML自動生成"""
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'money_machine.db')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'tools', 'sim-comparison')

def generate():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM comparison_data WHERE is_current = 1 AND category = 'sim' ORDER BY price ASC")
    plans = [dict(row) for row in c.fetchall()]
    conn.close()

    if not plans:
        print("  No data found!")
        return

    today = datetime.now().strftime('%Y年%m月%d日')

    # Build table rows
    rows_js = json.dumps(plans, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>格安SIM全プラン比較【自動更新】最安プランを即発見</title>
<meta name="description" content="主要格安SIM10社の全プランを料金・データ容量・GB単価で比較。自動更新で常に最新。あなたに最適なプランが見つかります。">
<meta property="og:title" content="格安SIM全プラン比較【自動更新】">
<meta property="og:description" content="主要10社の格安SIMプランを一括比較。料金順・データ容量順・GB単価順で並べ替え可能。">
<meta property="og:type" content="website">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans",sans-serif;background:#f5f7fa;color:#333;line-height:1.6}}
.container{{max-width:1200px;margin:0 auto;padding:16px}}
header{{background:linear-gradient(135deg,#1a73e8,#0d47a1);color:#fff;padding:32px 16px;text-align:center;border-radius:0 0 16px 16px}}
header h1{{font-size:clamp(1.4rem,4vw,2rem);margin-bottom:8px}}
header p{{opacity:.9;font-size:.95rem}}
.update-date{{font-size:.85rem;opacity:.7;margin-top:4px}}
.controls{{background:#fff;border-radius:12px;padding:16px;margin:16px 0;box-shadow:0 2px 8px rgba(0,0,0,.08);display:flex;flex-wrap:wrap;gap:12px;align-items:center}}
.controls label{{font-weight:600;font-size:.9rem;color:#555}}
.controls select,.controls button{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;font-size:.9rem;cursor:pointer;background:#fff}}
.controls button{{background:#1a73e8;color:#fff;border:none;font-weight:600}}
.controls button:hover{{background:#1557b0}}
.filter-chips{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}
.chip{{padding:6px 14px;border-radius:20px;border:1px solid #ddd;background:#fff;cursor:pointer;font-size:.85rem;transition:.2s}}
.chip.active{{background:#1a73e8;color:#fff;border-color:#1a73e8}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:16px 0}}
.stat-card{{background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.stat-card .num{{font-size:1.8rem;font-weight:700;color:#1a73e8}}
.stat-card .label{{font-size:.8rem;color:#888}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
thead{{background:#1a73e8;color:#fff}}
th{{padding:12px 8px;font-size:.85rem;cursor:pointer;white-space:nowrap;user-select:none}}
th:hover{{background:#1557b0}}
th .arrow{{margin-left:4px;font-size:.7rem}}
td{{padding:10px 8px;border-bottom:1px solid #f0f0f0;font-size:.9rem;text-align:center}}
tr:hover{{background:#f8f9ff}}
.provider-name{{font-weight:600;color:#333}}
.price{{font-weight:700;color:#1a73e8;font-size:1.05rem}}
.badge{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:.75rem;font-weight:600}}
.badge-best{{background:#e8f5e9;color:#2e7d32}}
.badge-good{{background:#fff3e0;color:#e65100}}
.gb-price{{color:#666}}
.btn-official{{display:inline-block;padding:6px 12px;background:#ff6d00;color:#fff;border-radius:6px;text-decoration:none;font-size:.8rem;font-weight:600;transition:.2s}}
.btn-official:hover{{background:#e65100}}
footer{{text-align:center;padding:24px 16px;color:#999;font-size:.8rem;margin-top:24px}}
@media(max-width:768px){{
  .controls{{flex-direction:column}}
  table{{font-size:.8rem}}
  td,th{{padding:8px 4px}}
  .btn-official{{padding:4px 8px;font-size:.75rem}}
}}
</style>
</head>
<body>
<header>
<h1>格安SIM 全プラン比較表</h1>
<p>主要10社の料金プランを一括比較 — あなたに最適なプランが見つかります</p>
<div class="update-date">最終更新: {today} ｜ 自動更新データ</div>
</header>
<div class="container">
<div class="stats" id="stats"></div>
<div class="controls">
<label>並び替え：</label>
<select id="sortSelect" onchange="sortTable()">
<option value="price">料金が安い順</option>
<option value="data_gb">データ容量順</option>
<option value="gb_price">GB単価が安い順</option>
<option value="provider">会社名順</option>
</select>
</div>
<div class="filter-chips" id="filterChips">
<div class="chip active" onclick="filterData('all')">全て</div>
<div class="chip" onclick="filterData(1)">1GB以下</div>
<div class="chip" onclick="filterData(3)">〜3GB</div>
<div class="chip" onclick="filterData(5)">〜5GB</div>
<div class="chip" onclick="filterData(10)">〜10GB</div>
<div class="chip" onclick="filterData(20)">〜20GB</div>
<div class="chip" onclick="filterData(999)">20GB+/無制限</div>
</div>
<table>
<thead>
<tr>
<th onclick="sortBy('provider')">会社名<span class="arrow"></span></th>
<th onclick="sortBy('plan_name')">プラン名<span class="arrow"></span></th>
<th onclick="sortBy('price')">月額料金<span class="arrow"></span></th>
<th onclick="sortBy('data_gb')">データ容量<span class="arrow"></span></th>
<th onclick="sortBy('gb_price')">GB単価<span class="arrow"></span></th>
<th>特徴</th>
<th>詳細</th>
</tr>
</thead>
<tbody id="tableBody"></tbody>
</table>
<footer>
<p>※ 表示価格は全て税込です。最新の正確な情報は各社公式サイトでご確認ください。</p>
<p>※ キャンペーン価格・割引適用前の通常価格を掲載しています。</p>
<p style="margin-top:8px">データ自動収集・更新 by Money Machine</p>
</footer>
</div>
<script>
const allPlans={json.dumps(plans, ensure_ascii=False)};
let currentSort="price";
let currentDir=1;
let currentFilter="all";
function init(){{
  renderStats();
  renderTable(allPlans);
}}
function renderStats(){{
  const el=document.getElementById("stats");
  const providers=new Set(allPlans.map(p=>p.provider));
  const minPrice=Math.min(...allPlans.filter(p=>p.price>0).map(p=>p.price));
  const avgPrice=Math.round(allPlans.filter(p=>p.price>0).reduce((a,b)=>a+b.price,0)/allPlans.filter(p=>p.price>0).length);
  el.innerHTML=`
    <div class="stat-card"><div class="num">${{providers.size}}</div><div class="label">社</div></div>
    <div class="stat-card"><div class="num">${{allPlans.length}}</div><div class="label">プラン</div></div>
    <div class="stat-card"><div class="num">${{minPrice.toLocaleString()}}円</div><div class="label">最安</div></div>
    <div class="stat-card"><div class="num">${{avgPrice.toLocaleString()}}円</div><div class="label">平均</div></div>`;
}}
function getGbPrice(p){{
  if(p.data_gb<=0||p.price<=0)return 99999;
  if(p.data_gb>=999)return Math.round(p.price/100);
  return Math.round(p.price/p.data_gb);
}}
function getFiltered(){{
  let d=[...allPlans];
  if(currentFilter!=="all"){{
    if(currentFilter===1)d=d.filter(p=>p.data_gb<=1);
    else if(currentFilter===999)d=d.filter(p=>p.data_gb>20);
    else d=d.filter(p=>p.data_gb<=currentFilter&&p.data_gb>0);
  }}
  return d;
}}
function sortBy(key){{
  if(currentSort===key)currentDir*=-1;
  else{{currentSort=key;currentDir=1;}}
  sortTable();
}}
function sortTable(){{
  currentSort=document.getElementById("sortSelect").value||currentSort;
  let data=getFiltered();
  data.sort((a,b)=>{{
    let va,vb;
    if(currentSort==="gb_price"){{va=getGbPrice(a);vb=getGbPrice(b);}}
    else if(currentSort==="price"||currentSort==="data_gb"){{va=a[currentSort];vb=b[currentSort];}}
    else{{va=a[currentSort]||"";vb=b[currentSort]||"";if(typeof va==="string")return va.localeCompare(vb)*currentDir;}}
    return(va-vb)*currentDir;
  }});
  renderTable(data);
}}
function filterData(f){{
  currentFilter=f;
  document.querySelectorAll(".chip").forEach(c=>c.classList.remove("active"));
  event.target.classList.add("active");
  sortTable();
}}
function renderTable(data){{
  const minGbPrice=Math.min(...data.filter(p=>p.price>0&&p.data_gb>0).map(p=>getGbPrice(p)));
  const minPrice=Math.min(...data.filter(p=>p.price>0).map(p=>p.price));
  const tbody=document.getElementById("tableBody");
  tbody.innerHTML=data.map(p=>{{
    const gbp=getGbPrice(p);
    const info=JSON.parse(p.data_json||"{{}}");
    const dataLabel=p.data_gb>=999?"無制限":p.data_gb+"GB";
    const gbLabel=p.data_gb>=999?"−":gbp+"円/GB";
    let badges="";
    if(p.price===minPrice&&p.price>0)badges+=`<span class="badge badge-best">最安</span> `;
    if(gbp===minGbPrice&&gbp<99999)badges+=`<span class="badge badge-good">GB単価最安</span> `;
    return`<tr>
      <td class="provider-name">${{p.provider}}</td>
      <td>${{p.plan_name}}</td>
      <td class="price">${{p.price.toLocaleString()}}円</td>
      <td>${{dataLabel}}</td>
      <td class="gb-price">${{gbLabel}}</td>
      <td style="text-align:left;font-size:.8rem">${{badges}}${{info.feature||""}}</td>
      <td><a href="#" class="btn-official">公式サイト</a></td>
    </tr>`;
  }}).join("");
}}
init();
</script>
</body>
</html>'''

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size = os.path.getsize(out_path)
    print(f"  Generated: {out_path}")
    print(f"  File size: {size:,} bytes")
    print(f"  Plans: {len(plans)}")

if __name__ == '__main__':
    print("=== SIM Comparison HTML Generator ===")
    generate()
    print("=== Done ===")
