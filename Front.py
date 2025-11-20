import tkinter as tk
from tkinter import ttk, messagebox

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controlador import (
    iniciar_problema,
    executar_metodo,
    obter_texto_relatorio,
)
from relatorio import salvar_relatorio_txt, salvar_relatorio_pdf


class TSPInterface:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Problema do Caixeiro Viajante - PCV (GUI)")

        # estado interno
        self.n = None               # tamanho do problema atual
        self.tem_solucao_inicial = False

        # para guardar entries de parâmetros por método
        self.param_entries = {}

        self._build_ui()

    # ------------------------------------------------------------------
    # CONSTRUÇÃO DA INTERFACE
    # ------------------------------------------------------------------
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=8)
        main.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Linha 0: tamanho do problema + botão "Gerar Problema"
        ttk.Label(main, text="Número de cidades:").grid(row=0, column=0, sticky=tk.W)
        self.num_var = tk.StringVar(value="6")
        ttk.Entry(main, textvariable=self.num_var, width=6).grid(
            row=0, column=1, sticky=tk.W, padx=4
        )

        ttk.Button(main, text="Gerar Problema", command=self.gerar_problema).grid(
            row=0, column=2, padx=6
        )

        ttk.Label(main, text="Inicializador:").grid(
            row=0, column=3, sticky=tk.W, padx=(12, 0)
        )
        self.init_var = tk.StringVar(value="Aleatória")
        self.init_combo = ttk.Combobox(
            main,
            textvariable=self.init_var,
            values=["Aleatória"],
            state="readonly",
            width=18,
        )
        self.init_combo.grid(row=0, column=4, padx=4)

        ttk.Button(
            main, text="Gerar Solução Inicial", command=self.gerar_solucao_inicial
        ).grid(row=0, column=5, padx=6)

        # Linha 1: método + botões Executar / Análise comparativa
        ttk.Label(main, text="Método de busca local:").grid(
            row=1, column=0, sticky=tk.W, pady=8
        )

        self.method_var = tk.StringVar(value="Subida de encosta")
        methods = [
            "Subida de encosta",
            "Subida de encosta com tentativas",
            "Têmpera simulada",
            "Algoritmos genéticos",
        ]
        self.method_combo = ttk.Combobox(
            main,
            textvariable=self.method_var,
            values=methods,
            state="readonly",
            width=36,
        )
        self.method_combo.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E))
        self.method_combo.bind("<<ComboboxSelected>>", self.on_method_change)

        ttk.Button(main, text="Executar Método", command=self.executar_metodo_ui).grid(
            row=1, column=4, padx=4
        )

        ttk.Button(
            main, text="Análise comparativa", command=self.gerar_analise_comparativa
        ).grid(row=1, column=5, padx=4)

        # Linha 2: quadro de parâmetros dinâmicos
        self.param_frame = ttk.Frame(main)
        self.param_frame.grid(row=2, column=0, columnspan=6, sticky=tk.W, pady=(4, 0))

        # Linha 3: resultados (texto)
        ttk.Label(main, text="Resultados:").grid(
            row=3, column=0, sticky=tk.W, pady=(8, 0)
        )
        self.text_results = tk.Text(main, width=70, height=14, wrap=tk.WORD)
        self.text_results.grid(
            row=4, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=4
        )

        # Canvas matplotlib para o grafo
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main)
        self.canvas.get_tk_widget().grid(row=0, column=6, rowspan=6, padx=10, pady=4)

        for i in range(6):
            main.columnconfigure(i, weight=0)
        main.columnconfigure(6, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Inicializa parâmetros para o método padrão
        self.atualizar_parametros("Subida de encosta")

    # ------------------------------------------------------------------
    # UTILITÁRIOS DE UI
    # ------------------------------------------------------------------
    def _add_result(self, text: str):
        self.text_results.insert(tk.END, text)
        self.text_results.see(tk.END)

    def limpar_param_frame(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries = {}

    def on_method_change(self, event=None):
        metodo_label = self.method_var.get()
        self.atualizar_parametros(metodo_label)

    def atualizar_parametros(self, metodo_label: str):
        """
        Cria dinamicamente os campos de parâmetros conforme o método selecionado.
        """
        self.limpar_param_frame()

        ttk.Label(self.param_frame, text="Parâmetros:").grid(
            row=0, column=0, sticky=tk.W
        )

        # mapa: label -> código interno do controlador
        if metodo_label == "Subida de encosta":
            # não há parâmetros extras
            ttk.Label(self.param_frame, text="(nenhum parâmetro)").grid(
                row=0, column=1, sticky=tk.W, padx=4
            )

        elif metodo_label == "Subida de encosta com tentativas":
            # tMax
            ttk.Label(self.param_frame, text="tMax:").grid(
                row=0, column=1, sticky=tk.W, padx=(8, 2)
            )
            entry = ttk.Entry(self.param_frame, width=8)
            entry.grid(row=0, column=2, sticky=tk.W)
            self.param_entries["tMax"] = entry

        elif metodo_label == "Têmpera simulada":
            # t_ini, t_fim, fr
            ttk.Label(self.param_frame, text="T_ini:").grid(
                row=0, column=1, sticky=tk.W, padx=(8, 2)
            )
            e_tini = ttk.Entry(self.param_frame, width=8)
            e_tini.grid(row=0, column=2, sticky=tk.W)
            self.param_entries["t_ini"] = e_tini

            ttk.Label(self.param_frame, text="T_fim:").grid(
                row=0, column=3, sticky=tk.W, padx=(8, 2)
            )
            e_tfim = ttk.Entry(self.param_frame, width=8)
            e_tfim.grid(row=0, column=4, sticky=tk.W)
            self.param_entries["t_fim"] = e_tfim

            ttk.Label(self.param_frame, text="FR:").grid(
                row=0, column=5, sticky=tk.W, padx=(8, 2)
            )
            e_fr = ttk.Entry(self.param_frame, width=8)
            e_fr.grid(row=0, column=6, sticky=tk.W)
            self.param_entries["fr"] = e_fr

        elif metodo_label == "Algoritmos genéticos":
            # TP, NG, TC, TM, IG
            labels = ["TP", "NG", "TC", "TM", "IG"]
            col = 1
            for nome in labels:
                ttk.Label(self.param_frame, text=f"{nome}:").grid(
                    row=0, column=col, sticky=tk.W, padx=(8, 2)
                )
                entry = ttk.Entry(self.param_frame, width=8)
                entry.grid(row=0, column=col + 1, sticky=tk.W)
                self.param_entries[nome] = entry
                col += 2

    # ------------------------------------------------------------------
    # BOTÕES PRINCIPAIS
    # ------------------------------------------------------------------
    def gerar_problema(self):
        """
        Define o tamanho n do problema.
        A matriz 30x30 é gerenciada pelo backend (io_pcv + controlador).
        Aqui só validamos n (1..30) e limpamos estado local.
        """
        try:
            n = int(self.num_var.get())
        except ValueError:
            messagebox.showerror(
                "Erro", "Informe um número inteiro válido para o tamanho do problema."
            )
            return

        if n <= 0 or n > 30:
            messagebox.showerror(
                "Erro", "O número de cidades deve estar entre 1 e 30 (matriz base 30x30)."
            )
            return

        self.n = n
        self.tem_solucao_inicial = False
        self._add_result(f"Problema definido com n = {n} cidades.\n")
        self.desenhar_grafo()  # desenha grafo sem rota ainda

    def gerar_solucao_inicial(self):
        """
        Chama iniciar_problema(n), que:
          - recorta matriz base 30x30 para n x n
          - gera SI
          - calcula VI
          - inicia um novo relatório
        Não mostramos todos os detalhes aqui, só avisamos que foi gerada.
        """
        if self.n is None:
            messagebox.showerror(
                "Erro", "Defina primeiro o tamanho do problema (Gerar Problema)."
            )
            return

        info = iniciar_problema(self.n)
        self.tem_solucao_inicial = True

        # desenha a SI no grafo
        self.desenhar_grafo(info["SI"])

        # mensagem simples (detalhes completos aparecerão ao executar método)
        self._add_result(
            f"Solução inicial gerada para n = {self.n}.\n"
        )

    def executar_metodo_ui(self):
        """
        Handler do botão 'Executar Método'.
        Usa executar_metodo(...) do controlador e mostra o texto retornado.
        """
        if not self.tem_solucao_inicial:
            messagebox.showerror(
                "Erro", "Gere a solução inicial antes de executar um método."
            )
            return

        metodo_label = self.method_var.get()

        # mapeia label -> código usado no controlador
        mapa_codigos = {
            "Subida de encosta": "SE",
            "Subida de encosta com tentativas": "SET",
            "Têmpera simulada": "TS",
            "Algoritmos genéticos": "AG",
        }

        codigo = mapa_codigos.get(metodo_label)
        if codigo is None:
            messagebox.showerror("Erro", f"Método desconhecido: {metodo_label}")
            return

        # lê parâmetros específicos
        parametros = {}
        tipos_por_metodo = {
            "SET": {"tMax": int},
            "TS": {"t_ini": float, "t_fim": float, "fr": float},
            "AG": {"TP": int, "NG": int, "TC": float, "TM": float, "IG": float},
        }

        tipos = tipos_por_metodo.get(codigo, {})
        for nome, tipo in tipos.items():
            entry = self.param_entries.get(nome)
            if not entry:
                continue
            texto = entry.get().strip()
            if not texto:
                # se estiver vazio, deixa o controlador usar o default
                continue
            try:
                parametros[nome] = tipo(texto)
            except ValueError:
                messagebox.showerror(
                    "Erro", f"Parâmetro {nome} inválido. Informe um valor {tipo.__name__}."
                )
                return

        try:
            resp = executar_metodo(codigo, parametros)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar o método:\n{e}")
            return

        # mostra o texto já formatado (SI, VI, SF, VF, Ganho %)
        self._add_result(resp["texto"])

        # atualiza o grafo com a rota final
        self.desenhar_grafo(resp["SF"])

    def gerar_analise_comparativa(self):
        """
        Gera o texto completo do relatório e salva em TXT e PDF.
        """
        try:
            texto = obter_texto_relatorio()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível obter o relatório:\n{e}")
            return

        # Se o relatório ainda não foi iniciado, a própria função retorna uma mensagem.
        # Vamos checar um caso óbvio:
        if "Nenhum relatório iniciado" in texto:
            messagebox.showwarning(
                "Aviso", "Nenhum relatório iniciado. Gere uma solução inicial e execute algum método."
            )
            return

        try:
            salvar_relatorio_txt("relatorio_pcv.txt")
            salvar_relatorio_pdf("relatorio_pcv.pdf")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar relatórios:\n{e}")
            return

        messagebox.showinfo(
            "Relatórios gerados",
            "Relatórios 'relatorio_pcv.txt' e 'relatorio_pcv.pdf' foram gerados na pasta do projeto.",
        )

    # ------------------------------------------------------------------
    # DESENHO DO GRAFO
    # ------------------------------------------------------------------
    def desenhar_grafo(self, rota=None):
        """
        Desenha um grafo completo com n nós (ou tamanho da rota, se n não estiver definido)
        e destaca a rota passada, se houver.
        """
        self.ax.clear()

        if self.n is None and rota is None:
            self.ax.text(
                0.5,
                0.5,
                "Nenhum problema definido",
                horizontalalignment="center",
                verticalalignment="center",
            )
            self.canvas.draw()
            return

        if self.n is not None:
            n = self.n
        else:
            n = len(rota)

        G = nx.complete_graph(n)
        pos = nx.circular_layout(G)

        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color="lightblue", node_size=200)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=8)

        if rota is not None and len(rota) > 0:
            edges = [
                (rota[i], rota[(i + 1) % len(rota)]) for i in range(len(rota))
            ]
            nx.draw_networkx_edges(
                G, pos, ax=self.ax, edgelist=edges, edge_color="red", width=2
            )
            titulo = "Grafo PCV - Rota"
        else:
            nx.draw_networkx_edges(G, pos, ax=self.ax, alpha=0.2)
            titulo = "Grafo PCV"

        self.ax.set_title(titulo)
        self.ax.axis("off")
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = TSPInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
