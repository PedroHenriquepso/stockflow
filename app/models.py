from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime  
from app.database import Base       

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True) 
    nome = Column(String, nullable=False)
    codigo_barras = Column(String, unique=True, nullable=True)
    preco_custo = Column(Float, default=0.0)
    preco_venda = Column(Float, nullable=False)
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=0)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Venda(Base):
    __tablename__ = "vendas"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
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