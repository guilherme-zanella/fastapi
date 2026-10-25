from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=['autenticação'])


def criar_token(id_usuario):
    token = f'fewagtaf{id_usuario}' 
    return token



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

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()

    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado')
    else:
        access_token = criar_token(usuario.id)
        return {'access_token': access_token,
                'token_type': 'Bearer'}

