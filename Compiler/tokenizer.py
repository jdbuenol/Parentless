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
        for x in self.tokens_list:
            print(x)