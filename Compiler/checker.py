from os import terminal_size
from token import token
from tokenizer import tokenizer
from symboltable import symbol_table

def warning(expected : str, found : str) -> bool:
    print("["+expected+"] expected, but [" + found + "] was found.")
    return False

def already_defined(symbol : str, as : str) -> bool:
    print("The symbol " + symbol + " is already defined as a " + as + ".")
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

arit_op : list = ['+', '-', '*', '/']
comp_op : list = ['>', '<', '=']
forms : list = ['triangle', 'rectangle', 'circle']

class checker:

    stack : list = []
    stream : tokenizer
    symbols : symbol_table
    state : str

    def __init__(self, tokens_stream : tokenizer) -> None:
        self.stream = tokens_stream
        self.symbols = symbol_table()
        self.state = "func_declaration"
    
    def parse(self) -> bool:
        while(not self.stream.is_empty()):

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
                if current_token.terminal == "bool" or current_token.terminal == "int" or current_token.terminal == "float" or current_token.terminal == "str":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "parameter")
                        self.state = "func_args2"
                        continue
                    return warning("symbol", current_token.content)
                return warning("[bool] or [int] or [float] or [str] or [nothing]", current_token.content)
            
            if self.state == "func_args2":
                if current_token.terminal == ',':
                    current_token = self.stream.pop()
                    if current_token.terminal == "bool" or current_token.terminal == "int" or current_token.terminal == "float" or current_token.terminal == "str":
                        current_token = self.stream.pop()
                        if current_token.terminal == "symbol":
                            if self.symbols.contains(current_token.content):
                                return already_defined(current_token.content, self.symbols.get(current_token.content))
                            self.symbols.append(current_token.content, "parameter")
                            continue
                        return warning("symbol", current_token.content)
                    return warning("[bool] or [int] or [float] or [str]", current_token.content)
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    continue
                return warning("[\\n] or [,]", current_token.content)
            
            if self.state == "func_args3":
                if current_token.terminal == '\\n':
                    self.state = "func_body"
                    continue
                return warning("[\\n]", current_token.content)
            
            if self.state == "func_body":
                if current_token.terminal == 'assign':
                    self.state = "assign_op"
                    continue
                if current_token.terminal == "end":
                    self.state = "func_end"
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
                    continue
                if current_token.terminal == "while":
                    self.state = "while"
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
                return warning("[+] or [-] or [*] or [/] or [>] or [<] or [&]", current_token.content)
            
            if self.state == "num_op3":
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
                if current_token.terminal == "to":
                    current_token = self.stream.pop()
                    if current_token.terminal == "symbol":
                        if self.symbols.contains(current_token.content):
                            return already_defined(current_token.content, self.symbols.get(current_token.content))
                        self.symbols.append(current_token.content, "bool")
                        self.state = "func_body"
                        continue
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
                if current_token.terminal == "Symbol":
                    if not self.symbols.contains(current_token.terminal):
                        return not_defined(current_token.terminal)
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