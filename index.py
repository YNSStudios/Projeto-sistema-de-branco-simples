import json 
import re
from app import *
from random import randint
from time import sleep 

try:
    with open("Clientes.json", 'r', encoding="utf-8") as dados:
        clientes = json.load(dados)

except FileExistsError:
    clientes = []

print()
print("==============================")
print()
print("Banco DECRADI")
print()
print("Digite seu CPF, telefone ou email (Digite em padrão de leitura, tanto telefone quanto CPF): ")


pessoa = login()
print()

print(f"Bem vindo de volta {pessoa['usuario']}")
print()
