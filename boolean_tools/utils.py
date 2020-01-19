from boolean import Symbol, NOT, BooleanAlgebra
from itertools import combinations


algebra = BooleanAlgebra()
TRUE, FALSE = algebra.TRUE, algebra.FALSE


def smart_not(expr):

    def eliminate_not(expr):
        if isinstance(expr, NOT) and isinstance(expr.args[0], NOT):
            return eliminate_not(expr.args[0].args[0])
        else:
            return expr

    new_expr = NOT(expr)

    return eliminate_not(new_expr)


def new_variable_generator():
    var_prefix = "__AUXILIARY_VAR__"
    cur_i = 0

    while True:
        yield Symbol(f"{var_prefix}{cur_i}")
        cur_i += 1


#
# Other utils
#
def underscore_text(s):
    return s + '\n' + '=' * len(s)


def upperscore_text(s):
    return '=' * len(s) + '\n' + s


def binarize_expression(expr):
    expr_type = type(expr)
    if isinstance(expr, Symbol):
        return expr
    if isinstance(expr, NOT):
        return NOT(binarize_expression(expr.args[0]))
    if len(expr.args) == 2:
        return expr_type(
            binarize_expression(expr.args[0]),
            binarize_expression(expr.args[1])
        )
    else:
        return expr_type(
            binarize_expression(expr.args[0]),
            binarize_expression(expr_type(*expr.args[1:]))
        )


def is_pos(x):
    return True if x > 0 else False


def str2expr(x):
    return binarize_expression(BooleanAlgebra().parse(x))
