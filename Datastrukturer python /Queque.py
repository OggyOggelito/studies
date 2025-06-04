class Queque:
    def __init__(self, size):
        """
        Initializes a circular deque with a given size.
        """
        self.__max_size = size  # Maximum capacity
        self.__deque = [None] * size  # Storage as a list
        self.__front = 1  # Starting index for front
        self.__rear = 0  # Starting index for rear
        self.__n_items = 0  # Number of elements currently in the deque

    def is_empty(self):
        """Returns True if the deque is empty, otherwise False."""
        return self.__n_items == 0

    def is_full(self):
        """Returns True if the deque is full, otherwise False."""
        return self.__n_items == self.__max_size

    def insert_left(self, item):
        """Inserts an item at the front of the deque."""
        if self.is_full():
            raise RuntimeError("Deque overflow")
        
        # Move front pointer one step left (circularly)
        self.__front = (self.__front - 1) % self.__max_size
        
        self.__deque[self.__front] = item # Inserts item to the new first index
        self.__n_items += 1  # Increase item count

    def insert_right(self, item):
        """Inserts an item at the rear of the deque."""
        if self.is_full():
            raise RuntimeError("Deque overflow")
        
        # Move rear pointer one step right (circularly)
        self.__rear = (self.__rear + 1) % self.__max_size
        self.__deque[self.__rear] = item 
        self.__n_items += 1  # Increase item count

    def remove_left(self):
        """Removes and returns an item from the front of the deque."""
        if self.is_empty():
            raise RuntimeError("Deque underflow")
        
        item = self.__deque[self.__front]  # Get the item to return
        self.__deque[self.__front] = None  # Clear the slot

        # Move front pointer one step right (circularly)
        self.__front = (self.__front + 1) % self.__max_size
        self.__n_items -= 1  # Decrease item count
        
        return item  # Return removed element

    def remove_right(self):
        """Removes and returns an item from the rear of the deque."""
        if self.is_empty():
            raise RuntimeError("Deque underflow")
        
        item = self.__deque[self.__rear]  # Get the item to return
        self.__deque[self.__rear] = None  # Clear the slot
        
        # Move rear pointer one step left (circularly)
        if self.__n_items > 1:
            self.__rear = (self.__rear - 1) % self.__max_size
        else:
            # Reset both pointers when deque is empty
            self.__rear = 0
            self.__front = 1

        self.__n_items -= 1  # Decrease item count
        
        return item  # Return removed element

    def __len__(self):
        """Returns the number of elements in the deque."""
        return self.__n_items

    def __str__(self):
        """Returns a string representation of the deque."""
        if self.is_empty():
            return "Deque: [] | Front: None | Rear: None"

        result = []
        index = self.__front
        for _ in range(self.__n_items):
            result.append(str(self.__deque[index]))
            index = (index + 1) % self.__max_size  # Move index circularly
        
        return f"Deque: [{', '.join(result)}] | Front: {self.__front} | Rear: {self.__rear}"