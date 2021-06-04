# Main class

from io import FileIO
from sys import argv
from typing import final
from tokenizer import tokenizer
from checker import checker
from translator import translate

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
    try:
        if(checker.parse()):
            print("SUCCESFULLY PARSED")
            script.close()
            script2 : FileIO = open(path)
            token_Stream_2 : tokenizer = tokenizer(script2)
            translate(token_Stream_2, checker, path)
        else:
            print()
    except IndexError:
        print("EOF reached while parsing")