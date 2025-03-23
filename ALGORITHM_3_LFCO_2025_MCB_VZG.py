# ALGORITMO 3: Construcción de árbol de derivación y visualización

import json
import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.font_manager import FontProperties

class TreeNode:
    def __init__(self, content, children=None):
        self.content = content
        self.children = children if children is not None else []
    
    def add_child(self, child):
        self.children.append(child)
        
    def __repr__(self):
        return f"Node({self.content})"

def build_leftmost_derivation_tree(input_string):
    
    if input_string == "":
        
        root = TreeNode("S")
        root.add_child(TreeNode("ε"))
        return root
    
    count_a = input_string.count('a')
    count_b = input_string.count('b')
    
    if count_a != count_b or input_string[:count_a] != "a" * count_a or input_string[count_a:] != "b" * count_b:
        return None  
    
    root = TreeNode("S")
    current_node = root
    
    for i in range(count_a):
       
        new_node = TreeNode("S" if i < count_a-1 else "ε")
        current_node.add_child(TreeNode("a"))
        current_node.add_child(new_node)
        current_node.add_child(TreeNode("b"))
        current_node = new_node
    
    return root

def build_pda_computation_tree(input_string, pda):
  
    pda.initialize()
    configurations = []
    state = pda.state
    stack = pda.stack.copy()
    remaining = input_string
    
    configurations.append({
        'state': state,
        'stack': stack.copy(),
        'remaining_input': remaining
    })
    
    for i, char in enumerate(input_string):
        if state == 'q0' and char == 'a':
            stack.append('A')
        elif state == 'q0' and char == 'b' and stack and stack[-1] == 'A':
            stack.pop()
        else:
            
            configurations.append({
                'state': 'qr',  
                'stack': stack.copy(),
                'remaining_input': remaining[i+1:] if i+1 < len(remaining) else ""
            })
            return configurations
        
        remaining = remaining[1:]
        
        configurations.append({
            'state': state,
            'stack': stack.copy(),
            'remaining_input': remaining
        })
    
    
    if stack == ['Z']:
        state = 'q1'  
    else:
        state = 'qr'  
    
    configurations.append({
        'state': state,
        'stack': stack.copy(),
        'remaining_input': ""
    })
    
    return configurations

def print_tree(node, prefix="", is_last=True, file=None):
    
    if file:
        print(f"{prefix}{'└── ' if is_last else '├── '}{node.content}", file=file)
    else:
        print(f"{prefix}{'└── ' if is_last else '├── '}{node.content}")
    
    prefix += "    " if is_last else "│   "
    
    for i, child in enumerate(node.children):
        is_last_child = (i == len(node.children) - 1)
        print_tree(child, prefix, is_last_child, file)

def export_tree_to_file(tree, filename):
    
    with open(filename, 'w', encoding='utf-8') as f:
        print_tree(tree, file=f)
    print(f"Árbol guardado en {filename}")

def tree_to_networkx(node, graph=None, parent=None, pos=None, x=0, y=0, level=0, width=1.0):
   
    if graph is None:
        graph = nx.DiGraph()
        pos = {}
    
    node_id = id(node)
    graph.add_node(node_id, label=node.content)
    pos[node_id] = (x, -level)  
    
    if parent is not None:
        graph.add_edge(parent, node_id)
    
    num_children = len(node.children)
    if num_children > 0:
        new_width = width / num_children
        start_x = x - (width / 2) + (new_width / 2)
        
        for i, child in enumerate(node.children):
            child_x = start_x + i * new_width
            tree_to_networkx(child, graph, node_id, pos, child_x, y-1, level+1, new_width)
    
    return graph, pos

def visualize_tree(tree, title, filename):
   
    if tree is None:
        print(f"No se puede visualizar un árbol nulo para {title}")
        return
    
    graph, pos = tree_to_networkx(tree)
    
    plt.figure(figsize=(12, 8))
    plt.title(title)
    
    nx.draw(graph, pos, with_labels=False, arrows=False, node_size=2500, 
            node_color='lightblue', node_shape='o', alpha=0.8, linewidths=1, 
            font_size=10, font_weight='bold', edge_color='grey')
    
    labels = {node: data['label'] for node, data in graph.nodes(data=True)}
    nx.draw_networkx_labels(graph, pos, labels, font_size=8, font_family='sans-serif')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Visualización guardada en {filename}")
    plt.close()

def visualize_computation(configurations, input_string, filename):
    
    if not configurations:
        print(f"No hay configuraciones para visualizar: {input_string}")
        return
    
    graph = nx.DiGraph()
    pos = {}
    
    for i, config in enumerate(configurations):
        node_id = i
        state = config['state']
        stack_str = ''.join(config['stack'])
        remaining = config['remaining_input']
        
        if i == 0:
            label = f"Inicio: q={state}, π={stack_str}"
        elif i == len(configurations) - 1:
            result = "ACEPTADA" if state == 'q1' else "RECHAZADA"
            label = f"Final: q={state}, π={stack_str}\n{result}"
        else:
            symbol = configurations[i-1]['remaining_input'][0] if configurations[i-1]['remaining_input'] else 'ε'
            action = "Push(A)" if len(config['stack']) > len(configurations[i-1]['stack']) else \
                    "Pop(A)" if len(config['stack']) < len(configurations[i-1]['stack']) else "No-op"
            label = f"Paso {i}: q={state}, π={stack_str}\nLeer: {symbol}, {action}"
        
        graph.add_node(node_id, label=label)
        pos[node_id] = (i, 0)  
        
        if i > 0:
            graph.add_edge(i-1, i)
    
    plt.figure(figsize=(15, 5))
    plt.title(f"Computación del PDA para la cadena: '{input_string}'")
    
    nx.draw(graph, pos, with_labels=False, arrows=True, node_size=3500, 
            node_color='lightgreen', node_shape='s', alpha=0.7, linewidths=1, 
            font_size=10, font_weight='bold', edge_color='grey', arrowsize=15)
    
    labels = {node: data['label'] for node, data in graph.nodes(data=True)}
    nx.draw_networkx_labels(graph, pos, labels, font_size=7, font_family='sans-serif')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Visualización de computación guardada en {filename}")
    plt.close()

def main():
    print("ALGORITMO 3: Construcción de árboles de derivación y visualización")
    print("=============================================================")
    
    try:
        from ALGORITHM_2_LFCO_2025_MCB_VZG import PushdownAutomaton
        pda = PushdownAutomaton()
    except ImportError:
        print("Error: No se pudo importar PushdownAutomaton del Algoritmo 2.")
        return
    
    try:
        with open("test_strings.json", "r") as file:
            test_strings = json.load(file)
        print(f"Se cargaron {len(test_strings)} cadenas de prueba.")
    except FileNotFoundError:
        print("No se encontró el archivo test_strings.json. Usando cadenas predeterminadas.")
        test_strings = ["", "ab", "aabb", "aaabbb", "a", "b", "aab", "abb", "abab"]
    
    output_dir = "resultados_arboles"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    accepted_strings = []
    
    for input_string in test_strings:
        print(f"\nProcesando cadena: \"{input_string}\"")
        is_accepted = pda.process_input(input_string)
        
        if is_accepted:
            accepted_strings.append(input_string)
            print(f"La cadena \"{input_string}\" es ACEPTADA por el PDA.")
            
            derivation_tree = build_leftmost_derivation_tree(input_string)
            safe_name = input_string.replace("", "empty") if input_string == "" else input_string
            
            derivation_file = os.path.join(output_dir, f"derivation_tree_{safe_name}.txt")
            export_tree_to_file(derivation_tree, derivation_file)
            
            derivation_img = os.path.join(output_dir, f"derivation_tree_{safe_name}.png")
            visualize_tree(derivation_tree, f"Árbol de derivación para '{input_string}'", derivation_img)
            
            configurations = build_pda_computation_tree(input_string, pda)
            
            comp_img = os.path.join(output_dir, f"computation_{safe_name}.png")
            visualize_computation(configurations, input_string, comp_img)
            
        else:
            print(f"La cadena \"{input_string}\" es RECHAZADA por el PDA.")
    
    print("\nResumen:")
    print(f"Total de cadenas procesadas: {len(test_strings)}")
    print(f"Cadenas aceptadas: {len(accepted_strings)}")
    print(f"Cadenas rechazadas: {len(test_strings) - len(accepted_strings)}")
    
    print("\nCadenas aceptadas:")
    for s in accepted_strings:
        print(f'  "{s}"')
    
    print("\nSe han generado visualizaciones en el directorio:", output_dir)

if __name__ == "__main__":
    main()