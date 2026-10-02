import re
from app import *

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

print(cep)