Since you are the Integration Lead (Member D), presenting your project in English on GitHub is the right move—it makes it look professional and accessible to a global audience (and most hackathon judges).

Here is the English version of your README.md. You can copy and paste this directly:

⚖️ Malaysia Legal AI Agent (Employment Act 1955)
2026 Hackathon Project - An automated contract audit system powered by RAG (Retrieval-Augmented Generation) specifically tailored for the Malaysian legal landscape.

🌟 Overview
This system is designed to automate the tedious process of auditing employment contracts against the Malaysian Employment Act 1955. It identifies non-compliant clauses and provides legal justifications and suggestions in seconds.

Key Features
Precision Retrieval: Uses ChromaDB to store and query the latest amendments of the Employment Act.

Automated Audit: Powered by DeepSeek/ILMU LLM to analyze complex legal phrasing.

Risk Categorization: Flags violations as HIGH, MEDIUM, or LOW risk with actionable advice.

🛠️ System Architecture
The project follows a modular micro-service design for high scalability:

Module A (OCR & Parsing): Extracts structured text from unstructured PDF contracts.

Module B (RAG & Vector DB): Converts legal sections into embeddings using all-MiniLM-L6-v2 for semantic search.

Module C (AI Brain): A sophisticated Prompt Engineering layer that handles legal reasoning and compliance checks.

Module D (Integration & UI): A Gradio-based web interface for seamless user interaction and system orchestration.

🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.9+ installed. Clone the repository and set up a clean environment:

Bash
git clone https://github.com/25062891/legal-ai-agent.git
cd legal-ai-agent

# Set up Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
2. Configuration
Create a .env file in the root directory:

Code snippet
MY_API_KEY=your_api_key_here
BASE_URL=your_api_endpoint_here
3. Initialize Legal Knowledge Base
Run the following script to populate the vector database with the Employment Act:

Bash
python3 member_b.py
4. Launch the Application
Start the Gradio web interface:

Bash
python3 app.py
Open your browser and navigate to: http://127.0.0.1:7860

📁 Project Structure
Plaintext
legal_agent_project/
├── data/raw/             # Sample PDF contracts for testing
├── vector_db/            # Persistent ChromaDB storage
├── member_b.py           # Script for legal document ingestion
├── brain.py              # Core AI logic and LLM API integration
├── app.py                # Gradio UI and main application entry
├── schemas.py            # Pydantic data models for type safety
├── requirements.txt      # Project dependencies
└── .gitignore            # Git exclusion rules (venv, model_cache, etc.)
👥 The Team
Zhang Xiyuan: PDF Parsing & Data Pre-processing.

Wang Zihao: Vector Database & Semantic Retrieval (RAG).

Ping Shuya: Prompt Engineering & LLM Legal Reasoning.

Zhu Guanyu:(Lead): System Integration, API Adaptation & Deployment.

Pan Dengyi:Front - end interface and PPT production
