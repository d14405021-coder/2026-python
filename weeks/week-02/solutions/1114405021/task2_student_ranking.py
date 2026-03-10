"""
Task 2: Student Ranking
Sort students by score (desc), then age (asc), then name (asc)
Output top k students
"""


def rank_students(students, k):
    """
    Rank students and return top k.
    
    Sorting criteria (multi-level key):
    1. Score: higher is better (descending)
    2. Age: lower is better (ascending) for tiebreaker
    3. Name: alphabetical order (ascending) for tiebreaker
    
    Time Complexity: O(n log n) due to sorting
    Space Complexity: O(k) for the result list
    
    Args:
        students: List of tuples (name, score, age)
        k: Number of top students to return
        
    Returns:
        List of top k student tuples (name, score, age), sorted by ranking
        
    Example:
        >>> students = [("alice", 90, 20), ("bob", 90, 19)]
        >>> rank_students(students, 1)
        [('bob', 90, 19)]  # Bob comes first due to younger age
    """
    # Sort by: -score (descending), age (ascending), name (ascending)
    # Negative score for ascending sort with higher values first
    ranked = sorted(students, key=lambda x: (-x[1], x[2], x[0]))
    return ranked[:k]


def main():
    """Main function to demonstrate ranking"""
    # Read input: first line is n and k
    n, k = map(int, input().split())
    
    # Read student data
    students = []
    for _ in range(n):
        parts = input().split()
        name = parts[0]
        score = int(parts[1])
        age = int(parts[2])
        students.append((name, score, age))
    
    # Rank students and get top k
    top_k = rank_students(students, k)
    
    # Output results
    for name, score, age in top_k:
        print(f"{name} {score} {age}")


if __name__ == "__main__":
    main()
