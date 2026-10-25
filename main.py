from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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
