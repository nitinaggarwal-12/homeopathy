# 🌿 Classical Homeopathy Portal

A compassionate digital homeopath trained on centuries of wisdom — practicing classical homeopathy with scientific discipline, empathy, and zero hallucination.

## Features

- **🎯 Classical Approach**: Kent, Boenninghausen, Hering, Allen methodology
- **🤖 Multi-Agent Workflow**: CaseTaker → Repertory → MateriaMedica → Differential → Prescription
- **🔍 AI-Powered Search**: OpenAI embeddings for semantic Materia Medica search
- **🌐 Bilingual UI**: Full English/Hindi support
- **⚕️ Safety First**: Red flag screening and emergency referral
- **📊 Single Remedy**: One medicine at a time based on totality of symptoms

## Quick Start

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### 2. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Launch Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
homeopathy/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── data/
│   ├── repertory_mapping.csv  # Rubrics and remedy mappings
│   ├── materia_medica/        # Remedy descriptions
│   └── mm_index.json          # Embeddings index (auto-generated)
├── prompts/
│   ├── system.txt             # LLM system prompt
│   ├── dosage_policy.txt      # Potency guidelines
│   └── disclaimer.txt         # Safety disclaimer
└── src/
    ├── orchestrator.py        # Multi-agent workflow
    ├── embeddings.py          # OpenAI embeddings search
    ├── repertory.py           # Rule-based repertorization
    ├── safety.py              # Red flag detection
    ├── translations.py        # Bilingual support
    └── utils.py               # Helper functions
```

## Workflow

1. **Case Taking**: Detailed symptom collection (mental, emotional, generals, particulars)
2. **Repertorization**: Rule-based mapping to rubrics with weighted scoring
3. **Materia Medica**: AI semantic search for remedy characteristics
4. **Differential**: LLM analysis comparing top 3 remedies
5. **Prescription**: Single remedy with conservative potency and monitoring advice

## Data Expansion

### Add More Remedies

Create new `.md` files in `data/materia_medica/`:

```markdown
Remedy: Remedy Name
Keynotes:
- Characteristic symptom 1
- Characteristic symptom 2
- Characteristic symptom 3

Modalities: Worse/Better conditions
Constitution: Physical and mental type
```

### Add More Rubrics

Edit `data/repertory_mapping.csv`:

```csv
rubric,keywords,weight,candidate_remedies
"Mind - Anxiety - health about","anxiety health, hypochondria",3,"Arsenicum album;Phosphorus"
```

## Safety & Disclaimer

⚠️ **This is educational software only**
- Does NOT replace a licensed medical professional
- In emergencies, seek immediate medical care
- Do not stop prescribed treatments without doctor's guidance
- Red flags trigger automatic emergency referral

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for API calls)

## License

Educational use only. Not for commercial medical practice.
