# NutriAI – LLaMA-2 Powered Supplement Recommender

NutriAI is a full-stack AI project that recommends supplements using a **local LLaMA-2 model** and integrates with **Supabase** for database and authentication management.

Built with:
- Backend: FastAPI (Python)
- Frontend: React
- Model: Local LLaMA-2-7B (.gguf)
- Database: Supabase (PostgreSQL)

---

## Quick Setup (Windows)

1. Clone the repository
```bash
git clone https://github.com/yardenDe/NutriAI.git
cd NutriAI

2. Run setup
bash
Copy code
run_project.bat
The script will automatically:
  Create a Python virtual environment
  Install all backend dependencies
  Check for the local LLaMA-2 model
  Start the backend (FastAPI + Uvicorn)
  Start the React frontend

Manual Setup (optional):
  Backend:
    cd Backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload
  Frontend:
    cd Frontend\app
    npm install
    npm start
  Local Model (LLaMA-2);
    Place your model file inside:    Backend/models/
    Example:  Backend/models/llama-2-7b-chat.Q4_K_S.gguf
    Download from:  https://huggingface.co/TheBloke/Llama-2-7B-GGUF

  Environment Variables
    Duplicate .env.example → .env and fill in:
      SUPABASE_URL=your_supabase_project_url
      SUPABASE_PASSWORD=your_supabase_service_password
      MODEL_PATH=models/llama-2-7b-chat.Q4_K_S.gguf
      PORT=8000


Project Structure:
  
  NutriAI/
  ├── Backend/
  │   ├── main.py
  │   ├── url.py
  │   ├── file_parser.py
  │   ├── db.py
  │   ├── api.py
  │   ├── chat.py
  │   ├── requirements.txt
  │   ├── .env.example
  │   ├── models/
  │   │   └── README.txt
  │   └── venv/ (ignored)
  │
  ├── Frontend/
  │   └── app/
  │
  ├── run_project.bat
  ├── .gitignore
  └── README.md

Branches:
main – stable release

local-llm – full integration with local LLaMA-2

Created by @yardenDe

רוצה שאעדכן לך גם גרסה של **`.env.example`** שתתאים לזה (כדי שתוכל פשוט להעתיק ולהשתמש בה)?




