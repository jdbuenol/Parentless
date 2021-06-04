#This class is the PARSER

from os import terminal_size
from token import token
from tokenizer import tokenizer
from symboltable import symbol_table

def warning(expected : str, found : str, line : int) -> bool:
    print("["+expected+"] expected, but [" + found + "] was found. in line " + str(line) + ".")
    return False

def already_defined(symbol : str, defined : str, line : int) -> bool:
    print("The symbol " + symbol + " is already defined as a " + defined + ". in line " + str(line) + ".")
    return False

def wrong_type(expected : str, found : str, line : int) -> bool:
    print("type " + expected + " expected, but " + found + " was found. in line " + str(line) + ".")
    return False

def not_defined(symbol : str, line : int) -> bool:
    print("The symbol " + symbol + " is not defined. in line " + str(line) + ".")
    return False

def wrong_str(symbol : str, line : int) -> bool:
    print("Wrong string close" + symbol +". in line " + str(line) + ".")
    return False

def wrong_number_params(func_name : str, expected : int, line : int) -> bool:
    print("Wrong number of parameters given for the function: " + func_name + ". " + str(expected) + " expected(s). in line " + str(line) + ".")
    return False

def wrong_param_type(expected : str, found : str, line : int) -> bool:
    print("Wrong parameter type: " + expected + " was expected but " + found + " was found. in line " + str(line) + ".")
    return False

def wrong_end(expected : str, found : str, line : int) -> bool:
    print("Wrong end: end " + expected + " expected but end " + found + " was found. in line " + str(line) + ".")
    return False

arit_op : list = ['+', '-', '*', '/']
comp_op : list = ['>', '<', '=']
forms : list = ['triangle', 'rectangle', 'circle']

class checker:

    stack : list = []
    params_dict : dict = {}
    params_dict2 : dict = {}
    func_vars : dict = {}
    current_func : str = ""
    stream : tokenizer
    symbols : symbol_table
    state : str
    func_called : str
    current_param : int = 0
    current_line : int = 1

    def __init__(self, tokens_stream : tokenizer) -> None:
        self.stream = tokens_stream
        self.symbols = symbol_table()
        self.state = "func_declaration"
    
    def parse(self) -> bool:
        #start of the machine
        while(not self.stream.is_empty()):
            current_token : token = self.stream.pop()

            if self.state == "func_declaration":
                if current_token.terminal == "start":
                    self.state = "func_name"
                    continue
                if current_token.terminal == "\\n":
                    self.current_line += 1
                    continue
                return warning("start", current_token.content, self.current_line)
            
            if self.state == "func_name":
                if current_token.terminal == "symbol":
                    if self.symbols.contains(current_token.content):
                        return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                    self.symbols.append(current_token.content, "function")
                    self.current_func = current_token.content
                    self.params_dict[self.current_func] = []
                    self.params_dict2[self.current_func] = []
                    self.func_vars[self.current_func] = []
                    self.stack.append(current_token.content)
                    current_token = self.stream.pop()
                    if current_token.terminal == 'with':
                        self.state = "func_args"
                        continue
                    return warning("with", current_token.content, self.current_line)
                return warning("symbol", current_token.content, self.current_line)
            
            if self.state == "func_args":
                if current_token.terminal == "nothing":
                    self.state = "func_args3"
                    continue
                if current_token.terminal == "bool":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "bool")
                        self.params_dict[self.current_func].append("bool")
                        self.params_dict2[self.current_func].append(current_token.content)
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content, self.current_line)
                if current_token.terminal == "int":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "num")
                        self.params_dict[self.current_func].append("num")
                        self.params_dict2[self.current_func].append(current_token.content)
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content, self.current_line)
                if current_token.terminal == "float":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "float_num")
                        self.params_dict[self.current_func].append("float_num")
                        self.params_dict2[self.current_func].append(current_token.content)
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content, self.current_line)
                if current_token.terminal == "str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "str")
                        self.params_dict[self.current_func].append("str")
                        self.params_dict2[self.current_func].append(current_token.content)
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[bool] or [int] or [float] or [str] or [nothing]", current_token.content, self.current_line)
            
            if self.state == "func_args2":
                if current_token.terminal == ',':
                    current_token = self.stream.pop()
                    if current_token.terminal == "bool":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "bool")
                            self.params_dict[self.current_func].append("bool")
                            self.params_dict2[self.current_func].append(current_token.content)
                            continue
                        return warning("symbol", current_token.content, self.current_line)
                    if current_token.terminal == "int":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "num")
                            self.params_dict[self.current_func].append("num")
                            self.params_dict2[self.current_func].append(current_token.content)
                            continue
                        return warning("symbol", current_token.content, self.current_line)
                    if current_token.terminal == "float":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "float_num")
                            self.params_dict[self.current_func].append("float_num")
                            self.params_dict2[self.current_func].append(current_token.content)
                            continue
                        return warning("symbol", current_token.content, self.current_line)
                    if current_token.terminal == "str":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "str")
                            self.params_dict[self.current_func].append("str")
                            self.params_dict2[self.current_func].append(current_token.content)
                            continue
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[bool] or [int] or [float] or [str]", current_token.content, self.current_line)
                if current_token.terminal == '\\n':
                    self.current_line += 1
                    self.state = "func_body"
                    continue
                return warning("[,] or [\\n]", current_token.content, self.current_line)

            if self.state == "func_args3":
                if current_token.terminal == '\\n':
                    self.current_line += 1
                    self.state = "func_body"
                    continue
                return warning("[\\n]", current_token.content, self.current_line)
            
            if self.state == "func_body":
                if current_token.terminal == 'assign':
                    self.state = "assign_op"
                    continue
                if current_token.terminal == "draw":
                    self.state = "draw_op"
                    continue
                if current_token.terminal == "set":
                    current_token = self.stream.pop()
                    if current_token.terminal == "color":
                        self.state = "set_color"
                        continue
                    return warning("[color]", current_token.content, self.current_line)
                if current_token.terminal == "do":
                    self.state = "func_call"
                    continue
                if current_token.terminal == "if":
                    self.state = "if"
                    self.stack.append("if")
                    continue
                if current_token.terminal == "while":
                    self.state = "while"
                    self.stack.append("while")
                    continue
                if current_token.terminal == "end":
                    self.state = "end"
                    continue
                if current_token.terminal == "\\n":
                    self.current_line += 1
                    continue
                if current_token.terminal == "update":
                    self.state = "update_op"
                    continue
                return warning("[assign] or [end] or [draw] or [set] or [do] or [if] or [while]", current_token.content, self.current_line)

            if self.state == "assign_op":
                if current_token.terminal == "int":
                    self.state = "assign_int"
                    continue
                if current_token.terminal == "bool":
                    self.state = "assign_bool"
                    continue
                if current_token.terminal == "str":
                    self.state = "assign_str"
                    continue
                if current_token.terminal == "float":
                    self.state = "assign_float"
                    continue
                return warning("[int] or [bool] or [str] or [float]", current_token.content, self.current_line)
            
            if self.state == "assign_int":
                if current_token.terminal == "num":
                    self.state = "int_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != 'num':
                        return wrong_type("int", self.symbols.get(current_token.content), self.current_line)
                    self.state = "int_op"
                    continue
                return warning("symbol or int", current_token.content, self.current_line)

            if self.state == "int_op":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "num":
                        continue
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if self.symbols.get(current_token.content) != 'num':
                            return wrong_type("int", self.symbols.get(current_token.content), self.current_line)
                        continue
                    return warning("symbol or int", current_token.content, self.current_line)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "num")
                        self.func_vars[self.current_func].append(current_token.content)
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.state = "func_body"
                            self.current_line += 1
                            continue
                        return warning("[\\n]", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[to] or [+] or [-] or [*] or [/]", current_token.content, self.current_line)
            
            if self.state == "assign_float":
                if "num" in current_token.terminal:
                    self.state = "num_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if not 'num' in self.symbols.get(current_token.content):
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    self.state = "num_op"
                    continue
                return warning("symbol or int or float", current_token.content, self.current_line)

            if self.state == "num_op":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if "num" in current_token.terminal:
                        continue
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if not "num" in self.symbols.get(current_token.content):
                            return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                        continue
                    return warning("symbol or int or float", current_token.content, self.current_line)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "float_num")
                        self.func_vars[self.current_func].append(current_token.content)
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.state = "func_body"
                            self.current_line += 1
                            continue
                        return warning("[\\n]", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[to] or [+] or [-] or [*] or [/]", current_token.content, self.current_line)

            if self.state == "assign_str":
                if current_token.terminal == "one word str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "str")
                            self.func_vars[self.current_func].append(current_token.content)
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.current_line += 1
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content, self.current_line)
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[to]", current_token.content, self.current_line)
                if current_token.terminal == "open str":
                    self.state = "multi_word_str"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != "str":
                        return wrong_type("string", self.symbols.get(current_token.content), self.current_line)
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "str")
                            self.func_vars[self.current_func].append(current_token.content)
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.current_line += 1
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content, self.current_line)
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[to]", current_token.content, self.current_line)
                return warning("string or symbol", current_token.content, self.current_line)
            
            if self.state == "multi_word_str":
                if current_token.terminal == "close str" or current_token.terminal == '"' or current_token.terminal == "'":
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                            self.symbols.append(current_token.content, "str")
                            self.func_vars[self.current_func].append(current_token.content)
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.current_line += 1
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content, self.current_line)
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[to]", current_token.content, self.current_line)
                if "'" in current_token.content or '"' in current_token.content:
                    return wrong_str(current_token.content, self.current_line)
                continue
            
            if self.state == "assign_bool":
                if current_token.terminal == '!':
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "num_op2"
                        continue
                    if "bool" in self.symbols.get(current_token.content):
                        self.state = "bool_op"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content), self.current_line)
                if current_token.terminal == "true" or current_token.terminal == "false":
                    self.state = "bool_op"
                    continue
                if "num" in current_token.terminal:
                    self.state = "num_op2"
                    continue
                return warning("int or float or bool or [true] or [false] or [!]", current_token.content, self.current_line)
            
            if self.state == "num_op2":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "num_op3"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        self.state = "num_op3"
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content, self.current_line)
            
            if self.state == "num_op3":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "bool")
                        self.func_vars[self.current_func].append(current_token.content)
                        current_token = self.stream.pop()
                        if current_token.content == '\\n':
                            self.state = "func_body"
                            self.current_line += 1
                            continue
                        return warning("\\n", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[+] or [-] or [*] or [/] or [to]", current_token.content, self.current_line)
            
            if self.state == "bool_op":
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "bool_op2"
                    continue
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content), self.current_line)
                        self.symbols.append(current_token.content, "bool")
                        self.func_vars[self.current_func].append(current_token.content)
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.current_line += 1
                            self.state = "func_body"
                            continue
                        return warning("\\n", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[&] or [|] or [to]", current_token.content, self.current_line)
            
            if self.state == "bool_op2":
                if current_token.terminal == '!':
                    continue
                if current_token.terminal == 'false' or current_token.terminal == 'true':
                    self.state = "bool_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type("bool", self.symbols.get(current_token.content), self.current_line)
                    self.state = "bool_op"
                    continue
                return warning("[!] or [false] or [true] or bool", current_token.content, self.current_line)
            
            if self.state == "update_op":
                if current_token.terminal == "int":
                    self.state = "update_int"
                    continue
                if current_token.terminal == "bool":
                    self.state = "update_bool"
                    continue
                if current_token.terminal == "str":
                    self.state = "update_str"
                    continue
                if current_token.terminal == "float":
                    self.state = "update_float"
                    continue
                return warning("[int] or [bool] or [str] or [float]", current_token.content, self.current_line)
            
            if self.state == "update_int":
                if current_token.terminal == "num":
                    self.state = "update_int_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != 'num':
                        return wrong_type("int", self.symbols.get(current_token.content), self.current_line)
                    self.state = "update_int_op"
                    continue
                return warning("symbol or int", current_token.content, self.current_line)

            if self.state == "update_int_op":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "num":
                        continue
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if self.symbols.get(current_token.content) != 'num':
                            return wrong_type("int", self.symbols.get(current_token.content), self.current_line)
                        continue
                    return warning("symbol or int", current_token.content, self.current_line)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if not self.symbols.get(current_token.content) == "num":
                            return wrong_type("int", self.symbols.get(current_token.content))
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.state = "func_body"
                            self.current_line += 1
                            continue
                        return warning("[\\n]", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[to] or [+] or [-] or [*] or [/]", current_token.content, self.current_line)
            
            if self.state == "update_float":
                if "num" in current_token.terminal:
                    self.state = "update_num_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if not 'num' in self.symbols.get(current_token.content):
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    self.state = "update_num_op"
                    continue
                return warning("symbol or int or float", current_token.content, self.current_line)

            if self.state == "update_num_op":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if "num" in current_token.terminal:
                        continue
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if not "num" in self.symbols.get(current_token.content):
                            return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                        continue
                    return warning("symbol or int or float", current_token.content, self.current_line)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if not self.symbols.get(current_token.content) == "float_num":
                            return wrong_type("float", self.symbols.get(current_token.content), self.current_line)
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.state = "func_body"
                            self.current_line += 1
                            continue
                        return warning("[\\n]", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[to] or [+] or [-] or [*] or [/]", current_token.content, self.current_line)

            if self.state == "update_str":
                if current_token.terminal == "one word str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if not self.symbols.contains(current_token.content):
                                return not_defined(current_token.content, self.current_line)
                            if not self.symbols.get(current_token.content) == "str":
                                return wrong_type("string", self.symbols.get(current_token.content))
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.current_line += 1
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content, self.current_line)
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[to]", current_token.content, self.current_line)
                if current_token.terminal == "open str":
                    self.state = "multi_word_update"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != "str":
                        return wrong_type("string", self.symbols.get(current_token.content), self.current_line)
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if not self.symbols.contains(current_token.content):
                                return not_defined(current_token.content, self.current_line)
                            if not self.symbols.get(current_token.content) == "str":
                                return wrong_type("string", self.symbols.get(current_token.content), self.current_line)
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.current_line += 1
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content, self.current_line)
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[to]", current_token.content, self.current_line)
                return warning("string or symbol", current_token.content, self.current_line)
            
            if self.state == "multi_word_update":
                if current_token.terminal == "close str" or current_token.terminal == '"' or current_token.terminal == "'":
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if not self.symbols.contains(current_token.content):
                                return not_defined(current_token.content, self.current_line)
                            if not self.symbols.get(current_token.content) == "str":
                                return wrong_type("string", self.symbols.get(current_token.content), self.current_line)
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.current_line += 1
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content, self.current_line)
                        return warning("symbol", current_token.content, self.current_line)
                    return warning("[to]", current_token.content, self.current_line)
                if "'" in current_token.content or '"' in current_token.content:
                    return wrong_str(current_token.content, self.current_line)
                continue
            
            if self.state == "update_bool":
                if current_token.terminal == '!':
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "update_num_op2"
                        continue
                    if "bool" in self.symbols.get(current_token.content):
                        self.state = "update_bool_op"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content), self.current_line)
                if current_token.terminal == "true" or current_token.terminal == "false":
                    self.state = "update_bool_op"
                    continue
                if "num" in current_token.terminal:
                    self.state = "update_num_op2"
                    continue
                return warning("int or float or bool or [true] or [false] or [!]", current_token.content, self.current_line)
            
            if self.state == "update_num_op2":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "update_num_op3"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        self.state = "update_num_op3"
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content, self.current_line)
            
            if self.state == "update_num_op3":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if not self.symbols.get(current_token.content) == "bool":
                            return wrong_type("bool", self.symbols.get(current_token.content), self.current_line)
                        current_token = self.stream.pop()
                        if current_token.content == '\\n':
                            self.state = "func_body"
                            self.current_line += 1
                            continue
                        return warning("\\n", current_token.content, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[+] or [-] or [*] or [/] or [to]", current_token.content, self.current_line)
            
            if self.state == "update_bool_op":
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "update_bool_op2"
                    continue
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if not self.symbols.get(current_token.content):
                            return wrong_type("bool", self.symbols.get(current_token.content), self.currnet_line)
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.current_line += 1
                            self.state = "func_body"
                            continue
                        return warning("\\n", current_token.contnet, self.current_line)
                    return warning("symbol", current_token.content, self.current_line)
                return warning("[&] or [|] or [to]", current_token.content, self.current_line)
            
            if self.state == "update_bool_op2":
                if current_token.terminal == '!':
                    continue
                if current_token.terminal == 'false' or current_token.terminal == 'true':
                    self.state = "update_bool_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type("bool", self.symbols.get(current_token.content), self.current_line)
                    self.state = "update_bool_op"
                    continue
                return warning("[!] or [false] or [true] or bool", current_token.content, self.current_line)

            if self.state == "draw_op":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    self.state = "draw_coords"
                    continue
                if current_token.terminal in forms:
                    self.state = "draw_coords"
                    continue
                if current_token.terminal == "one word str":
                    self.state = "draw_coords"
                    continue
                if current_token.terminal == "open str":
                    self.state = "draw multi words"
                    continue
                if "num" in current_token.terminal:
                    self.state = "draw_coords"
                    continue
                if current_token.terminal == "true" or current_token.terminal == "false":
                    self.state = "draw_coords"
                    continue
                return warning("symbol or form or string or int or num or [true] or [false]", current_token.content, self.current_line)
            
            if self.state == "draw multi words":
                if current_token.terminal == "close str" or current_token.terminal == '"' or current_token.terminal == "'":
                    self.state = "draw_coords"
                    continue
                if "'" in current_token.content or '"' in current_token.content:
                    return wrong_str(current_token.content, self.current_line)
                continue

            if self.state == "draw_coords":
                if current_token.terminal == "\\n":
                    self.state = "func_body"
                    continue
                return warning("\\n", current_token.content, self.current_line)
            
            if self.state == "set_color":
                if current_token.terminal == "white" or current_token.terminal == "black":
                    current_token = self.stream.pop()
                    if current_token.terminal == "\\n":
                        self.current_line += 1
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content, self.current_line)
                return warning("[white] or [black]", current_token.content, self.current_line)
            
            if self.state == "func_call":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if not self.symbols.get(current_token.content) == "function":
                        return wrong_type("function", self.symbols.get(current_token.content), self.current_line)
                    self.func_called = current_token.content
                    self.current_param = 0
                    current_token = self.stream.pop()
                    if current_token.terminal == "with":
                        self.state = "call_args"
                        continue
                    return warning("with", current_token.content, self.current_line)
                return warning("function name", current_token.content, self.current_line)
            
            if self.state == "call_args":
                if current_token.terminal == "nothing":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if self.current_param != len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    current_token = self.stream.pop()
                    if current_token == "\\n":
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content, self.current_line)
                if current_token.terminal == "num":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if "num" != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dic[self.func_called][self.current_param], "int", self.current_line)
                    self.current_param += 1
                    self.state = "end_call"
                    continue
                if current_token.terminal == "float_num":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if "float_num" != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dic[self.func_called][self.current_param], "float", self.current_line)
                    self.current_param += 1
                    self.state = "end_call"
                    continue
                if current_token.terminal == "true" or current_token.terminal == "false":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if "bool" != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dic[self.func_called][self.current_param], "bool", self.current_line)
                    self.current_param += 1
                    self.state = "end_call"
                    continue
                if current_token.terminal == "one word str":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if "str" != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dict[self.func_called][self.current_param], "string", self.current_line)
                    self.current_param += 1
                    self.state = "end_call"
                    continue
                if current_token.terminal == "open str":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if "str" != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dict[self.func_called][self.current_param], "string", self.current_line)
                    self.current_param += 1
                    self.state = "multi word param"
                    continue
                if current_token.terminal == "symbol":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    if self.symbols.get(current_token.content) != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dict[self.func_called][self.current_param], self.symbols.get(current_token.content), self.current_line)
                    self.current_param += 1
                    self.state = "end_call"
                    continue
                return warning("symbol or [nothing]", current_token.content, self.current_line)
            
            if self.state == "multi word param":
                if current_token.terminal == "close str" or current_token.terminal == '"' or current_token.terminal == "'":
                    self.state = "end_call"
                    continue
                if "'" in current_token.content or '"' in current_token.content:
                    return wrong_str(current_token.content, self.current_line)
                continue

            if self.state == "end_call":
                if current_token.terminal == "\\n":
                    if self.current_param != len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]), self.current_line)
                    self.current_line += 1
                    self.state = "func_body"
                    continue
                if current_token.terminal == ",":
                    self.state = "call_args"
                    continue
                return warning("[,] or [\\n]", current_token.content, self.current_line)
            
            if self.state == "if":
                if current_token.terminal == "!":
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "num_if"
                        continue
                    if self.symbols.get(current_token.content) == "bool":
                        self.state = "bool_if"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content), self.current_line)
                if "num" in current_token.terminal:
                    self.state = "num_if"
                    continue
                if current_token.terminal == "bool":
                    self.state = "bool_if"
                    continue
                return warning("[!] or int or float or bool", current_token.content, self.current_line)
            
            if self.state == "num_if":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "num_if2"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        self.state = "num_if2"
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content, self.current_line)
            
            if self.state == "num_if2":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    self.current_line += 1
                    continue
                return warning("[\\n] or [+] or [-] or [*] or [/]", current_token.content, self.current_line)
            
            if self.state == "bool_if":
                if current_token.terminal == "\\n":
                    self.current_line += 1
                    self.state = "func_body"
                    continue
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "bool_if2"
                    continue
                return warning("[\\n] or [&] or [|]", current_token.content, self.current_line)
            
            if self.state == "bool_if2":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type('bool', self.symbols.get(current_token.content), self.current_line)
                    self.state = "bool_if"
                    continue
                if current_token.terminal == "false" or current_token.terminal == "true":
                    self.state = "bool_if"
                    continue
                return warning("bool or [false] or [true]", current_token.content, self.current_line)
            
            if self.state == "while":
                if current_token.terminal == "!":
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "num_while"
                        continue
                    if self.symbols.get(current_token.content) == "bool":
                        self.state = "bool_while"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content), self.current_line)
                if "num" in current_token.terminal:
                    self.state = "num_while"
                    continue
                if current_token.terminal == "bool":
                    self.state = "bool_while"
                    continue
                return warning("[!] or int or float or bool", current_token.content, self.current_line)
            
            if self.state == "num_while":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "num_while2"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        self.state = "num_while2"
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content, self.current_line)
            
            if self.state == "num_while2":
                if current_token.terminal in arit_op:
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content, self.current_line)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content), self.current_line)
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content, self.current_line)
                if current_token.terminal == '\\n':
                    self.current_line += 1
                    self.state = "func_body"
                    continue
                return warning("[\\n] or [+] or [-] or [*] or [/]", current_token.content, self.current_line)
            
            if self.state == "bool_while":
                if current_token.terminal == "\\n":
                    self.current_line += 1
                    self.state = "func_body"
                    continue
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "bool_while2"
                    continue
                return warning("[\\n] or [&] or [|]", current_token.content, self.current_line)
            
            if self.state == "bool_while2":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type('bool', self.symbols.get(current_token.content), self.current_line)
                    self.state = "bool_while"
                    continue
                if current_token.terminal == "false" or current_token.terminal == "true":
                    self.state = "bool_while"
                    continue
                return warning("bool or [false] or [true]", current_token.content, self.current_line)
            
            if self.state == "end":
                if current_token.terminal == "if":
                    expected_end = self.stack.pop()
                    if expected_end != "if":
                        return wrong_end(expected_end, 'if', self.current_line)
                    current_token = self.stream.pop()
                    if current_token.terminal == '\\n':
                        self.current_line += 1
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content, self.current_line)
                if current_token.terminal == "while":
                    expected_end = self.stack.pop()
                    if expected_end != "while":
                        return wrong_end(expected_end, 'while', self.current_line)
                    current_token = self.stream.pop()
                    if current_token.terminal == "\\n":
                        self.current_line += 1
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content, self.current_line)
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content, self.current_line)
                    if self.symbols.get(current_token.content) != 'function':
                        return wrong_type('function', self.symbols.get(current_token.content, self.current_line))
                    expected_end = self.stack.pop()
                    if current_token.content != expected_end:
                        return wrong_end(expected_end, current_token.content, self.current_line)
                    self.state = "end_of_file"
                    continue
                return warning("[if] or [while] or function name", current_token.content, self.current_line)
            
            if self.state == "end_of_file":
                if current_token.terminal == '\\n':
                    self.current_line += 1
                    self.state = "func_declaration"
                    continue
                return warning("[\\n] or EOF", current_token.content, self.current_line)
        
        # End of the machine

        if not self.symbols.contains("main"):
            print("main function not found")
            return False
        if not self.symbols.get("main") == "function":
            print("main function expected but main " + self.symbols.get("main") + " found.")
            return False
        if self.state == "end_of_file" or self.state == "func_declaration":
            if len(self.stack) == 0:
                return True
        print("EOF reached while parsing")
        return False