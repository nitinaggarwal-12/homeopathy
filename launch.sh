#!/bin/bash

# Classical Homeopathy Portal Launch Script

echo "🌿 Classical Homeopathy Portal"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env 2>/dev/null || cat > .env << 'EOF'
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_HIGH_REASONING=gpt-4o
OPENAI_EMBED_MODEL=text-embedding-3-small
REPERTORY_PATH=data/repertory_mapping.csv
MM_DIR=data/materia_medica
EMBED_INDEX_PATH=data/mm_index.json
EOF
fi

# Check if API key is set
if grep -q "your-api-key-here" .env; then
    echo "⚠️  IMPORTANT: Please add your OpenAI API key to the .env file"
    echo ""
    echo "1. Open .env file in a text editor"
    echo "2. Replace 'your-api-key-here' with your actual OpenAI API key"
    echo "3. Save the file and run this script again"
    echo ""
    exit 1
fi

echo "✓ Configuration loaded"
echo ""

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "✓ Dependencies ready"
echo ""
echo "🚀 Launching application..."
echo ""
echo "   The app will open in your browser at: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
