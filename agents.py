import os
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "qwen3:1.7b"

from crewai import Agent

architect = Agent(
    role="Software Architect",
    goal="Design a simple Todo REST API",
    backstory="You design clean, simple backend architectures.",
    verbose=True,
)

coder = Agent(
    role="Python Developer",
    goal="Implement the Todo API in Python using Flask",
    backstory="You write clean, working Python code.",
    verbose=True,
)

tester = Agent(
    role="QA Engineer",
    goal="Write tests for the Todo API",
    backstory="You write thorough unit tests.",
    # betyder at agenten printer alt hvad den tænker og gør i terminalen mens den kører
    verbose=True,
)