from crewai import Crew, Process
from agents import architect, tech_lead, coder, AGENT_BASE_URLS
from tasks import (
    design_task, planning_task, code_task
)
import os
import re

# Create output folder
os.makedirs("output", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Create Crew
crew = Crew(
    agents=[architect, tech_lead, coder],
    tasks=[
        design_task,
        planning_task,
        code_task
    ],
    process=Process.sequential,
    verbose=True,
)

# Run the workflow
result = crew.kickoff()

# Save outputs
agent_names = ["architect","tech_lead","coder"]
tasks_list = [
    design_task, planning_task, code_task
]

for agent_name, task in zip(agent_names, tasks_list):
    with open(f"output/{agent_name}.md", "w") as f:
        base_url = AGENT_BASE_URLS.get(agent_name, "")
        f.write(f"Agent base_url (work location): {base_url}\n\n{str(task.output.raw)}")

# Extract coder's HTML to templates/index.html
html_match = re.search(r"```html\n(.*?)```", str(code_task.output.raw), re.DOTALL)
if html_match:
    with open("templates/index.html", "w") as f:
        f.write(html_match.group(1))

print("All tasks completed! Open http://localhost:5000 to preview.")