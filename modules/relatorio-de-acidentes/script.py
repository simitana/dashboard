# ============================================================================
# EXTRATOR CSV ROBUSTO → DADOS OTIMIZADOS PARA LLM
# Trata CSVs com problemas de formatação, delimitadores mistos, etc.
# ============================================================================

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import csv
import io

class CSVtoLLMOptimizerRobusto:
    """Converte CSV bruto (com problemas) em dados otimizados para LLM"""
    
    def __init__(self, caminho_csv):
        self.caminho_csv = caminho_csv
        self.df_raw = None
        self.data_extracao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.delimitador_detectado = None
        
    # ========================================================================
    # 1. DETECTAR DELIMITADOR
    # ========================================================================
    
    def detectar_delimitador(self):
        """Detecta automaticamente o delimitador do CSV"""
        try:
            with open(self.caminho_csv, 'r', encoding='utf-8') as f:
                primeira_linha = f.readline()
            
            # Testar delimitadores comuns
            delimitadores = [',', ';', '\t', '|', ' ']
            
            for delim in delimitadores:
                contagem = primeira_linha.count(delim)
                if contagem > 0:
                    print(f"  • Testando '{delim}': encontrados {contagem} delimitadores")
            
            # Usar Sniffer do CSV
            with open(self.caminho_csv, 'r', encoding='utf-8') as f:
                amostra = f.read(4096)
            
            sniffer = csv.Sniffer()
            delim = sniffer.sniff(amostra).delimiter
            
            self.delimitador_detectado = delim
            print(f"\n✓ Delimitador detectado: '{delim}' (código: {ord(delim)})\n")
            return delim
        
        except Exception as e:
            print(f"⚠️ Erro ao detectar delimitador: {e}")
            print("Tentando ';' como padrão...\n")
            self.delimitador_detectado = ';'
            return ';'
    
    # ========================================================================
    # 2. CARREGAR CSV COM TRATAMENTO DE ERROS
    # ========================================================================
    
    def carregar_csv(self):
        """Carrega CSV com múltiplas estratégias de tratamento"""
        
        print("=" * 80)
        print("📂 CARREGANDO CSV")
        print("=" * 80 + "\n")
        
        delim = self.detectar_delimitador()
        
        # Estratégia 1: Carregar com delimitador detectado
        try:
            print(f"Tentativa 1: Usando delimitador '{delim}'...")
            self.df_raw = pd.read_csv(
                self.caminho_csv,
                delimiter=delim,
                encoding='utf-8',
                on_bad_lines='skip',  # Pula linhas com problemas
                engine='python'
            )
            print(f"✓ Sucesso! {len(self.df_raw)} registros carregados\n")
            return True
        
        except Exception as e:
            print(f"❌ Falha: {e}\n")
        
        # Estratégia 2: Tentar com diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                print(f"Tentativa 2: Usando encoding '{encoding}'...")
                self.df_raw = pd.read_csv(
                    self.caminho_csv,
                    delimiter=delim,
                    encoding=encoding,
                    on_bad_lines='skip',
                    engine='python'
                )
                print(f"✓ Sucesso com {encoding}! {len(self.df_raw)} registros\n")
                return True
            except:
                continue
        
        # Estratégia 3: Ler manualmente e corrigir
        try:
            print("Tentativa 3: Leitura manual com tratamento de linhas...")
            linhas_validas = []
            
            with open(self.caminho_csv, 'r', encoding='utf-8') as f:
                leitor = csv.reader(f, delimiter=delim)
                cabecalho = None
                num_colunas = None
                
                for idx, linha in enumerate(leitor):
                    # Primeira linha é cabeçalho
                    if idx == 0:
                        cabecalho = linha
                        num_colunas = len(cabecalho)
                        linhas_validas.append(linha)
                        continue
                    
                    # Ajustar linhas com número incorreto de colunas
                    if len(linha) < num_colunas:
                        # Preencher com valores vazios
                        linha = linha + [''] * (num_colunas - len(linha))
                    elif len(linha) > num_colunas:
                        # Truncar ou mesclar últimas colunas
                        linha = linha[:num_colunas]
                    
                    linhas_validas.append(linha)
            
            # Converter para DataFrame
            self.df_raw = pd.DataFrame(linhas_validas[1:], columns=linhas_validas[0])
            print(f"✓ Sucesso na leitura manual! {len(self.df_raw)} registros\n")
            return True
        
        except Exception as e:
            print(f"❌ Falha na leitura manual: {e}\n")
        
        print("❌ Não foi possível carregar o CSV com nenhuma estratégia")
        return False
    
    # ========================================================================
    # 3. VISUALIZAR ESTRUTURA
    # ========================================================================
    
    def visualizar_estrutura(self):
        """Mostra estrutura completa do CSV"""
        print("\n" + "=" * 80)
        print("📊 ESTRUTURA DO CSV")
        print("=" * 80 + "\n")
        
        print(f"Total de registros: {len(self.df_raw)}")
        print(f"Total de colunas: {len(self.df_raw.columns)}\n")
        
        print("Colunas encontradas:")
        for idx, col in enumerate(self.df_raw.columns, 1):
            dtype = self.df_raw[col].dtype
            valores_unicos = self.df_raw[col].nunique()
            print(f"  {idx}. {col}")
            print(f"     • Tipo: {dtype}")
            print(f"     • Valores únicos: {valores_unicos}")
            print(f"     • Nulos: {self.df_raw[col].isnull().sum()}\n")
        
        print("\nPrimeiras 10 linhas:")
        print(self.df_raw.head(10).to_string())
        
        print("\n\nÚltimas 5 linhas:")
        print(self.df_raw.tail(5).to_string())
    
    # ========================================================================
    # 4. LIMPAR E NORMALIZAR
    # ========================================================================
    
    def limpar_dados(self):
        """Limpa dados rigorosamente"""
        df = self.df_raw.copy()
        
        print("\n" + "=" * 80)
        print("🧹 LIMPANDO DADOS")
        print("=" * 80 + "\n")
        
        # Remover espaços em branco nas colunas
        df.columns = df.columns.str.strip()
        
        # Remover espaços nas células de texto
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
        
        print("✓ Espaços em branco removidos")
        
        # Remover duplicatas
        antes = len(df)
        df = df.drop_duplicates()
        depois = len(df)
        print(f"✓ Duplicatas removidas: {antes - depois} linhas")
        
        # Remover linhas completamente vazias
        antes = len(df)
        df = df.dropna(how='all')
        depois = len(df)
        print(f"✓ Linhas vazias removidas: {antes - depois} linhas")
        
        return df
    
    # ========================================================================
    # 5. EXTRAIR DADOS INTELIGENTEMENTE
    # ========================================================================
    
    def extrair_dados_inteligentes(self, df):
        """Extrai dados automaticamente detectando padrões"""
        
        print("\n" + "=" * 80)
        print("🧠 EXTRAÇÃO INTELIGENTE DE DADOS")
        print("=" * 80 + "\n")
        
        resultados = []
        
        # Procurar padrões em cada coluna
        for col in df.columns:
            col_lower = col.lower()
            
            # Detectar tipo de dado
            if any(palavra in col_lower for palavra in ['tipo', 'categoria', 'classe', 'acidente', 'causa', 'motivo']):
                # Contar ocorrências
                contagens = df[col].value_counts().to_dict()
                
                dados = {
                    'coluna': col,
                    'tipo': 'CATEGORIAS',
                    'registros': [
                        {
                            'nome': str(k),
                            'quantidade': int(v),
                            'percentual': round(v / sum(contagens.values()) * 100, 2)
                        }
                        for k, v in sorted(contagens.items(), key=lambda x: x[1], reverse=True)
                    ],
                    'total': int(sum(contagens.values())),
                    'contagem': len(contagens)
                }
                
                resultados.append(dados)
                print(f"✓ {col}: {len(contagens)} categorias, total de {sum(contagens.values())} registros")
            
            elif any(palavra in col_lower for palavra in ['local', 'estrada', 'rodovia', 'br', 'município', 'região', 'cidade']):
                contagens = df[col].value_counts().to_dict()
                
                dados = {
                    'coluna': col,
                    'tipo': 'LOCALIZACOES',
                    'registros': [
                        {
                            'local': str(k),
                            'quantidade': int(v),
                            'percentual': round(v / sum(contagens.values()) * 100, 2)
                        }
                        for k, v in sorted(contagens.items(), key=lambda x: x[1], reverse=True)
                    ],
                    'total': int(sum(contagens.values())),
                    'contagem': len(contagens)
                }
                
                resultados.append(dados)
                print(f"✓ {col}: {len(contagens)} localizações")
        
        return resultados
    
    # ========================================================================
    # 6. GERAR PROMPT PARA LLM
    # ========================================================================
    
    def gerar_prompt_llm(self, dados_extraidos):
        """Gera prompt otimizado em Markdown"""
        
        prompt = f"""# 📊 DADOS ESTRUTURADOS - ACIDENTES DE TRÂNSITO 2025

## CONTEXTO
- **Data de Extração**: {self.data_extracao}
- **Total de Registros Processados**: {len(self.df_raw):,}
- **Arquivo Original**: {Path(self.caminho_csv).name}
- **Delimitador**: '{self.delimitador_detectado}'

---

"""
        
        for idx, secao in enumerate(dados_extraidos, 1):
            tipo = secao['tipo']
            coluna = secao['coluna']
            registros = secao['registros']
            total = secao['total']
            contagem = secao['contagem']
            
            prompt += f"\n## {idx}. {tipo}\n"
            prompt += f"**Coluna de origem**: {coluna}\n"
            prompt += f"**Total**: {total:,} | **Categorias**: {contagem}\n\n"
            
            prompt += "| # | Item | Quantidade | % |\n"
            prompt += "|---|------|------------|----|\n"
            
            for rank, reg in enumerate(registros, 1):
                chave = list(reg.keys())[1]  # Segunda chave (nome/local)
                valor = reg[chave]
                qtd = reg['quantidade']
                pct = reg['percentual']
                
                prompt += f"| {rank} | {valor} | {int(qtd):,} | {pct}% |\n"
            
            prompt += "\n"
        
        return prompt
    
    # ========================================================================
    # 7. EXPORTAR RESULTADOS
    # ========================================================================
    
    def exportar_resultados(self, prompt_llm, dados_extraidos):
        """Exporta em múltiplos formatos"""
        
        print("\n" + "=" * 80)
        print("💾 EXPORTANDO RESULTADOS")
        print("=" * 80 + "\n")
        
        # Salvar prompt
        with open('prompt_llm_otimizado.md', 'w', encoding='utf-8') as f:
            f.write(prompt_llm)
        print("✓ Exportado: prompt_llm_otimizado.md")
        
        # Salvar JSON
        saida_json = {
            'metadata': {
                'data_extracao': self.data_extracao,
                'arquivo_original': str(self.caminho_csv),
                'delimitador': self.delimitador_detectado,
                'total_registros': len(self.df_raw),
                'total_colunas': len(self.df_raw.columns)
            },
            'dados': dados_extraidos,
            'prompt_preview': prompt_llm[:500] + "..."
        }
        
        with open('dados_estruturados.json', 'w', encoding='utf-8') as f:
            json.dump(saida_json, f, ensure_ascii=False, indent=2)
        print("✓ Exportado: dados_estruturados.json")
        
        # Salvar CSV limpo
        self.df_raw.to_csv('csv_limpo.csv', index=False, encoding='utf-8')
        print("✓ Exportado: csv_limpo.csv (versão limpa)\n")
    
    # ========================================================================
    # 8. EXECUTAR PIPELINE
    # ========================================================================
    
    def processar(self):
        """Executa pipeline completo"""
        
        print("\n" + "=" * 80)
        print("🚀 INICIANDO PROCESSAMENTO CSV → LLM OTIMIZADO (VERSÃO ROBUSTA)")
        print("=" * 80 + "\n")
        
        # 1. Carregar
        if not self.carregar_csv():
            return None
        
        # 2. Visualizar
        self.visualizar_estrutura()
        
        # 3. Limpar
        df_limpo = self.limpar_dados()
        
        # 4. Extrair
        dados_extraidos = self.extrair_dados_inteligentes(df_limpo)
        
        # 5. Gerar prompt
        print("\n" + "=" * 80)
        print("💬 GERANDO PROMPT PARA LLM")
        print("=" * 80)
        
        prompt = self.gerar_prompt_llm(dados_extraidos)
        print(prompt)
        
        # 6. Exportar
        self.exportar_resultados(prompt, dados_extraidos)
        
        # 7. Resumo
        print("=" * 80)
        print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        print(f"\n📈 Resumo:")
        print(f"  • Registros processados: {len(df_limpo):,}")
        print(f"  • Seções de dados: {len(dados_extraidos)}")
        print(f"  • Arquivos gerados: 3")
        print(f"\n💡 Próximo passo: Copie o conteúdo de 'prompt_llm_otimizado.md' para sua LLM\n")
        
        return {
            'prompt': prompt,
            'dados': dados_extraidos,
            'df': df_limpo
        }


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    
    caminho_csv = "acidentes2025_todas_causas_tipos.csv"
    
    if not Path(caminho_csv).exists():
        print(f"\n❌ Arquivo não encontrado: {caminho_csv}\n")
        print("Arquivos CSV disponíveis:")
        for csv_file in Path('.').glob('*.csv'):
            print(f"  • {csv_file}")
        exit(1)
    
    # Processar
    optimizer = CSVtoLLMOptimizerRobusto(caminho_csv)
    resultado = optimizer.processar()

