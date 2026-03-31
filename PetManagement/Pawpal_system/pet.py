"""
Pet class representing a pet.
"""

from typing import List

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task import Task


class Pet:
    """Stores pet details and maintains a list of tasks specific to this pet.
    
    A Pet represents one animal owned by the owner and contains all relevant
    information about the pet plus all care tasks that need to be performed.
    """
    
    def __init__(self, name: str, species: str, age: int, special_needs: str = ""):
        """
        Initialize a Pet with its core attributes.
        
        Args:
            name: Pet name (unique identifier for this pet)
            species: Species (e.g., 'dog', 'cat', 'bird')
            age: Age in years (used to understand pet maturity)
            special_needs: Any special needs (e.g., 'diabetic', 'requires medication')
        """
        # Store pet's basic information
        self.name: str = name
        self.species: str = species
        self.age: int = age
        self.special_needs: str = special_needs
        
        # Initialize empty task list - will be populated with pet-specific tasks
        self.tasks: List['Task'] = []
    
    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list.
        
        Args:
            task: Task object to add to this pet
        """
        # Append task to the pet's task list
        self.tasks.append(task)
    
    def remove_task(self, task_name: str) -> bool:
        """Remove a task from this pet by task name.
        
        Args:
            task_name: Name of the task to remove
            
        Returns:
            True if task was found and removed, False if task not found
        """
        # Iterate through all tasks to find matching name
        for task in self.tasks:
            if task.name == task_name:
                # Remove the matching task
                self.tasks.remove(task)
                return True  # Indicate successful removal
        
        # Task not found
        return False
    
    def get_tasks(self) -> List['Task']:
        """Retrieve all tasks associated with this pet.
        
        Returns:
            A copy of the task list (prevents external modification)
        """
        # Return a copy of the task list to prevent accidental modifications from outside
        return self.tasks.copy()
    
    def to_dict(self) -> dict:
        """Convert pet and all its task data to a dictionary for storage/serialization.
        
        Returns:
            Dictionary containing pet details and all associated tasks as dictionaries
        """
        # Convert pet to dictionary with all attributes
        return {
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'special_needs': self.special_needs,
            # Convert each task to a dictionary as well
            'tasks': [task.to_dict() for task in self.tasks]
        }
