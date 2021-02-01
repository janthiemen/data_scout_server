from __future__ import division

from .transformation import Transformation
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import re
import operator

__author__ = 'Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__ = '''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''


class Custom(Transformation):
    """
    Most of this code comes from the fourFn.py pyparsing example
    """

    title = "Custom equation"
    key = "Math equation"
    fields = {
        "equation": {"name": "Equation", "type": "string", "help": "The equation to evaluate. Column values should be entered as {COLUMN NAME}",
                     "required": True, "input": "text", "default": ""},
        "output": {"name": "Output column", "type": "string", "input": "text", "required": True,
                   "help": "The name of the (newly created) column that contains the results", "default": ""},
    }

    def __init__(self, arguments: dict, sample_size: int, example: dict = None):
        """
        Initialize the transformation with the given parameters.

        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*

        Arguments:
            arguments {dict} -- The arguments
        """
        super().__init__(arguments, sample_size, example)
        self.equation = arguments["equation"]
        self.output = arguments["output"]

        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        mod = Literal("%")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div | mod
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.push_first))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.push_u_minus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
        ZeroOrMore((expop + factor).setParseAction(self.push_first))
        term = factor + \
               ZeroOrMore((multop + factor).setParseAction(self.push_first))
        expr << term + \
        ZeroOrMore((addop + term).setParseAction(self.push_first))
        # addop_term = ( addop + term ).setParseAction( self.push_first )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "%": operator.mod,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.expr_stack = None
        self.fn = {"sin": math.sin,
                   "sinh": math.sinh,
                   "cos": math.cos,
                   "cosh": math.cosh,
                   "tan": math.tan,
                   "tanh": math.tanh,
                   "exp": math.exp,
                   "sqrt": math.sqrt,
                   "radians": math.radians,
                   "degrees": math.degrees,
                   "sign": lambda x: 0 if x == 0 else x / abs(x),
                   "log": math.log10,
                   "ln": math.log,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "floor": math.floor,
                   "ceil": math.ceil,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def push_first(self, strg, loc, toks):
        self.expr_stack.append(toks[0])

    def push_u_minus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.expr_stack.append('unary -')

    def evaluate_stack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluate_stack(s)
        if op in "+-*/^%":
            op2 = self.evaluate_stack(s)
            op1 = self.evaluate_stack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluate_stack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parse_all=True):
        self.expr_stack = []
        results = self.bnf.parseString(num_string, parse_all)
        val = self.evaluate_stack(self.expr_stack[:])
        return val

    def __call__(self, row, index: int):
        """This class is called on each row.

        Arguments:
            row {dict} -- The complete row

        Returns:
            dict -- The row, including the extra output column
        """
        row[self.output] = self.eval(re.sub(r'{(\w+)}', lambda x: str(row.get(x.group(1), 0)), self.equation))

        return row, index
