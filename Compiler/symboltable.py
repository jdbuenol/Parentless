class symbol_table:
    symbols : dict = {}

    def __init__(self) -> None:
        pass

    def append(self, s : str, type : str) -> None:
        self.symbols[s] = str
    
    def contains(self, s : str) -> bool:
        return s in self.symbols
    
    def get(self, s : str) -> str:
        return self.symbols[s]