import random

# Generate a random number between 0 and 99
rand = random.randint(0, 99)

print(" .: HIGHER OR LOWER GAME :. ")
print("-----------------------------\nWelcome to the Higher or Lower game.")

tries = 4


# Loop until the correct number is guessed
while tries > 0:
    # Initial guess input
    numchoice = int(input('Guess a number between 0 and 99: '))
    
    if numchoice == rand:
        print(f'You guessed the right number! The number was {numchoice}.\n----------------------------------------------')
        break
    elif numchoice < rand:
        print('Guess a higher number!')
    else:
        print('Guess a lower number!')
    
    tries -= 1
if tries == 0 and numchoice != rand:
    print(f'Sorry, you have run out of tries. The number was {rand}')
