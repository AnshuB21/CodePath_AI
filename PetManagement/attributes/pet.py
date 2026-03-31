"""
Pet class representing a pet.
"""


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
