"""
Recurring Tasks Demonstration
Shows how the Task class automatically creates new instances for recurring tasks.
"""

from datetime import datetime, timedelta
from Pawpal_system.task import Task
from Pawpal_system.pet import Pet
from Pawpal_system.owner import Owner


def demo_one_time_task():
    """Demonstrate a one-time task that stays completed."""
    print("\n" + "=" * 60)
    print("DEMO 1: One-Time Task (No Auto-Recurrence)")
    print("=" * 60)
    
    # Create a one-time emergency vet visit
    vet_visit = Task(
        name="Emergency vet visit",
        duration_minutes=60,
        priority="critical",
        category="medical",
        frequency="once",
        due_date=datetime(2026, 3, 31, 14, 0)
    )
    
    print(f"✓ Created: {vet_visit.name}")
    print(f"  Frequency: {vet_visit.frequency}")
    print(f"  Due: {vet_visit.due_date}")
    print(f"  Completed: {vet_visit.completed}")
    
    # Mark as complete
    print(f"\n→ Marking task as complete...")
    next_task = vet_visit.mark_complete()
    
    print(f"✓ Task marked complete: {vet_visit.completed}")
    print(f"✓ Next task created: {next_task}")
    print(f"  → One-time tasks return None (no recurrence)")


def demo_daily_task():
    """Demonstrate a daily recurring task."""
    print("\n" + "=" * 60)
    print("DEMO 2: Daily Recurring Task (Auto-Generate Next)")
    print("=" * 60)
    
    # Create a daily feeding task
    daily_feed = Task(
        name="Feed Buddy",
        duration_minutes=15,
        priority="high",
        category="feeding",
        frequency="daily",
        due_date=datetime(2026, 3, 31, 8, 0)
    )
    
    print(f"✓ Created: {daily_feed.name}")
    print(f"  Frequency: {daily_feed.frequency}")
    print(f"  Due: {daily_feed.due_date.strftime('%A, %B %d, %Y at %I:%M %p')}")
    print(f"  Duration: {daily_feed.duration_minutes} minutes")
    print(f"  Completed: {daily_feed.completed}")
    
    # Mark as complete
    print(f"\n→ Marking task as complete...")
    next_feeding = daily_feed.mark_complete()
    
    print(f"✓ Current task marked complete: {daily_feed.completed}")
    print(f"✓ New task automatically created for next day:")
    print(f"  Name: {next_feeding.name}")
    print(f"  Due: {next_feeding.due_date.strftime('%A, %B %d, %Y at %I:%M %p')}")
    print(f"  Days until due: {(next_feeding.due_date - datetime.now()).days + 1}")
    print(f"  Completed: {next_feeding.completed}")


def demo_weekly_task():
    """Demonstrate a weekly recurring task."""
    print("\n" + "=" * 60)
    print("DEMO 3: Weekly Recurring Task (Auto-Generate Next)")
    print("=" * 60)
    
    # Create a weekly grooming task
    weekly_groom = Task(
        name="Groom Whiskers",
        duration_minutes=45,
        priority="medium",
        category="grooming",
        frequency="weekly",
        due_date=datetime(2026, 3, 31)
    )
    
    print(f"✓ Created: {weekly_groom.name}")
    print(f"  Frequency: {weekly_groom.frequency}")
    print(f"  Due: {weekly_groom.due_date.strftime('%A, %B %d, %Y')}")
    print(f"  Duration: {weekly_groom.duration_minutes} minutes")
    print(f"  Completed: {weekly_groom.completed}")
    
    # Mark as complete
    print(f"\n→ Marking task as complete...")
    next_groom = weekly_groom.mark_complete()
    
    print(f"✓ Current task marked complete: {weekly_groom.completed}")
    print(f"✓ New task automatically created for next week:")
    print(f"  Name: {next_groom.name}")
    print(f"  Due: {next_groom.due_date.strftime('%A, %B %d, %Y')}")
    print(f"  Days until due: {(next_groom.due_date - datetime.now()).days}")
    print(f"  Completed: {next_groom.completed}")


def demo_task_serialization():
    """Demonstrate storing recurring tasks in dictionary format."""
    print("\n" + "=" * 60)
    print("DEMO 4: Task Serialization (Storing with Frequency & Due Date)")
    print("=" * 60)
    
    task = Task(
        name="Walk Buddy",
        duration_minutes=30,
        priority="high",
        category="walking",
        frequency="daily",
        due_date=datetime(2026, 3, 31, 17, 0)
    )
    
    print(f"✓ Created task: {task.name}")
    print(f"\n→ Converting to dictionary for storage:")
    
    task_dict = task.to_dict()
    for key, value in task_dict.items():
        print(f"  {key}: {value}")
    
    print(f"\n→ Dictionary format ready for:")
    print(f"  - JSON serialization")
    print(f"  - Database storage")
    print(f"  - API transmission")


def demo_pet_with_recurring_tasks():
    """Demonstrate using recurring tasks with Pet objects."""
    print("\n" + "=" * 60)
    print("DEMO 5: Pet with Recurring Tasks")
    print("=" * 60)
    
    # Create a pet
    buddy = Pet(
        name="Buddy",
        species="Dog",
        age=5,
        special_needs="Requires daily exercise"
    )
    
    # Add recurring tasks
    daily_walk = Task(
        name="Walk Buddy in park",
        duration_minutes=45,
        priority="high",
        category="walking",
        frequency="daily",
        due_date=datetime(2026, 3, 31)
    )
    
    daily_feed = Task(
        name="Feed Buddy breakfast",
        duration_minutes=10,
        priority="high",
        category="feeding",
        frequency="daily",
        due_date=datetime(2026, 3, 31, 8, 0)
    )
    
    weekly_groom = Task(
        name="Groom Buddy",
        duration_minutes=30,
        priority="medium",
        category="grooming",
        frequency="weekly",
        due_date=datetime(2026, 3, 31)
    )
    
    buddy.add_task(daily_walk)
    buddy.add_task(daily_feed)
    buddy.add_task(weekly_groom)
    
    print(f"✓ Created pet: {buddy.name}")
    print(f"✓ Added {len(buddy.tasks)} recurring tasks:")
    for task in buddy.tasks:
        print(f"  - {task.name} ({task.frequency}, due: {task.due_date.strftime('%m/%d/%Y')})")
    
    print(f"\n→ Marking daily walk as complete...")
    next_walk = daily_walk.mark_complete()
    buddy.add_task(next_walk)  # Add the newly created task
    
    print(f"✓ Daily walk completed")
    print(f"✓ New daily walk task added for: {next_walk.due_date.strftime('%A, %B %d, %Y')}")
    print(f"✓ Pet now has {len(buddy.tasks)} tasks")


def main():
    """Run all recurring task demonstrations."""
    print("\n" + "🐾" * 30)
    print("RECURRING TASKS AUTOMATION DEMO")
    print("🐾" * 30)
    
    demo_one_time_task()
    demo_daily_task()
    demo_weekly_task()
    demo_task_serialization()
    demo_pet_with_recurring_tasks()
    
    print("\n" + "=" * 60)
    print("✅ SUMMARY: Recurring Task Features")
    print("=" * 60)
    print("""
✓ One-time tasks: Stay completed (no recurrence)
✓ Daily tasks: Automatically create next day's task
✓ Weekly tasks: Automatically create next week's task
✓ Dates are calculated using timedelta for accuracy
✓ All task properties preserved in recurring instances
✓ Full serialization support (to_dict) with date formatting
✓ Works seamlessly with Pet and Owner classes
    """)


if __name__ == "__main__":
    main()
