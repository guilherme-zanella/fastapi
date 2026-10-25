from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=['autenticação'])

@auth_router.get('/')
async def home():
    '''
    Essa é o rota padrão de autenticação do sistema.
    '''
    return {'msg': 'Você acessou a rota de autenticação', 'autenticado': False}

@auth_router.post('/criar_usuario')
async def criar_usuario(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail='Email já cadastrado')
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {'msg': f'Usuario {usuario_schema.email} cadastrado com sucesso'}
