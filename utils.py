import numpy as np


def corrigir_duplicatas(filho, outro_pai, indice_inicial):
    valor_atual = outro_pai[indice_inicial]  # o valor que foi inserido no filho
    pos_atual = indice_inicial

    while True:
        # Encontra todas as posições onde o valor atual aparece no filho
        posicoes = np.where(filho == valor_atual)[0]

        # Remove a posição original da lista (deixando só a duplicata)
        pos_duplicadas = [p for p in posicoes if p != pos_atual]

        if not pos_duplicadas:
            break  # Não tem mais duplicata, fim da correção

        # Pega a duplicata
        pos_duplicada = pos_duplicadas[0]

        # Substitui pelo valor do outro pai na mesma posição
        novo_valor = outro_pai[pos_duplicada]
        filho[pos_duplicada] = novo_valor

        # Atualiza para verificar se o novo valor também está duplicado
        valor_atual = novo_valor
        pos_atual = pos_duplicada

def gerar_filhos_com_crossover(casal):
    pai1 = casal[0]
    pai2 = casal[1]

    local_aleatorio = np.random.randint(0, len(pai1))

    #Copia inicial sem alteração
    filho1 = pai1.copy()
    filho2 = pai2.copy()

    # Troca o gene no índice aleatório entre os pais
    filho1[local_aleatorio] = pai2[local_aleatorio]
    filho2[local_aleatorio] = pai1[local_aleatorio]

    # Corrige duplicatas nos filhos
    corrigir_duplicatas(filho1, pai2, local_aleatorio)
    corrigir_duplicatas(filho2, pai1, local_aleatorio)

#    print("Após correção de duplicatas:")
#    print("Filho 1 corrigido:", filho1)
#    print("Filho 2 corrigido:", filho2)

    return filho1, filho2

def mutacao(populacao):
    nova_populacao = populacao.copy()
    tamanho = populacao.shape[1]  # número de genes por cromossomo

    for i in range(len(nova_populacao)):
        # escolhe duas posições aleatórias distintas para trocar
        pos1, pos2 = np.random.choice(tamanho, size=2, replace=False)
        # troca os valores
        nova_populacao[i, pos1], nova_populacao[i, pos2] = nova_populacao[i, pos2], nova_populacao[i, pos1]

    return nova_populacao
