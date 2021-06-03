from terminals import terminals_array as keywords

class token:
    content : str
    terminal : str

    def __init__(self, s : str) -> None:
        self.content = s
        if s in keywords:
            self.terminal = s
        elif s.isnumeric() and '.' in s:
            self.terminal = "float"
        elif s.isnumeric():
            self.terminal = "int"
        elif s.isalnum():
            self.terminal = "symbol"
        elif s == '\n':
            self.terminal = "\\n"
            self.content = "\\n"
        elif (s[0] == '"' or s[0] == "'") and (s[-1] == '"' or s[-1] == "'"):
            self.terminal = "one word str"
        elif s[0] == '"' or s[0] == "'":
            self.terminal = "open str"
        elif s[-1] == '"' or s[-1] == "'":
            self.terminal = "close str"
        else:
            self.terminal = "str"
            print()
    
    def __str__(self) -> str:
        return("content: " + self.content + "\nterminal: " + self.terminal + "\n")