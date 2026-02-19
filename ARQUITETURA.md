# 🏗️ Arquitetura do CapivaraFlow SaaS

## 📐 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENTE / NAVEGADOR                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       PUBLIC (Frontend)                         │   │
│  │  ┌──────────────────────────────────────────────────────────┐  │   │
│  │  │  login.html    │  index.html    │  dashboard.html       │  │   │
│  │  │  (Autenticação)│  (Chatbot)     │  (Principal)          │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────────────────┐  │   │
│  │  │         public/modules/                                  │  │   │
│  │  │  ├─ relatorio-acidentes.html  (Submódulo)             │  │   │
│  │  │  ├─ outro-modulo.html         (Extensível)            │  │   │
│  │  └──────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                  │                                       │
│                          HTTP Requests/Responses                        │
│                                  │                                       │
│                                  ▼                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                         SERVIDOR (Backend)                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    FLASK APPLICATION                            │  │
│  │                      (backend/app.py)                           │  │
│  │                                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │               ROTAS & ENDPOINTS                           │  │  │
│  │  ├─ GET/POST        /api/auth/*           (Autenticação)   │  │  │
│  │  ├─ GET             /api/modules          (Lista módulos)   │  │  │
│  │  ├─ GET             /api/modules/<id>     (Info módulo)     │  │  │
│  │  ├─ GET             /api/acidentes/*      (Dados)           │  │  │
│  │  ├─ GET             /api/health           (Status)          │  │  │
│  │  ├─ GET             /                     (Serve static)    │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  │                                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │         SISTEMA DE MÓDULOS (Plugável)                   │  │  │
│  │  │            backend/modules/                             │  │  │
│  │  │                                                          │  │  │
│  │  ├─ __init__.py                 (Classe base Module)     │  │  │
│  │  ├─ relatorio_acidentes.py      (Módulo funcionando)    │  │  │
│  │  └─ novo_modulo.py              (Template para novo)    │  │  │
│  │                                                          │  │  │
│  │  Cada módulo:                                            │  │  │
│  │    • Herda de Module (base)                             │  │  │
│  │    • Implementa get_data()                              │  │  │
│  │    • Processa dados estruturados                        │  │  │
│  │    • Fornece via API endpoints                          │  │  │
│  │                                                          │  │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │         AUTENTICAÇÃO & SEGURANÇA                      │  │  │
│  │  │               backend/auth.py                         │  │  │
│  │  │                                                       │  │  │
│  │  ├─ generate_token()         (JWT Token)               │  │  │
│  │  ├─ verify_token()          (Validação)                │  │  │
│  │  ├─ @token_required         (Decorator)               │  │  │
│  │  ├─ @admin_required         (Decorator)               │  │  │
│  │  └─ CORS configurado para segurança                    │  │  │
│  │                                                       │  │  │
│  └──────────────────────────────────────────────────────────┘  │  │
│  ┌──────────────────────────────────────────────────────────┐  │  │
│  │              ACESSO A DADOS                              │  │  │
│  │                                                          │  │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │  │
│  │  │  modules/relatorio-de-acidentes/                  │ │  │  │
│  │  │  ├─ dados_estruturados.json                       │ │  │  │
│  │  │  ├─ relatorio_acidentes.json                      │ │  │  │
│  │  │  ├─ acidentes2025_todas_causas_tipos.csv         │ │  │  │
│  │  │  └─ [outros dados do módulo]                     │ │  │  │
│  │  └────────────────────────────────────────────────────┘ │  │  │
│  │                                                          │  │  │
│  │  Futuro:                                               │  │  │
│  │  ├─ PostgreSQL/MongoDB       (Persistência)           │  │  │
│  │  ├─ Redis                    (Cache)                  │  │  │
│  │  └─ Celery                   (Background jobs)        │  │  │
│  │                                                          │  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Requisição

### 1️⃣ Login
```
[Browser] 
    ↓ POST /api/auth/login
[Flask] → Valida credenciais → Retorna token JWT
    ↓ localStorage.setItem('authToken')
[Browser] → Redireciona para dashboard.html
```

### 2️⃣ Carregamento do Dashboard
```
[Browser] → GET /dashboard.html
[Flask] → Serve arquivo estático
[Browser] → Carrega JavaScript
    ↓
[JS] → Verifica authToken no localStorage
    ↓ GET /api/modules (com token)
[Flask] → @token_required → Retorna lista de módulos
    ↓
[Browser] → Renderiza menu lateral com módulos
```

### 3️⃣ Carregamento de Módulo
```
[User] → Clica em "Relatório de Acidentes"
    ↓
[JS] → Carrega relatorio-acidentes.html em <iframe>
    ↓ GET /api/acidentes/summary (opcional)
[Flask] → Acessa backend/modules/relatorio_acidentes.py
    ↓
[Module] → Lê dados_estruturados.json
    ↓
[Flask] → Retorna JSON com dados
    ↓
[HTML] → Renderiza gráficos e dados
```

## 📦 Sistema de Módulos - Extensível

### Estrutura de um Módulo

```python
# backend/modules/novo_modulo.py
from . import Module

class NovoModulo(Module):
    def __init__(self):
        super().__init__(
            module_id='novo-modulo',
            name='Novo Módulo',
            icon='🆕',
            description='Descrição'
        )
    
    def get_data(self):
        # Retorna dados estruturados
        return {...}
    
    def get_summary(self):
        # Retorna resumo rápido
        return {...}
    
    def process_data(self, raw_data):
        # Processa os dados
        return processed_data
```

### Adicionando à Aplicação

```javascript
// dashboard.html
const MODULES = [
    { id: 'home', name: 'Dashboard', icon: '📊' },
    { id: 'relatorio-acidentes', name: 'Acidentes', icon: '📈' },
    { id: 'novo-modulo', name: 'Novo Módulo', icon: '🆕' },  // ← Novo
];
```

## 🔐 Autenticação & Permissões

### Fluxo de Segurança

```
┌─────────────────────────────────────────────┐
│  User Authorization Header                  │
│  "Authorization: Bearer <JWT_TOKEN>"        │
└────────────────┬──────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │  @token_required │
         │    decorator     │
         └────────┬─────────┘
                  │
         ┌────────▼──────────┐
         │ jwt.decode()      │
         │ Valida token      │
         └────────┬──────────┘
                  │
         ┌────────▼──────────────┐
         │ request.user = payload│
         │ (username, role, exp) │
         └────────┬──────────────┘
                  │
         ┌────────▼──────────────┐
         │  Rota executada com   │
         │  acesso ao usuário    │
         └───────────────────────┘
```

### Níveis de Acesso

| Role | Acesso |
|------|--------|
| public | Login, Chat |
| user | Dashboard, Módulos |
| admin | Tudo + Configurações |

## 📊 Separação de Responsabilidades

### Frontend (public/)
- Renderização de UI
- Interação com usuário
- Chamadas AJAX/Fetch à API
- Estado local com localStorage

### Backend (backend/)
- Autenticação & Autorização
- Processamento de dados
- Integração com módulos
- Validação de entrada
- Retorno de dados estruturados

### Dados (modules/)
- Dados estruturados (JSON, CSV)
- Configurações de módulos
- Cache/Cache layer

## 🚀 Deploy

### Opção 1: Local
```bash
python backend/app.py
# Acesse: http://localhost:5000
```

### Opção 2: Docker
```bash
docker-compose up
# Acesse: http://localhost:5000
```

### Opção 3: Produção (Gunicorn)
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 backend.app:app
```

## 🔄 Próximas Evoluções

### Fase 1 ✅ (Atual)
- [x] Frontend modular
- [x] Backend com módulos
- [x] Sistema de autenticação
- [x] Integração de dados

### Fase 2 📋 (Próximo)
- [ ] Banco de dados (PostgreSQL)
- [ ] Cache (Redis)
- [ ] WebSockets (tempo real)
- [ ] Notificações

### Fase 3 🎯 (Futuro)
- [ ] Multi-tenancy completo
- [ ] Integração com APIs externas
- [ ] Machine Learning
- [ ] Mobile app

## 📈 Performance & Escalabilidade

```
Single Server       →  Load Balancer
┌──────────┐           ┌──────────────┐
│ Flask    │           │ Nginx        │
│ SQLite   │    ==→    ├──────────────┤
│ localhost│           │ Flask #1     │
└──────────┘           │ Flask #2     │
                       │ Flask #3     │
                       ├──────────────┤
                       │ PostgreSQL   │
                       │ Redis        │
                       └──────────────┘
```

---

**CapivaraFlow Architecture** - Simples, Modular, Escalável 🦫
