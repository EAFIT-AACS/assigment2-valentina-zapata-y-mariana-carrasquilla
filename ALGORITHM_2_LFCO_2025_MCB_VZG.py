# ALGORITMO 2: Implementación de un PDA para reconocer cadenas de la gramática

import json

class PushdownAutomaton:
    def __init__(self):
        self.stack = []
        self.state = 'q0'  
        self.final_states = {'q1'}  
        self.input_symbols = {'a', 'b'}
        self.stack_symbols = {'Z', 'A'}  
        self.configurations = []
        
    def initialize(self):
        
        self.stack = ['Z']  
        self.state = 'q0'
        self.configurations = []
        
    def process_input(self, input_string):
        
        self.initialize()
        self.configurations.append({
            'state': self.state,
            'stack': self.stack.copy(),
            'remaining_input': input_string
        })
        
        for char in input_string:
            if self.state == 'q0' and char == 'a':
                self.stack.append('A')
            elif self.state == 'q0' and char == 'b' and self.stack and self.stack[-1] == 'A':
                self.stack.pop()
            else:
                return False  
        
        return self.stack == ['Z']

    def get_configurations(self): 
        return self.configurations

def main():
    
    with open("test_strings.json", "r") as file:
        test_strings = json.load(file)
    
    pda = PushdownAutomaton()
    
    accepted_strings = []
    rejected_strings = []
    
    for s in test_strings:
        print(f'\nProcesando cadena: "{s}"')  
        result = pda.process_input(s)
        status = "ACEPTADA" if result else "RECHAZADA"
        print(f"Resultado: {status}")
        
        if result:
            accepted_strings.append(s)
        else:
            rejected_strings.append(s)
    
    
    print("\nCadenas aceptadas:")
    for s in accepted_strings:
        print(f'  "{s}"')  
    
    print("\nCadenas rechazadas:")
    for s in rejected_strings:
        print(f'  "{s}"')  

if __name__ == "__main__":
    main()