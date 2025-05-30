import numpy as np
from utils import corrigir_duplicatas, gerar_filhos_com_crossover, mutacao

def rodar_genetico_multiplas_execucoes(data, num_cidades=20, cromossomos=20, geracoes=10000, execucoes=1):
    # Calcula matriz de distâncias uma única vez
    dCidades = np.zeros((num_cidades, num_cidades))
    for i in range(num_cidades):
        for j in range(num_cidades):
            dCidades[i][j] = np.sqrt((data[0, i] - data[0, j]) ** 2 + (data[1, i] - data[1, j]) ** 2)

    resultados_finais = []

    for execucao in range(execucoes):
        print(f"\n=== Execução {execucao + 1} ===")

        # Inicializa população aleatoriamente a cada execução
        populacao = np.array([np.random.permutation(np.arange(1, num_cidades + 1)) for _ in range(cromossomos)])

        for geracao in range(geracoes):
            # Calcula custo para toda população
            matrizComCusto = np.zeros((cromossomos, num_cidades + 1), dtype=float)
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

            # Ordena população pelo custo (aptidão)
            matrizOrdenada = matrizComCusto[matrizComCusto[:, -1].argsort()]

            if (geracao + 1) % 1000 == 0 or geracao == 0 or geracao == geracoes - 1:
                print(f"Geração {geracao + 1}: Melhor custo: {matrizOrdenada[0, -1]}")

            # Seleciona os 10 melhores pais
            top10 = matrizOrdenada[:10]

            # Pesos para seleção probabilística (melhores têm maior chance)
            pesos = np.arange(10, 0, -1)

            indices_pais = np.random.choice(len(top10), size=10, p=pesos / np.sum(pesos))
            pais_selecionados = top10[indices_pais]

            pais_genes = pais_selecionados[:, :-1].astype(int)

            # Forma 5 casais (pai1, pai2)
            casais = pais_genes.reshape(5, 2, -1)

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
            populacao = np.vstack((pais_genes, filhos_mutados))

        # Após as gerações, calcula novamente o custo para registrar o melhor resultado
        matrizComCusto_final = np.zeros((cromossomos, num_cidades + 1), dtype=float)
        for i in range(cromossomos):
            caminho = populacao[i] - 1
            caminho_completo = np.append(caminho, caminho[0])
            custo_total = 0.0
            for j in range(num_cidades):
                origem = caminho_completo[j]
                destino = caminho_completo[j + 1]
                custo_total += dCidades[origem, destino]
            matrizComCusto_final[i, :-1] = populacao[i]
            matrizComCusto_final[i, -1] = custo_total

        matrizOrdenada_final = matrizComCusto_final[matrizComCusto_final[:, -1].argsort()]
        melhor_cromossomo = matrizOrdenada_final[0]

        print(f"Melhor custo final da execução {execucao + 1}: {melhor_cromossomo[-1]}")

        resultados_finais.append(melhor_cromossomo)

    return resultados_finais

if __name__ == "__main__":
    data = np.loadtxt('cidades.mat')
    execucoes = 5  # quantas vezes rodar 10k gerações
    resultados = rodar_genetico_multiplas_execucoes(data, execucoes=execucoes)

    for i, resultado in enumerate(resultados):
        print(f"\nResultado final da execução {i+1}:")
        print("Caminho:", resultado[:-1].astype(int))
        print("Custo:", resultado[-1])
