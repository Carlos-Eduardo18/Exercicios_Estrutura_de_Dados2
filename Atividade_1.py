# atividade_1.py
# Construcao e visualizacao de arvores de expressoes aritmeticas
# Requisitos: pip install graphviz  + Graphviz instalado no sistema

import random
from graphviz import Digraph

# Nodo da arvore
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

# Tokenizer: transforma string em lista de tokens (numeros, operadores, parenteses)
def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c in '()+-*/':
            tokens.append(c)
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
        else:
            # aceitar sinal negativo apenas como parte do numero se necessario
            raise ValueError(f"Caracter invalido no input: '{c}'")
    return tokens

# Parser recursivo (assume expressao totalmente parentizada)
def parse_tokens(tokens):
    # parse retorna (node, proximo_indice)
    def parse_expr(i):
        if tokens[i] == '(':
            i += 1
            left_node, i = parse_expr(i)
            if i >= len(tokens):
                raise ValueError("Expressao incompleta: operador esperado")
            op = tokens[i]
            if op not in '+-*/':
                raise ValueError(f"Operador invalido: {op}")
            i += 1
            right_node, i = parse_expr(i)
            if i >= len(tokens) or tokens[i] != ')':
                raise ValueError("Expressao incompleta: falta ')'")
            node = Node(op, left_node, right_node)
            return node, i + 1
        else:
            # deve ser numero
            token = tokens[i]
            # converte para inteiro
            try:
                val = int(token)
            except:
                raise ValueError(f"Token inesperado ao ler numero: {token}")
            node = Node(val)
            return node, i + 1

    node, next_i = parse_expr(0)
    if next_i != len(tokens):
        raise ValueError("Sobra de tokens apos o parse")
    return node

# Visualizacao usando graphviz
def visualize_tree(root: Node, filename: str):
    dot = Digraph(format='png')
    counter = {'i': 0}

    def add_nodes(node, parent_id=None):
        nid = f"n{counter['i']}"
        counter['i'] += 1
        label = str(node.value)
        # forma diferente para operadores vs operandos
        if node.is_leaf():
            dot.node(nid, label, shape='circle')
        else:
            dot.node(nid, label, shape='box')
        if parent_id is not None:
            dot.edge(parent_id, nid)
        if node.left:
            add_nodes(node.left, nid)
        if node.right:
            add_nodes(node.right, nid)

    add_nodes(root)
    output_path = dot.render(filename=filename, cleanup=True)
    print(f"Arvore salva em: {output_path}")

# Gerador de expressao aleatoria totalmente parentizada
def generate_random_expression(num_operands=3, min_val=1, max_val=99):
    if num_operands < 2:
        raise ValueError("num_operands deve ser >= 2")
    ops = ['+', '-', '*', '/']
    operands = [str(random.randint(min_val, max_val)) for _ in range(num_operands)]
    # combinar aleatoriamente pares adjacentes ate sobrar 1 token
    while len(operands) > 1:
        i = random.randrange(len(operands) - 1)  # escolhe um par adjacente
        left = operands[i]
        right = operands[i+1]
        op = random.choice(ops)
        new = f"( {left} {op} {right} )"
        operands[i:i+2] = [new]
    return operands[0]

# Exemplo de uso: arvore fixa e arvore aleatoria
if __name__ == "__main__":
    # EXPRESSAO FIXA (interpretacao: multiplicacao entre os dois primeiros grupos)
    fixed_expr = "( ( ( 7 + 3 ) * ( 5 - 2 ) ) / ( 10 * 20 ) )"
    print("Expressao fixa (entrada):", fixed_expr)
    tokens = tokenize(fixed_expr)
    root_fixed = parse_tokens(tokens)
    visualize_tree(root_fixed, "tree_fixed")

    # EXPRESSAO RANDOMICA
    random_expr = generate_random_expression(num_operands=4)  # 4 operandos -> 3 operadores min
    print("Expressao rand omica gerada:", random_expr)
    tokens_r = tokenize(random_expr)
    root_random = parse_tokens(tokens_r)
    visualize_tree(root_random, "tree_random")

    print("Concluido. Arquivos gerados: tree_fixed.png e tree_random.png")
