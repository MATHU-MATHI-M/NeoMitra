import re
import random
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from translations import translate_text

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define topics and their keywords
topics = {
    'pregnancy_symptoms': ['morning sickness', 'nausea', 'fatigue', 'cramps', 'spotting', 'breast tenderness', 
                          'mood swings', 'heartburn', 'backache', 'headache', 'swelling'],
    'anemia': ['anemia', 'tired', 'weak', 'pale', 'dizzy', 'fainting', 'shortness of breath', 'iron', 
               'hemoglobin', 'blood test'],
    'high_risk_pregnancy': ['high risk', 'complication', 'diabetes', 'hypertension', 'preeclampsia', 
                           'multiple pregnancy', 'twins', 'previous cesarean', 'gestational diabetes'],
    'nutrition': ['diet', 'food', 'eat', 'nutrition', 'vitamin', 'folate', 'iron', 'calcium', 'protein', 
                 'meal', 'weight', 'healthy eating'],
    'government_schemes': ['scheme', 'government', 'benefit', 'financial', 'insurance', 'subsidy', 'aid', 
                          'assistance', 'support', 'program', 'PMMVY', 'JSY', 'Ayushman', 'Pradhan Mantri'],
    'hospital_visit': ['doctor', 'hospital', 'clinic', 'appointment', 'checkup', 'visit', 'test', 
                      'ultrasound', 'scan', 'examination'],
    'emergency': ['emergency', 'bleeding', 'pain', 'severe', 'contractions', 'water broke', 'fever', 
                 'swelling', 'blurred vision', 'headache', 'help'],
    'greetings': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 
                 'howdy', 'namaste', 'namaskar'],
    'farewell': ['bye', 'goodbye', 'see you', 'farewell', 'talk to you later', 'ttyl', 'cya']
}

# Responses for each topic
responses = {
    'pregnancy_symptoms': [
        "It's common to experience various symptoms during pregnancy. Which specific symptom are you concerned about?",
        "Pregnancy symptoms vary from person to person. What symptoms are you experiencing?",
        "Many pregnancy symptoms are normal, but it's always good to discuss them with your doctor. What are you experiencing?",
        "I can provide information on common pregnancy symptoms. Could you tell me more about what you're feeling?"
    ],
    'anemia': [
        "Anemia is common during pregnancy. Symptoms include fatigue, weakness, and pale skin. It's important to get your hemoglobin levels checked.",
        "If you're experiencing symptoms of anemia like fatigue or dizziness, please consult your doctor. They may recommend iron supplements.",
        "To prevent anemia, eat iron-rich foods like spinach, beans, and red meat, along with vitamin C foods to improve absorption.",
        "Regular blood tests are important to monitor hemoglobin levels during pregnancy. Have you had your levels checked recently?"
    ],
    'high_risk_pregnancy': [
        "High-risk pregnancies require special monitoring. It's crucial to attend all your doctor appointments.",
        "If you have conditions like diabetes or hypertension, your pregnancy might be considered high-risk. This means you'll need more frequent checkups.",
        "Being classified as high-risk doesn't necessarily mean you'll have complications. It just means you need closer monitoring.",
        "For high-risk pregnancies, it's important to follow your doctor's advice carefully and report any unusual symptoms immediately."
    ],
    'nutrition': [
        "A balanced diet during pregnancy should include fruits, vegetables, whole grains, lean proteins, and dairy products.",
        "It's important to take folic acid supplements before and during pregnancy to prevent neural tube defects.",
        "Iron-rich foods like spinach, beans, and fortified cereals can help prevent anemia during pregnancy.",
        "Stay hydrated by drinking plenty of water throughout the day. This helps prevent urinary tract infections and constipation."
    ],
    'government_schemes': [
        "There are several government schemes for pregnant women in India, such as Pradhan Mantri Matru Vandana Yojana (PMMVY) and Janani Suraksha Yojana (JSY).",
        "Ayushman Bharat provides health insurance coverage that can be beneficial during pregnancy and childbirth.",
        "Most government schemes require documents like Aadhaar card, bank account details, and proof of pregnancy. Have you registered for any schemes?",
        "Government schemes can provide financial assistance for prenatal care, institutional delivery, and postnatal care. Would you like information on how to apply?"
    ],
    'hospital_visit': [
        "Regular prenatal check-ups are essential. First trimester: monthly visits, second trimester: visits every 2-3 weeks, third trimester: weekly visits.",
        "During hospital visits, doctors will check your blood pressure, weight, baby's heartbeat, and may perform ultrasounds or other tests.",
        "Prepare questions for your doctor before each visit to make the most of your appointment time.",
        "Don't miss your scheduled appointments, they're crucial for monitoring both your health and your baby's development."
    ],
    'emergency': [
        "If you're experiencing severe abdominal pain, heavy bleeding, or decreased fetal movement, please seek emergency medical attention immediately.",
        "Symptoms like severe headache, vision changes, or sudden swelling could be signs of preeclampsia and require immediate medical attention.",
        "If your water breaks before 37 weeks, it could be preterm labor. Please go to the hospital right away.",
        "This sounds serious. Please call emergency services or go to the nearest emergency room immediately. Don't wait to seek help."
    ],
    'greetings': [
        "Hello! I'm the NeoMitra Assistant, here to help with information about pregnancy, anemia, and maternal health. How can I assist you today?",
        "Hi there! Welcome to NeoMitra. I can provide information on pregnancy care, government schemes, and health guidelines. What would you like to know?",
        "Namaste! I'm here to support you through your pregnancy journey. Feel free to ask me anything about maternal health.",
        "Greetings! How can I assist you with your pregnancy or maternal health concerns today?"
    ],
    'farewell': [
        "Goodbye! Take care of yourself and your baby. Feel free to chat again if you have more questions.",
        "Take care! Remember to attend your regular check-ups. I'm here if you need more information.",
        "Bye for now! Wishing you a healthy pregnancy journey. Don't hesitate to reach out again.",
        "See you later! Stay healthy and remember to follow your doctor's advice."
    ],
    'default': [
        "I'm not sure I understand. Could you please rephrase your question?",
        "I don't have information on that topic yet. Could you ask about pregnancy symptoms, anemia, nutrition, or government schemes?",
        "I'm still learning and don't have an answer for that. Could you ask something about pregnancy care or maternal health?",
        "I'm sorry, I didn't quite get that. I can help with questions about pregnancy, anemia, and maternal health. What would you like to know?"
    ]
}

# Function to preprocess the user message
def preprocess(message):
    # Convert to lowercase
    message = message.lower()
    # Tokenize
    tokens = word_tokenize(message)
    # Lemmatize
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

# Function to identify the topic of the user message
def identify_topic(tokens):
    for topic, keywords in topics.items():
        for keyword in keywords:
            # Check if any keyword appears in the message
            if any(keyword.lower() in ' '.join(tokens) for keyword in keywords):
                return topic
    return 'default'

# Function to check for emergency keywords
def is_emergency(message):
    emergency_keywords = [
        'bleeding', 'severe pain', 'contractions', 'water broke', 'can\'t feel baby', 
        'no movement', 'severe headache', 'blurred vision', 'swelling face', 'fever'
    ]
    
    # Check if any emergency keyword is in the message
    for keyword in emergency_keywords:
        if keyword.lower() in message.lower():
            return True
    return False

# Main function to get chatbot response
def get_chatbot_response(message, language='en'):
    # Check for emergencies first
    if is_emergency(message):
        response = random.choice(responses['emergency'])
        # Add emergency contact information
        response += " If this is a medical emergency, please call emergency services immediately."
        return translate_text(response, language)
    
    # Preprocess the message
    tokens = preprocess(message)
    
    # Identify the topic
    topic = identify_topic(tokens)
    
    # Select a random response from the identified topic
    response = random.choice(responses.get(topic, responses['default']))
    
    # Translate the response if needed
    if language != 'en':
        response = translate_text(response, language)
    
    return response
