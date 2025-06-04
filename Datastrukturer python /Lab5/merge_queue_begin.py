# 
# For DVA245 by Anna Friebe, January 2023 

from collections import deque
import random


def merge(S1, S2):
    """Merge two sorted queue instances S1 and S2.
       Result is returned in a new sorted queue.
       Leaves S1 and S2 empty.
       Queues are deques used with the front to the left."""
    S = deque()  # Initialize an empty deque for the merged result
    while S1 or S2:  # Continue as long as either S1 or S2 is not empty
        if not S1:  # If S1 is empty, take from S2
            S.append(S2.popleft())
        elif not S2:  # If S2 is empty, take from S1
            S.append(S1.popleft())
        elif S1[0] <= S2[0]:  # Compare the front elements of S1 and S2
            S.append(S1.popleft())  # Take from S1 if it's smaller or equal
        else:
            S.append(S2.popleft())  # Otherwise, take from S2
    return S  # Return the merged deque
  
def merge_level_queues(level_queues):
    """Merge the sorted queues in level_queues two by two
    into a new queue with about half the number of sorted 
    queues. level_queues is left empty."""
    next_level_queues = deque()
    while len(level_queues) > 1:
        # Pop two queues from the front of level_queues
        queue1 = level_queues.popleft()
        queue2 = level_queues.popleft()
        # Merge the two queues and append the result to next_level_queues
        next_level_queues.append(merge(queue1, queue2))
    
    # If there's an odd number of queues, append the last one to next_level_queues
    if level_queues:
        next_level_queues.append(level_queues.popleft())
        
    # Return the deque containing the merged queues
    
    
    return next_level_queues
  

def merge_sort(S):
    """Sort the elements of queue S using the merge-sort algorithm.
    The sorted result is returned in a new queue, S is left empty
    Queues are deques used with the front to the left. """
    level_queues = deque()  # Initialize a deque to hold queues at each level
    for item in S:
        level_queues.append(deque([item]))  # Create a queue for each item and add it to level_queues
    
    while len(level_queues) > 1:
        level_queues = merge_level_queues(level_queues)  # Merge queues at the current level
    
    if level_queues:
        return level_queues.popleft()  # Return the single remaining merged queue
    else:
        return deque()  # Return an empty queue if the input was empty


if __name__ == '__main__':
    # Tests for merge
    in_queue1 = deque([1, 2, 5, 8, 9])
    in_queue2 = deque([2, 3, 6, 7, 9])
    # correct size for output list
    merged_queue1 = merge(in_queue1, in_queue2)
    merged_result = deque([1, 2, 2, 3, 5, 6, 7, 8, 9, 9])
    if merged_result == merged_queue1:
        print("first merge ok")
    else:
        print("first merge failed")
    in_queue1 = deque([1, 2, 5, 8, 9])
    in_queue2 = deque([2, 3, 6, 7, 9])
    merged_queue2 = merge(in_queue2, in_queue1)
    if merged_result == merged_queue2:
        print("second merge ok")
    else:
        print("second merge failed")
    # Test for merge_queues
    in_queue1 = deque([1, 2, 5, 8, 9])
    in_queue2 = deque([2, 3, 6, 7, 9])
    in_queue3 = deque([3, 4, 8])
    in_queue4 = deque([3, 6, 7, 9])
    in_queue5 = deque([1, 4, 8])
    in_level_queues = deque([in_queue1, in_queue2, in_queue3, in_queue4, in_queue5])
    next_level_queues = merge_level_queues(in_level_queues)
    if len(next_level_queues) == 3:
        print("Expected number of queues from merge_level_queues")
        if next_level_queues[0] == deque([1, 2, 2, 3, 5, 6, 7, 8, 9, 9]):
            print("First queue as expected in merge_level_queues")
            print(next_level_queues[0])
        else:
            print("Error, unexpected queue[0]", next_level_queues[0])
        if next_level_queues[1] == deque([3, 3, 4, 6, 7, 8, 9]):
            print("Second queue as expected in merge_level_queues")
            print(next_level_queues[1])
        else:
            print("Error, unexpected queue[1]", next_level_queues[1])
        if next_level_queues[2] == deque([1, 4, 8]):
            print("Third queue as expected in merge_level_queues")
            print(next_level_queues[2])
        else:
            print("Error, unexpected queue[2]", next_level_queues[2])
        
    else:
        print("Error in merge_level_queues, wrong number of queues in next level")
        
    # Test for merge
    # create two lists with elements 0-99, randomly reordered
    orig_list1 = random.sample(range(100), 100)
    orig_list2 = random.sample(range(100), 100)
    # combine them into one deque with 200 elements
    input_queue = deque(orig_list1)
    input_queue.extend(orig_list2)
    merge_sort_queue = merge_sort(input_queue)
    error_indices = []
    for i in range(100):
        if merge_sort_queue.popleft() != i:
            error_indices.append(i*2)
        if merge_sort_queue.popleft() != i:
            error_indices.append(i*2 + 1)
    if len(error_indices) == 0:
        print("merge sort passed") 
    else:
        print("merge sort failed, errors in indices: ", error_indices)
        
