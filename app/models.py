from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    codigo_interno = Column(String, unique=True, nullable=True, index=True) # Para busca rápida
    codigo_barras = Column(String, unique=True, nullable=True)
    marca = Column(String, nullable=True) # Ex: Bosch, Cofap
    aplicacao = Column(Text, nullable=True) # Ex: Gol G5 1.6 2010-2013
    localizacao = Column(String, nullable=True) # Ex: Corredor 3, Gaveta B
    preco_custo = Column(Float, default=0.0)
    preco_venda = Column(Float, nullable=False)
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=0)
    # Campos fiscais
    ncm = Column(String, nullable=True)
    ipi = Column(Float, default=0.0)
    icms = Column(Float, default=0.0)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Veiculo(Base):
    __tablename__ = "veiculos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    placa = Column(String, index=True)
    marca = Column(String, nullable=True)
    modelo = Column(String, nullable=False)
    ano = Column(String, nullable=True)
    cliente = relationship("Cliente", backref="veiculos")

class Orcamento(Base):
    __tablename__ = "orcamentos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(String, default="aberto") # aberto, concluido, cancelado
    valor_bruto = Column(Float, default=0.0)
    desconto_porcentagem = Column(Float, default=0.0)
    desconto_valor = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    cliente = relationship("Cliente")
    veiculo = relationship("Veiculo")
    usuario = relationship("Usuario")
    itens = relationship("ItemOrcamento", back_populates="orcamento", cascade="all, delete-orphan")

class ItemOrcamento(Base):
    __tablename__ = "itens_orcamento"
    id = Column(Integer, primary_key=True, index=True)
    orcamento_id = Column(Integer, ForeignKey("orcamentos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    desconto_item = Column(Float, default=0.0) # Desconto em valor ou %
    
    orcamento = relationship("Orcamento", back_populates="itens")
    produto = relationship("Produto")

class Venda(Base):
    __tablename__ = "vendas"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), nullable=True)
    total = Column(Float, default=0.0)
    data = Column(DateTime, default=datetime.utcnow)
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

class ItemVenda(Base):
    __tablename__ = "itens_venda"
    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    venda = relationship("Venda", back_populates="itens")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    ativo = Column(Integer, default=1)
    is_admin = Column(Integer, default=0)
    criado_em = Column(DateTime, default=datetime.utcnow)