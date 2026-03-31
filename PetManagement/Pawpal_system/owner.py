"""
Owner class representing a pet owner.
"""

from typing import List

if False:  # TYPE_CHECKING workaround for forward references
    from task import Task
    from pet import Pet
    from schedule import Schedule


class Owner:
    """Manages multiple pets and provides unified access to all their tasks.
    
    The Owner class serves as the central point for managing pet portfolios,
    tracking available time for pet care, and requesting optimized schedules.
    """
    
    def __init__(self, name: str, available_minutes: int):
        """
        Initialize an Owner with their name and daily pet care time budget.
        
        Args:
            name: Owner's name
            available_minutes: Minutes available per day for pet care activities
        """
        # Store owner's name for identification
        self.name: str = name
        
        # Store the time constraint (budget) - how many minutes owner has daily
        self.available_minutes: int = available_minutes
        
        # Initialize empty list for owned pets
        self.pets: List['Pet'] = []
        
        # Initialize list for owner-level tasks (not pet-specific)
        self.tasks: List['Task'] = []
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection.
        
        Args:
            pet: Pet object to add
        """
        # Append pet to the owner's pet list
        self.pets.append(pet)
    
    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet from the owner's collection by name.
        
        Args:
            pet_name: Name of the pet to remove
            
        Returns:
            True if pet was found and removed, False if pet not found
        """
        # Iterate through all pets to find matching name
        for pet in self.pets:
            if pet.name == pet_name:
                # Remove the matching pet
                self.pets.remove(pet)
                return True  # Indicate successful removal
        
        # Pet not found
        return False
    
    def get_pets(self) -> List['Pet']:
        """Retrieve all pets owned by this owner.
        
        Returns:
            A copy of the pet list (prevents external modification)
        """
        # Return a copy of the pet list to prevent accidental modifications
        return self.pets.copy()
    
    def add_task(self, task: 'Task') -> None:
        """Add a general task to the owner's task list.
        
        Args:
            task: Task object to add
        """
        # Append task to the owner's general task list
        self.tasks.append(task)
    
    def remove_task(self, name: str) -> bool:
        """Remove a task from the owner's task list by name.
        
        Args:
            name: Name of the task to remove
            
        Returns:
            True if task was found and removed, False if task not found
        """
        # Iterate through all tasks to find matching name
        for task in self.tasks:
            if task.name == name:
                # Remove the matching task
                self.tasks.remove(task)
                return True  # Indicate successful removal
        
        # Task not found
        return False
    
    def get_tasks(self) -> List['Task']:
        """Retrieve ALL tasks across all pets plus owner-level tasks.
        
        This method provides unified access to the complete task inventory,
        combining owner-level tasks and all pet-specific tasks.
        
        Returns:
            List containing all tasks from owner and all owned pets
        """
        # Start with a copy of owner-level tasks
        all_tasks = self.tasks.copy()
        
        # Add all tasks from each pet
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        
        # Return the complete task list
        return all_tasks
    
    def request_schedule(self) -> 'Schedule':
        """Generate and return an optimized daily schedule.
        
        This method delegates to the Schedule class to create an optimized
        schedule based on all available tasks and the owner's time budget.
        
        Returns:
            Schedule object optimized to fit within available_minutes
        """
        # Import Schedule class locally to avoid circular imports
        from .schedule import Schedule
        
        # Create a new scheduler instance
        scheduler = Schedule()
        
        # Get all tasks from owner and pets
        all_tasks = self.get_tasks()
        
        # Generate and return optimized schedule with time constraint
        return scheduler.generate(all_tasks, self.available_minutes)
