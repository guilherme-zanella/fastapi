from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTE, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth', tags=['autenticação'])


def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dict_informacoes = {'sub': str(id_usuario), 'exp': data_expiracao} # sub é o nome para o id do usuario
    jwt_codificado = jwt.encode(dict_informacoes, SECRET_KEY, ALGORITHM)

    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario



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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas')
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario, duracao_token=timedelta(days=7))
        return {'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer'}

@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)

    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas')
    else:
        access_token = criar_token(usuario.id)
        return {'access_token': access_token,
                'token_type': 'Bearer'}
    

@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {'access_token': access_token,
            'token_type': 'Bearer'}
