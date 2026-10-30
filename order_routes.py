from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario

order_router = APIRouter(prefix='/pedidos', tags=['pedidos'], dependencies=[Depends(verificar_token)])

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

@order_router.post('/pediodo/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')

    if not usuario.admin and usuario.id != pedido.dono:
        raise HTTPException(status_code=401, detail='Você não tem permissão para cancelar esse pedido')

    pedido.status = 'cancelado'
    session.commit()
    return {
        'msg': f'Pedido {pedido.id} cancelado com sucesso',
        'pedido': pedido
    }


@order_router.get('/listar/')
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token), skip: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=0, le=100)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail='Você não tem permissão para realizar isso')
    else:
        pedidos = session.query(Pedido).all()
        return {
            'pedidos': pedidos[skip: limit+skip]
        }
        