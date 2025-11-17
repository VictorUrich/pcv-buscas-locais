from io_pcv import carregar_ou_gerar, recortar_matriz
from tspUtils import solucaoInicial, avalia
from metodosBusca import (
    Subida_de_Encosta,
    Subida_de_Encosta_Tentativas,
    Tempera_Simulada,
)
from ag_pcv import AlgoritmoGenetico


import relatorio  # importa o módulo inteiro

from relatorio import (
    novo_relatorio,
    registrar_execucao,
    gerar_texto_relatorio_atual,
)

# -------------------------------------------------------------------
# Matrizes
# -------------------------------------------------------------------

# Matriz base 30x30 carregada (ou gerada) uma única vez
MATRIZ_BASE = carregar_ou_gerar()

# Matriz recortada para o tamanho n do problema atual
MATRIZ_ATUAL = None


# -------------------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------------------

def calcular_ganho(vi, vf):
    """Cálculo do ganho percentual sobre o valor inicial vi."""
    return 100.0 * abs(vi - vf) / vi


# -------------------------------------------------------------------
# 1) Simula o botão "Solução Inicial"
# -------------------------------------------------------------------

def iniciar_problema(n):
    """
    Deve ser chamado quando o usuário clicar no botão 'Solução Inicial'.

    - Recorta a matriz base (30x30) para n x n.
    - Gera uma solução inicial SI.
    - Calcula VI = avalia(SI, matriz_recortada).
    - Inicia um novo relatório com (n, SI, VI).

    Retorna SI e VI apenas para teste/log; a interface
    não é obrigada a mostrar isso imediatamente.
    """
    global MATRIZ_ATUAL

    MATRIZ_ATUAL = recortar_matriz(MATRIZ_BASE, n)

    si = solucaoInicial(n)
    vi = avalia(n, si, MATRIZ_ATUAL)

    # Inicia o relatório com essa SI/VI
    novo_relatorio(n, si, vi)

    # Devolve se quiser exibir em algum lugar
    return {
        "n": n,
        "SI": si,
        "VI": vi,
    }


# -------------------------------------------------------------------
# 2) Simula o botão "Executar"
# -------------------------------------------------------------------

def executar_metodo(metodo, parametros=None):
    """
    Executa um método de busca local ou o AG sobre
    a MESMA solução inicial do relatório atual.

    métodos esperados:
      - "SE"  -> Subida de Encosta
      - "SET" -> Subida de Encosta com Tentativas
      - "TS"  -> Têmpera Simulada
      - "AG"  -> Algoritmo Genético

    Retorna um dicionário com todos os dados para a interface mostrar.
    """
    global MATRIZ_ATUAL

    if parametros is None:
        parametros = {}

    if relatorio.CURRENT_REPORT is None:
        raise RuntimeError("Nenhum problema iniciado. Gere a solução inicial primeiro.")

    # ...

    n = relatorio.CURRENT_REPORT["n"]
    si = relatorio.CURRENT_REPORT["SI"][:]
    vi = relatorio.CURRENT_REPORT["VI"]

    if MATRIZ_ATUAL is None:
        raise RuntimeError("Matriz atual não definida. Chame iniciar_problema(n) antes.")

    # Dados fixos do relatório
    n = relatorio.CURRENT_REPORT["n"]
    si = relatorio.CURRENT_REPORT["SI"][:]
    vi = relatorio.CURRENT_REPORT["VI"]
    m = MATRIZ_ATUAL

    # -------------------------------
    # Escolha do método
    # -------------------------------

    if metodo == "SE":
        sf, vf = Subida_de_Encosta(n, m, si)
        nome = "Subida de Encosta"
        config_texto = "Padrão"

    elif metodo == "SET":
        tMax = parametros.get("tMax", n)
        sf, vf = Subida_de_Encosta_Tentativas(n, m, tMax, si)
        nome = "Subida de Encosta com Tentativas"
        config_texto = f"tMax = {tMax}"

    elif metodo == "TS":
        t_ini = parametros.get("t_ini", 400.0)
        t_fim = parametros.get("t_fim", 0.1)
        fr    = parametros.get("fr", 0.9)
        sf, vf = Tempera_Simulada(n, m, t_ini, t_fim, fr, si)
        nome = "Têmpera Simulada"
        config_texto = f"Tini = {t_ini}, Tfim = {t_fim}, FR = {fr}"

    elif metodo == "AG":
        TP = parametros.get("TP", n)
        NG = parametros.get("NG", 3 * n)
        TC = parametros.get("TC", 0.8)
        TM = parametros.get("TM", 0.1)
        IG = parametros.get("IG", 0.2)

        # si_ag e vi_ag são internos do AG – aqui usamos só o melhor resultado final
        si_ag, sf, vi_ag, vf = AlgoritmoGenetico(n, m, TP, NG, TC, TM, IG)
        nome = "Algoritmo Genético"
        config_texto = f"TP = {TP}, NG = {NG}, TC = {TC}, TM = {TM}, IG = {IG}"

    else:
        raise ValueError(f"Método desconhecido: {metodo}")

    # -------------------------------
    # Ganho em relação à VI do relatório
    # -------------------------------
    ganho = calcular_ganho(vi, vf)

    # -------------------------------
    # Registrar no relatório (para PDF)
    # -------------------------------
    registrar_execucao(metodo, config_texto, ganho)

    # -------------------------------
    # Texto pronto para o campo de texto da interface
    # -------------------------------
    texto = (
        f"Método: {nome} ({metodo})\n"
        f"Configuração: {config_texto}\n"
        f"SI: {si}\n"
        f"VI: {vi}\n"
        f"SF: {sf}\n"
        f"VF: {vf}\n"
        f"Ganho: {ganho:.2f}%\n"
        "--------------------------------------\n"
    )

    return {
        "codigo": metodo,
        "nome": nome,
        "config": config_texto,
        "n": n,
        "SI": si,
        "VI": vi,
        "SF": sf,
        "VF": vf,
        "ganho": ganho,
        "texto": texto,
    }


# -------------------------------------------------------------------
# 3) Função para o botão "Análise Comparativa"
# -------------------------------------------------------------------

def obter_texto_relatorio():
    """
    Texto do relatório em formato pronto para:
    - ser mostrado num campo de texto, ou
    - ser salvo em .txt e depois exportado para PDF.
    """
    return gerar_texto_relatorio_atual()
