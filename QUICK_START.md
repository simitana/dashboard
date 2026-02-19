# 🚀 Guia Rápido de Início do CapivaraFlow

## ⚡ 5 Minutos para Começar

### Passo 1: Abrir Terminal
```bash
cd ~/Área\ de\ trabalho/ORG/Relatorio
```

### Passo 2: Instalar Dependências (primeira vez apenas)
```bash
pip install Flask Flask-CORS python-dotenv
```

### Passo 3: Iniciar o Servidor
```bash
python backend/app.py
```

Você verá:
```
╔═══════════════════════════════════════════════════════╗
║     CapivaraFlow Backend - SaaS Dashboard             ║
║     Iniciando servidor...                             ║
║     Acesse: http://localhost:5000                      ║
╚═══════════════════════════════════════════════════════╝
```

### Passo 4: Abrir Navegador
```
http://localhost:5000
```

### Passo 5: Fazer Login
- **Email/Usuário**: admin
- **Senha**: 123456

## 🎯 Após o Login

1. **Dashboard Principal** - Você verá a página de boas-vindas com a Capivara Bot
2. **Menu Lateral** - Navegue pelos módulos:
   - 📊 Dashboard (home)
   - 📈 Relatório de Acidentes
   - 📋 Produtos
3. **São Acessíveis** - Clique em "Relatório de Acidentes" para ver dados estruturados

## 🧩 Adicionar Novo Módulo em 3 Passos

### Passo 1: Criar Backend do Módulo
Arquivo: `backend/modules/meu_modulo.py`
```python
from . import Module

class MeuModulo(Module):
    def __init__(self):
        super().__init__(
            module_id='meu-modulo',
            name='Meu Módulo',
            icon='🆕',
            description='Descrição do meu módulo'
        )
    
    def get_data(self):
        return {
            'exemplo': 'dados',
            'total': 100
        }
```

### Passo 2: Frontend do Módulo
Arquivo: `public/modules/meu-modulo.html`
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Meu Módulo</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-deep-dark text-white p-8">
    <h1 class="text-3xl font-bold mb-6">Meu Módulo</h1>
    <div class="glass-container p-8 rounded-lg">
        <p>Conteúdo do módulo aqui</p>
    </div>
</body>
</html>
```

### Passo 3: Registrar no Dashboard
Arquivo: `public/dashboard.html`
```javascript
const MODULES = [
    { id: 'home', name: 'Dashboard', icon: '📊' },
    { id: 'relatorio-acidentes', name: 'Acidentes', icon: '📈' },
    { id: 'meu-modulo', name: 'Meu Módulo', icon: '🆕' },  // ← ADICIONE
];
```

## 📂 Estrutura de Pastas Criada

```
CapivaraFlow/
├── public/                    ← Interface (Frontend)
│   ├── login.html
│   ├── index.html
│   ├── dashboard.html         ← PRINCIPAL
│   ├── modules/
│   │   └── relatorio-acidentes.html
│   └── phrases.json
│
├── backend/                   ← Lógica (Backend)
│   ├── app.py                 ← APLICAÇÃO FLASK
│   ├── auth.py
│   ├── requirements.txt
│   └── modules/
│       ├── __init__.py
│       └── relatorio_acidentes.py
│
├── modules/                   ← Dados
│   └── relatorio-de-acidentes/
│       ├── dados_estruturados.json
│       └── ...
│
├── README.md                  ← Documentação
├── ARQUITETURA.md             ← Diagrama
├── docker-compose.yml         ← Docker
└── .gitignore
```

## 🎨 Personalizações Rápidas

### Mudar Cores do Dashboard
Editar: `public/dashboard.html`
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'deep-dark': '#NEW_COLOR',      // Fundo
                'chat-green': '#NEW_COLOR',     // Destaque
            },
        },
    },
}
```

### Mudar Logo/Mascote
Todos os arquivos web usam `capivara.png`. Substitua:
```bash
cp seu_logo.png public/capivara.png
```

### Adicionar Endpoints API
Editar: `backend/app.py`
```python
@app.route('/api/novo-endpoint', methods=['GET'])
def novo_endpoint():
    return jsonify({'dados': 'exemplo'}), 200
```

## 🔗 Endpoints Disponíveis

```
# Autenticação
POST   /api/auth/login

# Módulos
GET    /api/modules
GET    /api/modules/<module_id>

# Dados
GET    /api/acidentes/summary

# Status
GET    /api/health

# Frontend
GET    /
GET    /dashboard.html
GET    /login.html
GET    /<arquivo_static>
```

## 🐛 Debug & Troubleshoot

### Ver Logs do Backend
```bash
# Terminal onde Flask está rodando - veja os logs em tempo real
```

### Inspecionar Requisições
Abra DevTools no navegador:
- F12 → Network → Veja as chamadas AJAX
- Console → Veja mensagens JavaScript

### Testar API com curl
```bash
# Health check
curl http://localhost:5000/api/health

# Listar módulos
curl http://localhost:5000/api/modules
```

## 📦 Dependências Instaladas

```
Flask==2.3.3           # Framework web
Flask-CORS==4.0.0      # Habilita requisições cross-origin
python-dotenv==1.0.0   # Variáveis de ambiente
```

Se precisar de mais:
```bash
pip install <pacote>
pip freeze > backend/requirements.txt  # Atualizar lista
```

## 🚀 Deploy Fácil

### Com Docker
```bash
docker-compose up
# Acesse: http://localhost:5000
```

### Com Gunicorn (Produção)
```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 backend.app:app
```

## 📊 Próximos Passos

1. **Testar módulo de acidentes** - Clique em "Relatório de Acidentes"
2. **Criar novo módulo** - Siga o guia de 3 passos acima
3. **Integrar banco de dados** - Ver ARQUITETURA.md
4. **Fazer deploy** - Usar Docker ou Gunicorn

## ❓ Perguntas Comuns

**P: Como mudo a senha de login?**
R: Edite `USERS` em `backend/app.py` linha ~28

**P: Como adiciono autenticação real (banco de dados)?**
R: Consulte `ARQUITETURA.md` - Seção Banco de Dados

**P: Como faço a aplicação rodar sempre?**
R: Use `screen` no Linux: `screen -S capivara python backend/app.py`

**P: Como mudo a porta (não é 5000)?**
R: Edite `app.run(port=5000)` em `backend/app.py`

## 📞 Suporte Rápido

- 📖 Documentação Completa: `README.md`
- 🏗️ Arquitetura Técnica: `ARQUITETURA.md`
- 💻 Código Backend: `backend/app.py`
- 🎨 Interface: `public/dashboard.html`

---

**Bem-vindo ao CapivaraFlow!** 🦫✨

Qualquer dúvida, consulte a documentação ou abra um issue.
