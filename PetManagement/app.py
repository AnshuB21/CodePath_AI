import streamlit as st
from Pawpal_system.owner import Owner
from Pawpal_system.pet import Pet
from Pawpal_system.task import Task
from Pawpal_system.schedule import Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
A pet care planning assistant that helps you schedule daily tasks for your pet(s)
based on time constraints, priorities, and pet needs.
"""
)

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:  # Changed to support multiple pets
    st.session_state.pets = {}  # Dictionary to store pets by name
if "tasks" not in st.session_state:
    st.session_state.tasks = {}  # Dictionary to store tasks: {pet_name: [tasks]}
if "selected_pet_name" not in st.session_state:
    st.session_state.selected_pet_name = None  # Track currently selected pet

st.divider()

# Sidebar: Owner and Pet Setup
with st.sidebar:
    st.header("📋 Owner & Pet Setup")
    
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_name_input")
    available_minutes = st.number_input(
        "Available time per day (minutes)", 
        min_value=5, 
        max_value=1440, 
        value=120,
        key="available_minutes"
    )
    
    if st.button("Create/Update Owner", key="create_owner"):
        st.session_state.owner = Owner(owner_name, available_minutes)
        st.success(f"Owner '{owner_name}' created!")
    
    st.divider()
    
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "hamster", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=50, value=3)
    special_needs = st.text_area("Special needs (optional)", value="", height=80)
    
    if st.button("Create/Update Pet", key="create_pet"):
        # Create new pet and add to owner
        new_pet = Pet(pet_name, species, age, special_needs)
        st.session_state.pets[pet_name] = new_pet
        
        # Add pet to owner if owner exists
        if st.session_state.owner:
            st.session_state.owner.add_pet(new_pet)
        
        st.success(f"Pet '{pet_name}' created!")
    
    # Display and manage existing pets
    if st.session_state.pets:
        st.divider()
        st.subheader("Existing Pets")
        for pet_name, pet in st.session_state.pets.items():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🐾 **{pet.name}** - {pet.species} (Age: {pet.age})")
                if pet.special_needs:
                    st.caption(f"Special needs: {pet.special_needs}")
            with col2:
                if st.button("🗑️", key=f"delete_pet_{pet_name}"):
                    if st.session_state.owner:
                        st.session_state.owner.remove_pet(pet_name)
                    del st.session_state.pets[pet_name]
                    st.rerun()
    
    # Select active pet for task management
    if st.session_state.pets:
        st.divider()
        st.subheader("📌 Select Active Pet")
        selected_pet_name = st.selectbox(
            "Choose pet to add tasks to:",
            list(st.session_state.pets.keys()),
            key="selected_pet"
        )
        # Store selected pet in session state for use in task management
        st.session_state.selected_pet_name = selected_pet_name

# Main content area
col1, col2 = st.columns(2)

with col1:
    if st.session_state.owner:
        st.info(f"👤 Owner: **{st.session_state.owner.name}** ({st.session_state.owner.available_minutes} min/day)")
    else:
        st.warning("⚠️ Please create an owner first")

with col2:
    if st.session_state.pets:
        st.info(f"🐾 Total Pets: **{len(st.session_state.pets)}** pets")
    else:
        st.warning("⚠️ Please create at least one pet")

st.divider()

st.header("📝 Tasks Management")
st.caption("Add tasks that your pet needs. Each task should have a name, duration, priority, and category.")

# Task input form
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_name = st.text_input("Task name", value="Morning walk", key="task_name_input")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration_input")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority_input")
with col4:
    category = st.selectbox(
        "Category", 
        ["walking", "feeding", "grooming", "medication", "enrichment", "training", "other"],
        key="category_input"
    )

if st.button("➕ Add Task"):
    if not st.session_state.owner:
        st.error("❌ Please create an owner first")
    elif not st.session_state.pets:
        st.error("❌ Please create at least one pet first")
    else:
        # Get the selected pet from session state
        selected_pet_name = st.session_state.get('selected_pet_name')
        
        if not selected_pet_name:
            # Use first pet if no specific pet is selected
            selected_pet_name = list(st.session_state.pets.keys())[0]
        
        selected_pet = st.session_state.pets.get(selected_pet_name)
        
        if selected_pet:
            # Create task and add to the selected pet
            task = Task(task_name, duration, priority, category)
            selected_pet.add_task(task)
            
            # Track task in session state for display
            if selected_pet.name not in st.session_state.tasks:
                st.session_state.tasks[selected_pet.name] = []
            st.session_state.tasks[selected_pet.name].append(task)
            
            st.success(f"✅ Task '{task_name}' added to {selected_pet.name}!")
        else:
            st.error("❌ Could not add task - no pet selected")

# Display current tasks organized by pet
if st.session_state.tasks:
    st.subheader("Current Tasks by Pet:")
    for pet_name, task_list in st.session_state.tasks.items():
        with st.expander(f"🐾 {pet_name} ({len(task_list)} tasks)"):
            task_data = []
            for task in task_list:
                task_data.append({
                    "Task": task.name,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                    "Category": task.category,
                    "High Priority": "✅ Yes" if task.is_high_priority() else "❌ No"
                })
            st.dataframe(task_data, width='stretch')
    
    if st.button("🗑️ Clear All Tasks"):
        st.session_state.tasks = {}
        # Also clear tasks from pets
        for pet in st.session_state.pets.values():
            pet.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.header("📅 Generate Schedule")
st.caption("Create an optimized daily schedule based on available time and task priorities.")

if st.button("🔄 Generate Schedule", key="generate_schedule"):
    # Validation checks
    if not st.session_state.owner:
        st.error("❌ Please create an owner first")
    elif not st.session_state.pets:
        st.error("❌ Please create at least one pet first")
    elif not st.session_state.tasks or all(len(tasks) == 0 for tasks in st.session_state.tasks.values()):
        st.error("❌ Please add at least one task")
    else:
        try:
            # Generate schedule using the owner's request_schedule method
            # This will automatically gather all tasks from all pets
            schedule = st.session_state.owner.request_schedule()
            
            if schedule:
                st.subheader("✅ Generated Optimized Schedule")
                st.divider()
                
                # Calculate metrics
                total_tasks = len(st.session_state.owner.get_tasks())
                scheduled_tasks = len(schedule.planned_tasks)
                skipped_tasks = len(schedule.skipped_tasks)
                available_minutes = st.session_state.owner.available_minutes
                utilization = int((schedule.total_minutes / available_minutes) * 100) if available_minutes > 0 else 0
                
                # Display key metrics in columns
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric("⏱️ Time Used", f"{schedule.total_minutes}/{available_minutes} min")
                
                with metric_col2:
                    st.metric("✅ Tasks Scheduled", f"{scheduled_tasks}/{total_tasks}")
                
                with metric_col3:
                    st.metric("📊 Utilization", f"{utilization}%")
                
                with metric_col4:
                    status = "✅ Complete" if skipped_tasks == 0 else "⚠️ Partial"
                    st.metric("Status", status)
                
                st.divider()
                
                # Planned tasks section with expander
                with st.expander("✅ Scheduled Tasks", expanded=True):
                    if schedule.planned_tasks:
                        # Create task display
                        for idx, task in enumerate(schedule.planned_tasks, 1):
                            priority_color = "🔴" if task.is_high_priority() else "⚪"
                            category_emoji = {
                                'walking': '🚶',
                                'feeding': '🍖',
                                'grooming': '✂️',
                                'medication': '💊',
                                'enrichment': '🎾',
                                'training': '🎓',
                                'cleaning': '🧹',
                                'playing': '🎮'
                            }.get(task.category.lower(), '📌')
                            
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            with col1:
                                st.write(f"{idx}. **{task.name}**")
                            with col2:
                                st.write(f"**{task.duration_minutes}m**")
                            with col3:
                                st.write(priority_color)
                            with col4:
                                st.write(category_emoji)
                    else:
                        st.info("No tasks scheduled")
                
                # Skipped tasks section
                if schedule.skipped_tasks:
                    with st.expander("⏭️  Skipped Tasks", expanded=False):
                        skipped_time = sum(task.duration_minutes for task in schedule.skipped_tasks)
                        st.warning(f"⚠️ {len(schedule.skipped_tasks)} task(s) couldn't fit - would require {skipped_time} additional minutes")
                        for idx, task in enumerate(schedule.skipped_tasks, 1):
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"{idx}. {task.name}")
                            with col2:
                                st.write(f"**{task.duration_minutes}m**")
                            with col3:
                                st.write("⚪")
                
                # Display full formatted summary
                st.divider()
                st.subheader("📋 Full Schedule Summary")
                
                # Use code block to preserve formatting of the beautiful summary
                summary_text = schedule.summary()
                st.code(summary_text, language="")
                
                # Display scheduling reasoning
                st.divider()
                st.subheader("📝 Scheduling Decisions")
                explanations = schedule.explain()
                
                with st.expander("View detailed explanations", expanded=False):
                    for explanation in explanations:
                        st.write(f"• {explanation}")
                
                # Success message
                st.success("🎉 Schedule generated successfully!")
            else:
                st.error("❌ Failed to generate schedule")
        
        except Exception as e:
            st.error(f"❌ Error generating schedule: {str(e)}")

