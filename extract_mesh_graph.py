import os
import re

def parse_foam_list(filepath):
    """Parses a basic OpenFOAM labelList file."""
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the list content between parentheses
    match = re.search(r'\d+\s*\n\s*\((.*)\)', content, re.DOTALL)
    if not match:
        return []
    
    # Split by whitespace and convert to integers
    data = match.group(1).split()
    return [int(x) for x in data]

def extract_graph(case_path):
    mesh_path = os.path.join(case_path, 'constant/polyMesh')
    owner = parse_foam_list(os.path.join(mesh_path, 'owner'))
    neighbour = parse_foam_list(os.path.join(mesh_path, 'neighbour'))
    
    print(f"Total Faces: {len(owner)}")
    print(f"Internal Faces (Edges): {len(neighbour)}")
    
    # The first 'len(neighbour)' faces are the internal ones connecting two cells
    graph = []
    for i in range(len(neighbour)):
        u = owner[i]
        v = neighbour[i]
        graph.append((u, v))
        
    return graph

# Example usage on the airfoil tutorial
case = 'tutorials/incompressibleFluid/airFoil2D'
connections = extract_graph(case)

print("\nFirst 10 graph edges (Cell U -> Cell V):")
for edge in connections[:10]:
    print(f"Cell {edge[0]} <---> Cell {edge[1]}")
