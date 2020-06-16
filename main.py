import sys
import re
from Parser import Parser
from SymbolTable import *

if __name__ == "__main__":

    eq = sys.argv[1]
    
    if(".php" in eq):
        f = open(eq)
        code = f.read()
        resultado = Parser.run(code)
        st = SymbolTable()
        st_func = SymbolTable()
        resultado = resultado.Evaluate(st, st_func)
    else:
        raise Exception("ERRO")
    

