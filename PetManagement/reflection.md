# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML design for the PawPal+ system includes four main classes with the following responsibilities:

1. **Task**: Represents individual pet care activities (e.g., feeding, walking, grooming)
   - Attributes: name, duration_minutes, priority, category, completed status
   - Responsibilities: Store task metadata and determine priority level via `is_high_priority()` method
   - Converts task data to dictionary format via `to_dict()` for serialization

2. **Pet**: Represents a pet in the system
   - Attributes: name, species, age, special_needs
   - Responsibilities: Maintain pet information and characteristics
   - Converts pet data to dictionary format via `to_dict()` method

3. **Schedule**: Manages the daily pet care schedule
   - Attributes: planned_tasks list, skipped_tasks list, total_minutes
   - Responsibilities: Generate optimized schedules from a task list given time constraints, track which tasks fit and which are skipped, provide explanations and summaries of scheduling decisions
   - Core methods: `generate()` (schedule optimization), `explain()` (decision rationale), `summary()` (human-readable overview)

4. **Owner**: Represents the pet owner
   - Attributes: name, available_minutes (daily time budget), tasks list, pet reference
   - Responsibilities: Manage pet ownership, track available time for pet care, manage the task list, serve as the entry point to request a schedule
   - Core methods: `add_task()`, `remove_task()`, `get_tasks()`, `request_schedule()` (delegates to Schedule.generate())

**Key Design Relationships**: Owner owns a Pet (1:1), Owner manages multiple Tasks (1:N), and Owner requests a Schedule which optimizes those tasks given the available time constraint.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
