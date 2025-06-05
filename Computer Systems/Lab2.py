import threading
import time

# the buffer and its global index
buffer = [None,None,None,None,None]
bufferIndex=0
buffer_lock = threading.Lock() 
buffer_size = 5
empty_slot = threading.Semaphore(buffer_size) # empty slots
filled_slot = threading.Semaphore(0)
mutex = threading.Lock()
#The individual number of the item 
productItemNo=0


# Producer Thread 
def producer(no: int):
    global productItemNo
    print("Producer " + str(no) + " created!")
    
    while True:
        time.sleep(0.1)
        
        with buffer_lock:
            item = productItemNo
            productItemNo += 1

        
        
        
        ret = insert_item(item)
        print("producer " + str(no) + " produced " + str(item))
        
        
        if ret:
            print(f"Producer {no} produced {item}")
        else:
            print(f"Producer {no} error, buffer full")
        

# Consumer Thread 
def consumer(no: int):
    item = 0
    print("Consumer " + str(no) + " created!")
    
    while True:
        time.sleep(0.1)
        # filled slot acquired 
        ret, item = remove_item()
        # release empty slots 
        
        
        if ret:
            print("consumer " + str(no) + " consumed " + str(item))
        else:
            print(f"Consumer {no} error, buffer empty")
        


# Add an item to the buffer 
def insert_item(item:int):
    global bufferIndex
    #When the buffer is not full add the item
    empty_slot.acquire()
    with mutex:
        if(bufferIndex < 5):
            buffer[bufferIndex] = item
            bufferIndex+=1
            return True
    
        else: # Error the buffer is full
            return False
    filled_slot.release()

# Remove an item from the buffer */
def remove_item():
    global bufferIndex
    # When the buffer is not empty remove the item
    filled_slot.acquire()
    with mutex:
        if(bufferIndex > 0):
            item = buffer[(bufferIndex-1)]
            bufferIndex-=1
            return True,item
        else: # Error buffer empty 
            return False,None
    empty_slot.release()

def main(): 
    # THESE SHOULD BE CHANGED ACCORDING TO THE LAB SPECIFICATION   
    numProd = 10 #Number of producer threads 
    numCons = 3 #Number of consumer threads 
    threads = [] #Empty list
    
    #Create the producer threads 
    #Add code to start numProd producer() thread(s)
    for i in range(numProd): 
        t = threading.Thread(target=producer, args=(i,), daemon=True)
        threads.append(t)
        t.start()
        
    #Create the consumer threads */
    #Add code to start numCons consumer() thread(s)
    for i in range(numCons):
        t = threading.Thread(target=consumer, args=(i,), daemon=True)
        threads.append(t)
        t.start()
        
    

    #Let the program run for 10 seconds    
    time.sleep(10)

if __name__== "__main__":
    main()