import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train():
    # Load dataset
    data_path = 'data/symptoms_diseases.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return
    
    df = pd.read_csv(data_path)
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Accuracy check
    score = rf.score(X_test, y_test)
    print(f"Model trained with accuracy: {score:.2f}")
    
    # Save the model and symptom list
    os.makedirs('models', exist_ok=True)
    joblib.dump(rf, 'models/health_model.pkl')
    joblib.dump(X.columns.tolist(), 'models/symptom_list.pkl')
    print("Model and symptoms list saved to models/")

if __name__ == "__main__":
    train()
