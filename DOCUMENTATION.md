# HealthCheck AI - Full Project Documentation 🩺

## 1. Project Overview
**HealthCheck AI** is a lightweight, full-stack medical symptom checker. It leverages Machine Learning (Random Forest) to analyze user-provided symptoms and predict potential diseases. The application is designed with a modern, glassmorphism-inspired UI and provides clinical-grade metadata including severity levels, precautions, and health advice.

---

## 2. Technical Architecture
The project follows a **Client-Server Architecture**:
- **Frontend**: A Single Page Application (SPA) built with Vanilla JS, CSS3, and HTML5.
- **Backend**: A RESTful API built with FastAPI (Python) that serves ML predictions.
- **ML Engine**: Scikit-Learn based classification model.

---

## 3. Technology Stack
| Component | Technology |
| :--- | :--- |
| **Backend Framework** | FastAPI (Python) |
| **Machine Learning** | Scikit-Learn (Random Forest Classifier) |
| **Data Processing** | Pandas, NumPy |
| **Frontend** | HTML5, CSS3 (Custom Glassmorphism), JavaScript (ES6+) |
| **Server/Runtime** | Uvicorn |
| **History Tracking** | Browser LocalStorage |

---

## 4. Key Features
### 📝 Intelligent Symptom Selection
- Real-time search with auto-suggestions.
- Tag-based symptom management.
- Supports 130+ distinct medical symptoms.

### 🤖 AI Diagnosis Engine
- Predicts top possible diseases based on symptom patterns.
- Provides a **Match Confidence %** for each prediction.
- Classifies 40+ common medical conditions.

### 📊 Comprehensive Insights
- **Severity Indicators**: Color-coded risk levels (Low, Moderate, High, Critical).
- **Precautions**: Immediate actionable steps (e.g., hydration, isolation).
- **Health Advice**: Long-term lifestyle and dietary suggestions.

### 🕒 History Tracking
- Automatically saves recent diagnostics.
- Allows one-click recall of past symptom sets and results.
- Persistent storage using browser LocalStorage.

---

## 5. Directory Structure
```text
ai-health-checker/
├── backend/
│   ├── data/
│   │   ├── symptoms_diseases.csv     # Training Dataset
│   │   └── disease_info.json         # Disease Metadata
│   ├── models/
│   │   ├── health_model.pkl          # Trained RandomForest Model
│   │   └── symptom_list.pkl          # List of valid symptoms
│   ├── main.py                       # FastAPI Application
│   ├── data_gen.py                   # Data Generation & Metadata Script
│   ├── model_trainer.py              # ML Training Script
│   └── requirements.txt              # Backend Dependencies
├── frontend/
│   ├── index.html                    # Main UI
│   ├── style.css                     # Custom Aesthetics
│   └── script.js                     # Frontend Logic & History
├── run.ps1                           # One-click Startup Script
└── DOCUMENTATION.md                  # This File
```

---

## 6. Setup & Installation
### Prerequisites
- Python 3.8+ installed.
- PowerShell (for Windows users).

### Installation Steps
1. **Navigate to Project Directory**:
   ```powershell
   cd ai-health-checker
   ```
2. **Install Dependencies**:
   ```powershell
   pip install fastapi uvicorn scikit-learn pandas numpy python-multipart
   ```
3. **Run the Application**:
   ```powershell
   ./run.ps1
   ```

---

## 7. Machine Learning Model Logic
The system uses a **Random Forest Classifier**:
1. **Data**: Trained on a synthetic dataset representing 40+ diseases with various symptom combinations.
2. **Preprocessing**: Symptoms are converted into a binary vector (1 if present, 0 if absent).
3. **Prediction**: The model calculates the probability of each disease.
4. **Post-processing**: The top results are filtered and enriched with metadata from `disease_info.json`.

---

## 8. Development & Customization
- **Adding Symptoms**: Update `backend/data_gen.py` and re-run the script.
- **Updating UI**: Modify `frontend/style.css` for design changes or `frontend/index.html` for structural changes.
- **Port Settings**: If port `8001` is blocked, update `backend/main.py` and `frontend/script.js`.

---

## 9. Disclaimer
> [!IMPORTANT]
> This application is powered by Artificial Intelligence and is intended for **educational and informational purposes only**. It does **NOT** provide medical diagnoses. Always consult a certified healthcare professional for medical advice, diagnoses, or treatment.
