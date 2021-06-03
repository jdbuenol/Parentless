from io import FileIO
from sys import argv
import token
from token import token
from tokenizer import tokenizer

if __name__ == '__main__':
    if len(argv) != 2:
        print("Please, execute this file in the following form: 'python main.py <path/to/the/file>'")
        exit()
    path : str = argv[1]
    if path.split('.')[-1] != "pless":
        print("Wrong extension, expected 'file.pless'")
        exit()
    
    script : FileIO = open(path)
    token_stream : tokenizer = tokenizer(script)