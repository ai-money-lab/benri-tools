/**
 * Google Apps Script — 家賃診断データをJSON化する
 *
 * このスクリプトをGoogle Formsの回答先スプレッドシートの
 * Apps Scriptエディタに貼り付けて使用する。
 *
 * 使い方:
 * 1. スプレッドシート → 拡張機能 → Apps Script
 * 2. このコードを貼り付けて保存
 * 3. exportToJSON を一度手動実行（認証許可）
 * 4. トリガー設定: 週次で exportToJSON を実行
 */

// ============ 設定 ============
const SHEET_NAME = 'フォームの回答 1'; // デフォルトのシート名
const COLUMNS = {
  timestamp: 0,
  area: 1,
  rent: 2,
  age: 3,
  income: 4,
  family: 5,
  satisfaction: 6,
  priority: 7,
  score: 8,
  rentRatio: 9
};

// ============ メイン関数 ============

/**
 * スプレッドシートのデータをJSON形式でエクスポート
 * Web App として公開するとURLでアクセス可能
 */
function doGet(e) {
  const data = getFormData();
  return ContentService
    .createTextOutput(JSON.stringify(data, null, 2))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * フォームデータを取得して整形
 */
function getFormData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_NAME);

  if (!sheet) {
    return { error: 'Sheet not found', entries: [], summary: {} };
  }

  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const rows = data.slice(1);

  const entries = rows.map((row, idx) => ({
    id: idx + 1,
    timestamp: row[COLUMNS.timestamp] ? new Date(row[COLUMNS.timestamp]).toISOString() : '',
    area: String(row[COLUMNS.area] || ''),
    rent: parseInt(row[COLUMNS.rent]) || 0,
    age: String(row[COLUMNS.age] || ''),
    income: String(row[COLUMNS.income] || ''),
    family: String(row[COLUMNS.family] || ''),
    satisfaction: String(row[COLUMNS.satisfaction] || ''),
    priority: String(row[COLUMNS.priority] || ''),
    score: parseInt(row[COLUMNS.score]) || 0,
    rentRatio: parseFloat(row[COLUMNS.rentRatio]) || 0
  })).filter(e => e.area && e.rent > 0);

  const summary = generateSummary(entries);

  return {
    lastUpdated: new Date().toISOString(),
    totalEntries: entries.length,
    entries: entries,
    summary: summary
  };
}

/**
 * サマリーデータを生成
 */
function generateSummary(entries) {
  if (entries.length === 0) return {};

  // エリア別集計
  const byArea = {};
  entries.forEach(e => {
    if (!byArea[e.area]) byArea[e.area] = { count: 0, totalRent: 0, rents: [] };
    byArea[e.area].count++;
    byArea[e.area].totalRent += e.rent;
    byArea[e.area].rents.push(e.rent);
  });

  Object.keys(byArea).forEach(area => {
    const d = byArea[area];
    d.avgRent = Math.round(d.totalRent / d.count);
    d.rents.sort((a, b) => a - b);
    d.medianRent = d.rents[Math.floor(d.rents.length / 2)];
    d.minRent = d.rents[0];
    d.maxRent = d.rents[d.rents.length - 1];
    delete d.rents;
    delete d.totalRent;
  });

  // 年代別集計
  const byAge = {};
  entries.forEach(e => {
    if (!byAge[e.age]) byAge[e.age] = { count: 0, totalRent: 0 };
    byAge[e.age].count++;
    byAge[e.age].totalRent += e.rent;
  });
  Object.keys(byAge).forEach(age => {
    byAge[age].avgRent = Math.round(byAge[age].totalRent / byAge[age].count);
    delete byAge[age].totalRent;
  });

  // 満足度集計
  const bySatisfaction = {};
  entries.forEach(e => {
    if (!bySatisfaction[e.satisfaction]) bySatisfaction[e.satisfaction] = 0;
    bySatisfaction[e.satisfaction]++;
  });

  // 全体平均
  const allRents = entries.map(e => e.rent);
  const avgRent = Math.round(allRents.reduce((a, b) => a + b, 0) / allRents.length);
  const avgScore = Math.round(entries.map(e => e.score).reduce((a, b) => a + b, 0) / entries.length);
  const avgRatio = (entries.map(e => e.rentRatio).reduce((a, b) => a + b, 0) / entries.length).toFixed(1);

  return {
    totalResponses: entries.length,
    averageRent: avgRent,
    averageScore: avgScore,
    averageRentRatio: parseFloat(avgRatio),
    byArea: byArea,
    byAge: byAge,
    bySatisfaction: bySatisfaction
  };
}

/**
 * 手動エクスポート用 — ログに出力
 */
function exportToJSON() {
  const data = getFormData();
  Logger.log(JSON.stringify(data, null, 2));
  Logger.log('Total entries: ' + data.totalEntries);
}
