from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from app.security import hash_senha, verificar_senha

# ---------- PRODUTOS ----------
def criar_produto(db: Session, dados: schemas.ProdutoCreate):
    produto = models.Produto(**dados.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

def listar_produtos(db: Session):
    return db.query(models.Produto).all()

def buscar_produto(db: Session, produto_id: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# ---------- CLIENTES ----------
def criar_cliente(db: Session, dados: schemas.ClienteCreate):
    cliente = models.Cliente(**dados.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def listar_clientes(db: Session):
    return db.query(models.Cliente).all()

def buscar_cliente(db: Session, cliente_id: int):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

# ---------- VEICULOS ----------
def criar_veiculo(db: Session, dados: schemas.VeiculoCreate):
    veiculo = models.Veiculo(**dados.model_dump())
    db.add(veiculo)
    db.commit()
    db.refresh(veiculo)
    return veiculo

def listar_veiculos(db: Session):
    return db.query(models.Veiculo).all()

# ---------- ORÇAMENTOS ----------
def criar_orcamento(db: Session, dados: schemas.OrcamentoCreate, usuario_id: int):
    # Valida se o cliente existe
    buscar_cliente(db, dados.cliente_id)

    orcamento = models.Orcamento(
        cliente_id=dados.cliente_id,
        veiculo_id=dados.veiculo_id,
        usuario_id=usuario_id,
        status="aberto"
    )
    db.add(orcamento)
    db.flush()

    valor_bruto_total = 0.0

    for item in dados.itens:
        produto = buscar_produto(db, item.produto_id)
        
        item_orcamento = models.ItemOrcamento(
            orcamento_id=orcamento.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco_venda,
            desconto_item=item.desconto_item
        )
        db.add(item_orcamento)
        
        # Calcula o valor bruto do item (quantidade x preço)
        valor_bruto_total += (produto.preco_venda * item.quantidade)

    orcamento.valor_bruto = valor_bruto_total
    
    # Lógica de desconto geral
    desconto_total = 0.0
    if dados.desconto_porcentagem > 0:
        desconto_total = valor_bruto_total * (dados.desconto_porcentagem / 100)
    elif dados.desconto_valor > 0:
        desconto_total = dados.desconto_valor

    orcamento.desconto_porcentagem = dados.desconto_porcentagem
    orcamento.desconto_valor = desconto_total
    
    # Total final
    orcamento.total = valor_bruto_total - desconto_total

    db.commit()
    db.refresh(orcamento)
    return orcamento

def listar_orcamentos(db: Session, status: str = None):
    query = db.query(models.Orcamento)
    if status:
        query = query.filter(models.Orcamento.status == status)
    return query.order_by(models.Orcamento.criado_em.desc()).all()

# ---------- VENDAS (Mantido simples por enquanto) ----------
def criar_venda(db: Session, dados: schemas.VendaCreate):
    if dados.cliente_id:
        buscar_cliente(db, dados.cliente_id)

    venda = models.Venda(cliente_id=dados.cliente_id, veiculo_id=dados.veiculo_id, total=0.0)
    db.add(venda)
    db.flush()

    total = 0.0
    for item in dados.itens:
        produto = buscar_produto(db, item.produto_id)

        if produto.estoque_atual < item.quantidade:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para '{produto.nome}'. Disponível: {produto.estoque_atual}"
            )

        produto.estoque_atual -= item.quantidade

        item_venda = models.ItemVenda(
            venda_id=venda.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco_venda
        )
        db.add(item_venda)
        total += produto.preco_venda * item.quantidade

    venda.total = total
    db.commit()
    db.refresh(venda)
    return venda

def listar_vendas(db: Session):
    return db.query(models.Venda).all()

# ---------- USUARIOS ----------
def criar_usuario(db: Session, dados: schemas.UsuarioCreate):
    if db.query(models.Usuario).filter(models.Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def buscar_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = buscar_usuario_por_email(db, email)
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario

# ---------- BUSCAS ESPECÍFICAS PARA O ORÇAMENTO ----------
def buscar_clientes_por_termo(db: Session, termo: str):
    termo = f"%{termo}%"
    # Busca por nome ou código (id)
    return db.query(models.Cliente).filter(
        (models.Cliente.nome.ilike(termo)) | 
        (models.Cliente.id.cast(String).ilike(termo))
    ).limit(10).all()

def buscar_veiculos_por_placa(db: Session, placa: str):
    termo = f"%{placa}%"
    return db.query(models.Veiculo).filter(models.Veiculo.placa.ilike(termo)).limit(10).all()