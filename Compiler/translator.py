# This class translates from "Parentless" to the "Jack" VM language

from os import linesep, write
from tokenizer import tokenizer
from checker import checker
from io import FileIO

def translate(stream : tokenizer, checker : checker, path : str):

    target : FileIO = open("Main.vm", 'w')
    while_counter : int = 0
    if_counter : int = 0
    while_arr : list = []
    if_arr : list = []
    current_func : str

    while not stream.is_empty():

        current = stream.pop().content

        if current == "start":
            current = stream.pop().content
            current_func = current
            target.write("function Main." + current + " " + str(len(checker.func_vars[current_func])))
            while(stream.pop().content != '\\n'):
                pass
            target.write('\n')
            continue

        if current == "end":
            current = stream.pop().content
            if current == "if":
                target.write("label IF_FALSE" + str(if_arr.pop()))
                stream.pop()
                target.write("\n")
                continue
            if current == "while":
                current_while : str = str(while_arr.pop())
                target.write("goto WHILE_EXP" + current_while + '\n')
                target.write("label WHILE_END" + current_while + '\n')
                stream.pop()
                continue
            target.write("push constant 0\n")
            target.write("return\n")
            continue
        
        if current == "assign" or current == "update":
            current = stream.pop().content
            if current == "int":
                current = stream.pop()
                if current.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if current.terminal == "num":
                    target.write("push constant " + current.content + '\n')
                while current != "to":
                    current = stream.pop()
                    if current.terminal == "to":
                        break
                    num = stream.pop()
                    if num.terminal == "symbol":
                        if num.content in checker.func_vars[current_func]:
                            target.write("push local " + str(checker.func_vars[current_func].index(num.content)) + '\n')
                        else:
                            target.write("push argument " + str(checker.params_dict2[current_func].index(num.content))+ '\n')
                    if num.terminal == "num":
                        target.write("push constant " + num.content + '\n')
                    if current.content == '+':
                        target.write("add\n")
                    if current.content == '*':
                        target.write("call Math.multiply 2\n")
                    if current.content == '-':
                        target.write("sub\n")
                    if current.content == '/':
                        target.write("call Math.divide 2\n")
                current = stream.pop()
                target.write("pop local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                continue
            if current == "float":
                current = stream.pop()
                if current.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if "num" in current.terminal:
                    target.write("push constant " + current.content.split('.')[0] + '\n')
                while current != "to":
                    current = stream.pop()
                    if current.terminal == "to":
                        break
                    num = stream.pop()
                    if num.terminal == "symbol":
                        if current.content in checker.func_vars[current_func]:
                            target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                        else:
                            target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                    if "num" in num.terminal:
                        target.write("push constant " + current.content.split('.')[0] + '\n')
                    if current.content == '+':
                        target.write("add\n")
                    if current.content == '*':
                        target.write("call Math.multiply 2\n")
                    if current.content == '-':
                        target.write("sub\n")
                    if current.content == '/':
                        target.write("call Math.divide 2\n")
                current = stream.pop()
                target.write("pop local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                continue
            if current == "str":
                current = stream.pop()
                if current.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                else:
                    string_const : str = ""
                    if current.terminal == "one word str":
                        string_const = current.content[1:-1]
                    elif current.terminal == "open str":
                        if len(current.content) > 1:
                            string_const += current.content[1:]
                            string_const += " "
                        current = stream.pop()
                        while current.terminal != "close str":
                            string_const += current.content
                            string_const += " "
                            current = stream.pop()
                        string_const += current.content[:-1]
                    target.write("push constant " + str(len(string_const)) + '\n')
                    target.write("call string.new 1\n")
                    for x in string_const:
                        target.write("push constant " + str(ord(x)) + '\n')
                        target.write("call string.appendChar 2\n")
                stream.pop()
                current = stream.pop()
                target.write("pop local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                continue
            if current == "bool":
                not_counter : int = 0
                current = stream.pop()
                while(current.terminal == '!'):
                    not_counter += 1
                    current = stream.pop()
                if (current.terminal == "symbol" and checker.symbols.get(current.content) == "bool"):
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                elif current.terminal == "true":
                    target.write("push constant 0\nnot\n")
                elif current.terminal == "false":
                    target.write("push constant 0\n")
                elif current.terminal == "symbol" and checker.symbols.get(current.content) == "num":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                    current = stream.pop()
                    num = stream.pop()
                    if num.terminal == "symbol":
                        if current.content in checker.func_vars[current_func]:
                            target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                        else:
                            target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                    if num.terminal == "num":
                        target.write("push constant " + num.content + '\n')
                    if current.terminal == ">":
                        target.write('gt\n')
                    if current.terminal == "<":
                        target.write('lt\n')
                    if current.terminal == "=":
                        target.write('eq\n')
                elif current.terminal == "num":
                    target.write("push constant " + current.content + '\n')
                    current = stream.pop()
                    num = stream.pop()
                    if num.terminal == "symbol":
                        if current.content in checker.func_vars[current_func]:
                            target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                        else:
                            target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                    if num.terminal == "num":
                        target.write("push constant " + num.content + '\n')
                    if current.terminal == ">":
                        target.write('gt\n')
                    if current.terminal == "<":
                        target.write('lt\n')
                    if current.terminal == "=":
                        target.write('eq\n')
                stream.pop()
                current = stream.pop()
                for x in range(not_counter):
                    target.write("not\n")
                target.write("pop local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                continue
            
        if current == "draw":
            current = stream.pop()
            string_const : str = ""
            if current.terminal == "one word str" or current.terminal == "open str":
                if current.terminal == "one word str":
                    string_const = current.content[1:-1]
                elif current.terminal == "open str":
                    if len(current.content) > 1:
                        string_const += current.content[1:]
                        string_const += " "
                    current = stream.pop()
                    while current.terminal != "close str":
                        string_const += current.content
                        string_const += " "
                        current = stream.pop()
                    string_const += current.content[:-1]
                target.write("push constant " + str(len(string_const)) + '\n')
                target.write("call String.new 1\n")
                for x in string_const:
                    target.write("push constant " + str(ord(x)) + '\n')
                    target.write("call String.appendChar 2\n")
                target.write("call Output.printString 1\n")
            if current.terminal == "symbol":
                if current.content in checker.func_vars[current_func]:
                    target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                else:
                    target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if checker.symbols.get(current.content) == "str":
                    target.write("call Output.printString 1\n")
                if checker.symbols.get(current.content) == "num":
                    target.write("call Output.printInt 1\n")
                if checker.symbols.get(current.content) == "bool":
                    target.write("if-goto IF_TRUE"+ str(if_counter) +"\n")
                    target.write("goto IF_FALSE"+ str(if_counter) + "\n")
                    target.write("label IF_TRUE" + str(if_counter) + "\n")
                    target.write("push constant 4\n")
                    target.write("call String.new 1\n")
                    target.write("push constant 116\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 114\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 117\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 101\n")
                    target.write("call String.appendChar 2\n")
                    target.write("call Output.printString 1\n")
                    target.write("pop temp 0\n")
                    target.write("goto IF_END" + str(if_counter) + '\n')
                    target.write("label IF_FALSE" + str(if_counter) + '\n')
                    target.write("push constant 5\n")
                    target.write("call String.new 1\n")
                    target.write("push constant 102\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 97\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 108\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 115\n")
                    target.write("call String.appendChar 2\n")
                    target.write("push constant 101\n")
                    target.write("call String.appendChar 2\n")
                    target.write("call Output.printString 1\n")
                    target.write("pop temp 0\n")
                    target.write("label IF_END" + str(if_counter) + '\n')
                    if_counter += 1
                    continue
            if current.terminal == "num":
                target.write("push constant " + current.content + '\n')
                target.write("call Output.printInt 1\n")
            if current.terminal == "true":
                target.write("push constant 4\n")
                target.write("call String.new 1\n")
                target.write("push constant 116\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 114\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 117\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 101\n")
                target.write("call String.appendChar 2\n")
                target.write("call Output.printString 1\n")
            if current.terminal == "false":
                target.write("push constant 5\n")
                target.write("call String.new 1\n")
                target.write("push constant 102\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 97\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 108\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 115\n")
                target.write("call String.appendChar 2\n")
                target.write("push constant 101\n")
                target.write("call String.appendChar 2\n")
                target.write("call Output.printString 1\n")
            target.write("pop temp 0\n")
            continue

        if current == "if":
            current = stream.pop()
            not_counter : int = 0
            while(current.terminal == '!'):
                not_counter += 1
                current = stream.pop()
            if (current.terminal == "symbol" and checker.symbols.get(current.content) == "bool"):
                if current.content in checker.func_vars[current_func]:
                    target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                else:
                    target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
            elif current.terminal == "true":
                target.write("push constant 0\nnot\n")
            elif current.terminal == "false":
                target.write("push constant 0\n")
            elif current.terminal == "symbol" and checker.symbols.get(current.content) == "num":
                if current.content in checker.func_vars[current_func]:
                    target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                else:
                    target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                current = stream.pop()
                num = stream.pop()
                if num.terminal == "symbol":
                    if num.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(num.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(num.content))+ '\n')
                if num.terminal == "num":
                    target.write("push constant " + num.content + '\n')
                if current.terminal == ">":
                    target.write('gt\n')
                if current.terminal == "<":
                    target.write('lt\n')
                if current.terminal == "=":
                    target.write('eq\n')
            elif current.terminal == "num":
                target.write("push constant " + current.content + '\n')
                current = stream.pop()
                num = stream.pop()
                if num.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if num.terminal == "num":
                    target.write("push constant " + num.content + '\n')
                if current.terminal == ">":
                    target.write('gt\n')
                if current.terminal == "<":
                    target.write('lt\n')
                if current.terminal == "=":
                    target.write('eq\n')
            for x in range(not_counter):
                target.write("not\n")
            target.write("if-goto IF_TRUE" + str(if_counter) + '\n')
            target.write("goto IF_FALSE" + str(if_counter) + '\n')
            target.write("label IF_TRUE" + str(if_counter) + '\n')
            if_arr.append(if_counter)
            if_counter += 1
            continue

        if current == "while":
            target.write("label WHILE_EXP" + str(while_counter) + '\n')
            current = stream.pop()
            not_counter : int = 0
            while(current.terminal == '!'):
                not_counter += 1
                current = stream.pop()
            if (current.terminal == "symbol" and checker.symbols.get(current.content) == "bool"):
                if current.content in checker.func_vars[current_func]:
                    target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                else:
                    target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
            elif current.terminal == "true":
                target.write("push constant 0\nnot\n")
            elif current.terminal == "false":
                target.write("push constant 0\n")
            elif current.terminal == "symbol" and checker.symbols.get(current.content) == "num":
                if current.content in checker.func_vars[current_func]:
                    target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                else:
                    target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                current = stream.pop()
                num = stream.pop()
                if num.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if num.terminal == "num":
                    target.write("push constant " + num.content + '\n')
                if current.terminal == ">":
                    target.write('gt\n')
                if current.terminal == "<":
                    target.write('lt\n')
                if current.terminal == "=":
                    target.write('eq\n')
            elif current.terminal == "num":
                target.write("push constant " + current.content + '\n')
                current = stream.pop()
                num = stream.pop()
                if num.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if num.terminal == "num":
                    target.write("push constant " + num.content + '\n')
                if current.terminal == ">":
                    target.write('gt\n')
                if current.terminal == "<":
                    target.write('lt\n')
                if current.terminal == "=":
                    target.write('eq\n')
            for x in range(not_counter):
                target.write("not\n")
            target.write("not\n")
            target.write("if-goto WHILE_END" + str(while_counter) + '\n')
            while_arr.append(while_counter)
            while_counter += 1
            continue
        
        if current == "do":
            func_name : str = stream.pop().content
            current = stream.pop()
            while current.terminal != '\\n':
                current = stream.pop()
                if current.terminal == "symbol":
                    if current.content in checker.func_vars[current_func]:
                        target.write("push local " + str(checker.func_vars[current_func].index(current.content)) + '\n')
                    else:
                        target.write("push argument " + str(checker.params_dict2[current_func].index(current.content))+ '\n')
                if current.terminal == "num":
                    target.write("push constant " + current.content + '\n')
                if current.terminal == "one word str" or current.terminal == "open str":
                    if current.terminal == "one word str":
                        string_const = current.content[1:-1]
                    elif current.terminal == "open str":
                        if len(current.content) > 1:
                            string_const += current.content[1:]
                            string_const += " "
                        current = stream.pop()
                        while current.terminal != "close str":
                            string_const += current.content
                            string_const += " "
                            current = stream.pop()
                        string_const += current.content[:-1]
                    target.write("push constant " + str(len(string_const)) + '\n')
                    target.write("call String.new 1\n")
                    for x in string_const:
                        target.write("push constant " + str(ord(x)) + '\n')
                        target.write("call String.appendChar 2\n")
                if current.terminal == "true":
                    target.write("push constant 0\nnot\n")
                if current.terminal == "false":
                    target.write("push constant 0\n")
            target.write("call Main." + func_name + " " + str(len(checker.params_dict2[func_name])) + '\n')
            target.write('pop temp 0\n')
            continue
    target.close()