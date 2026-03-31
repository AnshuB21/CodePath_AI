"""
Class models for PawPal+ pet care scheduling system.
"""

from typing import List, Dict


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


class Pet:
    """Represents a pet."""
    
    def __init__(self, name: str, species: str, age: int, special_needs: str = ""):
        """
        Initialize a Pet.
        
        Args:
            name: Pet name
            species: Species (e.g., dog, cat)
            age: Age in years
            special_needs: Any special needs
        """
        self.name: str = name
        self.species: str = species
        self.age: int = age
        self.special_needs: str = special_needs
    
    def to_dict(self) -> dict:
        """Convert pet to dictionary."""
        pass


class Schedule:
    """Represents a daily pet care schedule."""
    
    def __init__(self):
        """Initialize a Schedule."""
        self.planned_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.total_minutes: int = 0
    
    def generate(self, tasks: List[Task], budget: int) -> 'Schedule':
        """
        Generate an optimized schedule given available time.
        
        Args:
            tasks: List of tasks to schedule
            budget: Available time in minutes
            
        Returns:
            Optimized Schedule object
        """
        pass
    
    def explain(self) -> List[str]:
        """Return explanations for the scheduling decisions."""
        pass
    
    def summary(self) -> str:
        """Return a summary of the schedule."""
        pass


class Owner:
    """Represents a pet owner."""
    
    def __init__(self, name: str, available_minutes: int):
        """
        Initialize an Owner.
        
        Args:
            name: Owner name
            available_minutes: Minutes available per day for pet care
        """
        self.name: str = name
        self.available_minutes: int = available_minutes
        self.tasks: List[Task] = []
        self.pet: Pet = None
    
    def add_task(self, task: Task) -> None:
        """
        Add a task to the owner's task list.
        
        Args:
            task: Task to add
        """
        pass
    
    def remove_task(self, name: str) -> None:
        """
        Remove a task by name.
        
        Args:
            name: Name of the task to remove
        """
        pass
    
    def get_tasks(self) -> List[Task]:
        """Return list of all tasks."""
        pass
    
    def request_schedule(self) -> Schedule:
        """Generate and return a daily schedule."""
        pass
