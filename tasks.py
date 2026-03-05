# importerer Task fra CrewAI biblioteket
from crewai import Task
# henter de tre agenter
from agents import architect, coder, tester

# opretter en ny opgave og gemmer den i variablen Task
design_task = Task(
    description="""Design a simple Todo web app in HTML/CSS/JS.
    Describe the layout, components, and how todos will be stored (localStorage).
    Keep it short.""",
    expected_output="A short design document describing the UI layout and components.",
    agent=architect,
)

code_task = Task(
    description="""Build a complete single-page Todo app using only HTML, CSS and vanilla JavaScript.
    Requirements:
    - Add a todo
    - Mark as completed
    - Delete a todo
    - Store todos in localStorage
    Save the result as a single index.html file.""",
    expected_output="A complete, working index.html file with embedded CSS and JS.",
    agent=coder,
    #  den siger "før du starter, læs hvad den forrige agent lavede"
    context=[design_task],
)

test_task = Task(
    description="""Review the Todo app HTML/CSS/JS code.
    List any bugs, missing features, accessibility issues, and improvements.
    Be specific and technical.""",
    expected_output="A written QA report with bugs and suggestions.",
    agent=tester,
    context=[code_task],
)