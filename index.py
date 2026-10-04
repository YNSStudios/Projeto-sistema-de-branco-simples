import json
import re 
import sys
from app import * 
from random import randint 
from time import sleep
from datetime import *

try:
    with open("Clientes.json", 'r', encoding="utf-8") as dados:
        clientes = json.load(dados)

except FileExistsError:
    clientes = []

print()
print("==============================")
print()
print("\033[33mBanco DECRADI\033[0m")
print()
print("Digite seu CPF, telefone ou email (Digite em padrão de leitura, tanto telefone quanto CPF): ")


cliente = login()
print()

print(f"Bem vindo de volta {cliente['usuario']}")
print()

print(f"Saldo: {cliente['saldo']}")
print()
print("Transferência    Empréstimo     Consórcio     Financiamento     Depósito     configurações    ")
print()

opçao = input("Digite aqui a opção: ").lower().strip()

if opçao in ["depósito", "deposito"]:

    print("Digite aqui o valor do depósito: ")
    deposito = verificar_numero()

    for i in range(3):

        print("Digite sua senha: ")

        com_senha = input("")

        senha = None
        
        if com_senha == cliente['senha']:
            senha = 1
            break
        else:
            print("\033[31mSenha incorrta\033[0m")

    if senha is None:
        print("\033[31mNúmero de tentativas excedida.\033[0m")
        sys.exit()

    cliente['saldo'] = cliente['saldo'] + deposito

    with open("clientes.json", 'w', encoding="utf-8") as dados:
        json.dump(clientes, dados, ensure_ascii=False, indent=14)
        
    codigo_deposito = randint(1000000, 9999999)

    print()
    print("===========================")
    print("  COMPROVANTE DE DEPÓSITO  ")
    print("===========================")
    print()
    print(f"Data: {date.today().strftime('%d/%m/%Y')}")
    print(f"Hora: {datetime.now().strftime('%H:%M:%S')}")
    print()
    print(f"Valor do depósito: R$ {deposito}")
    print()
    print(f"Nome completo: {cliente['nome']}")
    print(f"CPF: {cliente['cpf']}")
    print()
    print(f"Código de depósito: {codigo_deposito}")
    print()
    print("===========================")
    print("   REALIZADO COM SUCESSO   ")
    print("===========================")

