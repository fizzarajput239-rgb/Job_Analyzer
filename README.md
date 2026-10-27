# AI Job Description Analyzer (LangGraph)

## Workflow
Job Description -> Node 1 Extraction -> Node 2 Classification -> Node 3 Skill Analysis -> Node 4 Hiring Report

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env     # apni API key daalein, LLM_PROVIDER = groq ya gemini
```

## Run
```bash
streamlit run ui/app.py          # UI (skill tags + JSON download)
python main.py sample_job.txt    # CLI (hiring_report.json save hoti hai)
```

## Structure
- core/models.py     Pydantic models
- core/state.py      Shared LangGraph state
- core/nodes.py      4 nodes
- core/graph.py      Graph wiring + analyze_job_description()
- core/validation.py Empty/invalid input handling
- core/llm.py        Groq/Gemini factory
- core/export.py     JSON export
- ui/app.py          Streamlit UI
