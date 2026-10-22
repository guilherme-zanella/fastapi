from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=['autenticação'])

@auth_router.get('/')
async def autenticar():
    '''
    Essa é o rota padrão de autenticação do sistema.
    '''
    return {'msg': 'Você acessou a rota de autenticação', 'autenticado': False}