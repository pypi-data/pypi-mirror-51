
import casadi as cs
# noinspection PyUnresolvedReferences
from casadi.casadi import SX

import os
import warnings
import numpy as np
import symbtools as st

from sympy.printing.lambdarepr import lambdarepr, LambdaPrinter


class CassadiPrinter(LambdaPrinter):
    """
    This subclass serves to convert scalar sympy expressions to casady functions.

    It is strongly inspired by sympy.printing.lambdarepr.NumExprPrinter
    """
    _default_settings = {'fully_qualified_modules': False, 'inline': True,
                         'allow_unknown_functions': True, 'order': None,
                         'human': True,
                         'full_prec': True,
                         'user_functions': {}}

    printmethod = "_numexprcode"

    _numexpr_functions = {
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'asin': 'arcsin',
        'acos': 'arccos',
        'atan': 'arctan',
        'atan2': 'arctan2',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'asinh': 'arcsinh',
        'acosh': 'arccosh',
        'atanh': 'arctanh',
        'log': 'log',
        'exp': 'exp',
        'sqrt': 'sqrt',
        'Abs': 'fabs',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # a few functions are called differently in sympy and casadi
        # here we create the mapping {a: b, ...} where a is the name of the sympy func and b the name of cs func
        self.cs_func_keys = dict([(key, value) for key, value in self._numexpr_functions.items()])

        # some functions simply do not exisit in casadi
        self.unsupported_funcs = ["conjugate", "im", "re", "where", "complex", "contains"]
        for k in self.unsupported_funcs:
            pass
            # del self.cs_func_keys[k]

        self.cs_funcs = dict([(value, getattr(cs, value)) for key, value in self.cs_func_keys.items()])

        for k in self._numexpr_functions:
            setattr(self, '_print_%s' % k, self._print_Function)

    def _print_Function(self, e):
        func_name = e.func.__name__

        nstr = self._numexpr_functions.get(func_name, None)
        if nstr is None:
            raise TypeError("numexpr does not support function '%s'" %
                                func_name)
        return "%s(%s)" % (nstr, self._print_seq(e.args))

    def _print_seq(self, seq, delimiter=', '):
        s = [self._print(item) for item in seq]
        if s:
            return delimiter.join(s)
        else:
            return ""


def casidify(expr, state_vect, input_vect):
    # source: https://gist.github.com/cklb/60362e1f49ef65f5212fb5eb5904b3fd
    """
    Convert a sympy-expression into a casadi expression. This is used by create_casadi_func(...).

    :param expr:        symbolic expression which is to convert to casadi
    :param state_vect:  symbolic state vector
    :param input_vect:  symbolic input vector
    """

    syms = []
    res = ["rhs = vertcat("]
    state_str = ["x = vertcat("]
    input_str = ["u = vertcat("]

    # extract symbols
    for _s in state_vect:
        syms.append("{0} = SX.sym('{0}')".format(str(_s)))
        state_str.append(str(_s) + ", ")

    for _s in input_vect:
        syms.append("{0} = SX.sym('{0}')".format(str(_s)))
        input_str.append(str(_s) + ", ")

    state_str.append(")")
    input_str.append(")")

    # convert expression
    CP = CassadiPrinter()
    for entry in expr:
        # handle expr
        _expr = CP.doprint(entry)
        res.append(_expr + ", ")

    res.append(")")

    ode_str = os.linesep.join(syms
                              + res
                              + state_str
                              + input_str)

    scope = dict(SX=cs.SX, MX=cs.MX, vertcat=cs.vertcat, **CP.cs_funcs)
    exec(ode_str, scope)

    return scope["rhs"], scope["x"], scope["u"]


def create_casadi_func(sp_expr, sp_vars, sp_uu=None, name="cs_from_sp"):
    """

    :param sp_expr:     sympy expression which should be converted
    :param sp_vars:     sequence of sympy vars e.g. ( x1, x2, x3, x4, u1, lmd1 ) for a Lagrangian system model with
                        state_dim = 4, input_dim = 1, constraint_dim = 1
    :param sp_uu:       sequence of input variables (deprecated) put inputs into `sp_vars`
    :param name:
    :return:            callable casadi function
    """

    multiple_args = True
    if sp_uu is None:
        sp_uu = []
        multiple_args = False
    else:
        msg = "passing parameter `sp_uu` is deprecated and will not work in future symbtools releases anymore. "\
              "Please see the docstring of `create_casadi_func()` on how to pass input (and other variables)"
        warnings.warn(msg, DeprecationWarning)

    expr_cs, xx_cs, uu_cs = casidify(sp_expr, sp_vars, sp_uu)
    if multiple_args:
        func_cs = cs.Function(name, (xx_cs, uu_cs), (expr_cs,))
    else:
        func_cs = cs.Function(name, (xx_cs,), (expr_cs,))

    func_cs.xx = xx_cs
    func_cs.uu = uu_cs

    return func_cs


# convenience functions (maybe there is a more elegant way)

# noinspection PyPep8Naming
def seq_to_SX_matrix(seq):
    """
    In many cases this is equivalent to cs.vertcat.
    """
    n = len(seq)

    # leading element:
    e0 = SX(seq[0])
    if e0.shape == (1, 1):
        # we have a sequence of scalars and create a column vector
        res = SX(n, 1)
        for i, elt in enumerate(seq):
            res[i, 0] = elt
        return res
    else:
        # we assume we have a sequence of vectors and want to concatenate them (colstack)
        n1, n2 = e0.shape
        res = SX(n1, n2*n)
        for i, elt in enumerate(seq):
            res[:, i] = elt
        return res


# noinspection PyPep8Naming
def SX_diag_matrix(seq):
    n = len(seq)
    res = SX.zeros(n, n)
    for i, elt in enumerate(seq):
        res[i, i] = elt
    return res


def unpack(sx_matrix):
    """
    convert SX matrix (vector) to list
    """
    n1, n2 = sx_matrix.shape
    assert n2 == 1
    res = [sx_matrix[i, 0] for i in range(n1)]
    return res


def distribute(in_data, *shapes):
    """
    Return sequence of arrays which have shapes as in `shapes` and together contain the data in `in_data`.

    Call like so: distribute(arr, (1, 2), (7,) (100, 7))


    # NOTE: casadi has a different reshape behavior than numpy.

    This is useful for easy acces to the optimization results of e.g. casadi.

    :param in_data: (almost) flat array
    :param shapes: sequence of shapes
    :return:
    """

    assert isinstance(shapes[0], (tuple, list, np.ndarray))

    len_list = [np.prod(s) for s in shapes]

    # assert that in_data is almost flat (all but one dims are 1)

    assert np.count_nonzero(np.array(in_data.shape) - 1) in (1, 0)

    if isinstance(in_data, np.ndarray):
        in_data = np.array(in_data).squeeze()
        order = "C"
    else:
        order = "F"

    assert sum(len_list) == np.prod(in_data.shape)

    start = 0
    res = []
    for s, l in zip(shapes, len_list):
        d = in_data[start:start+l]

        if np.prod(d.shape) == 1:
            d = np.array(d)

        res.append(np.array(d).reshape(s, order=order))

        start += l

    return res






