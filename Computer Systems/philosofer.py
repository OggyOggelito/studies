import threading # Import threading module
import time # Import time
forks = [threading.Lock() for _ in range(5)] # 5 forks 

def philosopher(i):
    while True:
        print(f"Philosofer {i} thinking") 
        time.sleep(0.01)  # 10ms

        left = i
        right = (i + 1) % 5 

        # Index of the left and right forks for the philosofers
        if i % 2 == 0:
            forks[left].acquire()
            forks[right].acquire()
        else:
            forks[right].acquire()
            forks[left].acquire()
            
        
        print(f"Philosofer {i} has acquired their forks")
        # Grabs forks in different orders depending on philosopher index to prevent deadlock
        time.sleep(0.05)  # Eating
        print(f"Philosofer {i} is now full")

        forks[right].release() # release fork right direction
        forks[left].release() # release fork left direction
        print(f"Philosofer {i} has put back their forks")

        
def main():
    for i in range(5): 
        t = threading.Thread(target=philosopher, args=(i,))
        t.daemon = True
        t.start() 

    # Creates and starts 5 philosopher threads
    while True:
        time.sleep(10) # 10 second delay
        
if __name__ == "__main__":
    main()