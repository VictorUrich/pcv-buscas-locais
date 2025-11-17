from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

CURRENT_REPORT = None
# {
#   "n": n,
#   "SI": [...],
#   "VI": valor,
#   "linhas": [
#       {"metodo": "SE", "config": "tMax=30", "ganho": ganho},
#       ...
#   ]
# }


def novo_relatorio(n, si, vi):
    global CURRENT_REPORT
    CURRENT_REPORT = {
        "n": n,
        "SI": si[:],
        "VI": vi,
        "linhas": []
    }


def registrar_execucao(metodo, config, ganho):
    """
    Chamar SEMPRE que o usuário clicar em 'Executar'.
    """
    global CURRENT_REPORT
    if CURRENT_REPORT is None:
        raise RuntimeError("Nenhum relatório iniciado. Gere a solução inicial primeiro.")

    CURRENT_REPORT["linhas"].append({
        "metodo": metodo,
        "config": config,
        "ganho": ganho
    })


def gerar_texto_relatorio_atual():
    """
    Formato final do relatório para o PDF:

    Cabeçalho:
      - n
      - SI
      - VI

    Tabela:
      Método | Configuração | Ganho
    """
    if CURRENT_REPORT is None:
        return "Nenhum relatório iniciado.\nGere uma solução inicial primeiro.\n"

    n   = CURRENT_REPORT["n"]
    si  = CURRENT_REPORT["SI"]
    vi  = CURRENT_REPORT["VI"]
    lin = CURRENT_REPORT["linhas"]

    if not lin:
        return ("Relatório iniciado, mas sem execuções.\n"
                "Execute pelo menos um método para gerar comparações.\n")

    linhas = []
    # Cabeçalho
    linhas.append("RELATÓRIO – PROBLEMA DO CAIXEIRO VIAJANTE\n\n")
    linhas.append(f"Tamanho do problema (n): {n}\n")
    linhas.append(f"Solução inicial (SI): {si}\n")
    linhas.append(f"Valor inicial (VI): {vi}\n\n")

    # Tabela
    linhas.append(f"{'Método':8} | {'Configuração':40} | {'Ganho (%)':10}\n")
    linhas.append("-" * 70 + "\n")

    for e in lin:
        linhas.append(
            f"{e['metodo']:8} | {str(e['config']):40} | {e['ganho']:10.2f}\n"
        )

    return "".join(linhas)


def salvar_relatorio_txt(caminho="relatorio_pcv.txt"):
    texto = gerar_texto_relatorio_atual()
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    return caminho


def salvar_relatorio_pdf(caminho="relatorio_pcv.pdf"):
    texto = gerar_texto_relatorio_atual()

    # Criar PDF
    c = canvas.Canvas(caminho, pagesize=A4)

    largura, altura = A4
    x = 40
    y = altura - 40

    c.setFont("Helvetica", 12)

    for linha in texto.split("\n"):
        c.drawString(x, y, linha)
        y -= 16

        # Criar nova página se o texto passar do limite
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = altura - 40

    c.save()
    return caminho
