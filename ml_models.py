import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Constants for risk thresholds
HIGH_RISK_THRESHOLD = 70
MODERATE_RISK_THRESHOLD = 40
LOW_RISK_THRESHOLD = 20

# Placeholder for pregnancy risk model
# In a real scenario, this would be a trained model loaded from disk
pregnancy_risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
pregnancy_risk_model_trained = False

# Placeholder for anemia risk model
anemia_risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
anemia_risk_model_trained = False

# Feature lists for each model
pregnancy_risk_features = [
    'age_above_35', 'multiple_pregnancy', 'previous_csection', 
    'previous_preterm_birth', 'previous_miscarriage', 'diabetes', 
    'hypertension', 'heart_disease', 'kidney_disease', 
    'autoimmune_disease', 'gestational_diabetes', 'preeclampsia', 
    'placenta_previa', 'bleeding', 'smoking', 'alcohol', 'drug_use'
]

anemia_risk_features = [
    'fatigue', 'dizzy_spells', 'pale_skin', 'shortness_of_breath', 
    'poor_diet', 'recent_blood_loss', 'hemoglobin'
]

def train_pregnancy_risk_model():
    """
    Trains a simple pregnancy risk model with synthetic data.
    In a real application, this would be trained with real medical data.
    """
    global pregnancy_risk_model, pregnancy_risk_model_trained
    
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    X = np.random.randint(0, 2, (n_samples, len(pregnancy_risk_features)))
    
    # Create synthetic labels (higher sum of risk factors = higher risk)
    feature_weights = np.array([5, 4, 3, 4, 3, 4, 4, 5, 4, 3, 5, 5, 4, 4, 3, 4, 5])
    weighted_sum = X.dot(feature_weights)
    # Convert to probability (0-100)
    y = 100 * (weighted_sum - weighted_sum.min()) / (weighted_sum.max() - weighted_sum.min())
    
    # Train the model
    pregnancy_risk_model.fit(X, y)
    pregnancy_risk_model_trained = True
    
    return pregnancy_risk_model


def train_anemia_risk_model():
    """
    Trains a simple anemia risk model with synthetic data.
    In a real application, this would be trained with real medical data.
    """
    global anemia_risk_model, anemia_risk_model_trained
    
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    X = np.random.randint(0, 2, (n_samples, len(anemia_risk_features) - 1))  # All features except hemoglobin
    
    # Add hemoglobin values (normal range: 12-15.5 g/dL for women)
    hemoglobin = np.random.normal(12, 2, n_samples)
    X = np.column_stack((X, hemoglobin))
    
    # Create synthetic labels
    # Low hemoglobin and more symptoms = higher anemia risk
    feature_weights = np.array([3, 3, 4, 3, 4, 5, -10])  # Negative weight for hemoglobin (lower is worse)
    weighted_sum = X.dot(feature_weights)
    # Convert to probability (0-100)
    y = 100 * (weighted_sum - weighted_sum.min()) / (weighted_sum.max() - weighted_sum.min())
    
    # Train the model
    anemia_risk_model.fit(X, y)
    anemia_risk_model_trained = True
    
    return anemia_risk_model


def predict_pregnancy_risk(assessment_data):
    """
    Predicts pregnancy risk based on assessment data.
    
    Args:
        assessment_data (dict): Dictionary containing risk factors
        
    Returns:
        float: Risk score between 0-100
    """
    global pregnancy_risk_model, pregnancy_risk_model_trained
    
    # Train model if not already trained
    if not pregnancy_risk_model_trained:
        train_pregnancy_risk_model()
    
    # Extract features from assessment data
    features = []
    for feature in pregnancy_risk_features:
        features.append(1 if assessment_data.get(feature, False) else 0)
    
    # Make prediction
    features_array = np.array(features).reshape(1, -1)
    risk_score = pregnancy_risk_model.predict(features_array)[0]
    
    # Ensure the score is in 0-100 range
    risk_score = max(0, min(100, risk_score))
    
    return float(risk_score)


def predict_anemia_risk(assessment_data):
    """
    Predicts anemia risk based on assessment data.
    
    Args:
        assessment_data (dict): Dictionary containing risk factors and hemoglobin level
        
    Returns:
        float: Risk score between 0-100
    """
    global anemia_risk_model, anemia_risk_model_trained
    
    # Train model if not already trained
    if not anemia_risk_model_trained:
        train_anemia_risk_model()
    
    # Extract features from assessment data
    features = []
    for feature in anemia_risk_features[:-1]:  # All features except hemoglobin
        features.append(1 if assessment_data.get(feature, False) else 0)
    
    # Add hemoglobin value (default to slightly low if not provided)
    hemoglobin = assessment_data.get('hemoglobin', 11.0)
    features.append(hemoglobin)
    
    # Make prediction
    features_array = np.array(features).reshape(1, -1)
    risk_score = anemia_risk_model.predict(features_array)[0]
    
    # If hemoglobin is very low, increase risk regardless of model
    if hemoglobin < 9.0:
        risk_score = max(risk_score, 80)
    elif hemoglobin < 11.0:
        risk_score = max(risk_score, 60)
    
    # Ensure the score is in 0-100 range
    risk_score = max(0, min(100, risk_score))
    
    return float(risk_score)


def get_risk_level(risk_score):
    """
    Converts a numerical risk score to a categorical risk level.
    
    Args:
        risk_score (float): Risk score between 0-100
        
    Returns:
        str: Risk level (Low, Moderate, High)
    """
    if risk_score >= HIGH_RISK_THRESHOLD:
        return "High"
    elif risk_score >= MODERATE_RISK_THRESHOLD:
        return "Moderate"
    else:
        return "Low"


def get_recommendations(risk_factors, risk_level):
    """
    Generates recommendations based on risk factors and risk level.
    
    Args:
        risk_factors (list): List of risk factors
        risk_level (str): Risk level (Low, Moderate, High)
        
    Returns:
        list: List of recommendations
    """
    recommendations = []
    
    if risk_level == "High":
        recommendations.append("Consult with a healthcare provider immediately")
        recommendations.append("More frequent prenatal visits may be required")
        recommendations.append("Consider a referral to a maternal-fetal medicine specialist")
    
    elif risk_level == "Moderate":
        recommendations.append("Schedule a follow-up appointment soon")
        recommendations.append("Monitor symptoms closely")
        recommendations.append("Follow a healthy diet and lifestyle")
    
    else:  # Low risk
        recommendations.append("Continue routine prenatal care")
        recommendations.append("Maintain a balanced diet rich in iron and folic acid")
        recommendations.append("Stay physically active as recommended by your healthcare provider")
    
    # Add specific recommendations based on risk factors
    if 'diabetes' in risk_factors or 'gestational_diabetes' in risk_factors:
        recommendations.append("Monitor blood sugar levels regularly")
        recommendations.append("Follow a diabetic diet plan")
    
    if 'hypertension' in risk_factors or 'preeclampsia' in risk_factors:
        recommendations.append("Monitor blood pressure regularly")
        recommendations.append("Reduce salt intake")
        recommendations.append("Take prescribed medications as directed")
    
    if any(factor in risk_factors for factor in ['fatigue', 'dizzy_spells', 'pale_skin']):
        recommendations.append("Increase iron-rich foods in diet")
        recommendations.append("Take iron supplements as prescribed")
        recommendations.append("Include vitamin C with meals to improve iron absorption")
    
    return recommendations
