from controlador import (
    iniciar_problema,
    executar_metodo,
    obter_texto_relatorio
)
from relatorio import salvar_relatorio_pdf

def linha():
    print("-" * 60)

if __name__ == "__main__":
    # 1) Escolha do tamanho do problema
    n = 6
    print(f"Gerando problema com n = {n}...\n")

    info = iniciar_problema(n)
    print("Solução inicial gerada!")
    print("SI:", info["SI"])
    print("VI:", info["VI"])
    linha()

    # 2) Executar Subida de Encosta
    print("Executando Subida de Encosta...")
    resp = executar_metodo("SE")
    print(resp["texto"])
    linha()

    # 3) Executar Subida de Encosta com Tentativas
    print("Executando SET...")
    resp2 = executar_metodo("SET", {"tMax": 50})
    print(resp2["texto"])
    linha()

    # 4) Executar Têmpera Simulada
    print("Executando Têmpera Simulada...")
    resp3 = executar_metodo("TS", {"t_ini": 400, "t_fim": 0.1, "fr": 0.95})
    print(resp3["texto"])
    linha()

    # 5) Executar Algoritmo Genético
    print("Executando Algoritmo Genético...")
    resp4 = executar_metodo("AG", {"TP": 20, "NG": 60})
    print(resp4["texto"])
    linha()

    # 6) Exibir relatório completo
    print("\nRELATÓRIO COMPLETO:\n")
    print(obter_texto_relatorio())

    salvar_relatorio_pdf("relatorio_pcv.pdf")
