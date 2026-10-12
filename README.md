# StockFlow

Sistema de vendas e estoque para pequenas e médias empresas.

## Status

🚧 Em desenvolvimento — Fase 1 (MVP concluído)

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite (migração para PostgreSQL planejada)
- Pydantic

## Funcionalidades implementadas

- [x] Cadastro de produtos
- [x] Cadastro de clientes
- [x] Registro de vendas
- [x] Baixa automática de estoque
- [x] Bloqueio de venda sem estoque
- [ ] Autenticação de usuários
- [ ] Movimentações de estoque detalhadas
- [ ] Relatórios e dashboard
- [ ] Interface visual
- [ ] Emissão fiscal (NF-e/NFC-e)

## Como rodar localmente

```bash
# Criar ambiente virtual (Windows)
py -3.12 -m venv venv

# Ativar (PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Rodar o servidor
uvicorn main:app --reload

Acesse a documentação interativa em: http://localhost:8000/docs