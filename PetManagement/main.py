"""
Main.py - Demonstration of the PawPal+ Pet Care Scheduling System

This script showcases the complete PawPal+ system by:
1. Importing all necessary classes
2. Creating an Owner with multiple pets
3. Adding tasks to each pet with varying priorities and durations
4. Generating and displaying an optimized daily schedule
"""

# Import classes from the Pawpal_system module
from Pawpal_system.owner import Owner
from Pawpal_system.pet import Pet
from Pawpal_system.task import Task


def main():
    """Main function that demonstrates the PawPal+ scheduling system."""
    
    print("=" * 60)
    print("🐾 PAWPAL+ PET CARE SCHEDULING SYSTEM 🐾")
    print("=" * 60)
    print()
    
    # ===== STEP 1: Create an Owner =====
    print("[STEP 1] Creating Owner...")
    # Create an owner with 120 minutes (2 hours) available per day for pet care
    owner = Owner(name="Sarah", available_minutes=120)
    print(f"✓ Owner '{owner.name}' created with {owner.available_minutes} minutes available\n")
    
    # ===== STEP 2: Create Pets =====
    print("[STEP 2] Creating Pets...")
    
    # Create first pet - a dog
    dog = Pet(
        name="Buddy",
        species="Dog",
        age=5,
        special_needs="Requires daily exercise"
    )
    print(f"✓ Pet created: {dog.name} (Species: {dog.species}, Age: {dog.age})")
    
    # Create second pet - a cat
    cat = Pet(
        name="Whiskers",
        species="Cat",
        age=3,
        special_needs="Diabetic - needs insulin"
    )
    print(f"✓ Pet created: {cat.name} (Species: {cat.species}, Age: {cat.age})")
    
    # Create third pet - a parrot
    parrot = Pet(
        name="Polly",
        species="Parrot",
        age=2,
        special_needs="Social - needs interaction"
    )
    print(f"✓ Pet created: {parrot.name} (Species: {parrot.species}, Age: {parrot.age})\n")
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(parrot)
    
    # ===== STEP 3: Create and Add Tasks =====
    print("[STEP 3] Creating Tasks...")
    
    # Tasks for the dog (Buddy)
    task1 = Task(
        name="Walk Buddy in the park",
        duration_minutes=45,
        priority="high",
        category="walking"
    )
    dog.add_task(task1)
    print(f"✓ Task added to {dog.name}: {task1.name} ({task1.duration_minutes} min, {task1.priority} priority)")
    
    task2 = Task(
        name="Feed Buddy breakfast",
        duration_minutes=10,
        priority="high",
        category="feeding"
    )
    dog.add_task(task2)
    print(f"✓ Task added to {dog.name}: {task2.name} ({task2.duration_minutes} min, {task2.priority} priority)")
    
    # Tasks for the cat (Whiskers)
    task3 = Task(
        name="Insulin injection for Whiskers",
        duration_minutes=5,
        priority="critical",
        category="medication"
    )
    cat.add_task(task3)
    print(f"✓ Task added to {cat.name}: {task3.name} ({task3.duration_minutes} min, {task3.priority} priority)")
    
    task4 = Task(
        name="Feed Whiskers lunch",
        duration_minutes=10,
        priority="high",
        category="feeding"
    )
    cat.add_task(task4)
    print(f"✓ Task added to {cat.name}: {task4.name} ({task4.duration_minutes} min, {task4.priority} priority)")
    
    task5 = Task(
        name="Clean Whiskers' litter box",
        duration_minutes=5,
        priority="medium",
        category="cleaning"
    )
    cat.add_task(task5)
    print(f"✓ Task added to {cat.name}: {task5.name} ({task5.duration_minutes} min, {task5.priority} priority)")
    
    # Tasks for the parrot (Polly)
    task6 = Task(
        name="Interactive play with Polly",
        duration_minutes=20,
        priority="high",
        category="enrichment"
    )
    parrot.add_task(task6)
    print(f"✓ Task added to {parrot.name}: {task6.name} ({task6.duration_minutes} min, {task6.priority} priority)")
    
    task7 = Task(
        name="Feed Polly seeds",
        duration_minutes=5,
        priority="high",
        category="feeding"
    )
    parrot.add_task(task7)
    print(f"✓ Task added to {parrot.name}: {task7.name} ({task7.duration_minutes} min, {task7.priority} priority)\n")
    
    # ===== STEP 4: Display All Tasks =====
    print("[STEP 4] All Tasks in System...")
    all_tasks = owner.get_tasks()
    print(f"Total tasks to schedule: {len(all_tasks)}")
    for idx, task in enumerate(all_tasks, 1):
        print(f"  {idx}. {task.name} - {task.duration_minutes} min ({task.priority})")
    print()
    
    # ===== STEP 5: Generate Schedule =====
    print("[STEP 5] Generating Optimized Schedule...")
    schedule = owner.request_schedule()
    print()
    
    # ===== STEP 6: Display Schedule =====
    print("[STEP 6] Today's Schedule")
    print(schedule.summary())
    print()
    
    # ===== STEP 7: Display Scheduling Decisions =====
    print("[STEP 7] Scheduling Decisions Explained")
    explanations = schedule.explain()
    for explanation in explanations:
        print(explanation)
    print()
    
    # ===== SUMMARY =====
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join([pet.name for pet in owner.get_pets()])}")
    print(f"Total tasks: {len(all_tasks)}")
    print(f"Available time: {owner.available_minutes} minutes")
    print(f"Scheduled time: {schedule.total_minutes} minutes")
    print(f"Tasks scheduled: {len(schedule.planned_tasks)}/{len(all_tasks)}")
    print(f"Tasks not scheduled: {len(schedule.skipped_tasks)}")
    print("=" * 60)


if __name__ == "__main__":
    # Run the main demonstration
    main()
