import numpy as np

from algoritmo import algoritmoGenetico

if __name__ == "__main__":
    cidades = np.loadtxt('cidades.mat')
    execucoes = 5  # quantas vezes rodar 10k gerações
    resultados = algoritmoGenetico(cidades, execucoes=execucoes)

    for i, resultado in enumerate(resultados):
        # Melhor caminho esperado = entre 3 a 5
        print(f"\nResultado final da execução {i + 1}:")
        caminho_formatado = ", ".join(map(str, resultado[:-1].astype(int)))
        print("Caminho:", caminho_formatado)
        print("Custo:", resultado[-1])
