from boolean import Symbol, NOT


#
# Tseytin utils
#
def smart_not(expr):

    def eliminate_not(expr):
        if isinstance(expr, NOT) and isinstance(expr.args[0], NOT):
            return eliminate_not(expr.args[0].args[0])
        else:
            return expr

    new_expr = NOT(expr)

    return eliminate_not(new_expr)


def new_variable_generator():
    var_prefix = "__fake_var__"
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
