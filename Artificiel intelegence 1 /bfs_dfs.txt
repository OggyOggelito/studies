import collections
import time
items = [] # This is our list of items for the knapsack
"""Open txt file to read items"""
with open('Assignment 1 knapsack.txt', 'r') as f:
    lines = f.readlines()

start = False
for line in lines:
    if line.strip() == "ID b w":  # look for the start of the item list
        start = True
        continue
    if line.strip() == "EOF":  # stop reading when we reach the end of the file
        break
    if start:
        parts = line.strip().split()  # Split the line into parts
        if len(parts) == 3:
            _, total_benefit, weight = parts  # Get the benefit and weight
            items.append((int(total_benefit), int(weight))) # Add the item to our list

def knapsack_bfs(items, max_weight):
    max_benefit = 0  # track the maximum benefit we can get
    best_combination = []  # store the best combination of items
    queue = collections.deque([(0, 0, 0, [])])  #start with index, total_benefit, weight, and picked_items

    while queue:
        index, total_benefit, weight, picked_items = queue.popleft()  # get the first item from the queue
        if weight <= max_weight and total_benefit > max_benefit:  # check if this is a better option
            max_benefit = total_benefit
            best_combination = picked_items  # Update the best combination of items

        if index < len(items):  # If there are more items to consider
            # Include the current item
            next_benefit = total_benefit + items[index][0]
            next_weight = weight + items[index][1]
            queue.append((index + 1, next_benefit, next_weight, picked_items + [index]))  # add to the queue, traverse thru all nodes
            # exclude the current item
            queue.append((index + 1, total_benefit, weight, picked_items))  # move to the next item

    print("Most beneficial BFS:", max_benefit)  # output the best benefit found
    total_weight = sum(items[i][1] for i in best_combination) # calculates the total weight
    print("Total weight BFS:", total_weight) # output the total weight BFS
    print("Items taken in (BFS):", best_combination)  # show items picked
    return max_benefit  # return the best benefit

def knapsack_dfs(items, max_weight):
    max_benefit = 0  # track the maximum benefit found
    best_combination = []  # store best combination of items

    def dfs(index, total_benefit, weight, picked_items):
        nonlocal max_benefit, best_combination  # allow access to outer function variables
        if weight <= max_weight and total_benefit > max_benefit:  # check if we have a new best option
            max_benefit = total_benefit
            best_combination = picked_items  # update the best combination
        if index >= len(items):  # if we've checked all items, stop
            return
        # exclude the current item and move to the next
        dfs(index + 1, total_benefit, weight, picked_items) # recursive call
        # include the current item
        next_weight = weight + items[index][1]
        next_benefit = total_benefit + items[index][0]
        if next_weight <= max_weight:  # only continue if we don't exceed weight
            dfs(index + 1, next_benefit, next_weight, picked_items + [index])  # move next with the item picked

    dfs(0, 0, 0, [])  # start the DFS with the first item
    print("Most beneficial DFS:", max_benefit)  # show the best benefit found
    total_weight = sum(items[i][1] for i in best_combination) # calculate total weight
    print("Total weight DFS:", total_weight) # output total weight DFS
    print("Items taken in (DFS):", best_combination)  # show which items were picked
    
    return max_benefit  # return the best benefit
start_time = time.time()

if __name__ == '__main__':
    max_weight = 420  # set the maximum weight for the knapsack

    knapsack_bfs(items, max_weight)
    knapsack_dfs(items, max_weight)

    end_time = time.time()
    print(f"Total time running the code: {end_time - start_time:.4f} seconds")