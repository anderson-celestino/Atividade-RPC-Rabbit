from common.rpc_utils import RpcClient

client = RpcClient()

print("=== CLIENTE RPC ===")
print("1 - Soma")
print("2 - Multiplicação")
print("3 - Potência")
print("4 - Leitura de caracteres")
print("====================")

op = input("Escolha: ")

if op == "1":
    a = float(input("a = "))
    b = float(input("b = "))
    resposta = client.call("rpc_soma", {"a": a, "b": b})

elif op == "2":
    a = float(input("a = "))
    b = float(input("b = "))
    resposta = client.call("rpc_mult", {"a": a, "b": b})

elif op == "3":
    base = float(input("base = "))
    exp = float(input("expoente = "))
    resposta = client.call("rpc_potencia", {"base": base, "expoente": exp})

elif op == "4":
    txt = input("Digite um texto: ")
    resposta = client.call("rpc_leitura", {"texto": txt})

else:
    print("Opção inválida")
    exit()

print("\nResposta:", resposta)
