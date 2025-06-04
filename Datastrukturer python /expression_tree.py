# tokenize from:
#
# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class NumberNode:
    """ Represents a numeric leaf node in the expression tree."""
    def __init__(self, value):
        self.value = float(value)  # Ensure all values are stored as floating-point numbers

    def evaluate(self):
        """ Returns the numeric value of the node."""
        return self.value

    def __str__(self):
        return str(int(self.value) if self.value.is_integer() else self.value)

class OperatorNode:
    """ Represents an operator node in the expression tree, with left and right children."""
    def __init__(self, operator, left, right):
        self.operator = operator  # Operator: +, -, *, /
        self.left = left  # Left operand (subtree or number)
        self.right = right  # Right operand (subtree or number)

    def evaluate(self):
        """ Evaluates the expression for this node by evaluating children."""
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val if right_val != 0 else float('inf')
        else:
            raise ValueError("Unknown operator: " + self.operator)

    def __str__(self):
        """ Returns a string representation of the expression."""
        return f'({self.left} {self.operator} {self.right})'

def tokenize(raw):
    """Splits an expression string into tokens (numbers, operators, parentheses)."""
    SYMBOLS = set('+-*/() ')
    mark = 0
    tokens = []
    n = len(raw)
    
    for j in range(n):
        if raw[j] in SYMBOLS:
            if mark != j:                 
                tokens.append(raw[mark:j])  # Store preceding number
            if raw[j] != ' ':
                tokens.append(raw[j])       # Store operator or parenthesis
            mark = j + 1
    
    if mark != n:                 
        tokens.append(raw[mark:n])  # Store the last number
    
    return tokens

def build_expression_tree(tokens):
    """Builds an expression tree from a list of tokens using a stack."""
    stack = []
    
    for token in tokens:
        if token.isnumeric():
            stack.append(NumberNode(token))  # Push number as NumberNode
        elif token in '+-*/':
            stack.append(token)  # Push operator
        elif token == ')':
            # Pop operands and operator
            right = stack.pop()
            operator = stack.pop()
            left = stack.pop()
            stack.append(OperatorNode(operator, left, right))  # Push new OperatorNode
    
    return stack[0]  # Root of the expression tree

def main():
    """Main function to test expression tree construction and evaluation."""
    test_expression_string = "(((3+5)/(5-3))+((2*5)-(9-4)))"
    
    print("\nOriginal Expression:", test_expression_string)
    
    tokens = tokenize(test_expression_string)
    print("\nTokenized Expression:", tokens)  # Display tokenized output

    tree = build_expression_tree(tokens)

    print("\nExpression Tree (Infixed Notation):", tree)  # Should print structured expression
    print("\nEvaluated Result:", tree.evaluate())  # Compute final result
    

if __name__ == "__main__":
    main()
