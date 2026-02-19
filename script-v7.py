#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
🚀 EXTRATOR CSV ROBUSTO → APRESENTAÇÃO DE ACIDENTES DE TRÂNSITO
================================================================================
Script para processar CSV de acidentes e gerar dados para apresentação
Autor: Estratégica Engenharia
Data: 13/02/2026
================================================================================
"""

import pandas as pd
import csv
import json
from pathlib import Path
from datetime import datetime
import sys

class CSVtoApresentacao:
    """Converte CSV de acidentes em dados estruturados para slides"""
    
    def __init__(self, caminho_csv):
        self.caminho_csv = caminho_csv
        self.df = None
        self.delimitador = None
        self.data_extracao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    def detectar_delimitador(self):
        """Detecta automaticamente o delimitador do CSV"""
        try:
            with open(self.caminho_csv, 'r', encoding='utf-8') as f:
                primeira_linha = f.readline()
            
            # Testar delimitadores comuns
            if ';' in primeira_linha:
                self.delimitador = ';'
            elif ',' in primeira_linha:
                self.delimitador = ','
            elif '\t' in primeira_linha:
                self.delimitador = '\t'
            else:
                self.delimitador = ','
            
            return self.delimitador
        except Exception as e:
            print(f"⚠️  Erro ao detectar delimitador: {e}")
            self.delimitador = ';'
            return ';'
    
    def carregar_csv(self):
        """Carrega CSV com tratamento robusto de erros"""
        delim = self.detectar_delimitador()
        
        print(f"\n📂 Carregando CSV com delimitador: '{delim}'")
        print(f"   Caminho: {self.caminho_csv}")
        
        # Estratégia 1: Pandas com on_bad_lines='skip'
        try:
            self.df = pd.read_csv(
                self.caminho_csv,
                delimiter=delim,
                encoding='utf-8',
                on_bad_lines='skip',
                engine='python'
            )
            print(f"✓ Carregado com sucesso: {len(self.df):,} registros\n")
            return True
            
        except UnicodeDecodeError:
            print("⚠️  Erro de encoding UTF-8, tentando latin-1...")
            try:
                self.df = pd.read_csv(
                    self.caminho_csv,
                    delimiter=delim,
                    encoding='latin-1',
                    on_bad_lines='skip',
                    engine='python'
                )
                print(f"✓ Carregado com encoding latin-1: {len(self.df):,} registros\n")
                return True
            except Exception as e:
                print(f"❌ Erro ao carregar: {e}\n")
                return False
        
        except Exception as e:
            print(f"❌ Erro ao carregar: {e}\n")
            return False
    
    def calcular_kpis(self):
        """Calcula indicadores principais (KPIs)"""
        print("=" * 80)
        print("📊 CALCULANDO KPIs")
        print("=" * 80 + "\n")
        
        kpis = {
            "total_acidentes": len(self.df),
            "total_obitos": int(self.df['mortos'].sum()) if 'mortos' in self.df.columns else 0,
            "feridos_graves": int(self.df['feridos_graves'].sum()) if 'feridos_graves' in self.df.columns else 0,
            "feridos_leves": int(self.df['feridos_leves'].sum()) if 'feridos_leves' in self.df.columns else 0,
            "ilesos": int(self.df['ilesos'].sum()) if 'ilesos' in self.df.columns else 0,
        }
        
        # Calcular taxa de severidade (% de acidentes com morte)
        if kpis["total_acidentes"] > 0:
            kpis["taxa_severidade"] = round((kpis["total_obitos"] / kpis["total_acidentes"]) * 100, 1)
        else:
            kpis["taxa_severidade"] = 0
        
        # Total de vítimas
        kpis["total_vitimas"] = kpis["feridos_graves"] + kpis["feridos_leves"] + kpis["ilesos"]
        
        # Taxa de mortalidade (% de mortes entre vítimas)
        if kpis["total_vitimas"] > 0:
            kpis["taxa_mortalidade"] = round((kpis["total_obitos"] / kpis["total_vitimas"]) * 100, 1)
        else:
            kpis["taxa_mortalidade"] = 0
        
        print(f"Total de Acidentes: {kpis['total_acidentes']:,}")
        print(f"Óbitos: {kpis['total_obitos']:,}")
        print(f"Feridos Graves: {kpis['feridos_graves']:,}")
        print(f"Feridos Leves: {kpis['feridos_leves']:,}")
        print(f"Ilesos: {kpis['ilesos']:,}")
        print(f"Total de Vítimas: {kpis['total_vitimas']:,}")
        print(f"Taxa de Severidade: {kpis['taxa_severidade']:.1f}%")
        print(f"Taxa de Mortalidade: {kpis['taxa_mortalidade']:.1f}%\n")
        
        return kpis
    
    def analisar_tipos_acidentes(self):
        """Analisa tipos de acidentes"""
        print("=" * 80)
        print("🚗 TIPOS DE ACIDENTES")
        print("=" * 80 + "\n")
        
        if 'tipo_acidente' not in self.df.columns:
            print("⚠️  Coluna 'tipo_acidente' não encontrada\n")
            return {}
        
        tipos = self.df['tipo_acidente'].value_counts().head(5)
        total = tipos.sum()
        
        resultado = {}
        for i, (tipo, qtd) in enumerate(tipos.items(), 1):
            percentual = round((qtd / total) * 100, 0)
            resultado[tipo] = {"quantidade": int(qtd), "percentual": int(percentual)}
            print(f"{i}. {tipo}: {int(qtd)} ({percentual:.0f}%)")
        
        print()
        return resultado
    
    def analisar_causas(self):
        """Analisa causas principais"""
        print("=" * 80)
        print("⚠️  CAUSAS PRINCIPAIS")
        print("=" * 80 + "\n")
        
        if 'causa_acidente' not in self.df.columns:
            print("⚠️  Coluna 'causa_acidente' não encontrada\n")
            return {}
        
        causas = self.df['causa_acidente'].value_counts().head(5)
        total = causas.sum()
        
        resultado = {}
        for i, (causa, qtd) in enumerate(causas.items(), 1):
            percentual = round((qtd / total) * 100, 0)
            resultado[causa] = {"quantidade": int(qtd), "percentual": int(percentual)}
            print(f"{i}. {causa}: {int(qtd)} ({percentual:.0f}%)")
        
        print()
        return resultado
    
    def analisar_estradas(self):
        """Analisa estradas críticas"""
        print("=" * 80)
        print("🛣️  ESTRADAS CRÍTICAS")
        print("=" * 80 + "\n")
        
        if 'br' not in self.df.columns:
            print("⚠️  Coluna 'br' não encontrada\n")
            return {}
        
        try:
            estradas_data = self.df.groupby('br').agg({
                'id': 'count',
                'mortos': 'sum' if 'mortos' in self.df.columns else lambda x: 0,
                'feridos_graves': 'sum' if 'feridos_graves' in self.df.columns else lambda x: 0,
            }).rename(columns={'id': 'acidentes'}).sort_values('acidentes', ascending=False).head(5)
            
            resultado = {}
            for i, (estrada, row) in enumerate(estradas_data.iterrows(), 1):
                estrada_nome = f"BR-{int(estrada)}" if isinstance(estrada, (int, float)) else str(estrada)
                resultado[estrada_nome] = {
                    "acidentes": int(row['acidentes']),
                    "obitos": int(row['mortos']),
                    "feridos": int(row['feridos_graves'])
                }
                print(f"{i}. {estrada_nome}: {int(row['acidentes'])} acidentes, " +
                      f"{int(row['mortos'])} óbitos, {int(row['feridos_graves'])} feridos")
            
            print()
            return resultado
        except Exception as e:
            print(f"Erro ao analisar estradas: {e}\n")
            return {}
    
    def analisar_clima(self):
        """Analisa condições meteorológicas"""
        print("=" * 80)
        print("☀️  CONDIÇÕES METEOROLÓGICAS")
        print("=" * 80 + "\n")
        
        if 'condicao_metereologica' not in self.df.columns:
            print("⚠️  Coluna 'condicao_metereologica' não encontrada\n")
            return {}
        
        clima = self.df['condicao_metereologica'].value_counts().head(4)
        total = clima.sum()
        
        resultado = {}
        for i, (condicao, qtd) in enumerate(clima.items(), 1):
            percentual = round((qtd / total) * 100, 0)
            resultado[condicao] = {"quantidade": int(qtd), "percentual": int(percentual)}
            print(f"{i}. {condicao}: {int(qtd)} ({percentual:.0f}%)")
        
        print()
        return resultado
    
    def analisar_fase_dia(self):
        """Analisa fase do dia"""
        print("=" * 80)
        print("⏰ FASE DO DIA")
        print("=" * 80 + "\n")
        
        if 'fase_dia' not in self.df.columns:
            print("⚠️  Coluna 'fase_dia' não encontrada\n")
            return {}
        
        fase = self.df['fase_dia'].value_counts()
        total = fase.sum()
        
        resultado = {}
        for periodo, qtd in fase.items():
            percentual = round((qtd / total) * 100, 0)
            resultado[periodo] = {"quantidade": int(qtd), "percentual": int(percentual)}
            print(f"• {periodo}: {int(qtd)} ({percentual:.0f}%)")
        
        print()
        return resultado
    
    def analisar_municipios(self):
        """Analisa municípios mais afetados"""
        print("=" * 80)
        print("📍 MUNICÍPIOS MAIS AFETADOS")
        print("=" * 80 + "\n")
        
        if 'municipio' not in self.df.columns:
            print("⚠️  Coluna 'municipio' não encontrada\n")
            return {}
        
        try:
            municipios_data = self.df.groupby('municipio').agg({
                'id': 'count',
                'mortos': 'sum' if 'mortos' in self.df.columns else lambda x: 0,
            }).rename(columns={'id': 'acidentes'}).sort_values('acidentes', ascending=False).head(5)
            
            total_geral = len(self.df)
            resultado = {}
            for i, (municipio, row) in enumerate(municipios_data.iterrows(), 1):
                percentual = round((row['acidentes'] / total_geral) * 100, 1)
                resultado[municipio] = {
                    "acidentes": int(row['acidentes']),
                    "percentual": percentual,
                    "obitos": int(row['mortos'])
                }
                print(f"{i}. {municipio}: {int(row['acidentes'])} acidentes ({percentual:.1f}%), " +
                      f"{int(row['mortos'])} óbitos")
            
            print()
            return resultado
        except Exception as e:
            print(f"Erro ao analisar municípios: {e}\n")
            return {}
    
    def gerar_relatorio(self):
        """Gera relatório estruturado completo"""
        print("\n" + "=" * 80)
        print("🎯 GERANDO RELATÓRIO COMPLETO")
        print("=" * 80 + "\n")
        
        relatorio = {
            "data_extracao": self.data_extracao,
            "arquivo": str(self.caminho_csv),
            "total_registros": len(self.df),
            "colunas": list(self.df.columns),
            "slides": {}
        }
        
        # SLIDE 1: TÍTULO
        relatorio["slides"]["slide_1"] = {
            "nome": "Título",
            "titulo": "Acidentes de Trânsito",
            "subtitulo": "Análise Completa 2025",
            "rodape": "Estratégica Engenharia • Dados SPRF-PR"
        }
        
        # SLIDE 2: KPIs
        relatorio["slides"]["slide_2"] = {
            "nome": "Indicadores Principais",
            "kpis": self.calcular_kpis()
        }
        
        # SLIDE 3: Tipos de Acidentes
        relatorio["slides"]["slide_3"] = {
            "nome": "Tipos de Acidentes",
            "dados": self.analisar_tipos_acidentes()
        }
        
        # SLIDE 4: Causas
        relatorio["slides"]["slide_4"] = {
            "nome": "Causas Principais",
            "dados": self.analisar_causas()
        }
        
        # SLIDE 5: Estradas
        relatorio["slides"]["slide_5"] = {
            "nome": "Estradas Críticas",
            "dados": self.analisar_estradas()
        }
        
        # SLIDE 6: Clima
        relatorio["slides"]["slide_6"] = {
            "nome": "Condições Meteorológicas",
            "dados": self.analisar_clima()
        }
        
        # SLIDE 7: Fase do Dia
        relatorio["slides"]["slide_7"] = {
            "nome": "Distribuição por Fase do Dia",
            "dados": self.analisar_fase_dia()
        }
        
        # SLIDE 8: Municípios
        relatorio["slides"]["slide_8"] = {
            "nome": "Municípios Mais Afetados",
            "dados": self.analisar_municipios()
        }
        
        return relatorio


def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("🚀 INICIANDO PROCESSAMENTO CSV → APRESENTAÇÃO")
    print("=" * 80)
    
    # Detectar arquivo CSV no diretório atual
    arquivos_csv = list(Path('.').glob('*.csv'))
    
    if not arquivos_csv:
        print("\n❌ Nenhum arquivo CSV encontrado no diretório atual")
        print("📁 Coloque um arquivo .csv na mesma pasta deste script")
        sys.exit(1)
    
    caminho_csv = str(arquivos_csv[0])
    print(f"\n📂 CSV encontrado: {caminho_csv}")
    
    # Processar
    processador = CSVtoApresentacao(caminho_csv)
    
    if not processador.carregar_csv():
        sys.exit(1)
    
    # Gerar relatório
    relatorio = processador.gerar_relatorio()
    
    # Exibir resumo
    print("=" * 80)
    print("✅ RELATÓRIO GERADO COM SUCESSO")
    print("=" * 80)
    print(f"\nData de Extração: {relatorio['data_extracao']}")
    print(f"Arquivo: {relatorio['arquivo']}")
    print(f"Total de Registros: {relatorio['total_registros']:,}")
    print(f"Slides Gerados: {len(relatorio['slides'])}")
    print(f"\nColunas Disponíveis ({len(relatorio['colunas'])}):")
    for i, col in enumerate(relatorio['colunas'], 1):
        print(f"  {i}. {col}")
    
    # Salvar JSON
    arquivo_json = 'relatorio_acidentes.json'
    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Relatório salvo em: {arquivo_json}")
    print("\n" + "=" * 80)
    print("📊 PRÓXIMOS PASSOS:")
    print("=" * 80)
    print("\n1. Abra o arquivo 'relatorio_acidentes.json' para ver os dados estruturados")
    print("2. Use os dados para atualizar a apresentação HTML")
    print("3. Os valores estão prontos para copiar nos slides\n")


if __name__ == "__main__":
    main()
