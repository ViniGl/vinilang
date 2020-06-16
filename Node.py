from SymbolTable import *


class Node:

    def __init__(self, value=None, children=[]):

        self.value = value
        self.children = []

    def Evaluate(self, st, st_func):
        pass


class BinOp(Node):

    def Evaluate(self, st, st_func):

        child_1_result = self.children[0].Evaluate(st, st_func)
        child_2_result = self.children[1].Evaluate(st, st_func)

        if self.value == '+':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', child_1_result[1] + child_2_result[1])
            else:
                raise Exception(f'Operacao de "+" invalida')

        elif self.value == '-':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', child_1_result[1] - child_2_result[1])
            else:
                raise Exception(f'Operacao de "-" invalida')
        elif self.value == '*':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', child_1_result[1] * child_2_result[1])
            else:
                raise Exception(f'Operacao de "*" invalida')

        elif self.value == '/':
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('int', int(child_1_result[1] / child_2_result[1]))
            else:
                raise Exception(f'Operacao de "/" invalida')

        elif self.value == '.':
            return ('string', str(child_1_result[1]) + str(child_2_result[1]))


class UnaryOp(Node):

    def Evaluate(self, st, st_func):

        if self.value == '+':
            return self.children[0].Evaluate(st, st_func)
        else:
            return ('int', -1 * self.children[0].Evaluate(st, st_func)[1])


class IntVal(Node):

    def Evaluate(self, st, st_func):
        return ('int', self.value)


class BoolVal(Node):

    def Evaluate(self, st, st_func):
        return ('bool', self.value)

class StringVal(Node):

    def Evaluate(self, st, st_func):
        return ('string', self.value)


class NoOp(Node):

    def Evaluate(self, st, st_func):
        pass


class Assignment(Node):

    def Evaluate(self, st, st_func):

        expression = self.children[1].Evaluate(st, st_func)

        value = expression[1]
        ty = expression[0]

        var_name = self.children[0].value

        st.setter(var_name, value, ty)


class VarName(Node):

    def Evaluate(self, st, st_func):
        return st.getter(self.value)


class Echo(Node):

    def Evaluate(self, st, st_func):

        expression = self.children[0].Evaluate(st, st_func)

        print(expression[1])


class Commands(Node):

    def Evaluate(self, st, st_func):
        for cmd in self.children:
            if(not st.isSetted("$$RESULT")):
                cmd.Evaluate(st, st_func)


class LogOp(Node):

    def Evaluate(self, st, st_func):

        op = self.value
        child_1_result = self.children[0].Evaluate(st, st_func)

        if(len(self.children) > 1):
            child_2_result = self.children[1].Evaluate(st, st_func)

        if op == "<":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] < child_2_result[1])
            else:
                raise Exception(f'Operacao de "<" invalida')
        
        elif op == ">":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] > child_2_result[1])
            else:
                raise Exception(f'Operacao de ">" invalida')
        
        elif op == "==":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] == child_2_result[1])
            else:
                raise Exception(f'Operacao de "==" invalida')
        
        elif op == "!":
            if child_1_result[0] != 'string':
                return ('bool', not child_1_result[1])
            else:
                raise Exception(f'Operacao de "!" invalida')
        
        elif op == "or":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] or child_2_result[1])
            else:
                raise Exception(f'Operacao de "or" invalida')
        
        elif op == "and":
            if child_1_result[0] != 'string' and child_2_result != "string":
                return ('bool', child_1_result[1] and child_2_result[1])
            else:
                raise Exception(f'Operacao de "and" invalida')


class LoopOp(Node):

    def Evaluate(self, st, st_func):
        cond = self.children[0].Evaluate(st, st_func)
        while (cond[1]):
            self.children[1].Evaluate(st, st_func)
            cond = self.children[0].Evaluate(st, st_func)



class IfOp(Node):

    def Evaluate(self, st, st_func):

        cond = self.children[0].Evaluate(st, st_func)
        if (cond[1]):
            self.children[1].Evaluate(st, st_func)

        else:
            if len(self.children) > 2:
                self.children[2].Evaluate(st, st_func)


class ReadLineOp(Node):

    def Evaluate(self, st, st_func):
        return ('int', int(input()))

class FuncDec(Node):
    def Evaluate(self, st, st_func):
        name = self.value

        args = self.children

        st_func.setter(name, args, "FuncDec")

class FuncCall(Node):

    def Evaluate(self, st, st_func):
        
        name = self.value

        args = self.children

        func_dec = st_func.getter(name)

        args_dec = func_dec[1]

        if len(args_dec[0:-1]) != len(args):
            raise Exception ("Invalid number of arguments") 

        st_local = SymbolTable()

        for i in range(len(args)):
            args_value = args[i].Evaluate(st, st_func)
            st_local.setter(args_dec[i].value, args_value[1], args_value[0])
        
        func_call = args_dec[-1]

        func_call.Evaluate(st_local, st_func)

        if st_local.isSetted("$$RESULT"):
            result = st_local.getter("$$RESULT")
            return result

class ReturnOp(Node):

    def Evaluate(self, st, st_func):
        
        result = self.children[0].Evaluate(st, st_func)
        st.setter("$$RESULT", result[1], result[0])

