MLOps Project – Vehicle Insurance Predictor

Welcome to the Vehicle Insurance Prediction MLOps project!
This project demonstrates a complete end-to-end machine learning pipeline — from dataset ingestion and preprocessing to model training, evaluation, deployment, and CI/CD automation.

You can access the live app here:
👉 https://vd-mlops-vehicle-insurance.onrender.com

It is built to showcase strong understanding of MLOps, MongoDB, Docker, GitHub Actions, Render Deployment, and modular ML pipeline architecture suitable for real-world systems.

📁 Project Setup and Structure
Step 1: Create GitHub Repository,Created a new repository with:
README.md
.gitignore
LICENSE

Cloned it locally and opened in VS Code:

code .

Step 2: Generate Project Template

Executed template.py to auto-create full folder structure and boilerplate modules.

Step 3: Setup Local Packages

Added setup.py to register local modules for import.
Added and updated requirements.txt.

🧩 Virtual Environment & Dependency Setup
Step 4: Initialize uv Environment
uv init

Step 5: Install Dependencies
uv add -r requirements.txt
uv pip install -e .

This installs both external libraries and local packages.

📊 MongoDB Setup & Data Management
Step 6: Prepare Notebook

Created a notebook/ folder.
Added dataset.
Created mongoDB_demo.ipynb.

Step 7: Upload Data to MongoDB

Pushed dataset into MongoDB using the Jupyter notebook.

Step 8: Validate Data in MongoDB Atlas

Navigated to:

MongoDB Atlas → Database → Browse Collections
Confirmed the data stored in key–value document format.

📝 Logging, Exception Handling & EDA
Step 9: Add Logging & Error Handling

Added modular logging and exception utilities.
Tested using demo.py.

Step 10: Perform EDA

Conducted detailed Exploratory Data Analysis on dataset.
Identified relationships & patterns for modeling.

📥 Data Ingestion Pipeline
Step 11: Build Data Ingestion Components

Implemented the ingestion flow:
Declared variables in constants/__init__.py
Added MongoDB connection function in configuration/mongo_db_connections.py
Added logic to fetch MongoDB data in data_access/proj1_data.py

Updated:

entity/DataIngestionConfig
entity/DataIngestionArtifact

Implemented ingestion logic in:

components/data_ingestion.py
Integrated ingestion with Training Pipeline.

Step 12: Environment Variable Setup

Created .env file:

MONGODB_URL=<<URL of the MONGDB database>>

Loaded via:

from dotenv import load_dotenv
load_dotenv()

🔍 Data Validation, Transformation & Training
Step 13: Data Validation

Updated config/schema.yaml with dataset schema.
Added validation utilities in utils/main_utils.py.
Added validation logic under components/data_validation.py.

Step 14: Data Transformation

Created estimator.py under entity/.
Added feature transformation logic in components/data_transformation.py.

Step 15: Model Training

Implemented Random Forest Classifier training:
Code inside components/model_trainer.py
Uses logic from estimator.py
Trained model saved inside: RandomForestClassifier/

🏆 Model Evaluation & Model Pusher
Step 16: Evaluation Logic

Compared newly trained model’s F1 score with previously stored model (Google Drive / Local directory).
If performance improved → replaced old model.

Step 17: Model Pusher

Updated logic to push validated models to deployment directory:

RandomForestClassifier/

🤖 Prediction Pipeline & Web App
Step 18: Build Prediction Pipeline

Created reusable prediction class.
Integrated model loading & preprocessing.

Step 19: Create Web Interface

Implemented app.py
Added UI assets in:

static/
templates/

Users can now enter inputs and get predictions from the trained model.

🔄 CI/CD – Docker, GitHub Actions & Render
Step 20: Configure Deployment Files

Added:

Dockerfile
.dockerignore
.github/workflows/ for CI
render.yaml and render-run.yaml

Step 21: GitHub Secrets

Created GitHub Action secret for Render API key:
RENDER_API_KEY

Step 22: CI/CD Execution

Pushed code → GitHub Actions runs:

Build Docker image
Push to Render
Trigger deployment

🌐 Render Cloud Deployment
Step 23: Deployment on Render

Logged into Render Dashboard → Workbench
Viewed active deployment:
Vehicle Insurance Predictor

✔ Live URL

👉 https://vd-mlops-vehicle-insurance.onrender.com

🧪 Testing the App
Step 24: Test Prediction

Enter values in form → prediction returned instantly.

Step 25: Training Endpoint

App includes a training link to retrain the model with new data.

🎯 Project Workflow Summary
Data Ingestion 
    ➜ Data Validation
        ➜ Data Transformation
            ➜ Model Training
                ➜ Model Evaluation
                    ➜ Model Pusher
                        ➜ Prediction Pipeline
                            ➜ CI/CD & Deployment

🛠️ Technologies Used

Python
Scikit-learn
FastAPI / Flask
uv (environment & dependency management)
MongoDB Atlas
Pandas, NumPy
Docker
GitHub Actions
Render Cloud Deployment

💬 Connect

If you found this project helpful or want improvements, feel free to reach out or open an issue!

