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