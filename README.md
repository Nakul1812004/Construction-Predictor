# Construction Planner (ML + FastAPI + PySide6)

## Setup

### 1) Train ML Model
cd backend
pip install -r requirements.txt
python app/services/ml_model.py

### 2) Run Backend
uvicorn app.main:app --reload

### 3) Run Frontend
cd ../frontend
pip install -r requirements.txt
python app.py
