import sys
import ast
import astor
import random

# Mutation operators

def negate_comparison_ops(node):
    if isinstance(node, ast.Compare):
        # Negate comparison operators
        for i, op in enumerate(node.ops):
            if isinstance(op, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot)):
                node.ops[i] = negate_comparison(op)
    return node

def negate_comparison(op):
    if isinstance(op, ast.Eq):
        return ast.NotEq()
    elif isinstance(op, ast.NotEq):
        return ast.Eq()
    elif isinstance(op, ast.Lt):
        return ast.GtE()
    elif isinstance(op, ast.LtE):
        return ast.Gt()
    elif isinstance(op, ast.Gt):
        return ast.LtE()
    elif isinstance(op, ast.GtE):
        return ast.Lt()
    elif isinstance(op, ast.Is):
        return ast.IsNot()
    elif isinstance(op, ast.IsNot):
        return ast.Is()
    else:
        return op

def swap_binary_ops(node):
    if isinstance(node, ast.BinOp):
        # Swap binary operators
        if isinstance(node.op, ast.Add):
            node.op = ast.Sub()
        elif isinstance(node.op, ast.Sub):
            node.op = ast.Add()
        elif isinstance(node.op, ast.Mult):
            node.op = ast.FloorDiv()
        elif isinstance(node.op, ast.FloorDiv):
            node.op = ast.Mult()
    return node

def delete_statements(node):
    if isinstance(node, (ast.Assign, ast.Expr)):
        # Delete assignment or function call statements
        return None
    return node

def mutate_ast(tree):
    # Apply mutation operators to AST
    tree = ast.fix_missing_locations(tree)
    tree = negate_comparison_ops(tree)
    tree = swap_binary_ops(tree)
    tree = delete_statements(tree)
    return tree

def main():
    if len(sys.argv) != 3:
        print("Usage: python mutate.py <input_program.py> <num_mutants>")
        sys.exit(1)

    input_file = sys.argv[1]
    num_mutants = int(sys.argv[2])

    # Parse input program
    with open(input_file, 'r') as f:
        source_code = f.read()
    tree = ast.parse(source_code)

    # Create mutants
    for i in range(num_mutants):
        mutant_tree = mutate_ast(ast.copy.deepcopy(tree))

        # Serialize mutated AST to Python source code
        mutant_code = astor.to_source(mutant_tree)

        # Write mutant to file
        mutant_file = f"{i}.py"
        with open(mutant_file, 'w') as f:
            f.write(mutant_code)

if __name__ == "__main__":
    main()

