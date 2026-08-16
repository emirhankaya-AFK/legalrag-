# LegalRAG - AI Legal Document Analyzer

[English](README.md) | [Türkçe](README_TR.md)

LegalRAG is a complete, automated legal contract risk assessment and clause extraction system.

## Setup Instructions

1. **Navigate to Project Directory**:
   ```bash
   cd legalrag
   ```

2. **Install Dependencies**:
   Create a virtual environment and run:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Configure API Key**:
   Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```
   *Note: If no API key is provided, the application automatically runs in Mock Mode with simulated outputs for development/testing.*

4. **Start the FastAPI Backend**:
   ```bash
   uvicorn backend.main:app --port 8001 --reload
   ```

5. **Start the Streamlit Frontend**:
   In another terminal, run:
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```

## Features
- **Batch PDF upload**: Upload multiple agreements at once.
- **Risk Score Indicator**: Visual progress bar scoring risk (0-100) based on predefined rule weights.
- **Side-by-side Contract Comparison**: Compare clauses and risk weights of two separate agreements.
- **Citations Q&A**: Interactively query the contract text using semantic embeddings with citations.
- **Reports Export**: Export PDF report, CSV summary, and JSON data.
