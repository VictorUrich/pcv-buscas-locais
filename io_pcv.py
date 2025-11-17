import os
import random

tamanhoPadrao = 30

def gerarProblema(n, minimo = 1, maximo = 20):
    m = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            valor = random.randint(minimo, maximo)
            m[i][j] = valor
            m[j][i] = valor  # garante simetria

    return m

def salvar_matriz(m, nome_arquivo="matriz_pcv.txt"):
    with open(nome_arquivo, "w") as f:
        for linha in m:
            f.write(" ".join(map(str, linha)) + "\n")

def carregar_matriz(nome_arquivo="matriz_pcv.txt"):
    m = []
    with open(nome_arquivo, "r") as f:
        for linha in f:
            valores = list(map(int, linha.split()))
            m.append(valores)
    return m

def carregar_ou_gerar(nome_arquivo="matriz_pcv.txt"):
    if os.path.exists(nome_arquivo):
        print("Matriz carregada do arquivo.")
        return carregar_matriz(nome_arquivo)

    print("Arquivo não encontrado. Gerando matriz de 30 nós...")
    m = gerarProblema(tamanhoPadrao)
    salvar_matriz(m, nome_arquivo)
    return m

def recortar_matriz(matriz_completa, n):
    return [linha[:n] for linha in matriz_completa[:n]]