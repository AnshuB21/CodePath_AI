"""
Task class representing a pet care task.
"""


class Task:
    """Represents a single pet care activity (e.g., feeding, walking, grooming).
    
    This class encapsulates all information needed to manage a pet care task,
    including its description, time requirement, frequency/priority, and status.
    """
    
    def __init__(self, name: str, duration_minutes: int, priority: str, category: str):
        """
        Initialize a Task with its core attributes.
        
        Args:
            name: Task name (description of the activity)
            duration_minutes: Duration in minutes (how long does this task take)
            priority: Priority level (e.g., 'high', 'medium', 'low')
            category: Task category (e.g., 'feeding', 'walking', 'grooming')
        """
        # Store the task's basic information
        self.name: str = name
        self.duration_minutes: int = duration_minutes
        self.priority: str = priority
        self.category: str = category
        
        # Track whether this task has been completed today
        self.completed: bool = False
    
    def is_high_priority(self) -> bool:
        """Determine if this task is high priority and should be scheduled first.
        
        Returns:
            True if priority is 'high', 'critical', or 'urgent', False otherwise
        """
        # Check if priority matches any high-priority labels
        return self.priority.lower() in ['high', 'critical', 'urgent']
    
    def to_dict(self) -> dict:
        """Convert task data to a dictionary for storage or serialization.
        
        Returns:
            Dictionary containing all task attributes
        """
        # Return all task attributes as a dictionary
        return {
            'name': self.name,
            'duration_minutes': self.duration_minutes,
            'priority': self.priority,
            'category': self.category,
            'completed': self.completed
        }
