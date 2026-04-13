from crewai import Task
from agents import architect, tech_lead, coder

# 1. Architecture task
design_task = Task(
    description="""Design a simple To-Do web app.
    Include layout, components, and how todos will be stored (localStorage).""",
    expected_output="Short design document describing UI layout, components, and storage.",
    agent=architect,
)

# 2. Planning / Tech Lead task
planning_task = Task(
    description="""Break the To-Do app project into tasks:
    design, code, test, docs, deployment, with acceptance criteria and order.""",
    expected_output="Ordered task list with definitions of done.",
    agent=tech_lead,
    context=[design_task],
)

# 3. Implementation task
code_task = Task(
    description="""Build a single-page To-Do app using HTML/CSS/JS.
    Requirements:
    - Add todo
    - Mark as completed
    - Delete todo
    - Store todos in localStorage
    Save as a single index.html file.""",
    expected_output="Working index.html file with embedded CSS and JS.",
    agent=coder,
    context=[design_task, planning_task],
)

