from io import SEEK_CUR
from os import terminal_size
from token import token
from tokenizer import tokenizer
from symboltable import symbol_table

def warning(expected : str, found : str) -> bool:
    print("["+expected+"] expected, but [" + found + "] was found.")
    return False

def already_defined(symbol : str, defined : str) -> bool:
    print("The symbol " + symbol + " is already defined as a " + defined + ".")
    return False

def wrong_type(expected : str, found : str) -> bool:
    print("type " + expected + " expected, but " + found + " was found.")
    return False

def not_defined(symbol : str) -> bool:
    print("The symbol " + symbol + " is not defined.")
    return False

def wrong_str(symbol : str) -> bool:
    print("Wrong string close.")
    return False

def wrong_number_params(func_name : str, expected : int) -> bool:
    print("Wrong number of parameters given for the function: " + func_name + ". " + str(expected) + " expected(s).")
    return False

def wrong_param_type(expected : str, found : str) -> bool:
    print("Wrong parameter type: " + expected + " was expected but " + found + " was found.")
    return False

def wrong_end(expected : str, found : str) -> bool:
    print("Wrong end: end " + expected + " expected but end " + found + " was found.")
    return False

arit_op : list = ['+', '-', '*', '/']
comp_op : list = ['>', '<', '=']
forms : list = ['triangle', 'rectangle', 'circle']

class checker:

    stack : list = []
    params_dict : dict = {}
    current_func : str = ""
    stream : tokenizer
    symbols : symbol_table
    state : str
    func_called : str
    current_param : int = 0

    def __init__(self, tokens_stream : tokenizer) -> None:
        self.stream = tokens_stream
        self.symbols = symbol_table()
        self.state = "func_declaration"
    
    def parse(self) -> bool:
        #start of the machine
        while(not self.stream.is_empty()):

            print(self.state)
            print(self.stack)
            print()
            current_token : token = self.stream.pop()

            if self.state == "func_declaration":
                if current_token.terminal == "start":
                    self.state = "func_name"
                    continue
                if current_token.terminal == "\\n":
                    continue
                return warning("start", current_token.content)
            
            if self.state == "func_name":
                if current_token.terminal == "symbol":
                    if self.symbols.contains(current_token.content):
                        return already_defined(current_token.content, self.symbols.get(current_token.content))
                    self.symbols.append(current_token.content, "function")
                    self.current_func = current_token.content
                    self.params_dict[self.current_func] = []
                    self.stack.append(current_token.content)
                    current_token = self.stream.pop()
                    if current_token.terminal == 'with':
                        self.state = "func_args"
                        continue
                    return warning("with", current_token.content)
                return warning("symbol", current_token.content)
            
            if self.state == "func_args":
                if current_token.terminal == "nothing":
                    self.state = "func_args3"
                    continue
                if current_token.terminal == "bool":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "bool")
                        self.params_dict[self.current_func].append("bool")
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content)
                if current_token.terminal == "int":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "num")
                        self.params_dict[self.current_func].append("num")
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content)
                if current_token.terminal == "float":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "float_num")
                        self.params_dict[self.current_func].append("float_num")
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content)
                if current_token.terminal == "str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "str")
                        self.params_dict[self.current_func].append("str")
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content)
                return warning("[bool] or [int] or [float] or [str] or [nothing]", current_token.content)
            
            if self.state == "func_args2":
                if current_token.terminal == ',':
                    current_token = self.stream.pop()
                    if current_token.terminal == "bool":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "bool")
                            self.params_dict[self.current_func].append("bool")
                            continue
                        return warning("symbol", current_token.content)
                    if current_token.terminal == "int":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "num")
                            self.params_dict[self.current_func].append("num")
                            continue
                        return warning("symbol", current_token.content)
                    if current_token.terminal == "float":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "float_num")
                            self.params_dict[self.current_func].append("float_num")
                            continue
                        return warning("symbol", current_token.content)
                    if current_token.terminal == "str":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "str")
                            self.params_dict[self.current_func].append("str")
                            continue
                        return warning("symbol", current_token.content)
                    return warning("[bool] or [int] or [float] or [str]", current_token.content)
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    continue
                return warning("[,] or [\\n]", current_token.content)

            if self.state == "func_args3":
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    continue
                return warning("[\\n]", current_token.content)
            
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
                    return warning("[color]", current_token.content)
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
                    continue
                return warning("[assign] or [end] or [draw] or [set] or [do] or [if] or [while]", current_token.content)

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
                return warning("[int] or [bool] or [str] or [float]", current_token.content)
            
            if self.state == "assign_int":
                if current_token.terminal == "num":
                    self.state = "int_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if self.symbols.get(current_token.content) != 'num':
                        return wrong_type("int", self.symbols.get(current_token.content))
                    self.state = "int_op"
                    continue
                return warning("symbol or int", current_token.content)

            if self.state == "int_op":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "num":
                        continue
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if self.symbols.get(current_token.content) != 'num':
                            return wrong_type("int", self.symbols.get(current_token.content))
                        continue
                    return warning("symbol or int", current_token.content)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "num")
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.state = "func_body"
                            continue
                        return warning("[\\n]", current_token.content)
                    return warning("symbol", current_token.content)
                return warning("[to] or [+] or [-] or [*] or [/]", current_token.content)
            
            if self.state == "assign_float":
                if "num" in current_token.terminal:
                    self.state = "num_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if not 'num' in self.symbols.get(current_token.content):
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    self.state = "num_op"
                    continue
                return warning("symbol or int or float", current_token.content)

            if self.state == "num_op":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if "num" in current_token.terminal:
                        continue
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if not "num" in self.symbols.get(current_token.content):
                            return wrong_type("int or float", self.symbols.get(current_token.content))
                        continue
                    return warning("symbol or int or float", current_token.content)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "float_num")
                        current_token = self.stream.pop()
                        if current_token.terminal == "\\n":
                            self.state = "func_body"
                            continue
                        return warning("[\\n]", current_token.content)
                    return warning("symbol", current_token.content)
                return warning("[to] or [+] or [-] or [*] or [/]", current_token.content)

            if self.state == "assign_str":
                if current_token.terminal == "one word str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "str")
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content)
                        return warning("symbol", current_token.content)
                    if current_token.terminal == "+":
                        continue
                    return warning("[to] or [+]", current_token.content)
                if current_token.terminal == "open str":
                    self.state = "multi_word_str"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if self.symbols.get(current_token.content) != "str":
                        return wrong_type("string", self.symbols.get(current_token.content))
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "str")
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content)
                        return warning("symbol", current_token.content)
                    if current_token.terminal == "+":
                        continue
                    return warning("[to] or [+]", current_token.content)
                return warning("string or symbol", current_token.content)
            
            if self.state == "multi_word_str":
                if current_token.terminal == "close str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "to":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "str")
                            current_token = self.stream.pop()
                            if current_token.terminal == "\\n":
                                self.state = "func_body"
                                continue
                            return warning("[\\n]", current_token.content)
                        return warning("symbol", current_token.content)
                    if current_token.terminal == "+":
                        self.state = "assign_str"
                        continue
                    return warning("[to] or [+]", current_token.content)
                if "'" in current_token.content or '"' in current_token.content:
                    return wrong_str()
                continue
            
            if self.state == "assign_bool":
                if current_token.terminal == '!':
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "num_op2"
                        continue
                    if "bool" in self.symbols.get(current_token.content):
                        self.state = "bool_op"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content))
                if current_token.terminal == "true" or current_token.terminal == "false":
                    self.state = "bool_op"
                    continue
                if "num" in current_token.terminal:
                    self.state = "num_op2"
                    continue
                return warning("int or float or bool or [true] or [false] or [!]", current_token.content)
            
            if self.state == "num_op2":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "num_op3"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        self.state = "num_op3"
                        continue
                    return warning("int or float", current_token.content)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content)
            
            if self.state == "num_op3":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content)
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "bool")
                        current_token = self.stream.pop()
                        if current_token.content == '\\n':
                            self.state = "func_body"
                            continue
                        return warning("\\n", current_token.content)
                    return warning("symbol", current_token.content)
                return warning("[+] or [-] or [*] or [/] or [to]", current_token.content)
            
            if self.state == "bool_op":
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "bool_op2"
                    continue
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "bool")
                        self.state = "func_body"
                        continue
                    return warning("symbol", current_token.content)
                return warning("[&] or [|] or [to]", current_token.content)
            
            if self.state == "bool_op2":
                if current_token.terminal == '!':
                    continue
                if current_token.terminal == 'false' or current_token.terminal == 'true':
                    self.state = "bool_op"
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type("bool", self.symbols.get(current_token.content))
                    self.state = "bool_op"
                    continue
                return warning("[!] or [false] or [true] or bool", current_token.content)
            
            if self.state == "draw_op":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
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
                return warning("symbol or form or string or int or num or [true] or [false]", current_token.content)
            
            if self.state == "draw multi words":
                if current_token.terminal == "close str":
                    self.state = "draw_coords"
                    continue
                if "'" in current_token.content or '"' in current_token.content:
                    return wrong_str()
                continue

            if self.state == "draw_coords":
                if current_token.terminal == "in":
                    self.state = "coord_x"
                    continue
                return warning("in", current_token.content)
            
            if self.state == "coord_x":
                if current_token.terminal == "num":
                    current_token = self.stream.pop()
                    if current_token.terminal == ',':
                        self.state = "coord_y"
                        continue
                    return warning(",", current_token.content)
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if not self.symbols.get(current_token.content):
                        return wrong_type("int", self.symbols.get(current_token.content))
                    current_token = self.stream.pop()
                    if current_token.terminal == ",":
                        self.state = "coord_y"
                        continue
                    return warning(",", current_token.content)
                return warning("int", current_token.content)
            
            if self.state == "coord_y":
                if current_token.terminal == "num":
                    current_token = self.stream.pop()
                    if current_token.terminal == '\\n':
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content)
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if not self.symbols.get(current_token.content):
                        return wrong_type("int", self.symbols.get(current_token.content))
                    current_token = self.stream.pop()
                    if current_token.terminal == "\\n":
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content)
                return warning("int", current_token.content)
            
            if self.state == "set_color":
                if current_token.terminal == "white" or current_token.terminal == "black":
                    current_token = self.stream.pop()
                    if current_token.terminal == "\\n":
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content)
                return warning("[white] or [black]", current_token.content)
            
            if self.state == "func_call":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if not self.symbols.get(current_token.content) == "function":
                        return wrong_type("function", self.symbols.get(current_token.content))
                    self.func_called = current_token.content
                    self.current_param = 0
                    current_token = self.stream.pop()
                    if current_token.terminal == "with":
                        self.state = "call_args"
                        continue
                    return warning("with", current_token.content)
                return warning("function name", current_token.content)
            
            if self.state == "call_args":
                if current_token.terminal == "nothing":
                    if self.current_param != len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]))
                    current_token = self.stream.pop()
                    if current_token == "\\n":
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content)
                if current_token.terminal == "symbol":
                    if self.current_param >= len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]))
                    if self.symbols.get(current_token.content) != self.params_dict[self.func_called][self.current_param]:
                        return wrong_param_type(self.params_dict[self.func_called][self.current_param], self.symbols.get(current_token.content))
                    self.current_param += 1
                    self.state = "end_call"
                    continue
                return warning("symbol or [nothing]", current_token.content)
            
            if self.state == "end_call":
                if current_token.terminal == "\\n":
                    if self.current_param != len(self.params_dict[self.func_called]):
                        return wrong_number_params(self.func_called, len(self.params_dict[self.func_called]))
                    self.state = "func_body"
                    continue
                if current_token.terminal == ",":
                    self.state = "call_args"
                    continue
                return warning("[,] or [\\n]", current_token.content)
            
            if self.state == "if":
                if current_token.terminal == "!":
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "num_if"
                        continue
                    if self.symbols.get(current_token.content) == "bool":
                        self.state = "bool_if"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content))
                if "num" in current_token.terminal:
                    self.state = "num_if"
                    continue
                if current_token.terminal == "bool":
                    self.state = "bool_if"
                    continue
                return warning("[!] or int or float or bool", current_token.content)
            
            if self.state == "num_if":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "num_if2"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        self.state = "num_if2"
                        continue
                    return warning("int or float", current_token.content)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content)
            
            if self.state == "num_if2":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content)
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    continue
                return warning("[\\n] or [+] or [-] or [*] or [/]", current_token.content)
            
            if self.state == "bool_if":
                if current_token.terminal == "\\n":
                    self.state = "func_body"
                    continue
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "bool_if2"
                    continue
                return warning("[\\n] or [&] or [|]", current_token.content)
            
            if self.state == "bool_if2":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type('bool', self.symbols.get(current_token.content))
                    self.state = "bool_if"
                    continue
                if current_token.terminal == "false" or current_token.terminal == "true":
                    self.state = "bool_if"
                    continue
                return warning("bool or [false] or [true]", current_token.content)
            
            if self.state == "while":
                if current_token.terminal == "!":
                    continue
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if "num" in self.symbols.get(current_token.content):
                        self.state = "num_while"
                        continue
                    if self.symbols.get(current_token.content) == "bool":
                        self.state = "bool_while"
                        continue
                    return wrong_type("bool or int or float", self.symbols.get(current_token.content))
                if "num" in current_token.terminal:
                    self.state = "num_while"
                    continue
                if current_token.terminal == "bool":
                    self.state = "bool_while"
                    continue
                return warning("[!] or int or float or bool", current_token.content)
            
            if self.state == "num_while":
                if current_token.terminal in arit_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content)
                if current_token.terminal in comp_op:
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            self.state = "num_while2"
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        self.state = "num_while2"
                        continue
                    return warning("int or float", current_token.content)
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [=]", current_token.content)
            
            if self.state == "num_while2":
                if current_token.terminal in arit_op:
                    if current_token.terminal == "symbol":
                        if not self.symbols.contains(current_token.content):
                            return not_defined(current_token.content)
                        if "num" in self.symbols.get(current_token.content):
                            continue
                        return wrong_type("int or float", self.symbols.get(current_token.content))
                    if "num" in current_token.terminal:
                        continue
                    return warning("int or float", current_token.content)
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    continue
                return warning("[\\n] or [+] or [-] or [*] or [/]", current_token.content)
            
            if self.state == "bool_while":
                if current_token.terminal == "\\n":
                    self.state = "func_body"
                    continue
                if current_token.terminal == "&" or current_token.terminal == "|":
                    self.state = "bool_while2"
                    continue
                return warning("[\\n] or [&] or [|]", current_token.content)
            
            if self.state == "bool_while2":
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if self.symbols.get(current_token.content) != "bool":
                        return wrong_type('bool', self.symbols.get(current_token.content))
                    self.state = "bool_while"
                    continue
                if current_token.terminal == "false" or current_token.terminal == "true":
                    self.state = "bool_while"
                    continue
                return warning("bool or [false] or [true]", current_token.content)
            
            if self.state == "end":
                if current_token.terminal == "if":
                    expected_end = self.stack.pop()
                    if expected_end != "if":
                        return wrong_end(expected_end, 'if')
                    current_token = self.stream.pop()
                    if current_token.terminal == '\\n':
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content)
                if current_token.terminal == "while":
                    expected_end = self.stack.pop()
                    if expected_end != "while":
                        return wrong_end(expected_end, 'while')
                    current_token = self.stream.pop()
                    if current_token.terminal == "\\n":
                        self.state = "func_body"
                        continue
                    return warning("\\n", current_token.content)
                if current_token.terminal == "symbol":
                    if not self.symbols.contains(current_token.content):
                        return not_defined(current_token.content)
                    if self.symbols.get(current_token.content) != 'function':
                        return wrong_type('function', self.symbols.get(current_token.content))
                    expected_end = self.stack.pop()
                    if current_token.content != expected_end:
                        return wrong_end(expected_end, current_token.content)
                    self.state = "end_of_file"
                    continue
                return warning("[if] or [while] or function name", current_token.content)
            
            if self.state == "end_of_file":
                if current_token.terminal == '\\n':
                    self.state = "func_declaration"
                    continue
                return warning("[\\n] or EOF", current_token.content)
        
        # End of the machine

        if self.state == "end_of_file" or self.state == "func_declaration":
            if len(self.stack) == 0:
                return True
        print("EOF reached while parsing")
        return False