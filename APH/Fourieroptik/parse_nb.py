import json
import sys

def parse_notebook(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        for i, c in enumerate(nb['cells']):
            print(f"Cell {i} ({c['cell_type']})")
            print("".join(c.get('source', [])))
            print("-" * 40)

if __name__ == "__main__":
    parse_notebook(sys.argv[1])
