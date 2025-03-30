from flask_babel import _
import json
import os

# Dictionary to store translations
# In a real application, this would be integrated with a proper translation service
# or use a library like Flask-Babel with .po files
translations = {
    "hi": {  # Hindi
        "Hello! I'm the NeoMitra Assistant": "नमस्ते! मैं नियोमित्र सहायक हूँ",
        "High-risk pregnancies require special monitoring": "उच्च जोखिम वाले गर्भावस्था के लिए विशेष निगरानी की आवश्यकता होती है",
        "Anemia is common during pregnancy": "गर्भावस्था के दौरान एनीमिया आम है",
        "A balanced diet during pregnancy": "गर्भावस्था के दौरान संतुलित आहार",
        "Regular prenatal check-ups are essential": "नियमित प्रसव पूर्व जांच आवश्यक है",
        "If you're experiencing severe abdominal pain": "यदि आप गंभीर पेट दर्द का अनुभव कर रहे हैं",
        "Goodbye! Take care of yourself": "अलविदा! अपना ख्याल रखें",
        # Add more translations as needed
    },
    "ta": {  # Tamil
        "Hello! I'm the NeoMitra Assistant": "வணக்கம்! நான் நியோமித்ரா உதவியாளர்",
        "High-risk pregnancies require special monitoring": "அதிக ஆபத்துள்ள கர்ப்பங்களுக்கு சிறப்பு கண்காணிப்பு தேவை",
        "Anemia is common during pregnancy": "கர்ப்பத்தின் போது இரத்த சோகை பொதுவானது",
        "A balanced diet during pregnancy": "கர்ப்பத்தின் போது சமநிலை உணவு",
        "Regular prenatal check-ups are essential": "வழக்கமான கர்ப்பகால பரிசோதனைகள் அவசியம்",
        "If you're experiencing severe abdominal pain": "நீங்கள் கடுமையான வயிற்று வலி அனுபவித்தால்",
        "Goodbye! Take care of yourself": "பிரியாவிடை! உங்களை கவனித்துக்கொள்ளுங்கள்",
        # Add more translations as needed
    },
    "te": {  # Telugu
        "Hello! I'm the NeoMitra Assistant": "హలో! నేను నియోమిత్ర సహాయకుడిని",
        "High-risk pregnancies require special monitoring": "అధిక ప్రమాదం ఉన్న గర్భధారణలకు ప్రత్యేక పర్యవేక్షణ అవసరం",
        "Anemia is common during pregnancy": "గర్భధారణ సమయంలో రక్తహీనత సాధారణం",
        "A balanced diet during pregnancy": "గర్భధారణ సమయంలో సమతుల్య ఆహారం",
        "Regular prenatal check-ups are essential": "క్రమం తప్పకుండా ప్రసవ పూర్వ తనిఖీలు అవసరం",
        "If you're experiencing severe abdominal pain": "మీరు తీవ్రమైన కడుపు నొప్పిని అనుభవిస్తున్నట్లయితే",
        "Goodbye! Take care of yourself": "వీడ్కోలు! మిమ్మల్ని మీరు జాగ్రత్తగా చూసుకోండి",
        # Add more translations as needed
    },
    "bn": {  # Bengali
        "Hello! I'm the NeoMitra Assistant": "হ্যালো! আমি নিওমিত্র সহকারী",
        "High-risk pregnancies require special monitoring": "উচ্চ ঝুঁকিপূর্ণ গর্ভাবস্থার জন্য বিশেষ নজরদারি প্রয়োজন",
        "Anemia is common during pregnancy": "গর্ভাবস্থায় অ্যানিমিয়া সাধারণ",
        "A balanced diet during pregnancy": "গর্ভাবস্থায় সুষম খাবার",
        "Regular prenatal check-ups are essential": "নিয়মিত প্রসবপূর্ব পরীক্ষা অপরিহার্য",
        "If you're experiencing severe abdominal pain": "আপনি যদি তীব্র পেটে ব্যথা অনুভব করেন",
        "Goodbye! Take care of yourself": "বিদায়! নিজের যত্ন নিন",
        # Add more translations as needed
    },
    "mr": {  # Marathi
        "Hello! I'm the NeoMitra Assistant": "नमस्कार! मी निओमित्र मदतनीस आहे",
        "High-risk pregnancies require special monitoring": "उच्च जोखीमीच्या गर्भधारणेसाठी विशेष देखरेख आवश्यक आहे",
        "Anemia is common during pregnancy": "गर्भधारणेदरम्यान अॅनिमिया सामान्य आहे",
        "A balanced diet during pregnancy": "गर्भधारणेदरम्यान संतुलित आहार",
        "Regular prenatal check-ups are essential": "नियमित प्रसवपूर्व तपासण्या आवश्यक आहेत",
        "If you're experiencing severe abdominal pain": "तुम्हाला पोटात तीव्र वेदना होत असल्यास",
        "Goodbye! Take care of yourself": "निरोप! स्वतःची काळजी घ्या",
        # Add more translations as needed
    }
}

def translate_text(text, target_language):
    """
    Translates text to the target language using the predefined translations dictionary.
    Falls back to original text if translation is not available.
    
    Args:
        text (str): Text to translate
        target_language (str): Language code to translate to
        
    Returns:
        str: Translated text or original if translation not available
    """
    if target_language == 'en':
        return text
    
    # Try to find a matching translation
    if target_language in translations:
        for english_text, translated_text in translations[target_language].items():
            if english_text in text:
                # Replace the English part with the translation
                return text.replace(english_text, translated_text)
    
    # If no direct match, return the original text
    return text
