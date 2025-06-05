
# DVA245, Exercise session 3, bracket matching
left_brackets = "{[("
right_brackets = "}])"
# returns True if letter is a left bracket, False otherwise
def left_bracket(letter):
    return letter in left_brackets
# returns True if letter is a right bracket, False otherwise
def right_bracket(letter):
    return letter in right_brackets
# returns True if left and right are matching brackets
def matching(left, right):
# find returns the index in the string
# '(' and ')' both have index 2, so they match
    return left_brackets.find(left) == right_brackets.find(right)
# TODO: implement
def matching_brackets(expr):
    stack = []
    for letter in expr:
        if left_bracket(letter):
            stack.append(letter)
        
        elif right_bracket(letter):
            if len(stack) == 0:
                return False
            if not matching(stack.pop(), letter):
                return False
    return len(stack) == 0
        
if __name__=='__main__':
    expr = "(m{w[d]a}[d(s)l])"
    print("Matching should be True:", matching_brackets(expr))
    expr = "(m(w[d]a}[d(s)l])"
    print("Matching should be False:", matching_brackets(expr))
    expr = "(m{w[d]a}[d(s)l]"
    print("Matching should be False:", matching_brackets(expr)) 
    expr = ")m{w[d]a}[d(s)l])"
    print("Matching should be False:", matching_brackets(expr))
    # expr = input('Expression to check:')
    # result = matching_brackets(expr)
    # print("Result ok: ", result)
