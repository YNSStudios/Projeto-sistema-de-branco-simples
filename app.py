import json
import re 
import sys
from app import * 
from random import randint 
from time import sleep
from datetime import *

try:
    with open("Clientes.json", "r", encoding="utf-8") as dados:
        clientes = json.load(dados)

except FileExistsError:
    clientes = []

estados = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}

def verificar_numero():

    while True:

        numero = input("\033[33mDigite aqui: \033[0m")
        print()

        try:
            numero = float(numero)
            return numero
        except:
            print("\033[31mIsso não é um número...\033[0m")
            print()


def verificar_numero_inteiro():

    while True:

        numero = input("\033[33mDigite aqui: \033[0m")
        print()

        try:
            numero = int(numero)
            return numero
        except:
            print("\033[31mIsso não é um válido...\033[0m")
            print()


def login():

    while True:

        dado = input("")

        pd_email = re.search(r"[a-z0-9]+@\.[a-z]+", dado)
        pd_telefone = re.search(r"\([0-9]+\)[0-9]+\-[0-9]+", dado)
        pd_cpf = re.search(r"[0-9]+\.[0-9]+\.[0-9]+\-[0-9]+", dado)

        cliente_econ = None

        if pd_email:

            for cliente in clientes:
                if cliente['email'] == dado:
                    cliente_econ = cliente
                    break

            if cliente_econ is None:
                cadastro()
            else:

                while True:

                    senha = input("Digite sua senha: ")

                    senha_cer = None

                    for senha1 in clientes:
                        if senha1['senha'] == senha:
                            senha_cer = senha
                            return cliente
                        else:
                            print("\033[31mSenha incorreta !\033[0m")
                            print()    
                                      
        elif pd_telefone:

            for cliente in clientes:
                if cliente['telefone'] == dado:
                    cliente_econ = cliente
                    break

            if cliente_econ is None:
                cadastro()
            else:

                while True:

                    senha = input("Digite sua senha: ")

                    senha_cer = None

                    for senha1 in clientes:
                        if senha1['senha'] == senha:
                            senha_cer = senha
                            return cliente
                        else:
                            print("\033[31mSenha incorreta !\033[0m")
                            print()              

        elif pd_cpf:

            for cliente in clientes:
                if cliente['cpf'] == dado:
                    cliente_econ = cliente
                    break

            if cliente_econ is None:
                return cadastro()
            else:

                while True:

                    senha = input("Digite sua senha: ")

                    senha_cer = None

                    for senha1 in clientes:
                        if senha1['senha'] == senha:
                            senha_cer = senha
                            return cliente
                        else:
                            print("\033[31mSenha incorreta !\033[0m")
                            print()                       


def cadastro():

    nome = input("Digite seu nome completo: ").strip().title()
    print()

    nome_usuario = input("Como devemos te chamar: ").strip().title()
    print()

    while True:

        print("Digite seu dia, mês, e ano de nascimento nessa ordem.")
        print()

        print("Dia.")
        dia = int(verificar_numero())

        print("Mês.")
        mes = int(verificar_numero())

        print("Ano.")
        ano = int(verificar_numero())

        if mes < 1 or mes > 12:
            print("Mês inválido.")
            continue

        ano_atual = datetime.now().year

        if (ano_atual - ano) > 127 or ano > ano_atual:
            print("Ano inválido ou impossível.")
            continue

        try:
            nascimento = date(ano, mes, dia)
        except ValueError:
            print("Dia inválido para o mês e ano informados.")
            continue

        idade = ano_atual - nascimento.year

        status = "Maior" if idade >= 18 else "Menor"

        break

    while True:

        print("Digite seu CPF:")
        print()
        cpf = input("")

        pd_cpf = re.search(r"[0-9]+\.[0-9]+\.[0-9]+\-[0-9]+", cpf)

        if pd_cpf:
            if len(cpf) == 14:
                break
            else:
                print("\033[31mFormato inválido !\033[0m")
                print()
        else:
            print("\033[31mNão segue o padrão.\033[0m")
            print()

    while True:

        print("Digite o número do seu RG (00.000.000-00):")

        rg = input("")

        pd_rg = re.search(r"[0-9]+\.[0-9]+\.[0-9]+\-[0-9]+", rg)

        if pd_rg:
            if 7 <= len(rg) <= 14:
                break
            else:
                print("\033[31mO formato não confere com o padrão !\033[0m")
                print()
        else:
            print("\033[31mO formato não confere com o padrão !\033[0m")
            print()

    while True:

        estado = input("Digite seu estado ou UF: ")
        print()

        if len(estado) == 2:
            estado = estado.upper()
            if estado in estados:
                break
        elif 3 <= len(estado) <= 21:
            estado = estado.strip().title()
            if estado in estados:
                break
        else:
            print("\033[31mEscolha inválida !\033[0m")
            print()

    cidade = input("Digite o nome da sua cidade: ").strip().title()
    print()
    bairro = input("Digite o nome do seu bairro: ").strip().title()
    print()
    rua = input("Digite sua rua: ").strip().title()
    print()
    print("Número da casa:")
    nu_casa = verificar_numero_inteiro()

    while True:

        cep = input("Digite seu CEP (99999-999): ")
        print()

        pd_cep = re.search(r"[0-9]+\-[0-9]+", cep)

        if pd_cep:
            if len(cep) == 9:
                break
            else:
                print("\033[31mFormato inválido !\033[0m")
                print()
        else:
            print("\033[31mNão segue o padrão.\033[0m")
            print()

    while True:

        email = input("Digite seu email: ")
        print()

        pd_email = re.search(r"[a-z0-9]+@[a-z]+\.[a-z]+", email)

        if email.find("@") >= 9:
            if pd_email:
                break
            else:
                print("\033[31mO email não segue o padrão.\033[0m")
        else:
            print("\033[31mO email não segue o padrão.\033[0m")
            print()

    while True:

        print("Digite seu telefone no formato (99)99999-9999.")
        print()

        telefone = input("Digite seu telefone: ")
        pd_telefone = re.search(r"\([0-9]+\)[0-9]+\-[0-9]+", telefone)

        if len(telefone) == 14:
            if pd_telefone:
                break
            else:
                print("\033[31mNão segue o padrão descrito acima. \033[0m")
                print()
        else:
            print("\033[31mO telefone não segue o padrão. \033[0m")
            print()

    while True:

        print(
            "Crie uma senha que tenha pelo menos 8 caracteres, letras maiusculas e minusculas, e tenha mais de 8 caracteres e pelo menos 1 carácter especial."
        )
        print()

        senha = input("Digite sua senha: ")
        print()

        tem_minu = re.search(r"[a-z]", senha)
        tem_maiu = re.search(r"[A-Z]", senha)
        tem_num = re.search(r"\d", senha)
        tem_espe = re.search(r"[^a-zA-z0-9]", senha)
        condiçoes = tem_espe and tem_num and tem_maiu and tem_minu

        if len(senha) >= 8 and condiçoes:
            com_senha = input("Comfirme sua senha: ")
            print()
            if com_senha == senha:
                break
            else:
                print("\0333[31mAs senha não são iguais, \033[0m")
                print()
        else:
            print("\033[31mA senha não segue o padrão !\033[0m")
            print()

    clientes.append(
    {
        "nome": nome,
        "usuario": nome_usuario,
        "cpf": cpf,
        "rg": rg,
        "telefone": telefone,
        "email": email,
        "endereço": f"{rua}, {nu_casa} - {bairro}, {cidade}/{estado}",
        "cep": cep,
        "senha": senha,
        "nascimento": f"{dia}/{mes}/{ano}",
        "idade": idade,
        "status": status,
        "saldo": 0,
        "chave_pix": None,
    }
    )

    with open("clientes.json", "w", encoding="utf-8") as dados:
            json.dump(clientes, dados, ensure_ascii=False, indent= 4)

    for cliente in clientes:
        if cliente['cpf'] == cpf:
            return cliente
