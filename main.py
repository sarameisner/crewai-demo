from crewai import Crew, Process
# henter agenterne og opgaverne du har defineret i de andre filer
from agents import architect, coder, tester
from tasks import design_task, code_task, test_task
# importerer os-biblioteket så vi kan arbejde med filer og mapper.
import os

# opretter output/ mappen hvis den ikke allerede findes. exist_ok=True betyder at den ikke crasher hvis mappen allerede eksisterer.
os.makedirs("output", exist_ok=True)

# samler det hele til ét crew
crew = Crew(
    # hvilke agenter der er med
    agents=[architect, coder, tester],
    # hvilke opgaver skal løses, i den rigtige rækkefølge 
    tasks=[design_task, code_task, test_task],
    # kør opgaverne én ad gangen i rækkefølge
    process=Process.sequential,
    # print hvad der sker i terminalen mens det kører
    verbose=True,
)

# print hvad der sker i terminalen mens det kører
result = crew.kickoff()

# gem hver agents output separat
# "w" betyder at den overskriver filen hvis den allerede findes
# f.write(str(...)) skriver agentens output til filen som tekst
with open("output/architect.md", "w") as f:
    f.write(str(design_task.output.raw))

with open("output/coder.md", "w") as f:
    f.write(str(code_task.output.raw))

with open("output/tester.md", "w") as f:
    f.write(str(test_task.output.raw))

# printer en besked i terminalen når alt er gemt
print("Færdig! Åbn http://localhost:5000")