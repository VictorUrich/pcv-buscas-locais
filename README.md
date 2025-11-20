Instruções de Execução — Projeto PCV (Problema do Caixeiro Viajante)
Resumo
Este projeto implementa métodos de busca local e algoritmo genético aplicados ao Problema do Caixeiro Viajante (PCV),
acompanhado de uma interface gráfica em Tkinter (Front.py).

A interface permite:
Gerar um problema (matriz de custos);

Criar uma solução inicial;

Executar métodos de busca local (SE, SET, TS) e AG;

Visualizar as rotas no grafo;

Exibir resultados no painel de texto.

Dependências

As bibliotecas externas necessárias estão listadas no arquivo:
dependencias.txt

Para instalar todas elas, utilize:
python -m pip install -r dependencias.txt

As dependências são:
numpy
networkx
matplotlib

Requisitos de Python
Python 3.8 ou superior

Tkinter instalado
(faz parte da instalação padrão do Python no Windows; em Linux pode exigir pacote adicional)

Como executar
Abra o terminal (PowerShell, CMD ou Bash) e entre na pasta do projeto:

cd caminho/para/a/pasta/do/projeto


Execute a interface gráfica:
python Front.py


A janela da interface PCV será exibida.

Fluxo de uso na interface (GUI)

Informe o número de cidades desejado no campo “Número de cidades”.

Clique em Gerar Problema para criar a matriz de custos (grafo completo e simétrico).

Clique em Gerar Solução Inicial para gerar uma rota aleatória e calcular sua distância.

Escolha um método de busca local ou algoritmo genético na lista.

Clique em Executar Método para aplicar o método selecionado.

A rota resultante e a distância aparecem no painel de texto.

A rota também é destacada graficamente no painel do grafo.

Observações importantes

A matriz de custos é sempre simétrica e com zeros na diagonal.

Os algoritmos estão implementados nos módulos:

metodosBusca.py

tspUtils.py

ag_pcv.py

A interface aceita rotas representadas como list ou numpy.array sem problemas.