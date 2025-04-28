# ALGORITMO 1: Generación de cadenas de prueba para el PDA
import random
import json

def generate_grammar_string(max_depth=10, current_depth=0):
    
    if current_depth >= max_depth:
        return ""  
    
    choice = random.random()
    if choice < 0.5 or current_depth >= max_depth - 1:
        return ""  
    else:
        inner_string = generate_grammar_string(max_depth, current_depth + 1)
        return "a" + inner_string + "b"

def generate_non_grammar_string(max_length=10):
    
    length = random.randint(1, max_length)
    string = "".join(random.choice(["a", "b"]) for _ in range(length))
    
    while is_valid_grammar_string(string):
        if len(string) > 0:
            pos = random.randint(0, len(string) - 1)
            char = "a" if string[pos] == "b" else "b"
            string = string[:pos] + char + string[pos+1:]
        else:
            string = random.choice(["a", "b"])
    
    return string

def is_valid_grammar_string(s):
   
    if s == "":
        return True  
    
    count_a = 0
    count_b = 0
    i = 0
    while i < len(s) and s[i] == 'a':
        count_a += 1
        i += 1
    while i < len(s) and s[i] == 'b':
        count_b += 1
        i += 1
    
    return i == len(s) and count_a == count_b

def generate_test_strings():
    
    grammar_strings = []
    for _ in range(5):
        s = generate_grammar_string()
        if s not in grammar_strings:
            grammar_strings.append(s)
    
    if "" not in grammar_strings:
        grammar_strings.append("")
    if len(grammar_strings) < 2 or all(s == "" for s in grammar_strings):
        grammar_strings.append("aabb")
    
    non_grammar_strings = []
    for _ in range(5):
        s = generate_non_grammar_string()
        if s not in non_grammar_strings:
            non_grammar_strings.append(s)
    
    return grammar_strings + non_grammar_strings

def alg1_main():
    
    test_strings = generate_test_strings()
    
    with open("test_strings.json", "w") as file:
        json.dump(test_strings, file)
    
    return test_strings

if __name__ == "__main__":
    test_strings = alg1_main()
    print("Cadenas generadas:")
    for s in test_strings:
        print(f'  "{s}"')  