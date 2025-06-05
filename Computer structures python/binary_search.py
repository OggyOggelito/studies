def binary_search(item, sorted_list):
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == item:
            return mid
        elif sorted_list[mid] < item:
            low = mid + 1
        else: 
            high = mid -1
        return False

if __name__ == "__main__":
    sorted_list = [1, 3, 5, 7, 9, 12]
    targets_in_list = [1, 3, 5, 7, 9, 12]
    targets_not_in_list = [0, 2, 4, 6, 8, 10, 11, 13]
    
    for t in targets_in_list:
        if not binary_search(t, sorted_list):
            print(f"Failed, did not find", t)
        else: 
            print(f"Success, found {t}")
        
    for t in targets_not_in_list:
        if binary_search(t, sorted_list):
            print(f"Failed, found {t}")
        else:
            print(f"Success, did not find {t}")