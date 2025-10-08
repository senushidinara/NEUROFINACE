# ----------------------------------------------------------------------
# Training Script for the Fusion Engine Model
# Role: Defines the feature set and training routine.
# ----------------------------------------------------------------------
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
import joblib

def load_data():
    """Loads pre-processed feature data with risk labels."""
    # In production, this pulls from a data warehouse (e.g., BigQuery, S3)
    df = pd.DataFrame({
        'stress_level': np.random.rand(100),
        'typing_risk': np.random.rand(100),
        'behavioral_risk': np.random.rand(100),
        # Target variable: 1 (Impulsive/High-Risk), 0 (Rational/Low-Risk)
        'is_high_risk': np.random.randint(0, 2, 100)
    })
    return df

def train_fusion_model(df):
    """Trains the main risk classification model (e.g., Random Forest)."""
    X = df[['stress_level', 'typing_risk', 'behavioral_risk']]
    y = df['is_high_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    
    print(f"Model Trained. F1 Score: {f1:.4f}")
    
    # Save the model artifact to the 'models/' directory
    joblib.dump(model, '../../models/fusion_engine_v3.joblib')

if __name__ == '__main__':
    np.random.seed(42)
    data = load_data()
    train_fusion_model(data)
# ----------------------------------------------------------------------
