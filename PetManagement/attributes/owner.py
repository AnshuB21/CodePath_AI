"""
Owner class representing a pet owner.
"""

from typing import List

if False:  # TYPE_CHECKING workaround for forward references
    from task import Task
    from pet import Pet
    from schedule import Schedule


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
        self.tasks: List['Task'] = []
        self.pet: 'Pet' = None
    
    def add_task(self, task: 'Task') -> None:
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
    
    def get_tasks(self) -> List['Task']:
        """Return list of all tasks."""
        pass
    
    def request_schedule(self) -> 'Schedule':
        """Generate and return a daily schedule."""
        pass
