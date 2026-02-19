"""
CapivaraFlow Backend - Flask Application
SaaS Dashboard com Sistema de Módulos Modular
"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='../public', static_url_path='')
CORS(app)

# ==================== CONFIGURAÇÕES ====================
DEBUG = True
PORT = 5000
MODULES_PATH = os.path.join(os.path.dirname(__file__), 'modules')

# ==================== DADOS SIMULADOS ====================
USERS = {
    'admin': '123456',
    'user': 'password'
}

MODULES_CONFIG = [
    {
        'id': 'home',
        'name': 'Dashboard',
        'icon': '📊',
        'description': 'Dashboard principal',
        'active': True
    },
    {
        'id': 'relatorio-acidentes',
        'name': 'Relatório de Acidentes',
        'icon': '📈',
        'description': 'Análise de acidentes de trânsito 2025',
        'active': True,
        'url': '/modules/relatorio-acidentes.html'
    },
    {
        'id': 'produtos',
        'name': 'Produtos',
        'icon': '📋',
        'description': 'Gestão de produtos',
        'active': True
    }
]

# ==================== ROTAS ESTÁTICAS ====================
@app.route('/')
def index():
    """Serve a página principal (login)"""
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/dashboard.html')
def dashboard():
    """Serve o dashboard"""
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos"""
    return send_from_directory(app.static_folder, filename)

# ==================== API DE AUTENTICAÇÃO ====================
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Autentica usuário"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in USERS and USERS[username] == password:
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'user': {
                    'username': username,
                    'role': 'admin' if username == 'admin' else 'user'
                },
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar login: {str(e)}'
        }), 500

# ==================== API DE MÓDULOS ====================
@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Lista todos os módulos disponíveis"""
    try:
        return jsonify({
            'success': True,
            'modules': MODULES_CONFIG,
            'count': len(MODULES_CONFIG),
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao listar módulos: {str(e)}'
        }), 500

@app.route('/api/modules/<module_id>', methods=['GET'])
def get_module(module_id):
    """Obtém informações de um módulo específico"""
    try:
        module = next((m for m in MODULES_CONFIG if m['id'] == module_id), None)
        
        if module:
            return jsonify({
                'success': True,
                'module': module,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Módulo {module_id} não encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter módulo: {str(e)}'
        }), 500

# ==================== API DE DADOS (MÓDULO ACIDENTES) ====================
@app.route('/api/acidentes/summary', methods=['GET'])
def get_acidentes_summary():
    """Retorna sumário dos acidentes"""
    try:
        # Tenta carregar dados reais do JSON
        acidentes_data_path = os.path.join(
            os.path.dirname(__file__),
            '../modules/relatorio-de-acidentes/dados_estruturados.json'
        )
        
        if os.path.exists(acidentes_data_path):
            with open(acidentes_data_path, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return jsonify({
                    'success': True,
                    'data': dados,
                    'timestamp': datetime.now().isoformat()
                }), 200
        else:
            # Dados simulados se arquivo não existir
            return jsonify({
                'success': True,
                'data': {
                    'total_acidentes': 1250,
                    'feridos': 3420,
                    'mortos': 145,
                    'periodo': '2025'
                },
                'timestamp': datetime.now().isoformat()
            }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao obter dados de acidentes: {str(e)}'
        }), 500

# ==================== API DE HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica saúde da API"""
    return jsonify({
        'status': 'online',
        'service': 'CapivaraFlow Backend',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

# ==================== TRATAMENTO DE ERROS ====================
@app.errorhandler(404)
def not_found(error):
    """Trata erro 404"""
    return jsonify({
        'success': False,
        'message': 'Recurso não encontrado',
        'error': str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Trata erro 500"""
    return jsonify({
        'success': False,
        'message': 'Erro interno do servidor',
        'error': str(error)
    }), 500

# ==================== INICIALIZAÇÃO ====================
if __name__ == '__main__':
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║     CapivaraFlow Backend - SaaS Dashboard             ║
    ║     Iniciando servidor...                             ║
    ║     Acesse: http://localhost:{PORT}                    ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG,
        use_reloader=True
    )
