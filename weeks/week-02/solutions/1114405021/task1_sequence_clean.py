"""
Task 1: Sequence Clean
Operations: deduplicate, sort ascending, sort descending, extract evens
"""


def dedupe_preserve_order(numbers):
    """
    Remove duplicates while preserving the order of first occurrence.
    
    Time Complexity: O(n) where n is the length of numbers
    Space Complexity: O(n) for the seen dictionary and result list
    
    Args:
        numbers: List of integers
        
    Returns:
        List of integers with duplicates removed, preserving first occurrence order
        
    Note: Uses dictionary tracking instead of set to preserve insertion order
    """
    seen = {}
    result = []
    for num in numbers:
        if num not in seen:
            seen[num] = True
            result.append(num)
    return result


def sort_ascending(numbers):
    """
    Sort numbers in ascending order.
    
    Args:
        numbers: List of integers
        
    Returns:
        List of integers sorted in ascending order
    """
    return sorted(numbers)


def sort_descending(numbers):
    """
    Sort numbers in descending order.
    
    Args:
        numbers: List of integers
        
    Returns:
        List of integers sorted in descending order
    """
    return sorted(numbers, reverse=True)


def extract_evens(numbers):
    """
    Extract even numbers while maintaining original order.
    
    Args:
        numbers: List of integers
        
    Returns:
        List of even numbers in original order
    """
    return [num for num in numbers if num % 2 == 0]


def main():
    """Main function to demonstrate all operations"""
    # Read input
    line = input("Enter space-separated integers: ")
    numbers = list(map(int, line.split()))
    
    # Perform operations
    dedupe_result = dedupe_preserve_order(numbers)
    asc_result = sort_ascending(numbers)
    desc_result = sort_descending(numbers)
    evens_result = extract_evens(numbers)
    
    # Output results
    print(f"dedupe: {' '.join(map(str, dedupe_result))}")
    print(f"asc: {' '.join(map(str, asc_result))}")
    print(f"desc: {' '.join(map(str, desc_result))}")
    print(f"evens: {' '.join(map(str, evens_result))}")


if __name__ == "__main__":
    main()
