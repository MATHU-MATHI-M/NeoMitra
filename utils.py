from datetime import datetime, timedelta
import os
import json
from flask import session

# Function to calculate due date from last menstrual period
def calculate_due_date(last_menstrual_period):
    """
    Calculate the estimated due date based on last menstrual period.
    
    Args:
        last_menstrual_period (datetime): Date of the last menstrual period
        
    Returns:
        datetime: Estimated due date
    """
    return last_menstrual_period + timedelta(days=280)

# Function to calculate BMI
def calculate_bmi(weight_kg, height_cm):
    """
    Calculate Body Mass Index (BMI).
    
    Args:
        weight_kg (float): Weight in kilograms
        height_cm (float): Height in centimeters
        
    Returns:
        float: BMI value
    """
    if height_cm <= 0:
        return None
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 1)

# Function to get BMI category
def get_bmi_category(bmi):
    """
    Get the BMI category based on the BMI value.
    
    Args:
        bmi (float): BMI value
        
    Returns:
        str: BMI category
    """
    if bmi is None:
        return "Unknown"
    
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Function to check if hemoglobin level indicates anemia
def check_anemia(hemoglobin, is_pregnant=False):
    """
    Check if hemoglobin level indicates anemia.
    
    Args:
        hemoglobin (float): Hemoglobin level in g/dL
        is_pregnant (bool): Whether the person is pregnant
        
    Returns:
        tuple: (bool, str) indicating anemia status and severity
    """
    if hemoglobin is None:
        return (False, "Unknown")
    
    if is_pregnant:
        if hemoglobin < 7:
            return (True, "Severe anemia")
        elif hemoglobin < 10:
            return (True, "Moderate anemia")
        elif hemoglobin < 11:
            return (True, "Mild anemia")
        else:
            return (False, "Normal")
    else:
        if hemoglobin < 8:
            return (True, "Severe anemia")
        elif hemoglobin < 11:
            return (True, "Moderate anemia")
        elif hemoglobin < 12:
            return (True, "Mild anemia")
        else:
            return (False, "Normal")

# Function to check if blood pressure is in normal range
def check_blood_pressure(systolic, diastolic):
    """
    Check if blood pressure is in normal range.
    
    Args:
        systolic (int): Systolic blood pressure
        diastolic (int): Diastolic blood pressure
        
    Returns:
        tuple: (bool, str) indicating if BP is normal and category
    """
    if systolic is None or diastolic is None:
        return (True, "Unknown")
    
    if systolic < 90 or diastolic < 60:
        return (False, "Low blood pressure")
    elif systolic < 120 and diastolic < 80:
        return (True, "Normal blood pressure")
    elif systolic < 130 and diastolic < 80:
        return (False, "Elevated blood pressure")
    elif (systolic < 140 and diastolic < 90) or (systolic >= 140 and diastolic < 90) or (systolic < 140 and diastolic >= 90):
        return (False, "Stage 1 hypertension")
    else:
        return (False, "Stage 2 hypertension")

# Function to save chat history
def save_chat_history(user_id, message, response):
    """
    Save chat history to session.
    
    Args:
        user_id (int): User ID
        message (str): User message
        response (str): Bot response
    """
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append({
        'user_id': user_id,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': message,
        'response': response
    })
    
    # Limit history to last 20 messages
    if len(session['chat_history']) > 20:
        session['chat_history'] = session['chat_history'][-20:]

# Function to get recommended government schemes based on user profile
def get_recommended_schemes(user_data):
    """
    Get recommended government schemes based on user profile.
    
    Args:
        user_data (dict): User profile data
        
    Returns:
        list: List of recommended scheme IDs
    """
    recommended_schemes = []
    
    # Pradhan Mantri Matru Vandana Yojana (PMMVY)
    if user_data.get('is_pregnant', False) and user_data.get('previous_pregnancies', 0) < 1:
        recommended_schemes.append(1)  # PMMVY ID is 1
    
    # Janani Suraksha Yojana (JSY)
    if user_data.get('is_pregnant', False) and user_data.get('is_bpl', False):
        recommended_schemes.append(2)  # JSY ID is 2
    
    # Ayushman Bharat
    if user_data.get('is_economically_vulnerable', False):
        recommended_schemes.append(3)  # Ayushman Bharat ID is 3
    
    return recommended_schemes

# Function to generate nutrition advice based on pregnancy stage
def get_nutrition_advice(pregnancy_week, hemoglobin_level=None):
    """
    Generate nutrition advice based on pregnancy stage and hemoglobin level.
    
    Args:
        pregnancy_week (int): Current pregnancy week
        hemoglobin_level (float, optional): Hemoglobin level
        
    Returns:
        dict: Nutrition advice
    """
    advice = {
        'foods_to_eat': [],
        'foods_to_avoid': [],
        'supplements': []
    }
    
    # Basic advice for all pregnancy stages
    advice['foods_to_avoid'] = [
        'Alcohol',
        'Raw or undercooked meat',
        'Unpasteurized dairy products',
        'High-mercury fish (shark, swordfish, king mackerel, tilefish)',
        'Raw eggs',
        'Excessive caffeine (limit to 200mg/day)',
        'Unwashed fruits and vegetables'
    ]
    
    advice['supplements'] = ['Folic acid (400-800 mcg daily)']
    
    # First trimester (weeks 1-12)
    if pregnancy_week is not None and pregnancy_week <= 12:
        advice['foods_to_eat'] = [
            'Folate-rich foods (leafy greens, citrus fruits, beans)',
            'Vitamin B6 foods to combat nausea (chicken, bananas, potatoes)',
            'Small, frequent meals to manage morning sickness',
            'Ginger tea or candies for nausea',
            'High-protein snacks',
            'Complex carbohydrates (whole grains)'
        ]
        advice['supplements'].append('Vitamin B6 (if experiencing severe nausea)')
    
    # Second trimester (weeks 13-27)
    elif pregnancy_week is not None and pregnancy_week <= 27:
        advice['foods_to_eat'] = [
            'Calcium-rich foods (dairy products, fortified plant milks, tofu)',
            'Vitamin D sources (fatty fish, egg yolks, fortified foods)',
            'Magnesium-rich foods (nuts, seeds, whole grains)',
            'Lean proteins (poultry, fish, legumes)',
            'Omega-3 fatty acids (salmon, walnuts, flaxseeds)'
        ]
        advice['supplements'].append('Calcium (1,000 mg daily)')
        advice['supplements'].append('Vitamin D (600 IU daily)')
    
    # Third trimester (weeks 28-40)
    elif pregnancy_week is not None:
        advice['foods_to_eat'] = [
            'Iron-rich foods (lean red meat, spinach, beans, fortified cereals)',
            'Vitamin C foods to enhance iron absorption (citrus fruits, bell peppers)',
            'Fiber-rich foods to combat constipation (whole grains, fruits, vegetables)',
            'Healthy fats (avocados, olive oil, nuts)',
            'Protein-rich foods (meat, poultry, fish, eggs, legumes)'
        ]
        advice['supplements'].append('Iron (27 mg daily)')
    
    # If anemic or at risk of anemia
    if hemoglobin_level is not None and hemoglobin_level < 11:
        advice['foods_to_eat'].extend([
            'High-iron foods (red meat, liver, lentils, spinach)',
            'Vitamin C with meals to enhance iron absorption',
            'Avoid tea and coffee with meals as they can inhibit iron absorption'
        ])
        advice['supplements'].append('Additional iron supplements as prescribed by healthcare provider')
    
    return advice
