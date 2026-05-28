**Construction Planner** 

**Project Description**

Construction Planner ML is an AI-powered desktop application developed to help users estimate construction costs intelligently using Machine Learning. The system predicts future material prices, labour expenses, total project cost, construction duration, and the best time to start construction based on historical market trends, seasonal patterns, and temperature conditions.

The application combines a modern desktop interface with machine learning models and backend APIs to provide accurate construction planning insights for residential projects.


**Technologies & Libraries Used**

Frontend:  
->PySide6 → Desktop GUI development  
->Matplotlib → Graph visualization and analytics  

Backend:  
->FastAPI → REST API development  
->Uvicorn → Backend server  

Machine Learning:  
->Scikit-learn → ML model training and prediction  
->Random Forest Regressor → Non-linear prediction model  
->Linear Regression → Trend-based forecasting   
->Pandas → Dataset processing and analysis  
->NumPy → Numerical computations  
->Joblib → Saving and loading ML models  

Database & Authentication:  
->SQLite → Lightweight database  
->SQLAlchemy → ORM and database management  
->Passlib → Password hashing utilities  
->Argon2 → Secure password hashing algorithm  

Other Libraries:  
->Requests → Frontend-backend API communication  


**Setup**
1) Train ML Model  
cd backend pip install -r requirements.txt python app/services/ml_model.py

2) Run Backend
cd backend  
uvicorn core.main:app --reload

3) Run Frontend  
cd ../frontend pip install -r requirements.txt python app.py


**Team Members**  
Nakul Agrawal(EN23CS301646)    
Naman Patil(EN23CS301653)  
Naman Mathe(EN23CS301652)  