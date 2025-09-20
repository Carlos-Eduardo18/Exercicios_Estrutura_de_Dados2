# atividade_3.py

import random
from graphviz import Digraph


# -------------------------------
# Classe Nó da Árvore
# -------------------------------
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# -------------------------------
# Classe Árvore Binária de Busca
# -------------------------------
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Inserção
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)

    # Travessias
    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
        return result

    def preorder(self):
        return self._preorder(self.root, [])

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result

    def postorder(self):
        return self._postorder(self.root, [])

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
        return result

    # Visualização da árvore com Graphviz
    def visualize(self, filename="tree"):
        dot = Digraph()
        self._add_nodes(dot, self.root)
        dot.render(filename, format="png", cleanup=True)
        print(f"Árvore salva como {filename}.png")

    def _add_nodes(self, dot, node):
        if node:
            dot.node(str(node.value))
            if node.left:
                dot.edge(str(node.value), str(node.left.value))
                self._add_nodes(dot, node.left)
            if node.right:
                dot.edge(str(node.value), str(node.right.value))
                self._add_nodes(dot, node.right)


# -------------------------------
# Demonstração
# -------------------------------
if __name__ == "__main__":
    # ---- Árvore com valores fixos ----
    print("\n=== Árvore com Valores Fixos ===")
    valores_fixos = [55, 30, 80, 20, 45, 70, 90]
    bst_fixa = BinarySearchTree()
    for v in valores_fixos:
        bst_fixa.insert(v)

    bst_fixa.visualize("arvore_fixa")

    print("In-Order (Esquerda-Raiz-Direita):", bst_fixa.inorder())
    print("Pre-Order (Raiz-Esquerda-Direita):", bst_fixa.preorder())
    print("Post-Order (Esquerda-Direita-Raiz):", bst_fixa.postorder())

    # ---- Árvore com valores randômicos ----
    print("\n=== Árvore com Valores Randômicos ===")
    valores_random = random.sample(range(1, 100), 10)
    print("Valores gerados:", valores_random)

    bst_random = BinarySearchTree()
    for v in valores_random:
        bst_random.insert(v)

    bst_random.visualize("arvore_randomica")

    print("In-Order (Esquerda-Raiz-Direita):", bst_random.inorder())
    print("Pre-Order (Raiz-Esquerda-Direita):", bst_random.preorder())
    print("Post-Order (Esquerda-Direita-Raiz):", bst_random.postorder())
