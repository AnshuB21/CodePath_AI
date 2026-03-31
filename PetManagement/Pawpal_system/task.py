"""
Task class representing a pet care task.
"""
from datetime import datetime, timedelta


class Task:
    """Represents a single pet care activity (e.g., feeding, walking, grooming).
    
    This class encapsulates all information needed to manage a pet care task,
    including its description, time requirement, frequency/priority, and status.
    """
    
    def __init__(self, name: str, duration_minutes: int, priority: str, category: str, 
                 frequency: str = "once", due_date: datetime = None, pet_name: str = None):
        """
        Initialize a Task with its core attributes.
        
        Args:
            name: Task name (description of the activity)
            duration_minutes: Duration in minutes (how long does this task take)
            priority: Priority level (e.g., 'high', 'medium', 'low')
            category: Task category (e.g., 'feeding', 'walking', 'grooming')
            frequency: Recurrence frequency ("once", "daily", "weekly"). Defaults to "once"
            due_date: datetime object for when task is due. Defaults to None
            pet_name: Name of the pet this task belongs to. Defaults to None
        """
        # Store the task's basic information
        self.name: str = name
        self.duration_minutes: int = duration_minutes
        self.priority: str = priority
        self.category: str = category
        
        # Track whether this task has been completed today
        self.completed: bool = False
        
        # Recurring task fields
        self.frequency: str = frequency  # "once", "daily", or "weekly"
        self.due_date: datetime = due_date
        
        # Conflict detection field
        self.pet_name: str = pet_name  # Track which pet this task belongs to
        self.scheduled_start_time: datetime = None  # Assigned during scheduling
        self.scheduled_end_time: datetime = None    # Calculated as start + duration
    
    def get_priority_score(self) -> int:
        """Calculate numeric priority score for this task.
        
        Converts string priority to numeric value for better comparisons:
        - critical/urgent: 3 (must schedule)
        - high: 2 (should schedule)
        - medium: 1 (optional)
        - low: 0 (lowest priority)
        
        Returns:
            Integer priority score (0-3, higher = more important)
        """
        priority_map = {
            'critical': 3,
            'urgent': 3,
            'high': 2,
            'medium': 1,
            'low': 0
        }
        return priority_map.get(self.priority.lower(), 0)
    
    def is_high_priority(self) -> bool:
        """Determine if this task is high priority and should be scheduled first.
        
        Returns:
            True if priority score is 2 or higher (high/critical/urgent), False otherwise
        """
        # Check if priority score is high (2 or 3)
        return self.get_priority_score() >= 2
    
    def is_critical(self) -> bool:
        """Determine if this task is critical and must be scheduled.
        
        Returns:
            True if priority is 'critical' or 'urgent', False otherwise
        """
        # Check if priority score is critical (3)
        return self.get_priority_score() == 3
    
    def mark_complete(self) -> 'Task':
        """Mark this task as completed and handle recurring task logic.
        
        For one-time tasks (frequency="once"):
        - Simply marks completed=True and returns None
        
        For recurring tasks (frequency="daily" or "weekly"):
        - Marks current task as completed
        - Creates and returns a new Task instance for next occurrence:
            - daily: new due_date = current due_date + 1 day
            - weekly: new due_date = current due_date + 7 days
        
        Returns:
            A new Task instance if recurring (daily/weekly), None if one-time task
        
        Raises:
            ValueError: If due_date is not set for recurring tasks
        """
        # Mark this task as completed
        self.completed = True
        
        # If task is one-time, don't create a new instance
        if self.frequency == "once":
            return None
        
        # For recurring tasks, validate that due_date is set
        if self.due_date is None:
            raise ValueError(f"Cannot create recurring task '{self.name}' without a due_date")
        
        # Calculate next due date based on frequency
        if self.frequency == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = self.due_date + timedelta(days=7)
        else:
            raise ValueError(f"Unknown frequency: {self.frequency}")
        
        # Create and return a new Task instance for next occurrence
        return Task(
            name=self.name,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            due_date=next_due_date,
            pet_name=self.pet_name  # Preserve pet association
        )
    
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
            'completed': self.completed,
            'frequency': self.frequency,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'pet_name': self.pet_name,
            'scheduled_start_time': self.scheduled_start_time.isoformat() if self.scheduled_start_time else None,
            'scheduled_end_time': self.scheduled_end_time.isoformat() if self.scheduled_end_time else None
        }
