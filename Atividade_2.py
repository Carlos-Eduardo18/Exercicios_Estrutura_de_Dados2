# atividade_2.py
# Implementacao de Arvore Binaria de Busca (BST)
# Requisitos: pip install graphviz + Graphviz instalado no Windows

import random
from graphviz import Digraph

# Nodo da BST
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Classe Binary Search Tree
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Insercao
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert(node.right, value)
        # se valor igual, nao insere (evita duplicados)

    # Busca
    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return None
        if node.value == value:
            return node
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    # Remocao
    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Caso 1: sem filhos
            if node.left is None and node.right is None:
                return None
            # Caso 2: um filho
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Caso 3: dois filhos
            else:
                sucessor = self._min_value_node(node.right)
                node.value = sucessor.value
                node.right = self._delete(node.right, sucessor.value)
        return node

    def _min_value_node(self, node):
        atual = node
        while atual.left is not None:
            atual = atual.left
        return atual

    # Altura da arvore
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1  # altura de arvore vazia
        return 1 + max(self._height(node.left), self._height(node.right))

    # Profundidade de um valor
    def depth(self, value):
        return self._depth(self.root, value, 0)

    def _depth(self, node, value, nivel):
        if node is None:
            return -1
        if node.value == value:
            return nivel
        elif value < node.value:
            return self._depth(node.left, value, nivel + 1)
        else:
            return self._depth(node.right, value, nivel + 1)

    # Visualizacao com Graphviz
    def visualize(self, filename):
        dot = Digraph(format="png")
        counter = {"i": 0}

        def add_nodes(node, parent_id=None):
            if node is None:
                return
            nid = f"n{counter['i']}"
            counter["i"] += 1
            dot.node(nid, str(node.value), shape="circle")
            if parent_id is not None:
                dot.edge(parent_id, nid)
            add_nodes(node.left, nid)
            add_nodes(node.right, nid)

        add_nodes(self.root)
        output_path = dot.render(filename=filename, cleanup=True)
        print(f"Arvore salva em: {output_path}")

# --------------------------
# Testes das duas arvores
# --------------------------
if __name__ == "__main__":
    # -------- Arvore fixa --------
    print("=== Arvore Fixa ===")
    bst = BinarySearchTree()
    valores_fixos = [55, 30, 80, 20, 45, 70, 90]
    for v in valores_fixos:
        bst.insert(v)

    bst.visualize("bst_fixed")

    # Busca
    print("Busca pelo valor 45:", "Encontrado" if bst.search(45) else "Nao encontrado")

    # Remocao
    print("Removendo 30...")
    bst.delete(30)
    bst.visualize("bst_fixed_after_delete")

    # Nova insercao
    print("Inserindo 60...")
    bst.insert(60)
    bst.visualize("bst_fixed_after_insert")

    # Altura
    print("Altura da arvore:", bst.height())

    # Profundidade
    print("Profundidade do no 45:", bst.depth(45))

    # -------- Arvore randomica --------
    print("\n=== Arvore Randomica ===")
    bst_rand = BinarySearchTree()
    valores_random = random.sample(range(1, 200), 15)
    print("Valores inseridos:", valores_random)
    for v in valores_random:
        bst_rand.insert(v)

    bst_rand.visualize("bst_random")
    print("Altura da arvore randomica:", bst_rand.height())
