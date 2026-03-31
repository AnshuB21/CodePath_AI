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
        - Validation warnings about critical task constraints (scheduling_warning)
        - Time conflicts between scheduled tasks (conflicts)
        """
        # List to store tasks that fit within the time budget
        self.planned_tasks: List['Task'] = []
        
        # List to store tasks that don't fit due to insufficient time
        self.skipped_tasks: List['Task'] = []
        
        # Running total of minutes for all planned tasks
        self.total_minutes: int = 0
        
        # Warning message if critical tasks exceed available time
        self.scheduling_warning: str = None
        
        # Flag indicating if schedule has validation errors
        self.has_validation_error: bool = False
        
        # List of conflict warnings (time overlaps)
        self.conflicts: List[str] = []
    
    @staticmethod
    def sort_by_time(tasks: List['Task'], reverse: bool = False) -> List['Task']:
        """Sort Task objects by their duration (time attribute).
        
        Provides a clean, reusable way to sort tasks by duration.
        Useful for scheduling algorithms that need to optimize task ordering.
        
        Common use cases:
        - First Fit Decreasing: Sort longest first (reverse=True)
        - Time-efficient packing: Sort shortest first (reverse=False)
        - Balanced scheduling: Sort by other criteria first, then by time
        
        Args:
            tasks: List of Task objects to sort
            reverse: If True, sort descending (longest first)
                    If False, sort ascending (shortest first, default)
        
        Returns:
            New list of tasks sorted by duration (does not modify original list)
        """
        # Sort tasks by duration_minutes attribute
        # reverse parameter controls sort order
        return sorted(tasks, key=lambda t: t.duration_minutes, reverse=reverse)
    
    def _tasks_conflict(self, task1: 'Task', task2: 'Task') -> bool:
        """Check if two tasks have overlapping time slots.
        
        Two tasks conflict if their time windows overlap:
        task1.start < task2.end AND task2.start < task1.end
        
        Args:
            task1: First task to check
            task2: Second task to check
        
        Returns:
            True if tasks overlap in time, False if they don't conflict
        """
        # If either task doesn't have scheduled times, no conflict
        if not task1.scheduled_start_time or not task1.scheduled_end_time:
            return False
        if not task2.scheduled_start_time or not task2.scheduled_end_time:
            return False
        
        # Check for overlap: task1 starts before task2 ends AND task2 starts before task1 ends
        return (task1.scheduled_start_time < task2.scheduled_end_time and 
                task2.scheduled_start_time < task1.scheduled_end_time)
    
    def detect_conflicts(self) -> List[str]:
        """Detect all time conflicts in the schedule.
        
        Compares all planned tasks to find overlapping time slots.
        Generates human-readable warning messages for each conflict.
        
        Returns:
            List of conflict warning strings (empty if no conflicts)
        """
        # Clear existing conflicts
        self.conflicts = []
        
        # Compare each pair of tasks for conflicts
        for i, task1 in enumerate(self.planned_tasks):
            for task2 in self.planned_tasks[i+1:]:
                # Check if these tasks overlap in time
                if self._tasks_conflict(task1, task2):
                    # Create detailed conflict message
                    pet1_info = f" ({task1.pet_name})" if task1.pet_name else ""
                    pet2_info = f" ({task2.pet_name})" if task2.pet_name else ""
                    
                    conflict_msg = (
                        f"⚠️  TIME CONFLICT: '{task1.name}'{pet1_info} "
                        f"({task1.scheduled_start_time.strftime('%H:%M')}-"
                        f"{task1.scheduled_end_time.strftime('%H:%M')}) "
                        f"overlaps with '{task2.name}'{pet2_info} "
                        f"({task2.scheduled_start_time.strftime('%H:%M')}-"
                        f"{task2.scheduled_end_time.strftime('%H:%M')})"
                    )
                    self.conflicts.append(conflict_msg)
        
        return self.conflicts
    
    def _assign_time_slots(self) -> None:
        """Assign start and end times to planned tasks based on order.
        
        This is a simple sequential scheduling approach:
        - Assumes tasks start at 00:00 and are scheduled back-to-back
        - Each task gets a start time and calculated end time
        - Tasks with already-set times are preserved (for manual conflict testing)
        - Used by conflict detection to find overlapping schedules
        """
        current_time = None
        
        for task in self.planned_tasks:
            # Skip reassigning if this task already has a scheduled time
            # (allows for manual time slot testing)
            if task.scheduled_start_time and task.scheduled_end_time:
                # Update current_time to account for this task
                if task.scheduled_end_time > current_time or current_time is None:
                    current_time = task.scheduled_end_time
                continue
            
            # Initialize start time at beginning of day if not set
            if current_time is None:
                # Use due_date if available, otherwise use current date
                if task.due_date:
                    from datetime import time
                    current_time = task.due_date.replace(hour=0, minute=0, second=0)
                else:
                    from datetime import datetime as dt
                    current_time = dt.now().replace(hour=0, minute=0, second=0)
            
            # Assign start time to this task
            task.scheduled_start_time = current_time
            
            # Calculate end time (start + duration)
            from datetime import timedelta
            task.scheduled_end_time = current_time + timedelta(minutes=task.duration_minutes)
            
            # Next task starts when this one ends
            current_time = task.scheduled_end_time
    
    def _detect_conflicts(self) -> None:
        """Internal method to assign times and detect conflicts."""
        # First assign time slots to all planned tasks
        self._assign_time_slots()
        
        # Then detect any overlaps
        self.detect_conflicts()
    
    def generate(self, tasks: List['Task'], budget: int) -> 'Schedule':
        """Generate an optimized schedule given available time using TWO-TIER strategy.
        
        Two-Tier Scheduling Algorithm:
        TIER 1: Schedule ALL critical tasks first (must-schedule guarantee)
                Sort critical tasks by duration (shortest first)
        TIER 2: Fill remaining time with non-critical tasks
                Sort by priority score (highest first), then by duration (shortest first)
        
        This ensures critical/medical tasks are NEVER skipped due to time constraints.
        
        Args:
            tasks: List of Task objects to be scheduled
            budget: Available time in minutes (the owner's daily time constraint)
            
        Returns:
            Optimized Schedule object with planned and skipped tasks
        """
        # Create a new Schedule instance to store the results
        schedule = Schedule()
        
        # VALIDATION: Check if all critical tasks can fit in budget
        # This prevents scheduling failures for medical/essential tasks
        self._validate_critical_tasks(tasks, budget, schedule)
        
        # If schedule has validation errors, return early
        if hasattr(schedule, 'scheduling_warning') and schedule.scheduling_warning:
            return schedule
        
        # TIER 1: Schedule all critical tasks first
        # Sort critical tasks by duration (shortest first for efficiency)
        critical_tasks = self.sort_by_time(
            [t for t in tasks if t.is_critical()],
            reverse=False
        )
        
        remaining_budget = budget
        
        # Add all critical tasks to planned tasks
        for task in critical_tasks:
            schedule.planned_tasks.append(task)
            schedule.total_minutes += task.duration_minutes
            remaining_budget -= task.duration_minutes
        
        # TIER 2: Fill remaining time with non-critical tasks
        # Sort by priority score (highest first), then by duration (shortest first)
        non_critical_tasks = sorted(
            [t for t in tasks if not t.is_critical()],
            key=lambda t: (-t.get_priority_score(), t.duration_minutes)
        )
        
        # Iterate through non-critical tasks and fit them into remaining schedule
        for task in non_critical_tasks:
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
        
        # CONFLICT DETECTION: Check for time overlaps in scheduled tasks
        if schedule.planned_tasks:
            schedule._detect_conflicts()
        
        # Return the optimized schedule
        return schedule
    
    def explain(self) -> List[str]:
        """Return detailed explanations for each scheduling decision.
        
        This method provides enumerated explanations of why each task was
        scheduled or not, helping users understand the scheduler's reasoning.
        Also displays any validation warnings about critical task constraints
        and detected time conflicts.
        
        Returns:
            List of explanation strings describing scheduling decisions and warnings
        """
        # Initialize list to store all explanation lines
        explanations = []
        
        # SECTION 0: Display critical validation warning if present
        if self.scheduling_warning:
            explanations.append("⚠️  SCHEDULING ALERT")
            explanations.append(self.scheduling_warning)
            explanations.append("")
        
        # SECTION 0B: Display time conflicts if present
        if self.conflicts:
            explanations.append("⚠️  TIME CONFLICTS DETECTED")
            for conflict in self.conflicts:
                explanations.append(conflict)
            explanations.append("")
        
        # SECTION 1: Explain planned (scheduled) tasks
        if self.planned_tasks:
            # Header showing how many tasks were scheduled
            explanations.append(f"Scheduled {len(self.planned_tasks)} tasks:")
            
            # List each scheduled task with details
            for task in self.planned_tasks:
                # Use new priority score method for more detailed classification
                if task.is_critical():
                    priority_label = "⚠️  CRITICAL"
                elif task.is_high_priority():
                    priority_label = "HIGH PRIORITY"
                else:
                    priority_label = "Normal"
                
                # Add time slot info if available
                time_info = ""
                if task.scheduled_start_time and task.scheduled_end_time:
                    time_info = f" [{task.scheduled_start_time.strftime('%H:%M')}-{task.scheduled_end_time.strftime('%H:%M')}]"
                
                # Add explanation line for this task
                explanations.append(
                    f"  • {task.name}: {task.duration_minutes} min ({priority_label}){time_info}"
                )
        
        # SECTION 2: Explain skipped (unscheduled) tasks
        if self.skipped_tasks:
            # Header showing how many tasks couldn't fit
            explanations.append(
                f"\nCould not fit {len(self.skipped_tasks)} task(s) in available time:"
            )
            
            # List each skipped task with priority info
            for task in self.skipped_tasks:
                priority_label = "⚠️  CRITICAL" if task.is_critical() else "Normal"
                explanations.append(f"  • {task.name}: {task.duration_minutes} min ({priority_label})")
        
        # SECTION 3: Summary statistics
        explanations.append(
            f"\nTotal scheduled: {self.total_minutes} minutes"
        )
        
        # Return all explanations as a list
        return explanations
    
    def summary(self) -> str:
        """Return a formatted human-readable summary of the entire schedule.
        
        Creates a beautifully formatted report with visual separators, emojis,
        and detailed breakdowns showing all planned tasks, skipped tasks, and
        comprehensive time statistics.
        
        Returns:
            Formatted string containing the complete schedule summary
        """
        # Initialize list to build the summary
        summary_lines = []
        
        # DISPLAY CRITICAL VALIDATION WARNING IF PRESENT
        if self.scheduling_warning:
            summary_lines.append("╔" + "═" * 58 + "╗")
            summary_lines.append("║" + " " * 15 + "⚠️  SCHEDULING ALERT ⚠️" + " " * 15 + "║")
            summary_lines.append("╚" + "═" * 58 + "╝")
            summary_lines.append("")
            # Format warning message nicely
            warning_lines = self.scheduling_warning.split('\n')
            for line in warning_lines:
                summary_lines.append("│ " + line[:56].ljust(56) + " │")
            summary_lines.append("")
        
        # Calculate total time requested
        total_requested = sum(task.duration_minutes for task in self.planned_tasks + self.skipped_tasks)
        
        # Add decorative header
        summary_lines.append("╔" + "═" * 58 + "╗")
        summary_lines.append("║" + " " * 15 + "📅 DAILY SCHEDULE SUMMARY 📅" + " " * 15 + "║")
        summary_lines.append("╚" + "═" * 58 + "╝")
        
        # SECTION 1: Display planned (scheduled) tasks
        summary_lines.append("")
        summary_lines.append("┌─ ✅ SCHEDULED TASKS " + "─" * 36 + "┐")
        
        if self.planned_tasks:
            summary_lines.append(f"│ Count: {len(self.planned_tasks)} task(s) scheduled" + " " * 28 + "│")
            summary_lines.append("├" + "─" * 58 + "┤")
            
            # List each planned task with visual formatting
            for idx, task in enumerate(self.planned_tasks, 1):
                # Use priority score for better visual distinction
                if task.is_critical():
                    priority_icon = "🔴"  # Red circle for critical
                elif task.is_high_priority():
                    priority_icon = "🟠"  # Orange circle for high
                else:
                    priority_icon = "⚪"  # White circle for normal/low
                
                task_line = f"│ {idx}. {priority_icon} {task.name:<30} {task.duration_minutes:>3}min │"
                summary_lines.append(task_line)
        else:
            # Show when no tasks were scheduled
            summary_lines.append("│ No tasks scheduled for today" + " " * 29 + "│")
        
        summary_lines.append("└" + "─" * 58 + "┘")
        
        # SECTION 2: Display skipped (unscheduled) tasks
        summary_lines.append("")
        summary_lines.append("┌─ ⏭️  SKIPPED TASKS (Time Conflict) " + "─" * 22 + "┐")
        
        if self.skipped_tasks:
            summary_lines.append(f"│ Count: {len(self.skipped_tasks)} task(s) not scheduled" + " " * 28 + "│")
            summary_lines.append("├" + "─" * 58 + "┤")
            
            # List each skipped task
            for idx, task in enumerate(self.skipped_tasks, 1):
                # Use priority score for better visual distinction
                if task.is_critical():
                    priority_icon = "🔴"  # Red circle for critical
                elif task.is_high_priority():
                    priority_icon = "🟠"  # Orange circle for high
                else:
                    priority_icon = "⚪"  # White circle for normal/low
                
                task_line = f"│ {idx}. {priority_icon} {task.name:<30} {task.duration_minutes:>3}min │"
                summary_lines.append(task_line)
        else:
            # Show when all tasks fit
            summary_lines.append("│ All tasks fit in available time! 🎉" + " " * 21 + "│")
        
        summary_lines.append("└" + "─" * 58 + "┘")
        
        # SECTION 3: Show time statistics
        summary_lines.append("")
        summary_lines.append("┌─ ⏱️  TIME STATISTICS " + "─" * 36 + "┐")
        
        # Time breakdown
        summary_lines.append(f"│ Total Tasks Requested:       {total_requested:>3} minutes" + " " * 16 + "│")
        summary_lines.append(f"│ Tasks Scheduled:             {self.total_minutes:>3} minutes" + " " * 16 + "│")
        
        if self.skipped_tasks:
            skipped_time = sum(task.duration_minutes for task in self.skipped_tasks)
            summary_lines.append(f"│ Tasks Skipped:               {skipped_time:>3} minutes" + " " * 16 + "│")
        
        # Utilization percentage
        utilization_pct = 0
        if total_requested > 0:
            utilization_pct = int((self.total_minutes / total_requested) * 100)
        
        summary_lines.append(f"│ Utilization Rate:            {utilization_pct:>3}%" + " " * 19 + "│")
        
        # Completion status
        if self.skipped_tasks:
            summary_lines.append("│ Status:                      ⚠️  PARTIAL" + " " * 16 + "│")
        else:
            summary_lines.append("│ Status:                      ✅ COMPLETE" + " " * 16 + "│")
        
        summary_lines.append("└" + "─" * 58 + "┘")
        
        # SECTION 4: Display time conflicts if any
        if self.conflicts:
            summary_lines.append("")
            summary_lines.append("┌─ ⚠️  TIME CONFLICTS " + "─" * 37 + "┐")
            summary_lines.append(f"│ {len(self.conflicts)} conflict(s) detected" + " " * 37 + "│")
            summary_lines.append("├" + "─" * 58 + "┤")
            
            for conflict in self.conflicts:
                # Wrap long conflict messages
                max_len = 56
                if len(conflict) > max_len:
                    summary_lines.append(f"│ {conflict[:max_len]} │")
                    remaining = conflict[max_len:]
                    while remaining:
                        summary_lines.append(f"│   {remaining[:54]} │")
                        remaining = remaining[54:]
                else:
                    summary_lines.append(f"│ {conflict:<56} │")
            
            summary_lines.append("└" + "─" * 58 + "┘")
        
        # Add footer with decorative closing
        summary_lines.append("")
        summary_lines.append("╔" + "═" * 58 + "╗")
        summary_lines.append("║" + " " * 18 + "🐾 Happy Pet Care! 🐾" + " " * 18 + "║")
        summary_lines.append("╚" + "═" * 58 + "╝")
        
        # Join all lines with newlines and return as single string
        return "\n".join(summary_lines)
    
    def _validate_critical_tasks(self, tasks: List['Task'], budget: int, schedule: 'Schedule') -> None:
        """Validate that all critical tasks can fit within the available budget.
        
        CRITICAL TASK GUARANTEE: Ensures medical/essential tasks are never skipped.
        If critical tasks exceed available time, this alerts the user.
        
        Args:
            tasks: List of all Task objects
            budget: Available time in minutes
            schedule: Schedule object to attach warning to
        """
        # Calculate total time needed for all critical tasks
        critical_tasks = [t for t in tasks if t.is_critical()]
        critical_time = sum(t.duration_minutes for t in critical_tasks)
        
        # Check if critical tasks fit within budget
        if critical_time > budget:
            # ALERT: Critical tasks exceed available time!
            # Attach warning to schedule for user notification
            schedule.scheduling_warning = (
                f"⚠️  WARNING: Critical tasks ({critical_time} min) "
                f"exceed available time ({budget} min)!\n"
                f"Cannot schedule all essential/medical tasks.\n"
                f"Please increase available time or reduce task duration."
            )
            # Mark schedule as having validation error
            schedule.has_validation_error = True
        else:
            # All critical tasks fit - schedule is valid
            schedule.scheduling_warning = None
            schedule.has_validation_error = False
    
    def _get_category_icon(self, category: str) -> str:
        """Return an emoji icon based on task category.
        
        Args:
            category: Task category name
            
        Returns:
            Appropriate emoji for the category
        """
        # Map categories to emojis
        category_icons = {
            'walking': '🚶',
            'feeding': '🍖',
            'grooming': '✂️',
            'medication': '💊',
            'enrichment': '🎾',
            'training': '🎓',
            'playing': '🎮',
            'cleaning': '🧹',
            'other': '📌'
        }
        
        # Return the icon or default to generic pin icon
        return category_icons.get(category.lower(), '📌')
