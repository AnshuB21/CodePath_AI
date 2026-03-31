"""
Schedule class representing a daily pet care schedule.
"""

from typing import List

if False:  # TYPE_CHECKING workaround for forward references
    from task import Task


class Schedule:
    """Represents a daily pet care schedule."""
    
    def __init__(self):
        """Initialize a Schedule."""
        self.planned_tasks: List['Task'] = []
        self.skipped_tasks: List['Task'] = []
        self.total_minutes: int = 0
    
    def generate(self, tasks: List['Task'], budget: int) -> 'Schedule':
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
