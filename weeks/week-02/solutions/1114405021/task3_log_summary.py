"""
Task 3: Log Summary
Analyze user action logs and compute statistics
"""
from collections import defaultdict, Counter


def analyze_logs(logs):
    """
    Analyze event logs and return user statistics and top action.
    
    User Statistics:
    - Sort by event count (descending), then by user name (ascending)
    
    Top Action:
    - Find the action with the highest occurrence count
    
    Time Complexity: O(n log n) for sorting, where n is number of unique users
    Space Complexity: O(u + a) for users and actions, where u = unique users, a = unique actions
    
    Args:
        logs: List of tuples (user, action)
        
    Returns:
        Tuple of:
        - List of (user, count) tuples sorted by count (desc) then name (asc)
        - Tuple of (action, count) for the most common action
        
    Example:
        >>> logs = [("alice", "login"), ("bob", "login"), ("alice", "logout")]
        >>> users, top = analyze_logs(logs)
        >>> users
        [('alice', 2), ('bob', 1)]
        >>> top
        ('login', 2)
    """
    # Handle empty input
    if not logs:
        return [], (None, 0)
    
    # Count events per user using defaultdict
    user_counts = defaultdict(int)
    for user, action in logs:
        user_counts[user] += 1
    
    # Count action occurrences using Counter
    action_counts = Counter()
    for user, action in logs:
        action_counts[action] += 1
    
    # Sort users by count (descending) then by name (ascending)
    user_list = sorted(user_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Find top action
    top_action = action_counts.most_common(1)[0] if action_counts else (None, 0)
    
    return user_list, top_action


def main():
    """Main function to demonstrate log analysis"""
    # Read number of log entries
    m = int(input())
    
    # Read logs
    logs = []
    for _ in range(m):
        parts = input().split()
        user = parts[0]
        action = parts[1]
        logs.append((user, action))
    
    # Analyze logs
    user_stats, top_action = analyze_logs(logs)
    
    # Output user statistics
    for user, count in user_stats:
        print(f"{user} {count}")
    
    # Output top action
    if top_action[0] is not None:
        print(f"top_action: {top_action[0]} {top_action[1]}")


if __name__ == "__main__":
    main()
