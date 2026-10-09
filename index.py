import sys
from app import (
    carregar_clientes,
    salvar_clientes,
    login,
    cadastro,
    consultar_saldo,
    realizar_deposito,
    realizar_saque,
    realizar_pix,
    realizar_transferencia,
    exibir_extrato,
    analise_credito,
    solicitar_emprestimo,
    area_cartao_credito,
    alterar_senha
)

clientes = carregar_clientes()
salvar_clientes(clientes)

print()
print("==============================")
print("\033[33mBanco DECRADI\033[0m")
print("==============================")
print()

while True:
    print("1 - Entrar na conta")
    print("2 - Criar uma nova conta")
    print("3 - Sair do sistema")
    opcao_inicial = input("Escolha uma opcao: ").strip()
    print()

    cliente_atual = None

    if opcao_inicial == "1":
        cliente_atual = login(clientes)
        if cliente_atual is None:
            continue

    elif opcao_inicial == "2":
        cliente_atual = cadastro(clientes)

    elif opcao_inicial == "3":
        print("Obrigado por usar o Banco DECRADI. Ate logo!")
        sys.exit()

    else:
        print("\033[31mOpcao invalida. Escolha 1, 2 ou 3.\033[0m")
        print()
        continue

    print(f"Ola, {cliente_atual['usuario']}! Bem-vindo ao seu painel.")
    print()

    while True:
        print("==============================")
        print("        MENU PRINCIPAL        ")
        print("==============================")
        print("1  - Consultar Saldo e Dados")
        print("2  - Deposito")
        print("3  - Saque")
        print("4  - Pix (Enviar / Chaves)")
        print("5  - Transferencia Bancaria")
        print("6  - Extrato")
        print("7  - Analise de Credito")
        print("8  - Solicitar Emprestimo")
        print("9  - Cartao de Credito")
        print("10 - Alterar Senha")
        print("11 - Desconectar da Conta")
        print("12 - Sair do Sistema")
        print("==============================")

        escolha = input("Digite o numero da opcao desejada: ").strip()
        print()

        if escolha == "1":
            consultar_saldo(cliente_atual)

        elif escolha == "2":
            realizar_deposito(cliente_atual, clientes)

        elif escolha == "3":
            realizar_saque(cliente_atual, clientes)

        elif escolha == "4":
            realizar_pix(cliente_atual, clientes)

        elif escolha == "5":
            realizar_transferencia(cliente_atual, clientes)

        elif escolha == "6":
            exibir_extrato(cliente_atual)

        elif escolha == "7":
            analise_credito(cliente_atual, clientes)

        elif escolha == "8":
            solicitar_emprestimo(cliente_atual, clientes)

        elif escolha == "9":
            area_cartao_credito(cliente_atual, clientes)

        elif escolha == "10":
            alterar_senha(cliente_atual, clientes)

        elif escolha == "11":
            print("Sessao encerrada. Voltando ao menu inicial.")
            print()
            break

        elif escolha == "12":
            print("Obrigado por utilizar o Banco DECRADI. Ate logo!")
            sys.exit()

        else:
            print("\033[31mOpcao invalida! Digite um numero de 1 a 12.\033[0m")
            print()