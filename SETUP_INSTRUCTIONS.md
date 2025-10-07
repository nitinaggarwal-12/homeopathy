# 🚀 Setup Instructions

## Step 1: Add Your OpenAI API Key

Before launching the application, you need to add your OpenAI API key:

1. Open the `.env` file in a text editor
2. Find the line: `OPENAI_API_KEY=your-api-key-here`
3. Replace `your-api-key-here` with your actual OpenAI API key
4. Save the file

**Example:**
```
OPENAI_API_KEY=sk-proj-abc123xyz...
```

### Don't have an API key?

Get one from: https://platform.openai.com/api-keys

## Step 2: Launch the Application

### Option A: Using the launch script (Recommended)
```bash
./launch.sh
```

### Option B: Manual launch
```bash
streamlit run app.py
```

## Step 3: Access the Application

The application will automatically open in your browser at:
```
http://localhost:8501
```

## Features Available

1. **📋 New Case**: Complete case-taking form with multi-agent analysis
2. **🔍 Materia Medica Search**: AI-powered semantic search
3. **ℹ️ About**: System information and status

## Language Support

Switch between English and Hindi using the language selector in the sidebar.

## Troubleshooting

### "OpenAI API Key not found" error
- Make sure you've edited the `.env` file
- Check that there are no extra spaces around the API key
- Restart the application after editing `.env`

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

## Need Help?

Check the main README.md for more detailed information about the system architecture and data expansion.
