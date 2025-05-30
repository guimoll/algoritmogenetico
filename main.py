import os

import numpy as np

from utils import corrigir_duplicatas

data = np.loadtxt('cidades.mat')
# para calcular a aptidao, adicione os valores da primeira coluna na ultima posição, pois o caixeiro precisa começar e terminar na mesma cidade
# calcula a distancia, sorta de acordo com a distancia e retorna a aptidao
# agora pega os 10 melhores cromosomes e faz os pais para gerar os filhes
# Exibir a matriz carregada
print(data)

numCidades = 20
cromosomos = 20

matrizCromosomos = np.array([np.random.permutation(np.arange(1, cromosomos + 1)) for _ in range(cromosomos)])

# Mostrar a matriz
print("Matriz 20x20 com números de 1 a 20 sem repetição em cada linha:")
print(matrizCromosomos)

dCidades = np.zeros((numCidades, numCidades))

# Calcular a distância entre cada par de cidades
for i in range(numCidades):
    for j in range(numCidades):
        dCidades[i][j] = np.sqrt((data[0, i] - data[0, j]) ** 2 + (data[1, i] - data[1, j]) ** 2)

print(dCidades)

matrizCromossomosComCusto = np.zeros((cromosomos, numCidades + 1), dtype=float)

for i in range(cromosomos):
    caminho = matrizCromosomos[i] - 1  # De 0 a 19 para indexar em dCidades
    caminho_completo = np.append(caminho, caminho[0])  # volta à cidade inicial
    custo_total = 0.0
    for j in range(numCidades):
        origem = caminho_completo[j]
        destino = caminho_completo[j + 1]
        custo_total += dCidades[origem, destino]

    # Preenche a linha com o cromossomo original e o custo ao final
    matrizCromossomosComCusto[i, :-1] = matrizCromosomos[i]
    matrizCromossomosComCusto[i, -1] = custo_total

print("Cromossomos com custo ao final de cada linha:")
print(matrizCromossomosComCusto)

matrizOrdenada = matrizCromossomosComCusto[matrizCromossomosComCusto[:, -1].argsort()]
print("Matriz ordenada por custo:")
print(matrizOrdenada)

# Seleciona os 10 melhores cromossomos
top10 = matrizOrdenada[:10]

# Pesos invertidos (melhor tem mais chance)
pesos = np.arange(10, 0, -1)

# Seleciona 10 pais (5 pares)
indices_pais = np.random.choice(len(top10), size=10, p=pesos / np.sum(pesos))
pais_selecionados = top10[indices_pais]
print("Pais selecionados:")
print(pais_selecionados)

# vai pegar 5 pais 1 e 5 pais 2
# procura aonde esta repetindo e troca também até não ter mais repetição
# procura a repetição só no primeiro pai também
# trocar apenas 2 posições horizontalmente depois


# Cria uma matriz de 5 casais (pai1, pai2)
casais = pais_selecionados.reshape(5, 2, -1)

print("Casais (pai1, pai2):")
print(casais)

# Remove a última coluna (custo) de todos os pais antes de formar os casais
pais_somente_genes = pais_selecionados[:, :-1].astype(int)

# Formar os casais com os genes puros (sem o custo)
casais = pais_somente_genes.reshape(5, 2, -1)

print("Casais (pai1, pai2) sem custo:")
print(casais)
# COMEÇOCROSSOVER

local_aleatorio = np.random.randint(0, 20)

# MELHOR CUSTO ENTRE 3 E 5

# iniciando função de pegar os filhos

# Pegando o primeiro casal como exemplo
pai1 = casais[0][0]
pai2 = casais[0][1]

# Inicialmente, os filhos são cópias dos pais
filho1 = pai1.copy()
filho2 = pai2.copy()

# Trocar os genes no índice aleatório
filho1 = pai1.copy()
filho2 = pai2.copy()

filho1[local_aleatorio] = pai2[local_aleatorio]
filho2[local_aleatorio] = pai1[local_aleatorio]

print(f"\nÍndice aleatório escolhido: {local_aleatorio}")
print("Antes da correção:")
print("Filho 1:", filho1)
print("Filho 2:", filho2)

corrigir_duplicatas(filho1, pai2, local_aleatorio)
corrigir_duplicatas(filho2, pai1, local_aleatorio)

print("\nApós correção de duplicatas:")
print("Filho 1 corrigido:", filho1)
print("Filho 2 corrigido:", filho2)
