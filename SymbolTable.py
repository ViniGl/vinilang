class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def isSetted(self, name):
        
        if(name in self.symbols):
            return True
        return False 

    def setter(self, name, value, typ):
        self.symbols[name] = (typ, value)

    def getter(self, name):
        return self.symbols[name]