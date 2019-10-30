"""
functions.py
"""
import numpy as np
from sympy import lambdify, abc, latex, diff, integrate
from sympy.parsing.sympy_parser import parse_expr


class VariableNotFoundError(Exception):
    """Variable not found error.
    """
    def __str__(self) -> None:
        """Print this exception.
        """
        return "Variable not found"


def rect(x: np.ndarray) -> np.ndarray:
    """
    Rectangle function.
    """
    return np.array(
        [
            1.0 if (x_i < 0.5 and x_i > -0.5) else 0.
            for x_i in x
        ]
        )


class Functionx:
    """
    A callable function class that is a function of x,
    as well as any number of parameters

    Attributes:
    latex_repr [str]: The function as a LaTeX string.
    symbols [sympy.Symbol]: All variables used in this function.
    parameters [sympy.Symbol]: All variables used in this function,
                               except for x.
    """

    # Private Attributes:
    # _symbolic_func [sympy.Symbol]: symbol function
    # _lambda_func [sympy.Function]: lamba function

    def __init__(self, function_name: str) -> None:
        """
        The initializer. The parameter must be a
        string representation of a function, and it needs to
        be a function of x.
        """
        # Dictionary of modules and user defined functions.
        # Used for lambdify from sympy to parse input.
        module_list = ["numpy", {"rect": rect}]
        self._symbolic_func = parse_expr(function_name)
        symbol_set = self._symbolic_func.free_symbols
        symbol_list = list(symbol_set)
        if abc.x not in symbol_list:
            raise VariableNotFoundError("x not found - the"
                                        "function inputed must "
                                        "be a function of x.")
        self.latex_repr = latex(self._symbolic_func)
        symbol_list.remove(abc.x)
        self.parameters = symbol_list
        x_list = [abc.x]
        x_list.extend(symbol_list)
        self.symbols = x_list
        self._lambda_func = lambdify(
            self.symbols, self._symbolic_func, modules=module_list)

    def __call__(self, x: np.array, *args: float) -> np.array:
        """
        Call this class as if it were a function.
        """
        return self._lambda_func(x, *args)

    def derivative(self) -> None:
        """
        Mutate this function into its derivative.
        """
        self._symbolic_func = diff(self._symbolic_func,
                                   abc.x)
        self._reset_samesymbols()

    def antiderivative(self) -> None:
        """
        Mutate this function into its antiderivative.
        """
        self._symbolic_func = integrate(self._symbolic_func,
                                        abc.x)
        self._reset_samesymbols()

    def _reset_samesymbols(self) -> None:
        """
        Set to a new function, assuming the same variables.
        """
        self.latex_repr = latex(self._symbolic_func)
        self._lambda_func = lambdify(
            self.symbols, self._symbolic_func)


if __name__ == "__main__":
    f = Functionx("a*sin(k*x) + d")
    f.antiderivative()
    print(f.latex_repr)
    print(f._symbolic_func)
