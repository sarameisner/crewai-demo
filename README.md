# CrewAI Local Multi-Endpoint Toolchain

This project runs a small CrewAI workflow for a To-Do app using local LLM backends (for example, Ollama servers on different machines).

Current workflow roles:
- `architect`
- `tech_lead`
- `coder`

The workflow writes markdown artifacts to `output/` and extracts generated HTML into `templates/index.html` for preview.

## 1) Preconditions

- Python 3.10-3.12
- `pip`
- At least one local OpenAI-compatible endpoint (Ollama works)
- Optional: multiple machines running Ollama for per-agent routing

## 2) Install

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 3) Configure environment

Create `.env` from the template:

```bash
cp .env.example .env
```

Edit `.env` and set at least these values:

- `CREWAI_AGENT_BASE_URLS`: JSON mapping `agent_name -> http://<ip>:11434/v1`
- `CREWAI_DEFAULT_BASE_URL`: fallback endpoint
- `CREWAI_MODEL_NAME`: default model name
- `OPENAI_API_KEY`: can remain `ollama` for local Ollama

Optional:
- `CREWAI_AGENT_MODELS`: JSON mapping `agent_name -> model_name` for per-agent models

Example:

```env
CREWAI_AGENT_BASE_URLS={"architect":"http://10.136.133.45:11434/v1","tech_lead":"http://10.136.137.247:11434/v1","coder":"http://10.136.139.223:11434/v1"}
CREWAI_DEFAULT_BASE_URL=http://10.136.133.45:11434/v1
CREWAI_AGENT_MODELS={"architect":"qwen3:1.7b","tech_lead":"llama3.2:3b","coder":"qwen2.5-coder:7b"}
CREWAI_MODEL_NAME=qwen3:1.7b
OPENAI_API_KEY=ollama
```

## 4) Verify each endpoint (important)

Run from the controller machine (the one that runs `main.py`):

```bash
curl -s http://10.136.133.45:11434/api/tags
curl -s http://10.136.133.45:11434/v1/models
```

Repeat for every IP used in `CREWAI_AGENT_BASE_URLS`.

If LAN IP calls fail but `localhost` works on the remote machine, bind Ollama to the network:

```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

## 5) Run the Crew workflow

```bash
source .venv/bin/activate
python main.py
```

What happens:
- Crew runs tasks sequentially.
- Agent outputs are saved into `output/architect.md`, `output/tech_lead.md`, `output/coder.md`.
- `templates/index.html` is generated from the coder output (when fenced HTML is present).

## 6) Preview generated app

Start Flask preview server:

```bash
python app.py
```

Open:
- `http://localhost:5000` (generated HTML app)
- `http://localhost:5000/output` (rendered agent outputs)
- `http://localhost:5000/preview` (raw extracted HTML preview)

## 7) Operating guide (day-to-day)

- Update routing in `.env` to move an agent to another machine.
- Update `CREWAI_AGENT_MODELS` to change per-agent model without code edits.
- Re-run `python main.py` after config changes.
- Check `output/*.md` first line to confirm which base URL each agent used.

## 8) Common troubleshooting

- **Connection error to OpenAI API**
  - Verify IP/port with `curl` from the controller machine.
  - Confirm remote Ollama is running and reachable on LAN.
  - Check firewall and VPN/network segmentation.

- **Model not found**
  - Pull the model on the target host:
    - `ollama pull <model-name>`
  - Ensure `CREWAI_AGENT_MODELS` entries exist on their assigned hosts.

- **No `templates/index.html` generated**
  - The coder output did not include a fenced HTML block.
  - Inspect `output/coder.md` and re-run with clearer coder instructions in `tasks.py`.

## 9) Key files

- `agents.py`: agent definitions + per-agent endpoint/model config
- `tasks.py`: workflow task prompts and context
- `main.py`: kickoff and artifact writing
- `app.py`: preview server
- `.env.example`: config template

