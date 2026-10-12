from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Produto
class ProdutoBase(BaseModel):
    nome: str
    codigo_barras: Optional[str] = None
    preco_custo: float = 0.0
    preco_venda: float
    estoque_atual: int = 0
    estoque_minimo: int = 0

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    class Config:
        from_attributes = True

# Cliente
class ClienteBase(BaseModel):
    nome: str
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int
    class Config:
        from_attributes = True

# Venda
class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int

class VendaCreate(BaseModel):
    cliente_id: Optional[int] = None
    itens: List[ItemVendaCreate]

class ItemVendaOut(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    class Config:
        from_attributes = True

class VendaOut(BaseModel):
    id: int
    cliente_id: Optional[int]
    total: float
    data: datetime
    itens: List[ItemVendaOut]
    class Config:
        from_attributes = True

#-------Usuario-------- 
class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioOut(UsuarioBase):
    id: int
    ativo: int
    is_admin: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    