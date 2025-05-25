import colorama
import sys
from lupa import LuaRuntime
import argparse

parser = argparse.ArgumentParser(description='transpiler.')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
parser.add_argument('-t', '--target', type=str, required=True, help='Type of processing')
parser.add_argument('-o', '--output', type=str, required=True, help='Output file')
args = parser.parse_args()

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('os = nil')
lua.execute('io = nil')

keywords = {
    "init_var": 1,     # gets 1 arg
    "add": 3,          
    "sub": 3,          
    "jmp": 1,
    "cmp": 2,       
    "ret": 0,
    "call": 1,   
    "set": 2,          
    "and": 3,          
    "or": 3,           
    "xor": 3,          
    "shr": 3,          
    "shl": 3,          
    "sar": 3,          
    "asm": 1,          
    "sal": 3,          
    "get_index": 3,    
    "set_index": 3,
    "push":1,
    "pop":1
}

with open(args.input, 'r') as file:
    code = file.read()
with open(args.target, 'r') as file:
    transpiler_code = file.read()

lua.execute(transpiler_code)
funcs = lua.globals()
def tokenize(code: str) -> list:
    result = []
    i = 0

    while i < len(code):
        current = code[i]

        if current.isspace():
            i += 1
            continue

        if current == '.':
            match = ['.']
            i += 1
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                match.append(code[i])
                i += 1
            word = ''.join(match)
            if i < len(code) and code[i] == ':':
                i += 1
                result.append(("label_def", word))
            else:
                result.append(("label_ref", word))
            continue

        if current == '"':
            i += 1
            match = []
            while i < len(code) and code[i] != '"':
                match.append(code[i])
                i += 1
            if i >= len(code) or code[i] != '"':
                raise ValueError("Unterminated string literal")
            i += 1 
            result.append(("string", ''.join(match)))
            continue

        if current.isalpha():
            match = []
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                match.append(code[i])
                i += 1
            word = ''.join(match)
            if word in keywords:
                result.append((word, keywords[word]))
            else:
                result.append(("identifier", word))
            continue

        if current.isdigit():
            match = []
            while i < len(code) and code[i].isdigit():
                match.append(code[i])
                i += 1
            result.append(("num", ''.join(match)))
            continue

        raise ValueError(f"Unexpected character: '{current}' at position {i}")

    result.append(("eof", "eof"))
    return result



def transpile(code: str) -> None:
    tokenized = tokenize(code)
    i = 0
    vars = {}
    var_count = 0
    result = ""
    while i < len(tokenized):
        current = tokenized[i]
        if current[0] == "init_var":
            if tokenized[i+1][0] != 'identifier':
                print('expected identifier got ' + tokenized[i+1][0])
                sys.exit(1)
            if tokenized[i+1][1] not in vars: 
                vars[tokenized[i+1][1]] = var_count
                var_count+=1
            else:
                print("variable already defined : "+tokenized[i+1][1])
            i+=2
            continue
        elif current[0] in keywords:
            b = current[1]
            match = []
            i+=1
            while b != 0 and i < len(tokenized):
                match.append(tokenized[i])
                b-=1
                i+=1
            lua.globals().vars = vars
            result += funcs[current[0]](match)
            continue
        elif current[0] == "eof":
            return result
        i+=1    

                
    return result
print(transpile(code))