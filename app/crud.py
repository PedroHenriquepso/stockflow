from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas

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

def atualizar_produto(db: Session, produto_id: int, dados: schemas.ProdutoCreate):
    produto = buscar_produto(db, produto_id)
    for campo, valor in dados.model_dump().items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto

def deletar_produto(db: Session, produto_id: int):
    produto = buscar_produto(db, produto_id)
    db.delete(produto)
    db.commit()
    return {"ok": True}

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

# ---------- VENDAS ----------
def criar_venda(db: Session, dados: schemas.VendaCreate):
    if dados.cliente_id:
        buscar_cliente(db, dados.cliente_id)

    venda = models.Venda(cliente_id=dados.cliente_id, total=0.0)
    db.add(venda)
    db.flush()  # garante o id da venda

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

def buscar_venda(db: Session, venda_id: int):
    venda = db.query(models.Venda).filter(models.Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda