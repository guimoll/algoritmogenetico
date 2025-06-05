from utils import corrigir_duplicatas, gerar_filhos_com_crossover, mutacao
import numpy as np


def algoritmoGenetico(data, num_cidades=20, cromossomos=20, geracoes=10000, execucoes=1):
    # Calcula matriz de distâncias uma única vez
    dCidades = getDistanciaCidades(data, num_cidades)
    resultados_finais = []

    #Retorna o resultado
    executarAlgoritmo(cromossomos, dCidades, execucoes, geracoes, num_cidades, resultados_finais)

    return resultados_finais


def executarAlgoritmo(cromossomos, dCidades, execucoes, geracoes, num_cidades, resultados_finais):
    #Loop define o número de execuções que o algoritmo terá, para poder realizar um teste mais robusto
    for execucao in range(execucoes):
        print(f"\n=== Execução {execucao + 1} ===")

        # Inicializa população aleatoriamente a cada execução
        populacao = np.array([np.random.permutation(np.arange(1, num_cidades + 1)) for _ in range(cromossomos)])

        #Roda o código para cada uma das gerações
        populacao = loop_geracoes(cromossomos, dCidades, geracoes, num_cidades, populacao)

        # Após as gerações, calcula novamente o custo para registrar o melhor resultado
        matrizComCusto_final = np.zeros((cromossomos, num_cidades + 1), dtype=float)
        getCromossomoMatrizCusto(cromossomos, dCidades, matrizComCusto_final, num_cidades, populacao)

        matrizOrdenada_final = matrizComCusto_final[matrizComCusto_final[:, -1].argsort()]
        melhor_cromossomo = matrizOrdenada_final[0]

        print(f"Melhor custo final da execução {execucao + 1}: {melhor_cromossomo[-1]}")

        resultados_finais.append(melhor_cromossomo)


def loop_geracoes(cromossomos, dCidades, geracoes, num_cidades, populacao):
    for geracao in range(geracoes):
        # Calcula custo para toda população
        matrizComCusto = np.zeros((cromossomos, num_cidades + 1), dtype=float)

        # Retorna a matriz de custo do cromossomo preenchida
        getCromossomoMatrizCusto(cromossomos, dCidades, matrizComCusto, num_cidades, populacao)

        # Ordena população pelo custo (aptidão)
        matrizOrdenada = matrizComCusto[matrizComCusto[:, -1].argsort()]

        # Pega o melhor custo da primeira geração, da 1000, da 2000...
        if (geracao + 1) % 1000 == 0 or geracao == 0 or geracao == geracoes - 1:
            print(f"Geração {geracao + 1}: Melhor custo: {matrizOrdenada[0, -1]}")

        # Pega o melhor custo da primeira geração e a cada 100 gerações
        #  if geracao == 0 or (geracao + 1) % 100 == 0 or geracao == geracoes - 1:
        #     print(f"Geração {geracao + 1}: Melhor custo: {matrizOrdenada[0, -1]}")

        # Seleciona os 10 melhores pais
        top10 = matrizOrdenada[:10]

        # Pesos para seleção probabilística (melhores têm maior chance)
        pesos = np.arange(10, 0, -1)

        indices_pais = np.random.choice(len(top10), size=10, p=pesos / np.sum(pesos))
        # Seleciona os 10 primeiros pais
        pais_selecionados = top10[indices_pais]

        # Extrai os cromossomos dos pais selecionados (cromossomos sem o custo)
        pais_cromossomos = pais_selecionados[:, :-1].astype(int)

        # Forma 5 casais (pai1, pai2)
        casais = pais_cromossomos.reshape(5, 2, -1)

        # Gera filhos com crossover
        filhos = []
        for casal in casais:
            f1, f2 = gerar_filhos_com_crossover(casal)
            filhos.append(f1)
            filhos.append(f2)
        filhos = np.array(filhos)

        # Aplica mutação nos filhos
        filhos_mutados = mutacao(filhos)

        # Junta pais e filhos mutados para formar nova população
        populacao = np.vstack((pais_cromossomos, filhos_mutados))
    return populacao


def getCromossomoMatrizCusto(cromossomos, dCidades, matrizComCusto, num_cidades, populacao):
    for i in range(cromossomos):
        caminho = populacao[i] - 1
        caminho_completo = np.append(caminho, caminho[0])
        custo_total = 0.0
        for j in range(num_cidades):
            origem = caminho_completo[j]
            destino = caminho_completo[j + 1]
            custo_total += dCidades[origem, destino]
        matrizComCusto[i, :-1] = populacao[i]
        matrizComCusto[i, -1] = custo_total


def getDistanciaCidades(data, num_cidades):
    dCidades = np.zeros((num_cidades, num_cidades))
    for i in range(num_cidades):
        for j in range(num_cidades):
            dCidades[i][j] = np.sqrt((data[0, i] - data[0, j]) ** 2 + (data[1, i] - data[1, j]) ** 2)
    return dCidades