# This class saves the variables and functions names

class symbol_table:
    symbols : dict = {}

    def __init__(self) -> None:
        pass

    def append(self, s : str, type_name : str) -> None:
        self.symbols[s] = type_name
    
    def contains(self, s : str) -> bool:
        return s in self.symbols
    
    def get(self, s : str) -> str:
        return self.symbols[s]
    
    def __str__(self) -> str:
        return str(self.symbols)