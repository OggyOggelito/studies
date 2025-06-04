from Queque import Queque

def test_queque():
    dq = Queque(5)
    
    print('\nInitial Deque:')
    print(dq)
    
    # Insert elements at the right
    dq.insert_right(1)
    print("\nAfter insert_right(1):", dq)
    
    dq.insert_right(2)
    print("\nAfter insert_right(2):", dq)
    
    dq.insert_right(3)
    print("\nAfter insert_right(3):", dq)

    assert dq.remove_left() == 1
    print("\nAfter remove_left() (removed 1):", dq)

    assert dq.remove_left() == 2
    print("\nAfter remove_left() (removed 2):", dq)

    dq.insert_left(4)
    print("\nAfter insert_left(4):", dq)
    
    dq.insert_left(5)
    print("\nAfter insert_left(5):", dq)
    
    dq.insert_left(6)
    print("\nAfter insert_left(6):", dq)

    assert dq.remove_right() == 3
    print("\nAfter remove_right() (removed 3):", dq)

    assert dq.remove_right() == 4
    print("\nAfter remove_right() (removed 4):", dq)

    dq.insert_right(7)
    print("\nAfter insert_right(7):", dq)
    
    dq.insert_right(8)
    print("\nAfter insert_right(8):", dq)
    
    dq.insert_left(9)
    print("\nAfter insert_left(9):", dq)

    assert dq.remove_left() == 9
    print("\nAfter remove_left() (removed 9):", dq)

    assert dq.remove_right() == 8
    print("\nAfter remove_right() (removed 8):", dq)

    print("\nTest completed successfully.")

if __name__ == '__main__':
    test_queque()