import json
import os

from crewai import Agent
from crewai.llm import LLM

# Load project-local environment (./.env) if present.
try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass


DEFAULT_BASE_URL = os.getenv("CREWAI_DEFAULT_BASE_URL", "http://localhost:11434/v1")
MODEL_NAME = os.getenv("CREWAI_MODEL_NAME", "qwen3:1.7b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")


def _parse_agent_base_urls(raw: str) -> dict[str, str]:
    if not raw.strip():
        return {}

    # Preferred format: JSON object.
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {str(k): str(v) for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass

    # Fallback format: comma-separated key=url pairs.
    #   architect=http://1.2.3.4:11434/v1,tech_lead=http://...
    pairs: dict[str, str] = {}
    for item in raw.split(","):
        item = item.strip()
        if not item or "=" not in item:
            continue
        k, v = item.split("=", 1)
        pairs[k.strip()] = v.strip()
    return pairs


AGENT_BASE_URLS: dict[str, str] = _parse_agent_base_urls(os.getenv("CREWAI_AGENT_BASE_URLS", ""))
AGENT_MODELS: dict[str, str] = _parse_agent_base_urls(os.getenv("CREWAI_AGENT_MODELS", ""))


def _make_llm(agent_name: str) -> LLM:
    base_url = AGENT_BASE_URLS.get(agent_name, DEFAULT_BASE_URL)
    model = AGENT_MODELS.get(agent_name, MODEL_NAME)
    # CrewAI's Ollama/OpenAI-compatible endpoints generally don't require a real key,
    # but keeping OPENAI_API_KEY preserves your current behavior.
    return LLM(model=model, base_url=base_url, api_key=OPENAI_API_KEY)


architect = Agent(
    role="Software Architect",
    goal="Design a simple To-Do app UI, components, and storage (localStorage)",
    backstory="You design clean, simple frontend architectures.",
    verbose=True,
    llm=_make_llm("architect"),
)

tech_lead = Agent(
    role="Tech Lead",
    goal="Break the To-Do app project into incremental tasks with scope, acceptance criteria, and order",
    backstory="You organize work efficiently.",
    verbose=True,
    llm=_make_llm("tech_lead"),
)

coder = Agent(
    role="Frontend Developer",
    goal="Implement a single-page To-Do app using HTML, CSS, and vanilla JavaScript",
    backstory="You write clean, working HTML/JS code.",
    verbose=True,
    llm=_make_llm("coder"),
)

