import ArrayLab1

maxSize = 10  # Max size of the array
arr = ArrayLab1.Array(maxSize)  # Create an array object
arr.insert(77)  # Insert 5 items
arr.insert(12.34)
arr.insert(0)
arr.insert("baz")
arr.insert(-17)
arr.insert('😂')
arr.insert('👌')
arr.insert('💯')
print("Array containing", len(arr), "items")
arr.traverse()
print("Search for 12 returns", arr.search(12))
print("Search for 12.34 returns", arr.search(12.34))
print("Deleting 0 returns", arr.delete(0))
print("Deleting 17 returns", arr.delete(17))
print("Array after deletions has", len(arr), "items")
arr.traverse()
print(len(arr))

# New tests for insert_at
print("\n--- Tests for insert_at ---")

# Test 1: Insert at the beginning
print("\nTest 1: Insert at the beginning")
arr.insert_at(0, "start")  # Insert "start" at index 0
arr.traverse()
print("Length after test 1:", len(arr))

# Test 2: Insert at the end
print("\nTest 2: Insert at the end")
arr.insert_at(len(arr), "end")  # Insert "end" at the end of the array
arr.traverse()
print("Length after test 2:", len(arr))

# Test 3: Insert at in the middle
print("\nTest 3: Insert in the middle")
arr.insert_at(len(arr) // 2, "middle")  # Insert "middle" at the middle index 
arr.traverse()
print("Length after test 3:", len(arr))


# Verify the size of the array after all insertions
print("\nFinal array has", len(arr), "items")