from crewai import Crew, Process
from agents import architect, tech_lead, coder, tester, docs_ai, devops_ai
from tasks import (
    design_task, planning_task, code_task, test_task,
    documentation_task, deployment_task
)
import os
import re

# Create output folder
os.makedirs("output", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Create Crew
crew = Crew(
    agents=[architect, tech_lead, coder, tester, docs_ai, devops_ai],
    tasks=[
        design_task,
        planning_task,
        code_task,
        test_task,
        documentation_task,
        deployment_task
    ],
    process=Process.sequential,
    verbose=True,
)

# Run the workflow
result = crew.kickoff()

# Save outputs
agent_names = ["architect","tech_lead","coder","tester","docs_ai","devops_ai"]
tasks_list = [
    design_task, planning_task, code_task,
    test_task, documentation_task, deployment_task
]

for agent_name, task in zip(agent_names, tasks_list):
    with open(f"output/{agent_name}.md", "w") as f:
        f.write(str(task.output.raw))

# Extract coder's HTML to templates/index.html
html_match = re.search(r"```html\n(.*?)```", str(code_task.output.raw), re.DOTALL)
if html_match:
    with open("templates/index.html", "w") as f:
        f.write(html_match.group(1))

print("All tasks completed! Open http://localhost:5000 to preview.")