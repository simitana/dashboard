
// ============================================
// SCRIPT AVANÇADO - GOOGLE SHEETS + SLIDES
// ============================================
// Cole em um Google Sheet para sincronizar com Slides

// DADOS ESTRUTURADOS
const DADOS_ACIDENTES = {
  kpis: [
    ["Total de Acidentes", 2963, 8.2, "Aumentou"],
    ["Óbitos", 73, -3.1, "Diminuiu"],
    ["Feridos Graves", 251, 2.8, "Aumentou"],
    ["Taxa de Severidade", 2.5, 0, "Estável"]
  ],

  tipos_acidentes: [
    ["Saída de Leito", 536, 28.0],
    ["Colisão Traseira", 413, 22.0],
    ["Colisão com Objeto", 384, 20.5],
    ["Capotamento", 313, 16.7],
    ["Colisão Frontal", 244, 13.0]
  ],

  causas: [
    ["Reação Tardia/Ineficiente", 420, 30.0],
    ["Velocidade Incompatível", 397, 28.4],
    ["Ausência de Reação", 272, 19.5],
    ["Acessar Via sem Observar", 173, 12.4],
    ["Ingestão de Álcool", 160, 11.5]
  ],

  estradas: [
    ["BR-277", 937, 3, 85, "CRÍTICO"],
    ["BR-376", 687, 2, 53, "ALERTA"],
    ["BR-116", 414, 12, 9, "ALERTA"],
    ["BR-369", 275, 26, 39, "CRÍTICO"],
    ["BR-476", 190, 5, 31, "NORMAL"]
  ],

  municipios: [
    ["GUARAPUAVA", 191, 6.4, 0],
    ["CAMPINA GRANDE DO SUL", 177, 6.0, 9],
    ["GUARATUBA", 164, 5.5, 0],
    ["CURITIBA", 153, 5.2, 0],
    ["PONTA GROSSA", 122, 4.1, 0]
  ]
};

// ============================================
// FUNÇÃO 1: CRIAR PLANILHA COM ABAS
// ============================================
function criarPlanilhaCompleta() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // LIMPAR ABAS EXISTENTES (exceto primeira)
  const sheets = ss.getSheets();
  for (let i = sheets.length - 1; i > 0; i--) {
    ss.deleteSheet(sheets[i]);
  }

  const sheetPrincipal = ss.getSheets()[0];
  sheetPrincipal.setName("🎯 Dashboard");

  // Aba 1: Dashboard
  preencherDashboard(sheetPrincipal);

  // Aba 2: Tipos de Acidentes
  const abaTipos = ss.insertSheet("📊 Tipos");
  preencherAbaTipos(abaTipos);

  // Aba 3: Causas
  const abaCausas = ss.insertSheet("⚠️ Causas");
  preencherAbaCausas(abaCausas);

  // Aba 4: Estradas
  const abaEstradas = ss.insertSheet("🛣️ Estradas");
  preencherAbaEstradas(abaEstradas);

  // Aba 5: Municípios
  const abaMunicipios = ss.insertSheet("📍 Municípios");
  preencherAbaMunicipios(abaMunicipios);

  Logger.log("✅ Planilha criada com sucesso!");
  Logger.log("URL: " + ss.getUrl());
}

// ============================================
// FUNÇÃO 2: PREENCHER DASHBOARD
// ============================================
function preencherDashboard(sheet) {
  sheet.getRange("A1:D10").clearContent();

  // Cabeçalho
  sheet.getRange("A1").setValue("📊 INDICADORES PRINCIPAIS - 2025");
  sheet.getRange("A1").setFontSize(14).setFontWeight("bold").setBackground("#F49539").setFontColor("white");
  sheet.mergeRange("A1:D1");

  // Dados de KPIs
  sheet.getRange("A3:D3").setValues([["Indicador", "Valor", "Mudança (%)", "Tendência"]]);
  sheet.getRange("A3:D3").setBackground("#1a2332").setFontColor("#F49539").setFontWeight("bold");

  DADOS_ACIDENTES.kpis.forEach((kpi, idx) => {
    const row = 4 + idx;
    sheet.getRange(`A${row}:D${row}`).setValues([kpi]);
  });

  // Formatar colunas
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);

  // SEÇÃO 2: TOTAIS
  const rowSeparador = 10;
  sheet.getRange(`A${rowSeparador}`).setValue("📈 RESUMO DE VÍTIMAS");
  sheet.getRange(`A${rowSeparador}`).setFontSize(12).setFontWeight("bold").setBackground("#01B27C").setFontColor("white");
  sheet.mergeRange(`A${rowSeparador}:D${rowSeparador}`);

  const totais = [
    ["Total de Vítimas", 2882],
    ["Feridos Leves", 1368],
    ["Ilesos", 1263],
    ["Óbitos", 73]
  ];

  totais.forEach((item, idx) => {
    const row = rowSeparador + 2 + idx;
    sheet.getRange(`A${row}:B${row}`).setValues([[item[0], item[1]]]);
  });
}

// ============================================
// FUNÇÃO 3: PREENCHER ABA TIPOS
// ============================================
function preencherAbaTipos(sheet) {
  sheet.getRange("A1:C1").setValues([["Tipo de Acidente", "Quantidade", "Percentual (%)"]]);
  sheet.getRange("A1:C1").setBackground("#F49539").setFontColor("white").setFontWeight("bold");

  DADOS_ACIDENTES.tipos_acidentes.forEach((tipo, idx) => {
    sheet.getRange(`A${idx + 2}:C${idx + 2}`).setValues([tipo]);
  });

  sheet.setColumnWidth(1, 250);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);

  // Adicionar gráfico
  const chart = sheet.newChart()
    .setChartType(Charts.ChartType.COLUMN)
    .addRange(sheet.getRange(`A1:C${DADOS_ACIDENTES.tipos_acidentes.length + 1}`))
    .setPosition(5, 1, 0, 0)
    .setOption('title', 'Tipos de Acidentes')
    .setOption('hAxis', { title: 'Tipo' })
    .setOption('vAxis', { title: 'Quantidade' })
    .build();

  sheet.insertChart(chart);
}

// ============================================
// FUNÇÃO 4: PREENCHER ABA CAUSAS
// ============================================
function preencherAbaCausas(sheet) {
  sheet.getRange("A1:C1").setValues([["Causa", "Quantidade", "Percentual (%)"]]);
  sheet.getRange("A1:C1").setBackground("#F49539").setFontColor("white").setFontWeight("bold");

  DADOS_ACIDENTES.causas.forEach((causa, idx) => {
    sheet.getRange(`A${idx + 2}:C${idx + 2}`).setValues([causa]);
  });

  sheet.setColumnWidth(1, 280);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);

  // Adicionar gráfico
  const chart = sheet.newChart()
    .setChartType(Charts.ChartType.BAR)
    .addRange(sheet.getRange(`A1:C${DADOS_ACIDENTES.causas.length + 1}`))
    .setPosition(5, 1, 0, 0)
    .setOption('title', 'Causas Principais')
    .setOption('hAxis', { title: 'Quantidade' })
    .setOption('vAxis', { title: 'Causa' })
    .build();

  sheet.insertChart(chart);
}

// ============================================
// FUNÇÃO 5: PREENCHER ABA ESTRADAS
// ============================================
function preencherAbaEstradas(sheet) {
  sheet.getRange("A1:E1").setValues([["Estrada", "Acidentes", "Óbitos", "Feridos", "Status"]]);
  sheet.getRange("A1:E1").setBackground("#F49539").setFontColor("white").setFontWeight("bold");

  DADOS_ACIDENTES.estradas.forEach((estrada, idx) => {
    sheet.getRange(`A${idx + 2}:E${idx + 2}`).setValues([estrada]);

    // Colorir status
    const statusCell = sheet.getRange(`E${idx + 2}`);
    if (estrada[4] === "CRÍTICO") {
      statusCell.setBackground("#F49539").setFontColor("white");
    } else if (estrada[4] === "ALERTA") {
      statusCell.setBackground("#FFA500").setFontColor("white");
    } else {
      statusCell.setBackground("#01B27C").setFontColor("white");
    }
  });

  sheet.setColumnWidth(1, 100);
  sheet.setColumnWidth(2, 120);
  sheet.setColumnWidth(3, 100);
  sheet.setColumnWidth(4, 100);
  sheet.setColumnWidth(5, 120);
}

// ============================================
// FUNÇÃO 6: PREENCHER ABA MUNICÍPIOS
// ============================================
function preencherAbaMunicipios(sheet) {
  sheet.getRange("A1:D1").setValues([["Município", "Acidentes", "Percentual (%)", "Óbitos"]]);
  sheet.getRange("A1:D1").setBackground("#F49539").setFontColor("white").setFontWeight("bold");

  DADOS_ACIDENTES.municipios.forEach((municipio, idx) => {
    sheet.getRange(`A${idx + 2}:D${idx + 2}`).setValues([municipio]);
  });

  sheet.setColumnWidth(1, 280);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 100);
}

// ============================================
// FUNÇÃO 7: EXPORTAR PARA PDF
// ============================================
function exportarPDF() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const url = ss.getUrl()
    .replace("/edit", "/export?format=pdf");

  Logger.log("📥 Link para PDF: " + url);
  Logger.log("Clique no link para baixar");
}

// ============================================
// MENU PERSONALIZADO
// ============================================
function onOpen() {
  const ui = SpreadsheetApp.getUi();

  ui.createMenu("📊 Acidentes 2025")
    .addItem("📋 Criar Planilha Completa", "criarPlanilhaCompleta")
    .addItem("📥 Exportar para PDF", "exportarPDF")
    .addSeparator()
    .addItem("🔍 Ver Dados no Console", "verDadosConsole")
    .addToUi();
}

// ============================================
// VER DADOS NO CONSOLE
// ============================================
function verDadosConsole() {
  Logger.clear();
  Logger.log("=== ACIDENTES DE TRÂNSITO 2025 ===");
  Logger.log("");
  Logger.log("✓ KPIs: " + DADOS_ACIDENTES.kpis.length);
  Logger.log("✓ Tipos de Acidentes: " + DADOS_ACIDENTES.tipos_acidentes.length);
  Logger.log("✓ Causas: " + DADOS_ACIDENTES.causas.length);
  Logger.log("✓ Estradas: " + DADOS_ACIDENTES.estradas.length);
  Logger.log("✓ Municípios: " + DADOS_ACIDENTES.municipios.length);
}
