from typing import Tuple, Set, Generator
from boolean import Symbol, Expression, NOT, AND, OR
from .utils import new_variable_generator, smart_not, upperscore_text, underscore_text
import logging


# Returns a tuple of literal and set of expressions
def expr2cnf(expr: Expression):
    logging.info(upperscore_text("STARTING TSEYTIN PROCEDURE"))
    var_generator = new_variable_generator()
    result = __tseytin_procedure__(expr, set(), var_generator)
    return result

def __tseytin_procedure__(expr: Expression, delta: Set[Expression], var_generator: Generator):

    if expr.isliteral:
        return expr, delta

    if isinstance(expr, NOT):
        logging.info(f"Calling CNF({expr.args[0]}, {delta})")
        l, _delta = __tseytin_procedure__(expr.args[0], delta, var_generator)
        return_value = smart_not(l), _delta

    if isinstance(expr, AND) or isinstance(expr, OR):
        logging.info(f"Calling CNF({expr.args[0]}, {delta})")
        l1, delta1 = __tseytin_procedure__(expr.args[0], delta, var_generator)

        l2, delta2 = __tseytin_procedure__(expr.args[1], delta1, var_generator)
        logging.info(f"Calling CNF({expr.args[1]}, {delta1})")

        new_var = next(var_generator)

        if isinstance(expr, AND):
            _delta = delta2.union({
                OR(NOT(new_var), l1),
                OR(NOT(new_var), l2),
                OR(smart_not(l1), smart_not(l2), new_var)
            })

        if isinstance(expr, OR):
            t = smart_not(l2)
            _delta = delta2.union({
                OR(OR(NOT(new_var), l1), l2),
                OR(smart_not(l1), new_var),
                OR(t, new_var)
            })

        return_value = (new_var, _delta)

    logging.info(f"Returning CNF({expr}, {delta}) -> {return_value}")
    return return_value
