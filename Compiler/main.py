from io import FileIO
from sys import argv
from tokenizer import tokenizer
from checker import checker

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
    checker : checker = checker(token_stream)
    if(checker.parse()):
        print("SUCCESFULLY PARSED")
    else:
        print()