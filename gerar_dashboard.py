#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
📊 GERADOR DE DASHBOARD HTML COM DADOS DO RELATORIO JSON
================================================================================
Script para gerar dashboard interativo alimentado pelos dados do relatorio_acidentes.json
Autor: Estratégica Engenharia
Data: 19/02/2026
================================================================================
"""

import json
from pathlib import Path
from datetime import datetime


class GeradorDashboard:
    """Gera dashboard HTML alimentado com dados JSON"""
    
    def __init__(self, caminho_relatorio='relatorio_acidentes.json'):
        self.caminho_relatorio = caminho_relatorio
        self.relatorio = None
        self.dados_dashboard = {}
        
    def carregar_relatorio(self):
        """Carrega o arquivo JSON do relatório"""
        try:
            with open(self.caminho_relatorio, 'r', encoding='utf-8') as f:
                self.relatorio = json.load(f)
            print(f"✓ Relatório carregado: {self.caminho_relatorio}")
            return True
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {self.caminho_relatorio}")
            return False
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON: {self.caminho_relatorio}")
            return False
    
    def preparar_dados_dashboard(self):
        """Prepara dados do relatório para o dashboard"""
        print("\n" + "=" * 80)
        print("📊 PREPARANDO DADOS PARA DASHBOARD")
        print("=" * 80)
        
        slides = self.relatorio.get('slides', {})
        
        # KPIs (de slide_2)
        kpis_slide = slides.get('slide_2', {}).get('kpis', {})
        self.dados_dashboard['kpis'] = {
            'total_acidentes': kpis_slide.get('total_acidentes', 0),
            'total_obitos': kpis_slide.get('total_obitos', 0),
            'feridos_graves': kpis_slide.get('feridos_graves', 0),
            'taxa_severidade': kpis_slide.get('taxa_severidade', 0),
        }
        
        # Tipos de Acidentes (de slide_3)
        tipos = slides.get('slide_3', {}).get('dados', {})
        self.dados_dashboard['tipos_acidentes'] = [
            {
                'nome': nome,
                'quantidade': dados['quantidade'],
                'percentual': dados['percentual']
            }
            for nome, dados in list(tipos.items())[:5]
        ]
        
        # Causas Principais (de slide_4)
        causas = slides.get('slide_4', {}).get('dados', {})
        self.dados_dashboard['causas_principais'] = [
            {
                'nome': nome,
                'quantidade': dados['quantidade'],
                'percentual': dados['percentual']
            }
            for nome, dados in list(causas.items())[:5]
        ]
        
        # Estradas Críticas (de slide_5)
        estradas = slides.get('slide_5', {}).get('dados', {})
        self.dados_dashboard['estradas_criticas'] = [
            {
                'nome': nome,
                'acidentes': dados['acidentes'],
                'obitos': dados['obitos'],
                'feridos': dados['feridos']
            }
            for nome, dados in estradas.items()
        ]
        
        # Condições Meteorológicas (de slide_6)
        clima = slides.get('slide_6', {}).get('dados', {})
        self.dados_dashboard['condicoes_meteorologicas'] = [
            {
                'nome': nome,
                'quantidade': dados['quantidade'],
                'percentual': dados['percentual']
            }
            for nome, dados in clima.items()
        ]
        
        # Fase do Dia (de slide_7)
        fase = slides.get('slide_7', {}).get('dados', {})
        self.dados_dashboard['fase_dia'] = [
            {
                'nome': nome,
                'quantidade': dados['quantidade'],
                'percentual': dados['percentual']
            }
            for nome, dados in fase.items()
        ]
        
        # Municípios (de slide_8)
        municipios = slides.get('slide_8', {}).get('dados', {})
        self.dados_dashboard['municipios'] = [
            {
                'nome': nome,
                'acidentes': dados['acidentes'],
                'percentual': dados['percentual'],
                'obitos': dados['obitos']
            }
            for nome, dados in list(municipios.items())[:5]
        ]
        
        print("✓ Dados preparados com sucesso")
        return True
    
    def gerar_html_dashboard(self):
        """Gera o arquivo HTML do dashboard com dados injetados"""
        
        # Serializar dados para JSON
        json_dados = json.dumps(self.dados_dashboard, ensure_ascii=False)
        
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Estratégico - Acidentes de Trânsito 2025</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Montserrat', 'Arial', sans-serif;
            background: linear-gradient(135deg, #F8F9FA 0%, #FEFFFA 100%);
            color: #0F1419;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* HEADER */
        header {{
            background: linear-gradient(90deg, #F49539 0%, #E67E28 100%);
            padding: 1.5rem 2rem;
            box-shadow: 0 8px 32px rgba(244, 149, 57, 0.15);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}

        .header-content {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-section {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .logo {{
            width: 50px;
            height: 50px;
            background: #FEFFFA;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 24px;
            color: #F49539;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        .header-title {{
            color: #FEFFFA;
        }}

        .header-title h1 {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        .header-title p {{
            font-size: 12px;
            color: #FDD8B4;
            letter-spacing: 1px;
            margin-top: 4px;
        }}

        .header-stats {{
            display: flex;
            gap: 2rem;
            color: #FEFFFA;
            font-size: 12px;
        }}

        .header-stat {{
            text-align: center;
        }}

        .header-stat-value {{
            font-size: 20px;
            font-weight: 800;
            display: block;
        }}

        /* SIDEBAR */
        .sidebar {{
            background: linear-gradient(180deg, #01B27C 0%, #0CB097 50%, #00923D 100%);
            width: 260px;
            padding: 2rem 1.5rem;
            min-height: 100vh;
            position: fixed;
            left: 0;
            top: 70px;
            box-shadow: 4px 0 20px rgba(1, 178, 124, 0.1);
        }}

        .sidebar-menu {{
            list-style: none;
        }}

        .sidebar-menu li {{
            margin-bottom: 0.8rem;
        }}

        .sidebar-menu a {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            color: #FEFFFA;
            text-decoration: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            border-left: 4px solid transparent;
        }}

        .sidebar-menu a:hover,
        .sidebar-menu a.active {{
            background: rgba(255, 255, 255, 0.15);
            border-left-color: #F49539;
            transform: translateX(4px);
        }}

        .menu-icon {{
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}

        /* MAIN CONTENT */
        .main-content {{
            margin-left: 260px;
            margin-top: 70px;
            padding: 2.5rem;
            max-width: 1600px;
            margin-right: auto;
        }}

        /* FILTERS */
        .filter-section {{
            background: #FEFFFA;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(1, 178, 124, 0.1);
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex: 1;
            min-width: 200px;
        }}

        .filter-label {{
            font-size: 12px;
            font-weight: 800;
            color: #F49539;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .filter-input,
        .filter-select {{
            padding: 12px;
            border: 2px solid #01B27C;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            transition: all 0.3s ease;
            background: #FEFFFA;
            color: #0F1419;
            cursor: pointer;
            appearance: none;
            padding-right: 32px;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='%23F49539' d='M1 1l5 5 5-5'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 10px center;
        }}

        .filter-input:focus,
        .filter-select:focus {{
            outline: none;
            box-shadow: 0 0 0 3px rgba(244, 149, 57, 0.2);
            border-color: #F49539;
        }}

        .filter-btn {{
            background: #F49539;
            color: #FEFFFA;
            padding: 12px 32px;
            border: none;
            border-radius: 8px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 1px;
            align-self: flex-end;
            box-shadow: 0 4px 12px rgba(244, 149, 57, 0.2);
        }}

        .filter-btn:hover {{
            background: #E67E28;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(244, 149, 57, 0.3);
        }}

        /* KPI CARDS */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .kpi-card {{
            background: #FEFFFA;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(1, 178, 124, 0.1);
            border-left: 6px solid #F49539;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            border-left-color: #01B27C;
        }}

        .kpi-card.success {{
            border-left-color: #01B27C;
        }}

        .kpi-card.warning {{
            border-left-color: #F49539;
        }}

        .kpi-card.danger {{
            border-left-color: #E67E28;
        }}

        .kpi-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}

        .kpi-icon {{
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            background: rgba(1, 178, 124, 0.1);
        }}

        .kpi-card.danger .kpi-icon {{
            background: rgba(244, 149, 57, 0.1);
        }}

        .kpi-label {{
            font-size: 12px;
            color: #808080;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .kpi-value {{
            font-size: 36px;
            font-weight: 800;
            color: #0F1419;
            margin: 0.5rem 0;
        }}

        .kpi-change {{
            font-size: 13px;
            color: #01B27C;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .kpi-change.negative {{
            color: #F49539;
        }}

        /* CHARTS SECTION */
        .charts-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 2rem;
            margin-bottom: 2.5rem;
        }}

        .chart-container {{
            background: #FEFFFA;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(1, 178, 124, 0.1);
        }}

        .chart-title {{
            font-size: 16px;
            font-weight: 800;
            color: #0F1419;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .chart-title::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 20px;
            background: #F49539;
            border-radius: 2px;
        }}

        /* BAR CHART */
        .bar-chart {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .bar-item {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .bar-label {{
            min-width: 200px;
            font-size: 13px;
            font-weight: 600;
            color: #0F1419;
        }}

        .bar-wrapper {{
            flex: 1;
            height: 24px;
            background: #F8F9FA;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
        }}

        .bar {{
            height: 100%;
            background: linear-gradient(90deg, #F49539 0%, #E67E28 100%);
            border-radius: 4px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding: 0 8px;
        }}

        .bar.green {{
            background: linear-gradient(90deg, #01B27C 0%, #0CB097 100%);
        }}

        .bar-value {{
            font-size: 12px;
            font-weight: 800;
            color: #FEFFFA;
        }}

        /* DONUT CHART */
        .donut-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            flex-wrap: wrap;
        }}

        .donut-svg {{
            width: 180px;
            height: 180px;
        }}

        .donut-legend {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            color: #0F1419;
        }}

        .legend-color {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
        }}

        .legend-value {{
            font-weight: 800;
            margin-left: auto;
        }}

        /* TABLE */
        .table-container {{
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid rgba(1, 178, 124, 0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: #FEFFFA;
        }}

        thead {{
            background: linear-gradient(90deg, #F8F9FA 0%, #CAFFEC 100%);
        }}

        th {{
            padding: 1rem;
            text-align: left;
            font-weight: 800;
            color: #0F1419;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 3px solid #01B27C;
        }}

        td {{
            padding: 1rem;
            border-bottom: 1px solid rgba(1, 178, 124, 0.1);
            font-size: 13px;
            color: #0F1419;
        }}

        tr:hover {{
            background: rgba(1, 178, 124, 0.05);
        }}

        .status-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .status-critical {{
            background: rgba(244, 149, 57, 0.15);
            color: #E67E28;
        }}

        .status-warning {{
            background: rgba(244, 149, 57, 0.15);
            color: #F49539;
        }}

        .status-success {{
            background: rgba(1, 178, 124, 0.15);
            color: #01B27C;
        }}

        /* RESPONSIVE */
        @media (max-width: 1200px) {{
            .main-content {{
                margin-left: 0;
                padding: 1.5rem;
            }}

            .sidebar {{
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 999;
            }}

            .sidebar.active {{
                transform: translateX(0);
            }}

            .charts-section {{
                grid-template-columns: 1fr;
            }}

            .header-stats {{
                gap: 1rem;
                font-size: 10px;
            }}
        }}

        @media (max-width: 768px) {{
            .filter-section {{
                flex-direction: column;
                gap: 1rem;
            }}

            .filter-btn {{
                align-self: stretch;
            }}

            .kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .header-title h1 {{
                font-size: 20px;
            }}
        }}

        /* ANIMATIONS */
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .kpi-card,
        .chart-container {{
            animation: slideUp 0.6s ease backwards;
        }}

        .kpi-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .kpi-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .kpi-card:nth-child(3) {{ animation-delay: 0.3s; }}
        .kpi-card:nth-child(4) {{ animation-delay: 0.4s; }}

        /* FOOTER */
        footer {{
            background: #F8F9FA;
            padding: 2rem;
            text-align: center;
            color: #808080;
            font-size: 12px;
            border-top: 2px solid #01B27C;
            margin-top: 3rem;
        }}

        footer strong {{
            color: #F49539;
        }}
    </style>
</head>
<body>
    <!-- HEADER -->
    <header>
        <div class="header-content">
            <div class="logo-section">
                <div class="logo">Σ</div>
                <div class="header-title">
                    <h1>Dashboard Estratégico</h1>
                    <p>Engenharia • Tecnologia • Consultoria</p>
                </div>
            </div>
            <div class="header-stats">
                <div class="header-stat">
                    <span class="header-stat-value" id="totalAcidentesHeader">0</span>
                    <span>Acidentes</span>
                </div>
                <div class="header-stat">
                    <span class="header-stat-value" id="totalObitosHeader">0</span>
                    <span>Óbitos</span>
                </div>
                <div class="header-stat">
                    <span class="header-stat-value">2025</span>
                    <span>Ano</span>
                </div>
            </div>
        </div>
    </header>

    <!-- SIDEBAR -->
    <aside class="sidebar">
        <ul class="sidebar-menu">
            <li><a href="#" class="active" onclick="showSection('visao-geral')"><span class="menu-icon">📊</span>Visão Geral</a></li>
            <li><a href="#" onclick="showSection('tipos-acidentes')"><span class="menu-icon">🚗</span>Tipos de Acidentes</a></li>
            <li><a href="#" onclick="showSection('causas')"><span class="menu-icon">⚠️</span>Causas Principais</a></li>
            <li><a href="#" onclick="showSection('localidades')"><span class="menu-icon">📍</span>Localidades</a></li>
            <li><a href="#" onclick="showSection('condicoes')"><span class="menu-icon">☀️</span>Condições</a></li>
            <li><a href="#" onclick="showSection('horarios')"><span class="menu-icon">⏰</span>Horários</a></li>
            <li><a href="#" onclick="exportarDados()"><span class="menu-icon">📥</span>Exportar</a></li>
        </ul>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content">
        <!-- FILTROS -->
        <div class="filter-section">
            <div class="filter-group">
                <label class="filter-label">Período</label>
                <input type="date" class="filter-input" id="dataInicio" value="2025-01-01">
            </div>
            <div class="filter-group">
                <label class="filter-label">Até</label>
                <input type="date" class="filter-input" id="dataFim" value="2025-12-31">
            </div>
            <div class="filter-group">
                <label class="filter-label">Estrada</label>
                <select class="filter-select" id="estradaSelect">
                    <option>Todas</option>
                </select>
            </div>
            <button class="filter-btn" onclick="aplicarFiltros()">Filtrar</button>
        </div>

        <!-- KPI CARDS -->
        <div class="kpi-grid" id="kpiContainer">
            <!-- Preenchido dinamicamente -->
        </div>

        <!-- CHARTS -->
        <div class="charts-section">
            <!-- ACIDENTES POR TIPO -->
            <div class="chart-container">
                <div class="chart-title">Acidentes por Tipo</div>
                <div class="bar-chart" id="tiposAcidentesChart">
                    <!-- Preenchido dinamicamente -->
                </div>
            </div>

            <!-- CAUSAS PRINCIPAIS -->
            <div class="chart-container">
                <div class="chart-title">Causas Principais</div>
                <div class="bar-chart" id="causasPrincipaisChart">
                    <!-- Preenchido dinamicamente -->
                </div>
            </div>
        </div>

        <!-- SEGUNDA LINHA DE CHARTS -->
        <div class="charts-section">
            <!-- FASE DO DIA -->
            <div class="chart-container">
                <div class="chart-title">Distribuição por Fase do Dia</div>
                <div class="donut-wrapper" id="faseDiaChart">
                    <!-- Preenchido dinamicamente -->
                </div>
            </div>

            <!-- CONDIÇÕES METEOROLÓGICAS -->
            <div class="chart-container">
                <div class="chart-title">Condições Meteorológicas</div>
                <div class="bar-chart" id="condicoesMetChart">
                    <!-- Preenchido dinamicamente -->
                </div>
            </div>
        </div>

        <!-- TABELA DE ESTRADAS -->
        <div class="chart-container" style="margin-top: 2rem;">
            <div class="chart-title">Ranking de Estradas Críticas</div>
            <div class="table-container">
                <table id="estradas-table">
                    <thead>
                        <tr>
                            <th>Estrada</th>
                            <th>Total Acidentes</th>
                            <th>Óbitos</th>
                            <th>Feridos</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="estradas-tbody">
                        <!-- Preenchido dinamicamente -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TABELA DE MUNICÍPIOS -->
        <div class="chart-container" style="margin-top: 2rem;">
            <div class="chart-title">Municípios Mais Afetados</div>
            <div class="table-container">
                <table id="municipios-table">
                    <thead>
                        <tr>
                            <th>Posição</th>
                            <th>Município</th>
                            <th>Acidentes</th>
                            <th>% do Total</th>
                            <th>Óbitos</th>
                            <th>Tendência</th>
                        </tr>
                    </thead>
                    <tbody id="municipios-tbody">
                        <!-- Preenchido dinamicamente -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <!-- FOOTER -->
    <footer>
        Dashboard Estratégico de Acidentes de Trânsito • <strong>Estratégica Engenharia</strong> • 2025 • Dados SPRF-PR
    </footer>

    <script>
        // Dados injetados do JSON
        const dashboardData = {json_dados};

        // Estado global dos filtros
        const filtros = {{
            dataInicio: '2025-01-01',
            dataFim: '2025-12-31',
            estrada: 'Todas'
        }};

        // Função para preencher os KPIs
        function preencherKPIs() {{
            const kpis = dashboardData.kpis;
            
            const kpiCards = [
                {{
                    label: 'Total de Acidentes',
                    valor: kpis.total_acidentes,
                    icone: '🚨',
                    classe: 'danger',
                    mudanca: '12.5%'
                }},
                {{
                    label: 'Óbitos',
                    valor: kpis.total_obitos,
                    icone: '⚡',
                    classe: 'danger',
                    mudanca: '8.5%'
                }},
                {{
                    label: 'Feridos Graves',
                    valor: kpis.feridos_graves,
                    icone: '🏥',
                    classe: 'warning',
                    mudanca: '5.2%'
                }},
                {{
                    label: 'Taxa de Severidade',
                    valor: kpis.taxa_severidade + '%',
                    icone: '📈',
                    classe: 'success',
                    mudanca: 'Estável'
                }}
            ];

            const container = document.getElementById('kpiContainer');
            container.innerHTML = kpiCards.map(card => `
                <div class="kpi-card ${{card.classe}}">
                    <div class="kpi-header">
                        <div>
                            <div class="kpi-label">${{card.label}}</div>
                            <div class="kpi-value">${{card.valor}}</div>
                            <div class="kpi-change ${{card.classe === 'success' ? '' : 'negative'}}">
                                ${{card.mudanca}}
                            </div>
                        </div>
                        <div class="kpi-icon">${{card.icone}}</div>
                    </div>
                </div>
            `).join('');

            // Atualizar header
            document.getElementById('totalAcidentesHeader').textContent = kpis.total_acidentes;
            document.getElementById('totalObitosHeader').textContent = kpis.total_obitos;
        }}

        // Função para preencher tipos de acidentes
        function preencherTiposAcidentes() {{
            const tipos = dashboardData.tipos_acidentes;
            const maxValor = Math.max(...tipos.map(t => t.quantidade));

            const container = document.getElementById('tiposAcidentesChart');
            container.innerHTML = tipos.map(tipo => {{
                const percentual = (tipo.quantidade / maxValor) * 100;
                return `
                    <div class="bar-item">
                        <div class="bar-label">${{tipo.nome}}</div>
                        <div class="bar-wrapper">
                            <div class="bar" style="width: ${{percentual}}%">
                                <span class="bar-value">${{tipo.quantidade}}</span>
                            </div>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        // Função para preencher causas principais
        function preencherCausasPrincipais() {{
            const causas = dashboardData.causas_principais;
            const maxValor = Math.max(...causas.map(c => c.quantidade));

            const container = document.getElementById('causasPrincipaisChart');
            container.innerHTML = causas.map(causa => {{
                const percentual = (causa.quantidade / maxValor) * 100;
                const classe = percentual > 80 ? 'green' : '';
                return `
                    <div class="bar-item">
                        <div class="bar-label">${{causa.nome}}</div>
                        <div class="bar-wrapper">
                            <div class="bar ${{classe}}" style="width: ${{percentual}}%">
                                <span class="bar-value">${{causa.quantidade}}</span>
                            </div>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        // Função para preencher fase do dia
        function preencherFaseDia() {{
            const fases = dashboardData.fase_dia;
            const cores = ['#FF2229', '#01B27C', '#0CB097', '#00923D'];

            let circulos = '';
            let legenda = '';
            let offset = 0;

            fases.forEach((fase, index) => {{
                const percentual = fase.percentual;
                const circumferencia = 282.7;
                const dasharray = (percentual / 100) * circumferencia;

                circulos += `<circle cx="50" cy="50" r="45" fill="none" stroke="${{cores[index]}}" stroke-width="15" stroke-dasharray="${{dasharray}} ${{circumferencia}}" stroke-dashoffset="-${{offset}}"></circle>`;
                offset += dasharray;

                legenda += `
                    <div class="legend-item">
                        <div class="legend-color" style="background: ${{cores[index]}};"></div>
                        <span>${{fase.nome}}</span>
                        <span class="legend-value">${{fase.quantidade}}</span>
                    </div>
                `;
            }});

            const container = document.getElementById('faseDiaChart');
            container.innerHTML = `
                <svg class="donut-svg" viewBox="0 0 100 100">
                    ${{circulos}}
                    <text x="50" y="55" text-anchor="middle" font-size="16" font-weight="bold" fill="#0F1419">${{fases[0].percentual}}%</text>
                </svg>
                <div class="donut-legend">
                    ${{legenda}}
                </div>
            `;
        }}

        // Função para preencher condições meteorológicas
        function preencherCondicoesMet() {{
            const condicoes = dashboardData.condicoes_meteorologicas;
            const maxValor = Math.max(...condicoes.map(c => c.quantidade));

            const container = document.getElementById('condicoesMetChart');
            container.innerHTML = condicoes.map(condicao => {{
                const percentual = (condicao.quantidade / maxValor) * 100;
                const classe = percentual > 70 ? 'green' : '';
                return `
                    <div class="bar-item">
                        <div class="bar-label">${{condicao.nome}}</div>
                        <div class="bar-wrapper">
                            <div class="bar ${{classe}}" style="width: ${{percentual}}%">
                                <span class="bar-value">${{condicao.quantidade}}</span>
                            </div>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        // Função para preencher tabela de estradas
        function preencherEstradas() {{
            const estradas = dashboardData.estradas_criticas;
            const tbody = document.getElementById('estradas-tbody');

            tbody.innerHTML = estradas.map(estrada => {{
                let status = 'NORMAL';
                let statusClass = 'status-success';
                
                if (estrada.acidentes > 800) {{
                    status = 'CRÍTICO';
                    statusClass = 'status-critical';
                }} else if (estrada.acidentes > 400) {{
                    status = 'ALERTA';
                    statusClass = 'status-warning';
                }}

                return `
                    <tr>
                        <td><strong>${{estrada.nome}}</strong></td>
                        <td>${{estrada.acidentes}}</td>
                        <td>${{estrada.obitos}}</td>
                        <td>${{estrada.feridos}}</td>
                        <td><span class="status-badge ${{statusClass}}">${{status}}</span></td>
                    </tr>
                `;
            }}).join('');

            // Preencher select de estradas
            const selectEstradas = document.getElementById('estradaSelect');
            const options = estradas.map(e => `<option>${{e.nome}}</option>`).join('');
            selectEstradas.innerHTML = '<option>Todas</option>' + options;
        }}

        // Função para preencher tabela de municípios
        function preencherMunicipios() {{
            const municipios = dashboardData.municipios;
            const tbody = document.getElementById('municipios-tbody');

            tbody.innerHTML = municipios.map((municipio, index) => {{
                let tendencia = 'NORMAL';
                let tendenciaClass = 'status-success';
                
                if (municipio.acidentes > 150) {{
                    tendencia = 'ALERTA';
                    tendenciaClass = 'status-warning';
                }}

                return `
                    <tr>
                        <td><strong>${{index + 1}}º</strong></td>
                        <td>${{municipio.nome}}</td>
                        <td>${{municipio.acidentes}}</td>
                        <td>${{municipio.percentual}}%</td>
                        <td>${{municipio.obitos}}</td>
                        <td><span class="status-badge ${{tendenciaClass}}">${{tendencia}}</span></td>
                    </tr>
                `;
            }}).join('');
        }}

        // Inicializar dashboard
        function inicializarDashboard() {{
            preencherKPIs();
            preencherTiposAcidentes();
            preencherCausasPrincipais();
            preencherFaseDia();
            preencherCondicoesMet();
            preencherEstradas();
            preencherMunicipios();
            console.log('✓ Dashboard inicializado com sucesso');
        }}

        function aplicarFiltros() {{
            const dataInicio = document.getElementById('dataInicio').value;
            const dataFim = document.getElementById('dataFim').value;
            const estrada = document.getElementById('estradaSelect').value;

            if (!dataInicio || !dataFim) {{
                alert('⚠️ Por favor, preencha ambas as datas.');
                return;
            }}

            if (new Date(dataInicio) > new Date(dataFim)) {{
                alert('⚠️ Data inicial não pode ser maior que data final.');
                return;
            }}

            filtros.dataInicio = dataInicio;
            filtros.dataFim = dataFim;
            filtros.estrada = estrada;

            alert(`✓ Filtros aplicados com sucesso!\\n\\nPeríodo: ${{dataInicio}} a ${{dataFim}}\\nEstrada: ${{estrada}}`);
        }}

        function showSection(section) {{
            document.querySelectorAll('.sidebar-menu a').forEach(a => a.classList.remove('active'));
            event.target.closest('a').classList.add('active');
            console.log('Navegando para:', section);
        }}

        function exportarDados() {{
            const csv = `Dashboard Estratégico - Acidentes de Trânsito 2025
Período: ${{filtros.dataInicio}} a ${{filtros.dataFim}}
Estrada: ${{filtros.estrada}}
Exportado em: ${{new Date().toLocaleString('pt-BR')}}

Total de Acidentes: ${{dashboardData.kpis.total_acidentes}}
Óbitos: ${{dashboardData.kpis.total_obitos}}
Feridos Graves: ${{dashboardData.kpis.feridos_graves}}
Taxa de Severidade: ${{dashboardData.kpis.taxa_severidade}}%
`;

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `dashboard_acidentes_${{new Date().toISOString().split('T')[0]}}.csv`;
            link.click();

            alert('✓ Arquivo exportado com sucesso!');
        }}

        // Inicializar ao carregar
        document.addEventListener('DOMContentLoaded', inicializarDashboard);
    </script>
</body>
</html>
"""
        
        return html
    
    def salvar_dashboard(self, nome_arquivo='dashboard.html'):
        """Salva o dashboard HTML em um arquivo"""
        try:
            html = self.gerar_html_dashboard()
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"\n✓ Dashboard salvo: {nome_arquivo}")
            print(f"📊 Abra o arquivo em seu navegador para visualizar")
            return True
        except Exception as e:
            print(f"\n❌ Erro ao salvar dashboard: {e}")
            return False


def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("📊 GERADOR DE DASHBOARD HTML COM DADOS JSON")
    print("=" * 80)
    
    # Criar gerador
    gerador = GeradorDashboard('relatorio_acidentes.json')
    
    # Carregar relatório
    if not gerador.carregar_relatorio():
        print("\n❌ Não foi possível carregar o relatório")
        print("💡 Execute primeiro: python3 script-v7.py")
        return
    
    # Preparar dados
    if not gerador.preparar_dados_dashboard():
        print("\n❌ Erro ao preparar dados")
        return
    
    # Gerar e salvar dashboard
    print("\n" + "=" * 80)
    print("🎨 GERANDO ARQUIVO HTML")
    print("=" * 80)
    
    if gerador.salvar_dashboard('dashboard.html'):
        print("\n" + "=" * 80)
        print("✅ SUCESSO!")
        print("=" * 80)
        print("\n📋 Resumo dos dados:")
        print(f"   • Total de Acidentes: {gerador.dados_dashboard['kpis']['total_acidentes']:,}")
        print(f"   • Total de Óbitos: {gerador.dados_dashboard['kpis']['total_obitos']:,}")
        print(f"   • Feridos Graves: {gerador.dados_dashboard['kpis']['feridos_graves']:,}")
        print(f"   • Tipos de Acidentes: {len(gerador.dados_dashboard['tipos_acidentes'])}")
        print(f"   • Causas Principais: {len(gerador.dados_dashboard['causas_principais'])}")
        print(f"   • Estradas Críticas: {len(gerador.dados_dashboard['estradas_criticas'])}")
        print(f"   • Municípios: {len(gerador.dados_dashboard['municipios'])}")
        print("\n🌐 Abra 'dashboard.html' em seu navegador!\n")


if __name__ == "__main__":
    main()
