# atividade_4.py

import random
from graphviz import Digraph


# -------------------------------
# Classe Nó AVL
# -------------------------------
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # usado para calcular balanceamento


# -------------------------------
# Classe Árvore AVL
# -------------------------------
class AVLTree:
    def __init__(self):
        self.root = None

    # ---------------------------
    # Funções auxiliares
    # ---------------------------
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # ---------------------------
    # Rotações
    # ---------------------------
    def rotate_right(self, y):
        print(f"Rotação à direita em {y.value}")
        x = y.left
        T2 = x.right

        # Rotacionar
        x.right = y
        y.left = T2

        # Atualizar alturas
        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        print(f"Rotação à esquerda em {x.value}")
        y = x.right
        T2 = y.left

        # Rotacionar
        y.left = x
        x.right = T2

        # Atualizar alturas
        self.update_height(x)
        self.update_height(y)

        return y

    # ---------------------------
    # Inserção com balanceamento
    # ---------------------------
    def insert(self, root, value):
        # Inserção normal de BST
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        # Atualizar altura
        self.update_height(root)

        # Verificar balanceamento
        balance = self.get_balance(root)

        # Caso 1: Left Left
        if balance > 1 and value < root.left.value:
            return self.rotate_right(root)

        # Caso 2: Right Right
        if balance < -1 and value > root.right.value:
            return self.rotate_left(root)

        # Caso 3: Left Right
        if balance > 1 and value > root.left.value:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Caso 4: Right Left
        if balance < -1 and value < root.right.value:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def insert_value(self, value):
        self.root = self.insert(self.root, value)

    # ---------------------------
    # Visualização com Graphviz
    # ---------------------------
    def visualize(self, filename="avl_tree"):
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
    print("\n=== Árvore AVL com Rotações Simples ===")
    avl1 = AVLTree()
    for v in [10, 20, 30]:
        avl1.insert_value(v)
        avl1.visualize(f"avl_rotacao_simples_{v}")

    print("\n=== Árvore AVL com Rotação Dupla ===")
    avl2 = AVLTree()
    for v in [10, 30, 20]:
        avl2.insert_value(v)
        avl2.visualize(f"avl_rotacao_dupla_{v}")

    print("\n=== Árvore AVL com Valores Randômicos ===")
    valores_random = random.sample(range(1, 100), 20)
    print("Valores gerados:", valores_random)

    avl_random = AVLTree()
    for v in valores_random:
        avl_random.insert_value(v)

    avl_random.visualize("avl_randomica")
