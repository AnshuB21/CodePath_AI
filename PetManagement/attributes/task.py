"""
Task class representing a pet care task.
"""


class Task:
    """Represents a pet care task."""
    
    def __init__(self, name: str, duration_minutes: int, priority: str, category: str):
        """
        Initialize a Task.
        
        Args:
            name: Task name
            duration_minutes: Duration in minutes
            priority: Priority level
            category: Task category (e.g., feeding, walking, grooming)
        """
        self.name: str = name
        self.duration_minutes: int = duration_minutes
        self.priority: str = priority
        self.category: str = category
        self.completed: bool = False
    
    def is_high_priority(self) -> bool:
        """Check if task is high priority."""
        pass
    
    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        pass
