# 🔹 LLM Text Pipeline Visualizer

A Streamlit-based application for visualizing text extraction, custom chunking with overlaps, and tokenization processes for Large Language Models (LLMs).

## Features

- **📝 Sentence Extraction** - Extract and analyze individual sentences from input text using spaCy NLP
- **🧩 Custom Overlap Chunks** - Create text chunks with configurable size and overlap for better LLM processing
- **🎟️ Tokenization Process** - Visualize how text is tokenized using OpenAI's tiktoken encoder
- **📊 Analytics Dashboard** - View detailed metrics about your text processing pipeline

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chunking-model
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running Locally

```bash
streamlit run app2.py
```

The app will open at `http://localhost:8501`

## Configuration

Use the sidebar to configure:
- **Max Chunk Size** - Number of words per chunk (5-100)
- **Chunk Overlap** - Words carried over between chunks (0-50)

**Note:** Overlap must be strictly less than chunk size

## Dependencies

- **streamlit** - Web application framework
- **spacy** - Natural language processing
- **tiktoken** - OpenAI tokenizer
- **plotly** - Interactive visualizations

See `requirements.txt` for exact versions

## Deployment on Render

### Free Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - The deployment will auto-configure from `render.yaml`
   - Click "Deploy"

3. **Access Your App**
   - Your live app will be at: `https://<service-name>.onrender.com`

### Free Tier Details
- ✅ Always free
- ⏱️ App spins down after 15 min of inactivity (wakes up on request)
- 💾 512 MB memory
- 🔄 Auto-deploys on GitHub commits to main branch

## Project Structure

```
.
├── app2.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Usage Example

1. Enter or paste text in the text area
2. Adjust chunk size and overlap in the sidebar
3. View results in four tabs:
   - Sentence Extraction
   - Custom Overlap Chunks
   - Tokenization Process
   - Analytics Dashboard

## Troubleshooting

**Issue:** spaCy model not found
- **Solution:** Run `python -m spacy download en_core_web_sm`

**Issue:** Port 8501 already in use
- **Solution:** Use `streamlit run app2.py --server.port=8502`

**Issue:** App is slow on Render free tier
- **Solution:** Free tier apps spin down after inactivity. This is expected behavior.

## License

MIT License

## Author

Created for LLM text processing and visualization

## Support

For issues or feature requests, please create an issue on the GitHub repository.
