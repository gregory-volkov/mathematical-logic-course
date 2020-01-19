from itertools import combinations
from .CNFWrapper import CNFWrapper
from .tseytin_transform import expr2cnf
from .utils import str2expr


def clique_colors(color_num, nodes_num):
    conjuncts = []
    conjuncts_colors = []
    colors = set(range(color_num))

    for i, j, k in combinations(range(nodes_num), 3):
        for color in colors:
            s = f"(a_{i}_{j}_{color} & a_{j}_{k}_{color} & a_{i}_{k}_{color})"
            conjuncts.append(s)

    if conjuncts:
        expr1 = f"!({'|'.join(conjuncts)})"
    else:
        expr1 = ''

    for i, j in combinations(range(nodes_num), 2):
        temp_conjucts = []
        for color in colors:
            s = f"(a_{i}_{j}_{color}"
            if len(colors) > 1:
                s += f" & {' & '.join(f'!a_{i}_{j}_{_color}' for _color in colors.difference({color}))})"
            else:
                s += ')'
            temp_conjucts.append(s)
        conjuncts_colors.append(f"({' | '.join(temp_conjucts)})")

    expr2 = f"({' & '.join(conjuncts_colors)})"

    if expr1:
        expr = expr1 + ' & ' + expr2
    else:
        expr = expr2

    t = str2expr(expr)
    disjoint_set = expr2cnf(t)
    a = CNFWrapper(disjoint_set)
    return a.dpll()
