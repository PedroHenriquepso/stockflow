from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# ---------- PRODUTOS ----------
class ProdutoBase(BaseModel):
    nome: str
    codigo_interno: Optional[str] = None
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    aplicacao: Optional[str] = None
    localizacao: Optional[str] = None
    preco_custo: float = 0.0
    preco_venda: float
    estoque_atual: int = 0
    estoque_minimo: int = 0
    ncm: Optional[str] = None
    ipi: float = 0.0
    icms: float = 0.0

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    class Config:
        from_attributes = True

# ---------- CLIENTES ----------
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

# ---------- VEICULOS ----------
class VeiculoBase(BaseModel):
    placa: str
    marca: Optional[str] = None
    modelo: str
    ano: Optional[str] = None

class VeiculoCreate(VeiculoBase):
    cliente_id: Optional[int] = None

class VeiculoOut(VeiculoBase):
    id: int
    cliente_id: Optional[int] = None
    class Config:
        from_attributes = True

# ---------- ORÇAMENTOS ----------
class ItemOrcamentoCreate(BaseModel):
    produto_id: int
    quantidade: int
    desconto_item: float = 0.0

class ItemOrcamentoOut(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    desconto_item: float
    class Config:
        from_attributes = True

class OrcamentoCreate(BaseModel):
    cliente_id: int
    veiculo_id: Optional[int] = None
    itens: List[ItemOrcamentoCreate]
    desconto_porcentagem: float = 0.0
    desconto_valor: float = 0.0

class OrcamentoOut(BaseModel):
    id: int
    cliente_id: int
    veiculo_id: Optional[int]
    usuario_id: int
    status: str
    valor_bruto: float
    desconto_porcentagem: float
    desconto_valor: float
    total: float
    criado_em: datetime
    itens: List[ItemOrcamentoOut]
    class Config:
        from_attributes = True

# ---------- VENDAS ----------
class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int

class VendaCreate(BaseModel):
    cliente_id: Optional[int] = None
    veiculo_id: Optional[int] = None
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
    veiculo_id: Optional[int]
    total: float
    data: datetime
    itens: List[ItemVendaOut]
    class Config:
        from_attributes = True

# ---------- USUARIOS ----------
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
    nome_usuario: str