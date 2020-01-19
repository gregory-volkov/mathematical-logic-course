from typing import Set
from boolean import Expression, NOT
import logging
from .utils import upperscore_text, is_pos


class CNFWrapper(object):

    def __init__(self, expressions: Set[Expression]):
        self.var2id = {}
        self.id2var = {}
        self.n = 1
        self.expressions = []

        for expr in expressions:
            for var in expr.get_symbols():
                if var not in self.var2id:
                    self.var2id[var] = self.n
                    self.id2var[self.n] = var
                    self.n += 1
            self.expressions.append(self.__encode_expr__(expr))


    def __encode_expr__(self, expr: Expression):
        encoded_expr = set()
        for literal in expr.literals:
            encoded_expr.add(
                (-1 if isinstance(literal, NOT) else 1) *
                self.var2id[literal.get_symbols()[0]])
        return encoded_expr

    def dpll(self):
        logging.info(upperscore_text("STARTING DPLL PROCEDURE"))
        model = self.__dpll__(self.expressions.copy(), {})
        var2val = {}
        if model:
            for k, v in model.items():
                var_name = self.id2var[abs(k)]
                if k > 0:
                    var2val[var_name] = v
                else:
                    var2val[var_name] = (v + 1) % 2
            return var2val
            # return {('' if is_pos(k) else '!') + str(self.id2var[abs(k)]): v for k, v in model.items()}
        else:
            return None

    def __dpll__(self, disjoints, model):
        logging.info(f"Starting disjoints: {disjoints}")
        logging.info(f"Current model: {model}")
        if any(len(s) == 0 for s in disjoints):
            return None

        if len(disjoints) == 0:
            return model

        def check_set(s):
            l_ids = set()
            for disjoint in filter(lambda x: len(x) == 1, s):
                l_id = next(iter(disjoint))
                if -l_id in l_ids:
                    return False
                else:
                    l_ids.add(l_id)
            return True

        def choose_literal(s):
            for disjoint in s:
                for l in disjoint:
                    return l

        def eliminate_pure_literal(s, l_id, from_unit_prop=False):
            res = []
            for disjoint in s:
                if l_id in disjoint:
                    new_disjoint = disjoint.copy()
                    new_disjoint.remove(l_id)
                    if from_unit_prop:
                        res.append(new_disjoint)
                else:
                    res.append(disjoint)
            return res

        def unit_propogate(s, l_id):
            return eliminate_pure_literal([disjoint for disjoint in s if l_id not in disjoint], -l_id, from_unit_prop=True)

        logging.info("Starting unit propogate")
        for disjoint in filter(lambda x: len(x) == 1, disjoints):
            logging.info(f'Disjoint for unit propogate: {disjoint}')
            l_id = next(iter(disjoint))
            disjoints = unit_propogate(disjoints, l_id)
            logging.info(f"After unit_propogate: {disjoints}")
            model[l_id] = 1

        logging.info("Finished unit propogate")

        pure_literals = set()

        for l_id in set().union(*disjoints):
            if -l_id not in pure_literals:
                pure_literals.add(l_id)
            else:
                pure_literals.remove(-l_id)

        logging.info(f"Pure literals: {pure_literals}")
        for l_id in pure_literals:
            logging.info(f"Starting elimination of: {l_id}")
            disjoints = eliminate_pure_literal(disjoints, l_id)
            logging.info(f"After elimination: {disjoints}")
            model[l_id] = 1

        if not check_set(disjoints):
            return None

        l_id = choose_literal(disjoints)
        if l_id is not None:
            _model = model.copy()
            _disjoints = disjoints.copy()
            _model[l_id] = 1
            logging.info(f"Calling DPLL with assuming M[{l_id}] = 1")
            model_1 = self.__dpll__(_disjoints + [{l_id}], _model)
            if model_1 is not None:
                return model_1
            else:
                logging.info(f"Calling DPLL with assuming M[{l_id}] = 0")
                _model = model.copy()
                _disjoints = disjoints.copy()
                _model[l_id] = 0
                return self.__dpll__(_disjoints + [{-l_id}], _model)
        else:
            return self.__dpll__(disjoints, model)
