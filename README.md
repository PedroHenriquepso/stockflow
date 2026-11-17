# 📦 StockFlow

Sistema web de **vendas e estoque** para pequenas e médias empresas, com foco em lojas de autopeças: cadastro de produtos com aplicação veicular, clientes, veículos, orçamentos e vendas.

> 🚧 **Em desenvolvimento.** A Fase 1 (MVP) está concluída.

## ✨ Funcionalidades

**Já implementado**
- [x] Cadastro de produtos (com marca, aplicação, localização no estoque e dados fiscais)
- [x] Cadastro de clientes e veículos
- [x] Orçamentos com itens e desconto
- [x] Registro de vendas com **baixa automática de estoque**
- [x] **Bloqueio de venda sem estoque**
- [x] Autenticação com **JWT + bcrypt** e rotas protegidas
- [x] Tela de login, dashboard com menu lateral, telas de produtos e orçamentos
- [x] Busca de clientes com sugestões enquanto digita

**Planejado**
- [ ] Movimentações de estoque detalhadas
- [ ] Dashboard com dados reais e relatórios
- [ ] Telas de clientes e vendas
- [ ] Emissão fiscal (NF-e/NFC-e)
- [ ] Migração do SQLite para PostgreSQL

## 🛠️ Tecnologias

| | |
|---|---|
| Back-end | Python 3.12, FastAPI, SQLAlchemy, Pydantic |
| Banco de dados | SQLite (PostgreSQL planejado) |
| Segurança | JWT (python-jose) e bcrypt (passlib) |
| Front-end | HTML, CSS e JavaScript puro |

## 📁 Estrutura

```
stockflow/
├── app/
│   ├── routers/        # Rotas da API (auth, produtos, clientes, vendas, veículos, orçamentos)
│   ├── models.py       # Tabelas do banco
│   ├── schemas.py      # Validação dos dados
│   ├── crud.py         # Regras de negócio
│   └── security.py     # Hash de senha e tokens
├── frontend/           # Telas (HTML, CSS, JS)
├── main.py
└── requirements.txt
```

## ▶️ Como rodar localmente

```bash
# 1. Criar ambiente virtual (Windows)
py -3.12 -m venv venv

# 2. Ativar (PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar o servidor
uvicorn main:app --reload
```

Depois acesse:
- Sistema: http://localhost:8000
- Documentação interativa da API: http://localhost:8000/docs

## 🔒 Segurança

As senhas são salvas com hash bcrypt e as rotas exigem token JWT. Antes de usar em produção, a `SECRET_KEY` deve vir de uma variável de ambiente.

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE`.

---
Feito por [Pedro Henrique](https://github.com/PedroHenriquepso)
