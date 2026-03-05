import os
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "qwen3:1.7b"

from crewai import Agent
# 1. Architecture
architect = Agent(
    role="Software Architect",
    goal="Design a simple To-Do app UI, components, and storage (localStorage)",
    backstory="You design clean, simple frontend architectures.",
    verbose=True,
)

# 2. Tech Lead
tech_lead = Agent(
    role="Tech Lead",
    goal="Break the To-Do app project into incremental tasks with scope, acceptance criteria, and order",
    backstory="You organize work efficiently.",
    verbose=True,
)

# 3. Implementation
coder = Agent(
    role="Frontend Developer",
    goal="Implement a single-page To-Do app using HTML, CSS, and vanilla JavaScript",
    backstory="You write clean, working HTML/JS code.",
    verbose=True,
)

# 4. QA / Testing
tester = Agent(
    role="QA Engineer",
    goal="Review the To-Do app code and report bugs, missing features, and improvements",
    backstory="You write thorough QA reports.",
    verbose=True,
)

# 5. Documentation
docs_ai = Agent(
    role="Documentation Specialist",
    goal="Write developer and user documentation for the To-Do app",
    backstory="You write clear, concise documentation.",
    verbose=True,
)

# 6. Deployment Validation
devops_ai = Agent(
    role="Deployment Validator",
    goal="Verify the To-Do app runs in browser, persists todos in localStorage, and produce a deployment checklist",
    backstory="You validate that software can be deployed reliably.",
    verbose=True,
)