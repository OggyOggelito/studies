
"""Uppgift 1 a) & b)"""
""" import time # Import time module

def myMoon():
    while True:
        
        print("Hello Moon!")
        time.sleep(1/5)
def main(): # Main function
    myMoon()
    for i in range(1, 11): # for-statement to print "Hello World 10 times"
        i = "Hello World"
        print(i)
        time.sleep(1) # Prints "Hello World with 1 second delay"


if __name__ == "__main__":
    main() """
    
"""Uppgift 2"""
"""import time
import threading

def myMoon(user_input):
    
    while True:
        print(user_input)
        time.sleep(1/5)
    
if __name__ == "__main__":
    user_input = input("Enter string: ")
    x = threading.Thread(target=myMoon, args=(user_input,), daemon=True)
    x.start()
    
    for i in range(1, 11):
        print("Hello World")
        time.sleep(1)"""
        


"""Uppgift 3"""
import time # Import time module
import time # Import time module
import threading # Import threading module
lock = threading.Lock()
turn = "main" #set turn to moon to start with myMoon function

def myMoon(user_input): # myMoon is a copied function of main
    global turn # global turn to check which turn 
    while True:
        with lock: # lock the function
            if turn == "moon": #check if turn is moon
                for _ in range(10): # print 10 times
                    print(user_input)
                    time.sleep(1) 
                turn = "main" #switch turn to main

if __name__ == "__main__":
    # main doesn't need global turn cause it is the main function
    user_input = input("Enter string input: ") # start with user input
    x = threading.Thread(target=myMoon, args=(user_input,), daemon=True) # thread target myMoon function
    x.start() # start the threads
    
    while True:
        with lock: # lock main from printing
            if turn == "main": # if turn == main, then we print hello world
                
                for _ in range(10): #Prints hello world! 10 times
                    print("Hello World!")
                    time.sleep(1) # Prints "Hello World with 1 second delay
                turn = "moon" # switch the turn to myMoon function