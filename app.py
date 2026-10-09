import json
import re
import sys
from random import randint
from datetime import datetime, date

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
    "TO": "Tocantins"
}

def carregar_clientes():
    try:
        with open("clientes.json", "r", encoding="utf-8") as dados:
            clientes = json.load(dados)
    except FileNotFoundError:
        clientes = []

    for c in clientes:
        if "agencia" not in c:
            c["agencia"] = "0001"
        if "conta" not in c:
            c["conta"] = f"{randint(10000, 99999)}-1"
        if "chave_pix" not in c:
            c["chave_pix"] = None
        if "limite_cartao" not in c:
            c["limite_cartao"] = 1500.0
        if "fatura_cartao" not in c:
            c["fatura_cartao"] = 0.0
        if "score_credito" not in c:
            c["score_credito"] = 550
        if "limite_credito" not in c:
            c["limite_credito"] = 2000.0
        if "emprestimos" not in c:
            c["emprestimos"] = []
        if "extrato" not in c:
            c["extrato"] = []

    return clientes

def salvar_clientes(clientes):
    with open("clientes.json", "w", encoding="utf-8") as dados:
        json.dump(clientes, dados, ensure_ascii=False, indent=4)

def verificar_numero(mensagem="Digite aqui: "):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("\033[31mIsso nao e um numero valido.\033[0m")
            print()

def verificar_numero_inteiro(mensagem="Digite aqui: "):
    while True:
        valor = input(mensagem).strip()
        try:
            return int(valor)
        except ValueError:
            print("\033[31mIsso nao e um numero inteiro valido.\033[0m")
            print()

def autenticar_senha(cliente):
    for i in range(3):
        senha = input("Digite sua senha de confirmacao: ")
        if senha == cliente["senha"]:
            return True
        else:
            print("\033[31mSenha incorreta!\033[0m")
            print()
    print("\033[31mNumero de tentativas excedido!\033[0m")
    print()
    return False

def login(clientes):
    print("Digite seu CPF, telefone ou email: ")
    dado = input().strip()

    cliente_encontrado = None
    for cliente in clientes:
        if cliente["cpf"] == dado or cliente["telefone"] == dado or cliente["email"] == dado:
            cliente_encontrado = cliente
            break

    if cliente_encontrado is None:
        print("\033[31mCliente nao encontrado no sistema.\033[0m")
        print()
        return None

    for i in range(3):
        senha = input("Digite sua senha: ")
        if senha == cliente_encontrado["senha"]:
            return cliente_encontrado
        else:
            print("\033[31mSenha incorreta!\033[0m")
            print()

    print("\033[31mNumero maximo de tentativas excedido.\033[0m")
    print()
    return None

def cadastro(clientes):
    nome = input("Digite seu nome completo: ").strip().title()
    print()

    nome_usuario = input("Como devemos te chamar: ").strip().title()
    print()

    while True:
        print("Digite sua data de nascimento.")
        dia = verificar_numero_inteiro("Dia: ")
        mes = verificar_numero_inteiro("Mes: ")
        ano = verificar_numero_inteiro("Ano: ")
        print()

        ano_atual = datetime.now().year
        if ano_atual - ano > 120 or ano > ano_atual:
            print("\033[31mAno de nascimento invalido.\033[0m")
            print()
            continue

        try:
            nascimento = date(ano, mes, dia)
            break
        except ValueError:
            print("\033[31mData invalida para o calendario.\033[0m")
            print()

    idade = ano_atual - nascimento.year
    status = "Maior" if idade >= 18 else "Menor"

    while True:
        cpf = input("Digite seu CPF (000.000.000-00): ").strip()
        pd_cpf = re.search(r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$", cpf)

        if not pd_cpf:
            print("\033[31mFormato de CPF invalido! Use o padrao 000.000.000-00\033[0m")
            print()
            continue

        cpf_existente = False
        for c in clientes:
            if c["cpf"] == cpf:
                cpf_existente = True
                break

        if cpf_existente:
            print("\033[31mEsse CPF ja esta cadastrado no banco.\033[0m")
            print()
            continue

        break

    while True:
        rg = input("Digite seu RG (00.000.000-00): ").strip()
        pd_rg = re.search(r"^\d{2}\.\d{3}\.\d{3}\-\d{2}$", rg)
        if pd_rg or 7 <= len(rg) <= 14:
            break
        else:
            print("\033[31mFormato de RG invalido.\033[0m")
            print()

    while True:
        estado = input("Digite seu estado ou UF: ").strip()
        print()
        if len(estado) == 2:
            estado = estado.upper()
            if estado in estados:
                break
        else:
            estado = estado.title()
            if estado in estados.values():
                break
        print("\033[31mEstado ou UF invalida!\033[0m")
        print()

    cidade = input("Digite o nome da sua cidade: ").strip().title()
    print()
    bairro = input("Digite o nome do seu bairro: ").strip().title()
    print()
    rua = input("Digite sua rua: ").strip().title()
    print()
    nu_casa = verificar_numero_inteiro("Numero da casa: ")
    print()

    while True:
        cep = input("Digite seu CEP (00000-000): ").strip()
        pd_cep = re.search(r"^\d{5}\-\d{3}$", cep)
        if pd_cep:
            break
        else:
            print("\033[31mCEP invalido! Use o padrao 00000-000\033[0m")
            print()

    while True:
        email = input("Digite seu email: ").strip().lower()
        pd_email = re.search(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$", email)

        if not pd_email:
            print("\033[31mEmail em formato invalido!\033[0m")
            print()
            continue

        email_existente = False
        for c in clientes:
            if c["email"] == email:
                email_existente = True
                break

        if email_existente:
            print("\033[31mEsse email ja esta cadastrado.\033[0m")
            print()
            continue

        break

    while True:
        telefone = input("Digite seu telefone (ex: (11)99999-9999): ").strip()
        pd_telefone = re.search(r"^\(\d{2}\)\d{4,5}\-\d{4}$", telefone)

        if not pd_telefone:
            print("\033[31mTelefone em formato invalido!\033[0m")
            print()
            continue

        telefone_existente = False
        for c in clientes:
            if c["telefone"] == telefone:
                telefone_existente = True
                break

        if telefone_existente:
            print("\033[31mEsse telefone ja esta cadastrado.\033[0m")
            print()
            continue

        break

    while True:
        print("Crie uma senha com no minimo 8 digitos, letras maiusculas, minusculas, numero e caractere especial:")
        senha = input("Senha: ").strip()
        print()

        tem_minu = re.search(r"[a-z]", senha)
        tem_maiu = re.search(r"[A-Z]", senha)
        tem_num = re.search(r"\d", senha)
        tem_espe = re.search(r"[^a-zA-Z0-9]", senha)

        if len(senha) >= 8 and tem_minu and tem_maiu and tem_num and tem_espe:
            com_senha = input("Confirme sua senha: ").strip()
            print()
            if com_senha == senha:
                break
            else:
                print("\033[31mAs senhas nao conferem!\033[0m")
                print()
        else:
            print("\033[31mA senha nao cumpre todos os requisitos de seguranca.\033[0m")
            print()

    nova_conta = f"{randint(10000, 99999)}-{randint(1, 9)}"

    novo_cliente = {
        "nome": nome,
        "usuario": nome_usuario,
        "cpf": cpf,
        "rg": rg,
        "telefone": telefone,
        "email": email,
        "endereço": f"{rua}, {nu_casa} - {bairro}, {cidade}/{estado}",
        "cep": cep,
        "senha": senha,
        "nascimento": f"{dia:02d}/{mes:02d}/{ano}",
        "idade": idade,
        "status": status,
        "agencia": "0001",
        "conta": nova_conta,
        "saldo": 0.0,
        "chave_pix": None,
        "limite_cartao": 1500.0,
        "fatura_cartao": 0.0,
        "score_credito": 550,
        "limite_credito": 2000.0,
        "emprestimos": [],
        "extrato": []
    }

    clientes.append(novo_cliente)
    salvar_clientes(clientes)

    print("===========================")
    print("  CONTA CRIADA COM SUCESSO ")
    print("===========================")
    print(f"Titular: {novo_cliente['nome']}")
    print(f"Agencia: {novo_cliente['agencia']}")
    print(f"Conta: {novo_cliente['conta']}")
    print("===========================")
    print()

    return novo_cliente

def consultar_saldo(cliente):
    print("========================================")
    print("            DADOS DA CONTA             ")
    print("========================================")
    print(f"Titular: {cliente['nome']}")
    print(f"Usuario: {cliente['usuario']}")
    print(f"Agencia: {cliente['agencia']} | Conta: {cliente['conta']}")
    print(f"CPF: {cliente['cpf']}")
    print(f"Saldo em conta: R$ {cliente['saldo']:.2f}")
    print(f"Limite de credito: R$ {cliente['limite_credito']:.2f}")
    limite_disp = cliente["limite_cartao"] - cliente["fatura_cartao"]
    print(f"Limite disponivel no cartao: R$ {limite_disp:.2f}")
    print(f"Fatura atual do cartao: R$ {cliente['fatura_cartao']:.2f}")
    print("========================================")
    print()

def realizar_deposito(cliente, clientes):
    print("===========================")
    print("         DEPOSITO          ")
    print("===========================")
    valor = verificar_numero("Digite o valor do deposito: R$ ")
    print()

    if valor <= 0:
        print("\033[31mO valor do deposito deve ser maior que zero.\033[0m")
        print()
        return

    if not autenticar_senha(cliente):
        return

    cliente["saldo"] += valor
    codigo = randint(1000000, 9999999)
    agora = datetime.now()

    cliente["extrato"].append({
        "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": "Deposito",
        "valor": valor,
        "detalhe": f"Codigo: {codigo}"
    })

    salvar_clientes(clientes)

    print()
    print("===========================")
    print("  COMPROVANTE DE DEPOSITO  ")
    print("===========================")
    print(f"Data: {agora.strftime('%d/%m/%Y')}")
    print(f"Hora: {agora.strftime('%H:%M:%S')}")
    print(f"Valor: R$ {valor:.2f}")
    print(f"Titular: {cliente['nome']}")
    print(f"Conta: {cliente['conta']}")
    print(f"Codigo de operacao: {codigo}")
    print("===========================")
    print("   DEPOSITO CONCLUIDO      ")
    print("===========================")
    print()

def realizar_saque(cliente, clientes):
    print("===========================")
    print("           SAQUE           ")
    print("===========================")
    valor = verificar_numero("Digite o valor do saque: R$ ")
    print()

    if valor <= 0:
        print("\033[31mO valor deve ser maior que zero.\033[0m")
        print()
        return

    if valor > cliente["saldo"]:
        print("\033[31mSaldo insuficiente para realizar esse saque.\033[0m")
        print()
        return

    confirmar = input(f"Confirma o saque de R$ {valor:.2f}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Operacao cancelada.")
        print()
        return

    if not autenticar_senha(cliente):
        return

    cliente["saldo"] -= valor
    codigo = randint(1000000, 9999999)
    agora = datetime.now()

    cliente["extrato"].append({
        "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": "Saque",
        "valor": valor,
        "detalhe": f"Codigo: {codigo}"
    })

    salvar_clientes(clientes)

    print()
    print("===========================")
    print("   COMPROVANTE DE SAQUE    ")
    print("===========================")
    print(f"Data: {agora.strftime('%d/%m/%Y')}")
    print(f"Hora: {agora.strftime('%H:%M:%S')}")
    print(f"Valor retirado: R$ {valor:.2f}")
    print(f"Saldo restante: R$ {cliente['saldo']:.2f}")
    print(f"Codigo: {codigo}")
    print("===========================")
    print("     SAQUE REALIZADO       ")
    print("===========================")
    print()

def realizar_pix(cliente, clientes):
    print("===========================")
    print("         AREA PIX          ")
    print("===========================")
    print("1 - Enviar Pix")
    print("2 - Cadastrar ou ver Chave Pix")
    print("3 - Voltar")
    opcao = input("Escolha uma opcao: ").strip()
    print()

    if opcao == "1":
        chave_destino = input("Digite a chave Pix, CPF, telefone ou email de quem vai receber: ").strip()

        destinatario = None
        for c in clientes:
            if c.get("chave_pix") == chave_destino or c["cpf"] == chave_destino or c["telefone"] == chave_destino or c["email"] == chave_destino:
                destinatario = c
                break

        if destinatario is None:
            print("\033[31mChave ou destinatario nao encontrado no sistema.\033[0m")
            print()
            return

        if destinatario["cpf"] == cliente["cpf"]:
            print("\033[31mVoce nao pode fazer uma transferencia para si mesmo.\033[0m")
            print()
            return

        print(f"Destinatario: {destinatario['nome']}")
        valor = verificar_numero("Digite o valor do Pix: R$ ")
        print()

        if valor <= 0:
            print("\033[31mO valor do Pix deve ser maior que zero.\033[0m")
            print()
            return

        if valor > cliente["saldo"]:
            print("\033[31mSaldo insuficiente para enviar esse Pix.\033[0m")
            print()
            return

        confirma = input(f"Confirmar envio de R$ {valor:.2f} para {destinatario['nome']}? (s/n): ").strip().lower()
        if confirma != "s":
            print("Operacao cancelada.")
            print()
            return

        if not autenticar_senha(cliente):
            return

        cliente["saldo"] -= valor
        destinatario["saldo"] += valor

        codigo = randint(1000000, 9999999)
        agora = datetime.now()

        cliente["extrato"].append({
            "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": "Pix Enviado",
            "valor": valor,
            "detalhe": f"Para: {destinatario['nome']} (Cod: {codigo})"
        })

        destinatario["extrato"].append({
            "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": "Pix Recebido",
            "valor": valor,
            "detalhe": f"De: {cliente['nome']} (Cod: {codigo})"
        })

        salvar_clientes(clientes)

        print()
        print("===========================")
        print("   COMPROVANTE DE PIX      ")
        print("===========================")
        print(f"Data: {agora.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Valor: R$ {valor:.2f}")
        print(f"Origem: {cliente['nome']}")
        print(f"Destino: {destinatario['nome']}")
        print(f"Codigo Pix: {codigo}")
        print("===========================")
        print("     PIX CONCLUIDO         ")
        print("===========================")
        print()

    elif opcao == "2":
        cadastrar_chave_pix(cliente, clientes)

def cadastrar_chave_pix(cliente, clientes):
    print("===========================")
    print("     CONFIGURAR CHAVE      ")
    print("===========================")
    if cliente.get("chave_pix"):
        print(f"Sua chave Pix cadastrada atualmente e: {cliente['chave_pix']}")
    else:
        print("Voce ainda nao tem uma chave Pix cadastrada.")
    print()
    print("Escolha o tipo de chave que deseja usar:")
    print("1 - CPF")
    print("2 - Telefone")
    print("3 - Email")
    print("4 - Chave aleatoria")
    print("5 - Cancelar")
    escolha = input("Opcao: ").strip()
    print()

    if escolha == "1":
        cliente["chave_pix"] = cliente["cpf"]
    elif escolha == "2":
        cliente["chave_pix"] = cliente["telefone"]
    elif escolha == "3":
        cliente["chave_pix"] = cliente["email"]
    elif escolha == "4":
        cliente["chave_pix"] = f"pix-{randint(100000, 999999)}"
    elif escolha == "5":
        return
    else:
        print("\033[31mOpcao invalida.\033[0m")
        print()
        return

    salvar_clientes(clientes)
    print(f"Chave Pix cadastrada com sucesso: {cliente['chave_pix']}")
    print()

def realizar_transferencia(cliente, clientes):
    print("===========================")
    print("   TRANSFERENCIA BANCARIA  ")
    print("===========================")
    conta_destino = input("Digite o numero da conta de destino (ex: 12345-1): ").strip()

    destinatario = None
    for c in clientes:
        if c.get("conta") == conta_destino:
            destinatario = c
            break

    if destinatario is None:
        print("\033[31mConta de destino nao encontrada.\033[0m")
        print()
        return

    if destinatario["cpf"] == cliente["cpf"]:
        print("\033[31mNao e possivel transferir para a sua propria conta.\033[0m")
        print()
        return

    print(f"Conta encontrada: {destinatario['nome']} - Agencia: {destinatario['agencia']}")
    valor = verificar_numero("Digite o valor da transferencia: R$ ")
    print()

    if valor <= 0:
        print("\033[31mO valor deve ser maior que zero.\033[0m")
        print()
        return

    if valor > cliente["saldo"]:
        print("\033[31mSaldo insuficiente para realizar a transferencia.\033[0m")
        print()
        return

    confirma = input(f"Confirma transferir R$ {valor:.2f} para {destinatario['nome']}? (s/n): ").strip().lower()
    if confirma != "s":
        print("Operacao cancelada.")
        print()
        return

    if not autenticar_senha(cliente):
        return

    cliente["saldo"] -= valor
    destinatario["saldo"] += valor
    codigo = randint(1000000, 9999999)
    agora = datetime.now()

    cliente["extrato"].append({
        "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": "TED Enviada",
        "valor": valor,
        "detalhe": f"Para: {destinatario['nome']} Conta: {destinatario['conta']}"
    })

    destinatario["extrato"].append({
        "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": "TED Recebida",
        "valor": valor,
        "detalhe": f"De: {cliente['nome']} Conta: {cliente['conta']}"
    })

    salvar_clientes(clientes)

    print()
    print("===========================")
    print(" COMPROVANTE TRANSFERENCIA ")
    print("===========================")
    print(f"Data: {agora.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Valor: R$ {valor:.2f}")
    print(f"Origem: {cliente['nome']}")
    print(f"Destino: {destinatario['nome']}")
    print(f"Conta Destino: {destinatario['conta']}")
    print(f"Codigo: {codigo}")
    print("===========================")
    print("  TRANSFERENCIA REALIZADA  ")
    print("===========================")
    print()

def exibir_extrato(cliente):
    print("==================================================")
    print("               EXTRATO DA CONTA                  ")
    print("==================================================")
    print(f"Cliente: {cliente['nome']}")
    print(f"Agencia: {cliente['agencia']} | Conta: {cliente['conta']}")
    print(f"Data de emissao: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("--------------------------------------------------")

    extrato = cliente.get("extrato", [])
    if len(extrato) == 0:
        print("Nenhuma movimentacao registrada ate o momento.")
    else:
        for item in extrato:
            data = item.get("data", "")
            tipo = item.get("tipo", "")
            valor = item.get("valor", 0.0)
            detalhe = item.get("detalhe", "")
            print(f"[{data}] {tipo:<14} R$ {valor:>8.2f} | {detalhe}")

    print("--------------------------------------------------")
    print(f"Saldo atual em conta: R$ {cliente['saldo']:.2f}")
    print("==================================================")
    print()

def analise_credito(cliente, clientes):
    print("===========================")
    print("     ANALISE DE CREDITO    ")
    print("===========================")
    profissao = input("Digite sua profissao: ").strip().title()
    renda = verificar_numero("Digite sua renda mensal comprovada: R$ ")
    print()

    if renda <= 0:
        print("\033[31mRenda informada deve ser maior que zero.\033[0m")
        print()
        return

    if renda < 1500:
        score = 420
        limite = renda * 0.4
        motivo = "Renda inicial com margem de seguranca padrao."
    elif renda <= 4000:
        score = 680
        limite = renda * 0.9
        motivo = "Bom perfil financeiro e capacidade de pagamento estavel."
    else:
        score = 850
        limite = renda * 1.6
        motivo = "Excelente perfil de credito com margem ampliada."

    cliente["score_credito"] = score
    cliente["limite_credito"] = round(limite, 2)
    cliente["limite_cartao"] = round(limite * 0.8, 2)

    salvar_clientes(clientes)

    print("========================================")
    print("          RESULTADO DA ANALISE          ")
    print("========================================")
    print(f"Profissao: {profissao}")
    print(f"Score de credito calculado: {score} pontos")
    print(f"Novo limite de credito aprovado: R$ {cliente['limite_credito']:.2f}")
    print(f"Novo limite do cartao: R$ {cliente['limite_cartao']:.2f}")
    print(f"Parecer: {motivo}")
    print("========================================")
    print()

def solicitar_emprestimo(cliente, clientes):
    print("===========================")
    print("   SIMULAR EMPRESTIMO      ")
    print("===========================")
    print(f"Limite maximo disponivel para emprestimo: R$ {cliente['limite_credito']:.2f}")
    valor = verificar_numero("Digite o valor desejado: R$ ")
    print()

    if valor <= 0:
        print("\033[31mO valor do emprestimo deve ser maior que zero.\033[0m")
        print()
        return

    if valor > cliente["limite_credito"]:
        print("\033[31mEmprestimo negado: o valor solicitado ultrapassa o limite disponivel.\033[0m")
        print()
        return

    parcelas = verificar_numero_inteiro("Em quantas parcelas deseja pagar (de 1 a 24 vezes): ")
    print()

    if parcelas < 1 or parcelas > 24:
        print("\033[31mQuantidade de parcelas invalida. Escolha entre 1 e 24.\033[0m")
        print()
        return

    taxa_mensal = 0.025
    total_juros = valor * taxa_mensal * parcelas
    total_pagar = valor + total_juros
    valor_parcela = total_pagar / parcelas

    print("========================================")
    print("        SIMULACAO DO EMPRESTIMO         ")
    print("========================================")
    print(f"Valor solicitado: R$ {valor:.2f}")
    print(f"Parcelas: {parcelas}x de R$ {valor_parcela:.2f}")
    print(f"Taxa de juros: 2.5% ao mes")
    print(f"Total em juros: R$ {total_juros:.2f}")
    print(f"Total que sera pago: R$ {total_pagar:.2f}")
    print("========================================")
    print()

    contratar = input("Deseja contratar esse emprestimo agora? (s/n): ").strip().lower()
    if contratar != "s":
        print("Contratacao cancelada.")
        print()
        return

    if not autenticar_senha(cliente):
        return

    cliente["saldo"] += valor
    cliente["limite_credito"] -= valor

    codigo = randint(1000000, 9999999)
    agora = datetime.now()

    cliente["emprestimos"].append({
        "codigo": codigo,
        "data": agora.strftime("%d/%m/%Y"),
        "valor_original": valor,
        "parcelas": parcelas,
        "valor_parcela": round(valor_parcela, 2),
        "total_pagar": round(total_pagar, 2)
    })

    cliente["extrato"].append({
        "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": "Emprestimo",
        "valor": valor,
        "detalhe": f"Credito liberado em conta ({parcelas}x de R$ {valor_parcela:.2f})"
    })

    salvar_clientes(clientes)

    print()
    print("========================================")
    print("    EMPRESTIMO APROVADO E CREDITADO     ")
    print("========================================")
    print(f"Valor de R$ {valor:.2f} adicionado ao seu saldo.")
    print(f"Novo saldo em conta: R$ {cliente['saldo']:.2f}")
    print(f"Codigo do contrato: {codigo}")
    print("========================================")
    print()

def area_cartao_credito(cliente, clientes):
    while True:
        limite_disp = cliente["limite_cartao"] - cliente["fatura_cartao"]
        print("===========================")
        print("     CARTAO DE CREDITO     ")
        print("===========================")
        print(f"Limite total: R$ {cliente['limite_cartao']:.2f}")
        print(f"Fatura em aberto: R$ {cliente['fatura_cartao']:.2f}")
        print(f"Limite disponivel: R$ {limite_disp:.2f}")
        print("---------------------------")
        print("1 - Simular compra no cartao")
        print("2 - Pagar fatura do cartao")
        print("3 - Voltar ao menu principal")
        opcao = input("Opcao: ").strip()
        print()

        if opcao == "1":
            estabelecimento = input("Nome do estabelecimento ou loja: ").strip()
            valor = verificar_numero("Valor da compra: R$ ")
            print()

            if valor <= 0:
                print("\033[31mO valor da compra deve ser maior que zero.\033[0m")
                print()
                continue

            if valor > limite_disp:
                print("\033[31mCompra recusada: limite insuficiente no cartao.\033[0m")
                print()
                continue

            if not autenticar_senha(cliente):
                continue

            cliente["fatura_cartao"] += valor
            agora = datetime.now()

            cliente["extrato"].append({
                "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
                "tipo": "Compra Cartao",
                "valor": valor,
                "detalhe": f"Loja: {estabelecimento}"
            })

            salvar_clientes(clientes)

            print("===========================")
            print(" COMPRA APROVADA NO CARTAO ")
            print("===========================")
            print(f"Local: {estabelecimento}")
            print(f"Valor: R$ {valor:.2f}")
            print(f"Fatura atual: R$ {cliente['fatura_cartao']:.2f}")
            print("===========================")
            print()

        elif opcao == "2":
            if cliente["fatura_cartao"] <= 0:
                print("Nao ha fatura em aberto para pagamento.")
                print()
                continue

            print(f"Valor total da fatura: R$ {cliente['fatura_cartao']:.2f}")
            print(f"Seu saldo em conta: R$ {cliente['saldo']:.2f}")
            valor_pagar = verificar_numero("Quanto deseja pagar da fatura: R$ ")
            print()

            if valor_pagar <= 0:
                print("\033[31mO valor do pagamento deve ser maior que zero.\033[0m")
                print()
                continue

            if valor_pagar > cliente["fatura_cartao"]:
                print("\033[31mO valor informado e maior que o total da fatura.\033[0m")
                print()
                continue

            if valor_pagar > cliente["saldo"]:
                print("\033[31mSaldo em conta insuficiente para pagar a fatura.\033[0m")
                print()
                continue

            if not autenticar_senha(cliente):
                continue

            cliente["saldo"] -= valor_pagar
            cliente["fatura_cartao"] -= valor_pagar
            agora = datetime.now()

            cliente["extrato"].append({
                "data": agora.strftime("%d/%m/%Y %H:%M:%S"),
                "tipo": "Pgto Fatura",
                "valor": valor_pagar,
                "detalhe": f"Fatura restante: R$ {cliente['fatura_cartao']:.2f}"
            })

            salvar_clientes(clientes)

            print("===========================")
            print(" FATURA PAGA COM SUCESSO   ")
            print("===========================")
            print(f"Valor pago: R$ {valor_pagar:.2f}")
            print(f"Fatura restante: R$ {cliente['fatura_cartao']:.2f}")
            print(f"Saldo em conta: R$ {cliente['saldo']:.2f}")
            print("===========================")
            print()

        elif opcao == "3":
            break
        else:
            print("\033[31mOpcao invalida.\033[0m")
            print()

def alterar_senha(cliente, clientes):
    print("===========================")
    print("       ALTERAR SENHA       ")
    print("===========================")
    senha_atual = input("Digite sua senha atual: ").strip()
    if senha_atual != cliente["senha"]:
        print("\033[31mSenha atual incorreta!\033[0m")
        print()
        return

    while True:
        nova_senha = input("Digite sua nova senha: ").strip()
        print()

        tem_minu = re.search(r"[a-z]", nova_senha)
        tem_maiu = re.search(r"[A-Z]", nova_senha)
        tem_num = re.search(r"\d", nova_senha)
        tem_espe = re.search(r"[^a-zA-Z0-9]", nova_senha)

        if len(nova_senha) >= 8 and tem_minu and tem_maiu and tem_num and tem_espe:
            confirma = input("Confirme a nova senha: ").strip()
            print()
            if confirma == nova_senha:
                cliente["senha"] = nova_senha
                salvar_clientes(clientes)
                print("Senha alterada com sucesso!")
                print()
                break
            else:
                print("\033[31mAs senhas nao conferem!\033[0m")
                print()
        else:
            print("\033[31mA nova senha nao cumpre os requisitos de seguranca.\033[0m")
            print()