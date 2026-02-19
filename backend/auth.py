"""
Módulo de Autenticação e Segurança para CapivaraFlow
"""

import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.environ.get('SECRET_KEY', 'capivara-secret-key-2026')

def generate_token(username, role='user', expires_in=86400):
    """
    Gera um JWT token para o usuário após login bem-sucedido.
    
    Args:
        username (str): Nome do usuário
        role (str): Papel/permissão do usuário
        expires_in (int): Tempo em segundos até a expiração (padrão: 24 horas)
    
    Returns:
        str: Token JWT codificado
    """
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """
    Verifica e decodifica um JWT token.
    
    Args:
        token (str): Token JWT a ser verificado
    
    Returns:
        dict: Payload do token se válido
        None: Se token for inválido ou expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def token_required(f):
    """
    Decorator para proteger rotas que precisam de autenticação.
    Valida o token JWT no header Authorization.
    
    Usage:
        @app.route('/api/protected')
        @token_required
        def protected_route():
            return jsonify({'message': 'Success'})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'success': False, 'message': 'Token não fornecido'}), 401
        
        try:
            # Extrai o token do header "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({'success': False, 'message': 'Formato de token inválido'}), 401
            
            token = parts[1]
            payload = verify_token(token)
            
            if payload is None:
                return jsonify({'success': False, 'message': 'Token inválido ou expirado'}), 401
            
            # Adiciona o payload ao request para uso na rota
            request.user = payload
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Erro ao validar token: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """
    Decorator para proteger rotas que requerem permissão de admin.
    Usa token_required como base.
    """
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.user.get('role') != 'admin':
            return jsonify({'success': False, 'message': 'Acesso negado: requer permissão de admin'}), 403
        return f(*args, **kwargs)
    
    return decorated
