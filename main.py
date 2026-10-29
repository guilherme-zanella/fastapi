from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTE = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTE'))  

app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

from order_routes import order_router
from auth_routes import auth_router

# para rodar o código: uvicorn main:app --reload

# /ordens:

app.include_router(order_router)
app.include_router(auth_router)

# Rest apis
# Get -> leitura
# Post -> enviar/criar
# Put/Patch -> edição
# Delete -> deletar
