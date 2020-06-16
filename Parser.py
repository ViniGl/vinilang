from Pre_pros import Pre_process
from Tokenizer import Tokenizer, Token
from Node import *
import sys


class Parser:

    tokens = ""

    # PROGRAM
    @staticmethod
    def parseProgram():
        if Parser.tokens.actual.value == "<?viniLang":
            Parser.tokens.select_next()
            commands = Parser.parseCommand()
            if Parser.tokens.actual.value != "?>":
                raise Exception("?> delimiter not found")

            Parser.tokens.select_next()
            return commands
        else:
            raise Exception("{ delimiter not found")

    # TERM
    @staticmethod
    def parseTerm():
        resultado_mult = Parser.parseFactor()
        Parser.tokens.select_next()

        while Parser.tokens.actual.value == "*" or Parser.tokens.actual.value == "/" or Parser.tokens.actual.value == "and":
            if Parser.tokens.actual.value == "*":
                node = BinOp("*", [])
                node.children.append(resultado_mult)
                Parser.tokens.select_next()
                node.children.append(Parser.parseFactor())

            elif Parser.tokens.actual.value == "/":
                node = BinOp("/", [])
                node.children.append(resultado_mult)
                Parser.tokens.select_next()
                node.children.append(Parser.parseFactor())

            elif Parser.tokens.actual.value == "and":
                node = LogOp("and", [])
                node.children.append(resultado_mult)
                Parser.tokens.select_next()
                node.children.append(Parser.parseFactor())

            resultado_mult = node

            Parser.tokens.select_next()

        return resultado_mult

    # FACTOR
    @staticmethod
    def parseFactor():
        resultado_factor = 0

        if isinstance(Parser.tokens.actual.value, int):
            resultado_factor = Parser.tokens.actual.value
            node = IntVal(resultado_factor)
            return node

        elif Parser.tokens.actual.value == "+":
            node = UnaryOp("+", [])
            Parser.tokens.select_next()
            node.children.append(Parser.parseFactor())
            return node

        elif Parser.tokens.actual.value == "-":
            node = UnaryOp("-", [])
            Parser.tokens.select_next()
            node.children.append(Parser.parseFactor())
            return node

        elif Parser.tokens.actual.value == "!":
            node = LogOp("!", [])
            Parser.tokens.select_next()
            node.children.append(Parser.parseFactor())
            return node

        elif Parser.tokens.actual.token_type == "BOOL":
            node = BoolVal(Parser.tokens.actual.value, [])
            return node

        elif Parser.tokens.actual.token_type == "STRING":
            node = StringVal(Parser.tokens.actual.value, [])
            return node

        elif Parser.tokens.actual.value == '(':
            Parser.tokens.select_next()
            resultado_factor = Parser.parseRelExpression()
            if Parser.tokens.actual.value == ')':

                return resultado_factor

        elif Parser.tokens.actual.value == "tupni":
            rl_node = ReadLineOp('tupni', [])
            Parser.tokens.select_next()
            if Parser.tokens.actual.value == '(':
                Parser.tokens.select_next()
                if Parser.tokens.actual.value == ')':
                    pass
                else:
                    raise Exception(") not found after tupni")
            else:
                raise Exception("( not found after tupni")

            return rl_node

        elif "$" in Parser.tokens.actual.value:
            return VarName(Parser.tokens.actual.value)

        elif Parser.tokens.actual.token_type == "FuncName":

            name = Parser.tokens.actual.value
            func_call = FuncCall(name, [])

            Parser.tokens.select_next()

            if (Parser.tokens.actual.value == "("):
                Parser.tokens.select_next()

                while Parser.tokens.actual.value != ")":

                    func_call.children.append(Parser.parseRelExpression())

                    if Parser.tokens.actual.value == ",":
                        Parser.tokens.select_next()
                return func_call

            else:
                raise Exception("Expected (")

        else:
            raise Exception("No options on Factor")

    # EXPRESSION
    @staticmethod
    def parseExpression():
        Parser.resultado = Parser.parseTerm()

        while Parser.tokens.actual.value == "+" or Parser.tokens.actual.value == "-" or Parser.tokens.actual.value == "or" or Parser.tokens.actual.value == ".":
            if Parser.tokens.actual.value == "+":
                node = BinOp("+", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseTerm())

            elif Parser.tokens.actual.value == "-":
                node = BinOp("-", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseTerm())

            elif Parser.tokens.actual.value == "or":
                node = LogOp("or", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseTerm())

            elif Parser.tokens.actual.value == ".":
                node = BinOp(".", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseTerm())

            Parser.resultado = node

        return Parser.resultado

    # RelEXPRESSION
    @staticmethod
    def parseRelExpression():
        Parser.resultado = Parser.parseExpression()

        while Parser.tokens.actual.value == "==" or Parser.tokens.actual.value == "<" or Parser.tokens.actual.value == ">":
            if Parser.tokens.actual.value == "==":
                node = LogOp("==", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseExpression())

            elif Parser.tokens.actual.value == "<":
                node = LogOp("<", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseExpression())

            elif Parser.tokens.actual.value == ">":
                node = LogOp(">", [])
                node.children.append(Parser.resultado)
                Parser.tokens.select_next()
                node.children.append(Parser.parseExpression())

            Parser.resultado = node

        return Parser.resultado

    # BLOCK
    @staticmethod
    def parseBlock():
        if Parser.tokens.actual.value == "{":
            commands = Commands("Commands")
            Parser.tokens.select_next()
            while(Parser.tokens.actual.value != "}"):
                cmd = Parser.parseCommand()

                if cmd is not None:
                    commands.children.append(cmd)

                if Parser.tokens.actual.value == ";":
                    Parser.tokens.select_next()

            if Parser.tokens.actual.value != "}":
                raise Exception("} delimiter not found")

            Parser.tokens.select_next()
            return commands
        else:
            raise Exception("{ delimiter not found")

    # COMMAND
    @staticmethod
    def parseCommand():

        if Parser.tokens.actual.value == ";":
            pass

        elif Parser.tokens.actual.token_type == "VARIABLE":
            var_name = Parser.tokens.actual.value
            var_node = VarName(var_name, [])

            Parser.tokens.select_next()

            if Parser.tokens.actual.value == "=":
                assign = Assignment("=", [])
                assign.children.append(var_node)
                Parser.tokens.select_next()
                value = Parser.parseRelExpression()

                assign.children.append(value)

            else:
                raise Exception("Invalid Syntax")

            if Parser.tokens.actual.value != ";":
                raise Exception("; not found")
            return assign

        elif Parser.tokens.actual.value == "ohce":

            echo_node = Echo("ohce", [])
            Parser.tokens.select_next()
            echo_value = Parser.parseRelExpression()

            echo_node.children.append(echo_value)

            if Parser.tokens.actual.value != ";":
                raise Exception("; not found")

            Parser.tokens.select_next()
            return echo_node

        elif Parser.tokens.actual.value == "elihw":
            while_node = LoopOp('elihw', [])
            Parser.tokens.select_next()

            if Parser.tokens.actual.value == '(':
                Parser.tokens.select_next()
                while_node.children.append(Parser.parseRelExpression())

                if Parser.tokens.actual.value == ')':
                    Parser.tokens.select_next()
                    while_node.children.append(Parser.parseCommand())
                else:
                    raise Exception(") not found on while statment")

            else:
                raise Exception("( not found on while statment")

            return while_node

        elif Parser.tokens.actual.value == "fi":
            cond_node = IfOp('fi', [])
            Parser.tokens.select_next()

            if Parser.tokens.actual.value == '(':
                Parser.tokens.select_next()
                cond_node.children.append(Parser.parseRelExpression())

                if Parser.tokens.actual.value == ')':
                    Parser.tokens.select_next()
                    cond_node.children.append(Parser.parseCommand())
                else:
                    raise Exception(") not found on if clause")
            else:
                raise Exception("( not found on If clause")

            if Parser.tokens.actual.value == 'esle':
                Parser.tokens.select_next()
                cond_node.children.append(Parser.parseCommand())

            return cond_node

        elif Parser.tokens.actual.value == "fed":

            Parser.tokens.select_next()

            if Parser.tokens.actual.token_type == "FuncName":
                name = Parser.tokens.actual.value
                func_node = FuncDec(name, [])

                Parser.tokens.select_next()

                if Parser.tokens.actual.value == "(":
                    args = []
                    Parser.tokens.select_next()
                    if Parser.tokens.actual.value != ')':
                        while (Parser.tokens.actual.value != ")"):
                            func_node.children.append(
                                Parser.parseRelExpression())
                            # Parser.tokens.select_next()

                            if Parser.tokens.actual.value == ",":
                                Parser.tokens.select_next()

                    Parser.tokens.select_next()
                    func_node.children.append(Parser.parseCommand())

                    return func_node
                else:
                    raise Exception("( required on function declaration")
            else:
                raise Exception("Invalid function name")

        elif Parser.tokens.actual.token_type == "FuncName":

            name = Parser.tokens.actual.value
            func_call = FuncCall(name, [])

            Parser.tokens.select_next()

            if (Parser.tokens.actual.value == "("):
                Parser.tokens.select_next()

                while Parser.tokens.actual.value != ")":
                    func_call.children.append(Parser.parseRelExpression())
                    if Parser.tokens.actual.value == ",":
                        Parser.tokens.select_next()

                Parser.tokens.select_next()
                return func_call
            else:
                raise Exception("Expected (")

        elif Parser.tokens.actual.value == "nruter":

            return_node = ReturnOp('nruter', [])

            Parser.tokens.select_next()

            return_node.children.append(Parser.parseRelExpression())

            Parser.tokens.select_next()
            return return_node

        else:
            return Parser.parseBlock()

    @staticmethod
    def run(code):

        code = Pre_process.filter(code)
        Parser.tokens = Tokenizer(code)
        resultado = Parser.parseProgram()

        if Parser.tokens.actual.value != 'eof':
            raise Exception("EOF not reached")

        return resultado
