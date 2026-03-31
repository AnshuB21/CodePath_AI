"""
Schedule class representing a daily pet care schedule.
"""

from typing import List

if False:  # TYPE_CHECKING workaround for forward references
    from task import Task


class Schedule:
    """
    The "Brain" of the scheduling system.
    Retrieves, organizes, and manages tasks across pets.
    """
    
    def __init__(self):
        """Initialize a new empty Schedule.
        
        Creates the internal data structures needed to track:
        - Tasks that fit within the time budget (planned_tasks)
        - Tasks that don't fit due to time constraints (skipped_tasks)
        - Total time allocated to scheduled tasks (total_minutes)
        """
        # List to store tasks that fit within the time budget
        self.planned_tasks: List['Task'] = []
        
        # List to store tasks that don't fit due to insufficient time
        self.skipped_tasks: List['Task'] = []
        
        # Running total of minutes for all planned tasks
        self.total_minutes: int = 0
    
    def generate(self, tasks: List['Task'], budget: int) -> 'Schedule':
        """Generate an optimized schedule given available time.
        
        This is the core scheduling algorithm that uses a greedy approach:
        1. Sort tasks by priority (high priority first, then by duration)
        2. Fit as many high-priority tasks as possible within the time budget
        3. Fill remaining time with lower-priority tasks
        4. Track which tasks don't fit due to time constraints
        
        Args:
            tasks: List of Task objects to be scheduled
            budget: Available time in minutes (the owner's daily time constraint)
            
        Returns:
            Optimized Schedule object with planned and skipped tasks
        """
        # Create a new Schedule instance to store the results
        schedule = Schedule()
        
        # Sort tasks by priority: high priority tasks first, then by shorter duration
        # The sorting key uses (not is_high_priority, duration) to ensure:
        # - High priority tasks come first (True sorts after False)
        # - Among same priority, shorter tasks come first
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (not t.is_high_priority(), t.duration_minutes)
        )
        
        # Track remaining time budget as we add tasks
        remaining_budget = budget
        
        # Iterate through sorted tasks and fit them into the schedule
        for task in sorted_tasks:
            # Check if this task fits within remaining time
            if task.duration_minutes <= remaining_budget:
                # Task fits - add it to planned tasks
                schedule.planned_tasks.append(task)
                # Update total scheduled time
                schedule.total_minutes += task.duration_minutes
                # Reduce remaining budget
                remaining_budget -= task.duration_minutes
            else:
                # Task doesn't fit - add to skipped tasks list
                schedule.skipped_tasks.append(task)
        
        # Return the optimized schedule
        return schedule
    
    def explain(self) -> List[str]:
        """Return detailed explanations for each scheduling decision.
        
        This method provides enumerated explanations of why each task was
        scheduled or not, helping users understand the scheduler's reasoning.
        
        Returns:
            List of explanation strings describing scheduling decisions
        """
        # Initialize list to store all explanation lines
        explanations = []
        
        # SECTION 1: Explain planned (scheduled) tasks
        if self.planned_tasks:
            # Header showing how many tasks were scheduled
            explanations.append(f"Scheduled {len(self.planned_tasks)} tasks:")
            
            # List each scheduled task with details
            for task in self.planned_tasks:
                # Determine priority label for display
                priority_label = "HIGH PRIORITY" if task.is_high_priority() else "Normal"
                # Add explanation line for this task
                explanations.append(
                    f"  • {task.name}: {task.duration_minutes} min ({priority_label})"
                )
        
        # SECTION 2: Explain skipped (unscheduled) tasks
        if self.skipped_tasks:
            # Header showing how many tasks couldn't fit
            explanations.append(
                f"\nCould not fit {len(self.skipped_tasks)} task(s) in available time:"
            )
            
            # List each skipped task
            for task in self.skipped_tasks:
                explanations.append(f"  • {task.name}: {task.duration_minutes} min")
        
        # SECTION 3: Summary statistics
        explanations.append(
            f"\nTotal scheduled: {self.total_minutes} minutes"
        )
        
        # Return all explanations as a list
        return explanations
    
    def summary(self) -> str:
        """Return a formatted human-readable summary of the entire schedule.
        
        Creates a nicely formatted report with visual separators, showing
        all planned tasks, skipped tasks, and time statistics.
        
        Returns:
            Formatted string containing the complete schedule summary
        """
        # Initialize list to build the summary
        summary_lines = []
        
        # Add header with visual separator
        summary_lines.append("=" * 50)
        summary_lines.append("DAILY SCHEDULE SUMMARY")
        summary_lines.append("=" * 50)
        
        # SECTION 1: Display planned (scheduled) tasks
        if self.planned_tasks:
            # Header showing count of planned tasks
            summary_lines.append(f"\n✓ Planned Tasks ({len(self.planned_tasks)}):")
            
            # List each planned task with details
            for task in self.planned_tasks:
                summary_lines.append(
                    f"  • {task.name} ({task.duration_minutes} min) - {task.category}"
                )
        else:
            # Show when no tasks were scheduled
            summary_lines.append("\n✓ Planned Tasks: None")
        
        # SECTION 2: Display skipped (unscheduled) tasks
        if self.skipped_tasks:
            # Header showing count of skipped tasks
            summary_lines.append(f"\n✗ Skipped Tasks ({len(self.skipped_tasks)}):")
            
            # List each skipped task with details
            for task in self.skipped_tasks:
                summary_lines.append(
                    f"  • {task.name} ({task.duration_minutes} min) - {task.category}"
                )
        else:
            # Show when all tasks fit
            summary_lines.append("\n✗ Skipped Tasks: None")
        
        # SECTION 3: Show time statistics
        summary_lines.append(f"\nTotal Time Required: {self.total_minutes} minutes")
        
        # Add footer with visual separator
        summary_lines.append("=" * 50)
        
        # Join all lines with newlines and return as single string
        return "\n".join(summary_lines)
