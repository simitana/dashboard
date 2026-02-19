"""
Módulo de Relatório de Acidentes para CapivaraFlow
Processa e fornece dados de acidentes de trânsito
"""

import json
import os
from . import Module

class RelatorioAcidentesModule(Module):
    """Módulo especializado em análise de acidentes de trânsito"""
    
    def __init__(self):
        super().__init__(
            module_id='relatorio-acidentes',
            name='Relatório de Acidentes',
            icon='📈',
            description='Análise detalhada de acidentes de trânsito 2025'
        )
        self.data_path = None
        self._load_data_path()
    
    def _load_data_path(self):
        """Encontra o caminho do arquivo de dados"""
        # Procura pelos dados estruturados
        possible_paths = [
            os.path.join(
                os.path.dirname(__file__),
                '../../modules/relatorio-de-acidentes/dados_estruturados.json'
            ),
            os.path.join(
                os.path.dirname(__file__),
                '../../modules/relatorio-de-acidentes/relatorio_acidentes.json'
            ),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.data_path = path
                return
    
    def get_data(self):
        """Retorna os dados de acidentes"""
        if self.data_path and os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return self.process_data(data)
            except Exception as e:
                return {'error': f'Erro ao carregar dados: {str(e)}'}
        else:
            # Retorna dados simulados se arquivo não existir
            return self._get_mock_data()
    
    def get_summary(self):
        """Retorna um sumário dos dados de acidentes"""
        try:
            data = self.get_data()
            if isinstance(data, list):
                return {
                    'total': len(data),
                    'período': '2025',
                    'status': 'completo'
                }
            elif isinstance(data, dict):
                return {
                    'total': data.get('total', 0),
                    'período': data.get('ano', '2025'),
                    'status': 'carregado'
                }
        except:
            pass
        
        return self._get_mock_summary()
    
    def process_data(self, data):
        """Processa os dados brutos do módulo"""
        # Aqui você pode adicionar transformações nos dados
        return data
    
    def _get_mock_data(self):
        """Retorna dados simulados para demonstração"""
        return {
            'periodo': '2025',
            'total_acidentes': 1250,
            'feridos': 3420,
            'mortos': 145,
            'acidentes_por_mes': [
                {'mes': 'Janeiro', 'total': 98},
                {'mes': 'Fevereiro', 'total': 112},
            ],
            'causas_principais': [
                {'causa': 'Velocidade excessiva', 'percentual': 35},
                {'causa': 'Distração do motorista', 'percentual': 28},
            ]
        }
    
    def _get_mock_summary(self):
        """Retorna sumário simulado"""
        return {
            'total': 1250,
            'período': '2025',
            'status': 'simulado'
        }

# Factory para criar instâncias de módulos
def create_module(module_id):
    """Cria uma instância do módulo solicitado"""
    modules = {
        'relatorio-acidentes': RelatorioAcidentesModule,
    }
    
    module_class = modules.get(module_id)
    if module_class:
        return module_class()
    return None
