import streamlit as st
from attributes import Owner, Pet, Task, Schedule

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
if "pet" not in st.session_state:
    st.session_state.pet = None
if "tasks" not in st.session_state:
    st.session_state.tasks = {}

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
        st.session_state.pet = Pet(pet_name, species, age, special_needs)
        st.success(f"Pet '{pet_name}' created!")
    
    if st.session_state.owner and st.session_state.pet:
        st.session_state.owner.pet = st.session_state.pet

# Main content area
col1, col2 = st.columns(2)

with col1:
    if st.session_state.owner:
        st.info(f"👤 Owner: **{st.session_state.owner.name}** ({st.session_state.owner.available_minutes} min/day)")
    else:
        st.warning("⚠️ Please create an owner first")

with col2:
    if st.session_state.pet:
        st.info(f"🐾 Pet: **{st.session_state.pet.name}** ({st.session_state.pet.species}, {st.session_state.pet.age} years old)")
    else:
        st.warning("⚠️ Please create a pet first")

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
    if st.session_state.owner:
        task = Task(task_name, duration, priority, category)
        st.session_state.tasks[task_name] = task
        st.session_state.owner.add_task(task)
        st.success(f"Task '{task_name}' added!")
    else:
        st.error("Please create an owner first")

# Display current tasks
if st.session_state.tasks:
    st.subheader("Current Tasks:")
    task_data = []
    for task_name, task in st.session_state.tasks.items():
        task_data.append({
            "Task": task.name,
            "Duration (min)": task.duration_minutes,
            "Priority": task.priority,
            "Category": task.category,
            "High Priority": task.is_high_priority() if hasattr(task, 'is_high_priority') else "❓"
        })
    st.dataframe(task_data, use_container_width=True)
    
    if st.button("🗑️ Clear All Tasks"):
        st.session_state.tasks = {}
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.header("📅 Generate Schedule")
st.caption("Create an optimized daily schedule based on available time and task priorities.")

if st.button("🔄 Generate Schedule", key="generate_schedule"):
    if not st.session_state.owner:
        st.error("Please create an owner first")
    elif not st.session_state.pet:
        st.error("Please create a pet first")
    elif not st.session_state.tasks:
        st.error("Please add at least one task")
    else:
        st.session_state.owner.get_tasks()
        schedule = st.session_state.owner.request_schedule()
        if schedule:
            st.subheader("✅ Generated Schedule")
            st.write(f"**Total scheduled time:** {schedule.total_minutes} minutes")
            
            if schedule.planned_tasks:
                st.markdown("### Planned Tasks")
                for task in schedule.planned_tasks:
                    st.write(f"- **{task.name}** ({task.duration_minutes} min) - Priority: {task.priority}")
            
            if schedule.skipped_tasks:
                st.markdown("### Tasks Not Scheduled")
                for task in schedule.skipped_tasks:
                    st.write(f"- {task.name} ({task.duration_minutes} min)")
            
            if hasattr(schedule, 'explain') and callable(schedule.explain):
                st.markdown("### Reasoning")
                explanations = schedule.explain()
                for explanation in explanations:
                    st.write(f"- {explanation}")
            
            if hasattr(schedule, 'summary') and callable(schedule.summary):
                st.markdown("### Summary")
                st.write(schedule.summary())
        else:
            st.info("Schedule generation not fully implemented yet.")

