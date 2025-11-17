import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import ag_pcv
import metodosBusca
import tspUtils


class TSPInterface:
	def __init__(self, root):
		self.root = root
		self.root.title('Problema do Caixeiro Viajante - PCV (GUI)')
		self.mat = None
		self.rota = None
		self._build_ui()

	def _build_ui(self):
		main = ttk.Frame(self.root, padding=8)
		main.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

		ttk.Label(main, text='Número de cidades (>=30):').grid(row=0, column=0, sticky=tk.W)
		self.num_var = tk.StringVar(value='30')
		ttk.Entry(main, textvariable=self.num_var, width=6).grid(row=0, column=1, sticky=tk.W, padx=4)
		ttk.Button(main, text='Gerar Problema', command=self.gerar_problema).grid(row=0, column=2, padx=6)

		ttk.Label(main, text='Inicializador:').grid(row=0, column=3, sticky=tk.W, padx=(12, 0))
		self.init_var = tk.StringVar(value='Aleatória')
		op_init = ['Aleatória']
		self.init_combo = ttk.Combobox(main, textvariable=self.init_var, values=op_init, state='readonly', width=18)
		self.init_combo.grid(row=0, column=4, padx=4)
		ttk.Button(main, text='Gerar Solução Inicial', command=self.gerar_solucao_inicial).grid(row=0, column=5, padx=6)

		ttk.Label(main, text='Método de busca local:').grid(row=1, column=0, sticky=tk.W, pady=8)
		self.method_var = tk.StringVar(value='Subida de encosta')
		methods = ['Subida de encosta', 'Subida de encosta com tentativas', 'Têmpera simulada', 'Algoritmos genéticos']
		self.method_combo = ttk.Combobox(main, textvariable=self.method_var, values=methods, state='readonly', width=36)
		self.method_combo.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E))
		ttk.Button(main, text='Executar Método', command=self.executar_metodo).grid(row=1, column=5, padx=6)

		ttk.Label(main, text='Resultados:').grid(row=2, column=0, sticky=tk.W, pady=(8, 0))
		self.text_results = tk.Text(main, width=70, height=12, wrap=tk.WORD)
		self.text_results.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=4)

		# Canvas matplotlib
		self.fig, self.ax = plt.subplots(figsize=(6, 5))
		self.canvas = FigureCanvasTkAgg(self.fig, master=main)
		self.canvas.get_tk_widget().grid(row=0, column=6, rowspan=6, padx=10, pady=4)

		for i in range(6):
			main.columnconfigure(i, weight=0)
		main.columnconfigure(6, weight=1)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

	def _add_result(self, text):
		self.text_results.insert(tk.END, text)
		self.text_results.see(tk.END)

	def gerar_problema(self):
		try:
			n = int(self.num_var.get())
		except ValueError:
			messagebox.showerror('Erro', 'Informe um número inteiro válido para o tamanho do problema.')
			return
		if n < 30:
			messagebox.showerror('Erro', 'O número de cidades deve ser pelo menos 30.')
			return
		try:
			# valores mínimos e máximos fixos (podemos expor na UI depois)
			self.mat = ag_pcv.GerarProblema(n, 10, 100)
			self.rota = None
			self._add_result(f'Problema gerado: {n} cidades\n')
			self.desenhar_grafo()
		except Exception as e:
			messagebox.showerror('Erro', f'Falha ao gerar problema: {e}')

	def gerar_solucao_inicial(self):
		if self.mat is None:
			messagebox.showerror('Erro', 'Primeiro gere o problema (Gerar Problema).')
			return
		n = self.mat.shape[0]
		rota = tspUtils.solucaoInicial(n)
		# garantir tipo iterável do Python (lista) para evitar ambiguidades com numpy
		try:
			rota = list(np.asarray(rota))
		except Exception:
			rota = list(rota)
		dist = ag_pcv.Avalia(n, self.mat, rota)
		self.rota = rota
		self._add_result(f"Rota inicial (Aleatória): {' -> '.join(map(str, rota))}\nDistância: {dist:.2f}\n\n")
		self.desenhar_grafo(rota)

	def executar_metodo(self):
		if self.mat is None:
			messagebox.showerror('Erro', 'Primeiro gere o problema (Gerar Problema).')
			return
		n = self.mat.shape[0]
		method = self.method_var.get()
		try:
			rota = None
			if method == 'Subida de encosta':
				rota, dist = metodosBusca.Subida_de_Encosta(n, self.mat, self.rota)
			elif method == 'Subida de encosta com tentativas':
				rota, dist = metodosBusca.Subida_de_Encosta_Tentativas(n, self.mat, 100, self.rota)
			elif method == 'Têmpera simulada':
				rota, dist = metodosBusca.Tempera_Simulada(n, self.mat, 1000, 0.1, 0.9, self.rota)
			elif method == 'Algoritmos genéticos':
				# AlgoritmoGenetico retorna si, sf, vi, vf
				si, sf, vi, vf = ag_pcv.AlgoritmoGenetico(n, self.mat, 30, 300, 0.9, 0.1, 0.2)
				rota, dist = sf, vf
			# se nenhum método foi selecionado corretamente
			if rota is None:
				messagebox.showerror('Erro', 'Método desconhecido')
				return
			# garantir lista python
			try:
				rota = list(np.asarray(rota))
			except Exception:
				rota = list(rota)
		except Exception as e:
			messagebox.showerror('Erro', f'Falha ao executar o método: {e}')
			return

		self.rota = rota
		self._add_result(f"Método: {method}\nDistância total: {dist:.2f}\nRota: {' -> '.join(map(str, rota))}\n\n")
		self.desenhar_grafo(rota)

	def desenhar_grafo(self, rota=None):
		self.ax.clear()
		if self.mat is None:
			self.ax.text(0.5, 0.5, 'Nenhum problema gerado', horizontalalignment='center', verticalalignment='center')
			self.canvas.draw()
			return
		n = self.mat.shape[0]
		G = nx.complete_graph(n)
		pos = nx.circular_layout(G)
		nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='lightblue', node_size=200)
		nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=8)
		if rota is not None and len(rota) > 0:
			edges = [(rota[i], rota[(i + 1) % len(rota)]) for i in range(len(rota))]
			nx.draw_networkx_edges(G, pos, ax=self.ax, edgelist=edges, edge_color='red', width=2)
		else:
			nx.draw_networkx_edges(G, pos, ax=self.ax, alpha=0.2)
		self.ax.set_title('Grafo PCV' + (' - Rota' if rota else ''))
		self.ax.axis('off')
		self.canvas.draw()


def main():
	root = tk.Tk()
	app = TSPInterface(root)
	root.mainloop()


if __name__ == '__main__':
	main()

