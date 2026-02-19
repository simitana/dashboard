# CapivaraFlow - SaaS Dashboard 🦫

Um **SaaS modular e escalável** construído em Flask com interface glassmorphism moderna para gestão de relatórios e análises.

## 🏗️ Arquitetura do Projeto

```
CapivaraFlow/
├── public/                          # Frontend (HTML/CSS/JS) - Acesso público
│   ├── login.html                   # Página de login
│   ├── index.html                   # Página do chatbot
│   ├── dashboard.html               # Dashboard principal (modular)
│   ├── modules/                     # Submódulos da interface
│   │   └── relatorio-acidentes.html # Módulo de acidentes
│   └── phrases.json                 # Dados de frases motivacionais
│
├── backend/                         # Backend (Python/Flask) - Lógica protegida
│   ├── app.py                      # Aplicação principal Flask
│   ├── auth.py                     # Autenticação e segurança
│   ├── requirements.txt            # Dependências Python
│   └── modules/                    # Sistema de módulos backend
│       ├── __init__.py             # Base para módulos
│       └── relatorio_acidentes.py  # Módulo de acidentes
│
├── modules/                         # Dados e lógica compartilhados
│   └── relatorio-de-acidentes/    # Dados estruturados do módulo
│       ├── dados_estruturados.json
│       ├── relatorio_acidentes.json
│       ├── acidentes2025_todas_causas_tipos.csv
│       └── ... (outros dados)
│
└── CapivaraFlow/                    # Arquivos legados
    ├── docm_processor.py            # Processador de DOCM
    └── relatoriosExemplo/           # Exemplos de relatórios
```

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)

### 1. Instalar Dependências
```bash
cd backend
pip install -r requirements.txt
```

### 2. Iniciar o Servidor Backend
```bash
cd backend
python app.py
```

Você verá:
```
╔═══════════════════════════════════════════════════════╗
║     CapivaraFlow Backend - SaaS Dashboard             ║
║     Iniciando servidor...                             ║
║     Acesse: http://localhost:5000                      ║
╚═══════════════════════════════════════════════════════╝
```

### 3. Acessar a Aplicação
Abra seu navegador e acesse: **http://localhost:5000**

### 4. Credenciais de Teste
- **Usuário**: admin
- **Senha**: 123456

## 📋 Funcionalidades

### ✅ Login & Autenticação
- Página de login com glassmorphism design
- Mascote interativa (Capivara) que muda com foco
- Validação de credenciais

### 📊 Dashboard Modular
- Interface responsiva com sidebar
- Sistema de navegação entre módulos
- Carregamento dinâmico de componentes
- Menu colapsível com submódulos

### 📈 Módulo Relatório de Acidentes
- Integração com dados estruturados
- Análise de acidentes de trânsito 2025
- Gráficos e KPIs em tempo real
- Filtros avançados

### 💬 Capivara Bot Chat
- Chatbot com IA (integração Gemini)
- Interface conversacional
- Sistema de prompts personalizados

### 🔐 Segurança
- Autenticação baseada em token (JWT)
- Proteção de rotas com decorators
- Separação frontend/backend
- CORS configurado

## 🔗 Endpoints da API

### Autenticação
```
POST /api/auth/login
Body: { "username": "admin", "password": "123456" }
```

### Módulos
```
GET /api/modules                    # Lista todos os módulos
GET /api/modules/<module_id>        # Info de módulo específico
```

### Dados de Acidentes
```
GET /api/acidentes/summary          # Sumário de acidentes
```

### Health Check
```
GET /api/health                     # Status da API
```

## 🎨 Design System

### Cores Principais (Glassmorphism)
- **Deep Dark**: `#0a1917` - Fundo principal
- **Chat Green**: `#10b981` - Destaque/CTA
- **Surface Dark**: `rgba(26, 26, 26, 0.95)` - Superfícies

### Componentes
- **Glass Container**: Efeito glassmorphism com glow verde
- **KPI Cards**: Cards informativos com borders coloridos
- **Menu Links**: Links com hover animado
- **Buttons**: Botões com glow effects

## 📦 Estrutura de Módulos

Cada módulo é uma entidade plugável com:

```python
class Module:
    - id: Identificador único
    - name: Nome legível
    - icon: Emoji ou ícone
    - description: Descrição do módulo
    - get_data(): Retorna dados do módulo
    - get_info(): Retorna info do módulo
```

### Adicionando Novo Módulo

1. **Backend** (`backend/modules/novo_modulo.py`):
```python
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
        return {...}
```

2. **Frontend** (Adicionar ao `dashboard.html`):
```javascript
const MODULES = [
    // ... módulos existentes
    { id: 'novo-modulo', name: 'Novo Módulo', icon: '🆕' },
];
```

3. **HTML do Módulo** (`public/modules/novo-modulo.html`):
Criar interface do módulo

## 🔄 Fluxo de Autenticação

```
1. Usuário acessa http://localhost:5000
   ↓
2. Redireciona para /login.html
   ↓
3. Submete credenciais via formulário
   ↓
4. JavaScript armazena token em localStorage
   ↓
5. Redireciona para /dashboard.html
   ↓
6. Dashboard carrega módulos disponíveis
   ↓
7. Usuário pode navegar entre módulos
```

## 🛡️ Segurança

### Boas Práticas Implementadas
- ✅ Separação frontend/backend
- ✅ Tokens salvos no localStorage
- ✅ CORS configurado
- ✅ Funções de autenticação reutilizáveis
- ✅ Decorators para proteção de rotas

### Próximos Passos (TODO)
- [ ] Implementar JWT tokens
- [ ] Adicionar refresh tokens
- [ ] Rate limiting
- [ ] Validação de CSRF
- [ ] Encriptação de dados sensíveis

## 📊 Database (Futuro)
Estrutura preparada para:
- MongoDB/PostgreSQL
- Armazenamento de usuários
- Cache com Redis
- Fila de tarefas com Celery

## 🐛 Troubleshooting

### Erro: "Port 5000 already in use"
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Erro: "ModuleNotFoundError"
```bash
pip install -r backend/requirements.txt
```

### Módulo não carrega
1. Verificar console do navegador (F12)
2. Verificar logs do backend
3. Confirmar arquivo HTML existe em `/public/modules/`

## 📝 Variáveis de Ambiente (Futuro)

Criar `.env` na pasta backend:
```
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@localhost/capivara
CORS_ORIGINS=http://localhost:3000
```

## 🤝 Contribuindo

Para adicionar novos recursos:

1. Crie uma branch: `git checkout -b feature/novo-recurso`
2. Commit suas mudanças: `git commit -am 'Adiciona novo recurso'`
3. Push para a branch: `git push origin feature/novo-recurso`
4. Abra um Pull Request

## 📄 Licença

Todos os direitos reservados © 2026 CapivaraFlow

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório ou entre em contato.

---

**CapivaraFlow**: Construindo o futuro, um módulo por vez. 🦫✨
