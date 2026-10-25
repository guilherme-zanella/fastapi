from fastapi import APIRouter, Depends
from models import Usuario
from hashlib import sha256
from dependencies import pegar_sessao

auth_router = APIRouter(prefix='/auth', tags=['autenticação'])

@auth_router.get('/')
async def home():
    '''
    Essa é o rota padrão de autenticação do sistema.
    '''
    return {'msg': 'Você acessou a rota de autenticação', 'autenticado': False}

@auth_router.post('/criar_usuario')
async def criar_usuario(nome:str, email:str, senha:str, session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if usuario:
        return {'msg': 'Já existe um usuário com esse email'}
    else:
        hash = sha256(senha.encode('utf-8')).hexdigest()
        novo_usuario = Usuario(nome, email, hash)
        session.add(novo_usuario)
        session.commit()
        return {'msg': f'Usuario {nome} cadastrado com sucesso'}
