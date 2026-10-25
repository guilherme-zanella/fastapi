from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Pedido

order_router = APIRouter(prefix='/pedidos', tags=['pedidos'])

@order_router.get('/')
async def pedidos():
    '''
    Essa é a rota padrão de pedidos.  Todos os usuários precisam estar autenticados para acessa-lá!
    '''
    return {'msg': 'Você acessou a rota de pedidos'}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(dono=pedido_schema.dono)
    session.add(novo_pedido)
    session.commit()
    return {'msg': f'Pedido criado com sucesso. ID do pedido: {novo_pedido.id}'}
