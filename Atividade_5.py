# -*- coding: utf-8 -*-

class No:
    """
    Representa um nó na Árvore AVL.
    Cada nó armazena uma chave, referências para os filhos e sua altura.
    """
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1 # A altura de um novo nó (folha) é sempre 1


class ArvoreAVL:
    """
    Implementa a estrutura e as operações de uma Árvore AVL.
    """
    def __init__(self):
        self.raiz = None

    # ===============================================================
    # MÉTODOS AUXILIARES E ROTAÇÕES
    # ===============================================================

    def obter_altura(self, no):
        """Calcula a altura de um nó. Se o nó for nulo, a altura é 0."""
        if not no:
            return 0
        return no.altura

    def obter_fator_balanceamento(self, no):
        """Fator de balanceamento = altura(esquerda) - altura(direita)."""
        if not no:
            return 0
        return self.obter_altura(no.esquerda) - self.obter_altura(no.direita)

    def _atualizar_altura(self, no):
        """Atualiza a altura do nó com base nos filhos."""
        no.altura = 1 + max(self.obter_altura(no.esquerda),
                            self.obter_altura(no.direita))

    def obter_no_valor_minimo(self, no):
        """Retorna o nó com o menor valor em uma subárvore (mais à esquerda)."""
        atual = no
        while atual.esquerda:
            atual = atual.esquerda
        return atual

    def _rotacao_direita(self, y):
        """Rotação simples à direita."""
        x = y.esquerda
        T2 = x.direita

        # Rotacionar
        x.direita = y
        y.esquerda = T2

        # Atualizar alturas
        self._atualizar_altura(y)
        self._atualizar_altura(x)

        return x

    def _rotacao_esquerda(self, x):
        """Rotação simples à esquerda."""
        y = x.direita
        T2 = y.esquerda

        # Rotacionar
        y.esquerda = x
        x.direita = T2

        # Atualizar alturas
        self._atualizar_altura(x)
        self._atualizar_altura(y)

        return y

    # ===============================================================
    # INSERÇÃO
    # ===============================================================

    def inserir(self, chave):
        """Método público para inserir uma chave na árvore."""
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no_atual, chave):
        # Inserção padrão de BST
        if not no_atual:
            return No(chave)
        elif chave < no_atual.chave:
            no_atual.esquerda = self._inserir_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._inserir_recursivo(no_atual.direita, chave)
        else:
            raise ValueError("Chave duplicada não permitida na AVL.")

        # Atualizar altura
        self._atualizar_altura(no_atual)

        # Verificar balanceamento
        balance = self.obter_fator_balanceamento(no_atual)

        # Caso 1: Esquerda-Esquerda
        if balance > 1 and chave < no_atual.esquerda.chave:
            return self._rotacao_direita(no_atual)

        # Caso 2: Direita-Direita
        if balance < -1 and chave > no_atual.direita.chave:
            return self._rotacao_esquerda(no_atual)

        # Caso 3: Esquerda-Direita
        if balance > 1 and chave > no_atual.esquerda.chave:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Caso 4: Direita-Esquerda
        if balance < -1 and chave < no_atual.direita.chave:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    # ===============================================================
    # DELEÇÃO
    # ===============================================================

    def deletar(self, chave):
        """Método público para deletar uma chave da árvore."""
        self.raiz = self._deletar_recursivo(self.raiz, chave)

    def _deletar_recursivo(self, no_atual, chave):
        # 1. Deleção padrão BST
        if not no_atual:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esquerda = self._deletar_recursivo(no_atual.esquerda, chave)
        elif chave > no_atual.chave:
            no_atual.direita = self._deletar_recursivo(no_atual.direita, chave)
        else:
            # Nó encontrado
            if not no_atual.esquerda:
                return no_atual.direita
            elif not no_atual.direita:
                return no_atual.esquerda
            else:
                sucessor = self.obter_no_valor_minimo(no_atual.direita)
                no_atual.chave = sucessor.chave
                no_atual.direita = self._deletar_recursivo(no_atual.direita, sucessor.chave)

        if not no_atual:
            return no_atual

        # 2. Atualizar altura
        self._atualizar_altura(no_atual)

        # 3. Verificar balanceamento
        balance = self.obter_fator_balanceamento(no_atual)

        # Caso 1: Esquerda-Esquerda
        if balance > 1 and self.obter_fator_balanceamento(no_atual.esquerda) >= 0:
            return self._rotacao_direita(no_atual)

        # Caso 2: Esquerda-Direita
        if balance > 1 and self.obter_fator_balanceamento(no_atual.esquerda) < 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        # Caso 3: Direita-Direita
        if balance < -1 and self.obter_fator_balanceamento(no_atual.direita) <= 0:
            return self._rotacao_esquerda(no_atual)

        # Caso 4: Direita-Esquerda
        if balance < -1 and self.obter_fator_balanceamento(no_atual.direita) > 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    # ===============================================================
    # BUSCAS
    # ===============================================================

    def encontrar_nos_intervalo(self, chave1, chave2):
        """Retorna todas as chaves no intervalo [chave1, chave2]."""
        resultado = []
        self._buscar_intervalo(self.raiz, chave1, chave2, resultado)
        return resultado

    def _buscar_intervalo(self, no, chave1, chave2, resultado):
        if not no:
            return
        if chave1 < no.chave:
            self._buscar_intervalo(no.esquerda, chave1, chave2, resultado)
        if chave1 <= no.chave <= chave2:
            resultado.append(no.chave)
        if chave2 > no.chave:
            self._buscar_intervalo(no.direita, chave1, chave2, resultado)

    def obter_profundidade_no(self, chave):
        """Calcula a profundidade de um nó com a chave dada."""
        return self._profundidade_recursiva(self.raiz, chave, 0)

    def _profundidade_recursiva(self, no, chave, nivel):
        if not no:
            return -1
        if chave == no.chave:
            return nivel
        elif chave < no.chave:
            return self._profundidade_recursiva(no.esquerda, chave, nivel + 1)
        else:
            return self._profundidade_recursiva(no.direita, chave, nivel + 1)


# --- Bloco de Teste e Demonstração da Atividade AVL ---
if __name__ == "__main__":
    arvore_avl = ArvoreAVL()
    
    print("\n--- ATIVIDADE PRÁTICA: ÁRVORE AVL ---")
    
    print("\n--- 1. Inserindo nós ---")
    chaves_para_inserir = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for chave in chaves_para_inserir:
            arvore_avl.inserir(chave)
        print("Inserção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A INSERÇÃO: {e}")

    print("\n--- 2. Deletando nós ---")
    try:
        chaves_para_deletar = [10, 11]
        for chave in chaves_para_deletar:
            arvore_avl.deletar(chave)
        print("Deleção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A DELEÇÃO: {e}")

    print("\n--- 3. Buscando nós no intervalo [1, 9] ---")
    try:
        nos_no_intervalo = arvore_avl.encontrar_nos_intervalo(1, 9)
        print(f"Nós encontrados: {sorted(nos_no_intervalo)}")
    except Exception as e:
        print(f"\nERRO DURANTE A BUSCA POR INTERVALO: {e}")

    print("\n--- 4. Calculando profundidade do nó 6 ---")
    try:
        profundidade = arvore_avl.obter_profundidade_no(6)
        if profundidade != -1:
            print(f"O nó 6 está no nível/profundidade: {profundidade}")
        else:
            print("O nó 6 não foi encontrado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE PROFUNDIDADE: {e}")
