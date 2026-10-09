from app import carregar_clientes

clientes = carregar_clientes()
print(f"Total de clientes carregados: {len(clientes)}")
for c in clientes:
    print(c["nome"], c["agencia"], c["conta"], c["saldo"])
