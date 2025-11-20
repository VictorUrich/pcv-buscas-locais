# 📘 Instruções de Execução — Projeto PCV (Problema do Caixeiro Viajante)

## 📌 Resumo

Este projeto implementa métodos de busca local e algoritmo genético aplicados ao **Problema do Caixeiro Viajante (PCV)**, acompanhado de uma interface gráfica desenvolvida em Tkinter (`Front.py`).

A interface permite:

- Gerar um problema (matriz de custos)
- Criar uma solução inicial
- Executar métodos de busca local (SE, SET, TS) e AG
- Visualizar as rotas no grafo
- Exibir resultados no painel de texto

---

## 📦 Dependências

As bibliotecas externas necessárias estão listadas no arquivo:
- `dependencias.txt`

Para instalar todas elas execute:
- `python -m pip install -r dependencias.txt`

As dependências são:
- `numpy`
- `networkx`
- `matplotlib`

---

## 🐍 Requisitos de Python

- Python **3.8 ou superior**
- Tkinter instalado  
  (faz parte da instalação padrão do Python no Windows; em Linux pode exigir instalar `python3-tk`)

---

## ▶️ Como Executar

Abra o terminal (PowerShell, CMD ou Bash) e entre na pasta do projeto:
- `cd caminho/para/a/pasta/do/projeto`

Execute a interface gráfica:
- `python Front.py`

A janela da interface PCV será exibida.

---

## 🖱️ Fluxo de Uso da Interface (GUI)

1. Informe o número de cidades no campo **"Número de cidades"**.
2. Clique em **Gerar Problema** para criar a matriz de custos.
3. Clique em **Gerar Solução Inicial** para gerar uma rota inicial aleatória.
4. Escolha um método de busca local ou algoritmo genético.
5. Clique em **Executar Método** para rodar a busca.
6. A rota resultante e a distância aparecerão no painel de texto.
7. A rota será destacada graficamente no painel do grafo.

---

## 📝 Observações Importantes

- A matriz de custos gerada é **simétrica**, completa e com **zeros na diagonal**.
- Os algoritmos estão implementados nos módulos:
  - `metodosBusca.py`
  - `tspUtils.py`
  - `ag_pcv.py`
- A interface aceita rotas como `list` ou `numpy.array`.

---




