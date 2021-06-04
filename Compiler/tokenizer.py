# This class is the lexer

from io import FileIO
from token import token

class tokenizer:
    tokens_list : list = []

    def __init__(self, script : FileIO) -> None:
        for x in script:
            current_line : list = x.split(' ')
            if current_line[-1][-1] == '\n':
                current_line[-1] = current_line[-1][:-1]
                current_line.append('\n')
            for y in current_line:
                if len(y) > 0:
                    self.tokens_list.append(token(y))
    
    def is_empty(self) -> bool:
        return len(self.tokens_list) == 0
    
    def pop(self) -> token:
        return self.tokens_list.pop(0)