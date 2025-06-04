#Mathlete program
print(' .: MATHLETE v2.0 :. ')
print('---------------------')
#List for numbers
numbers = []
#While-loop for user to store numbers and break the loop
while True:
    user_input = input('> ')
    
    if user_input.lower() == 'exit':
        break
    #try to fetch numbers and append to list
    try: 
        number = float(user_input)
        numbers.append(number)
        #except values that does not fit the list
    except ValueError:
        print('Error: Invalid number')
#If-statement for counting, calculating and the sum of all numbers
if numbers:
    count = len(numbers)
    total_sum = sum(numbers)
    mean_value = total_sum / count
    
print('----------------------------')
print('Cardinality:', count, '\n', 'Sum:', total_sum, '\n', 'Mean value:', mean_value)