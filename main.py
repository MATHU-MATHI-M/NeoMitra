import os
import re
import logging
from flask import Flask, send_from_directory, jsonify, render_template_string, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "neomitra-secret-key")

# Mock user database for demo purposes
users = {}

# Health check endpoint
@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "NeoMitra API is running"})

# Chatbot endpoint
@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    data = request.json
    user_message = data.get('message', '')
    
    # Simple chatbot logic
    if 'pregnancy' in user_message.lower():
        response = "Pregnancy care is essential. Make sure to have regular check-ups and follow your doctor's advice on nutrition and supplements."
    elif 'anemia' in user_message.lower():
        response = "Anemia can affect both men and women. Ensure you're getting enough iron in your diet through foods like spinach, beans, and lean meats."
    elif 'diabetes' in user_message.lower():
        response = "Managing diabetes involves regular blood sugar monitoring, healthy eating, and regular exercise. Consult your healthcare provider for a personalized plan."
    elif 'diet' in user_message.lower() or 'nutrition' in user_message.lower():
        response = "A balanced diet rich in vegetables, fruits, whole grains, and lean proteins supports overall health. Consider consulting with a nutritionist for personalized advice."
    else:
        response = "Hello! I'm NeoMitra Assistant. I can help you with health questions related to pregnancy, anemia, diabetes, and general health. Just ask me anything!"
    
    return jsonify({
        "response": response,
        "status": "success"
    })

# Voice processing endpoint
@app.route('/api/voice/process', methods=['POST'])
def process_voice_input():
    """
    Process voice transcripts and extract health data using NLP
    """
    data = request.json
    
    if not data or 'transcript' not in data:
        return jsonify({"error": "No transcript provided"}), 400
    
    transcript = data.get('transcript', '')
    user_language = data.get('language', 'en')
    
    # Log the transcript for debugging
    app.logger.info(f"Processing voice transcript: {transcript}")
    
    # Process the transcript to extract health data
    # In a real application, we would use a more sophisticated NLP model
    # Here we're using simple pattern matching for demonstration
    
    extracted_data = {}
    
    # Extract weight information (e.g., "my weight is 70 kg")
    weight_regex = r"weight\s+(?:is|of)\s+(\d+\.?\d*)\s*(?:kg|kilograms)"
    weight_match = re.search(weight_regex, transcript, re.IGNORECASE)
    if weight_match:
        extracted_data['weight'] = float(weight_match.group(1))
    
    # Extract height information (e.g., "my height is 175 cm")
    height_regex = r"height\s+(?:is|of)\s+(\d+\.?\d*)\s*(?:cm|centimeters)"
    height_match = re.search(height_regex, transcript, re.IGNORECASE)
    if height_match:
        extracted_data['height'] = float(height_match.group(1))
    
    # Extract blood pressure (e.g., "my blood pressure is 120 over 80")
    bp_regex = r"blood\s+pressure\s+(?:is|of)\s+(\d+)\s+(?:over|by)\s+(\d+)"
    bp_match = re.search(bp_regex, transcript, re.IGNORECASE)
    if bp_match:
        extracted_data['blood_pressure_systolic'] = int(bp_match.group(1))
        extracted_data['blood_pressure_diastolic'] = int(bp_match.group(2))
    
    # Extract blood sugar (e.g., "my blood sugar is 95 mg/dl")
    bs_regex = r"blood\s+sugar\s+(?:is|of)\s+(\d+\.?\d*)\s*(?:mg\/dl)"
    bs_match = re.search(bs_regex, transcript, re.IGNORECASE)
    if bs_match:
        extracted_data['blood_sugar'] = float(bs_match.group(1))
    
    # Extract hemoglobin (e.g., "my hemoglobin is 14.5 g/dl")
    hb_regex = r"hemoglobin\s+(?:is|of)\s+(\d+\.?\d*)\s*(?:g\/dl)"
    hb_match = re.search(hb_regex, transcript, re.IGNORECASE)
    if hb_match:
        extracted_data['hemoglobin'] = float(hb_match.group(1))
    
    # Extract pregnancy status (e.g., "I am pregnant" or "I am not pregnant")
    if re.search(r'\b(?:I\s+am|I\'m)\s+pregnant\b', transcript, re.IGNORECASE):
        extracted_data['is_pregnant'] = True
    elif re.search(r'\b(?:I\s+am|I\'m)\s+not\s+pregnant\b', transcript, re.IGNORECASE):
        extracted_data['is_pregnant'] = False
    
    # Extract pregnancy week (e.g., "I am 20 weeks pregnant")
    preg_week_regex = r"(\d+)\s+weeks?\s+pregnant"
    preg_week_match = re.search(preg_week_regex, transcript, re.IGNORECASE)
    if preg_week_match:
        extracted_data['pregnancy_week'] = int(preg_week_match.group(1))
    
    # Extract symptoms or health concerns
    symptoms = []
    common_symptoms = [
        "fever", "headache", "nausea", "vomiting", "dizziness", 
        "fatigue", "pain", "cramps", "swelling", "bleeding"
    ]
    
    for symptom in common_symptoms:
        if re.search(rf'\b{symptom}\b', transcript, re.IGNORECASE):
            symptoms.append(symptom)
    
    if symptoms:
        extracted_data['symptoms'] = symptoms
    
    # Generate a response based on the extracted data
    if extracted_data:
        response = "I've extracted the following health information from your speech:\n"
        for key, value in extracted_data.items():
            response += f"- {key.replace('_', ' ').capitalize()}: {value}\n"
        
        # Add a suggestion for what to do next
        response += "\nWould you like me to save this information to your health records?"
    else:
        response = "I couldn't extract any specific health information from your speech. Please try again with more details about your health metrics like weight, height, blood pressure, etc."
    
    return jsonify({
        "success": True,
        "transcript": transcript,
        "extracted_data": extracted_data,
        "response": response
    })

# Register page as the first page
@app.route('/')
def index():
    # Redirect to register page
    return redirect('/register')

# Home page with gradient background like in the provided screenshot  
@app.route('/home')
def home():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
        
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NeoMitra - Maternal Healthcare Platform</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                color: #333;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .navbar {
                background-color: rgba(255, 255, 255, 0.95);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 0.8rem 1rem;
            }
            
            .navbar-brand {
                display: flex;
                align-items: center;
                font-weight: 700;
                color: var(--primary-color);
                font-size: 1.5rem;
            }
            
            .navbar-brand i {
                margin-right: 0.5rem;
                font-size: 1.8rem;
            }
            
            .nav-link {
                color: #495057;
                font-weight: 500;
                padding: 0.5rem 1rem;
                transition: color 0.3s;
                position: relative;
            }
            
            .nav-link:hover {
                color: var(--primary-color);
            }
            
            .nav-link.active {
                color: var(--primary-color);
            }
            
            .hero-section {
                position: relative;
                height: 80vh;
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: white;
                overflow: hidden;
            }
            
            .hero-content {
                z-index: 2;
                max-width: 800px;
                padding: 2rem;
            }
            
            .hero-title {
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            
            .hero-subtitle {
                font-size: 1.5rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }
            
            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
                padding: 0.8rem 2rem;
                font-weight: 600;
                border-radius: 50px;
                transition: all 0.3s;
            }
            
            .btn-primary:hover {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            .btn-outline-light {
                padding: 0.8rem 2rem;
                font-weight: 600;
                border-radius: 50px;
                transition: all 0.3s;
            }
            
            .btn-outline-light:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            
            .wave-bottom {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 100px;
                background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="1" d="M0,96L80,112C160,128,320,160,480,160C640,160,800,128,960,128C1120,128,1280,160,1360,176L1440,192L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,160,320,80,320L0,320Z"></path></svg>') no-repeat;
                background-size: 100% 100%;
            }
            
            .features-section {
                padding: 5rem 0;
                background-color: white;
            }
            
            .section-title {
                text-align: center;
                margin-bottom: 3rem;
                color: var(--primary-color);
                font-weight: 700;
            }
            
            .feature-card {
                background-color: white;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                padding: 2rem;
                height: 100%;
                transition: var(--transition);
                border: none;
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            
            .feature-icon {
                font-size: 2.5rem;
                color: var(--primary-color);
                margin-bottom: 1.5rem;
            }
            
            .feature-title {
                font-weight: 600;
                margin-bottom: 1rem;
                color: var(--dark-color);
            }
            
            .feature-text {
                color: #6c757d;
            }
            
            footer {
                background-color: var(--dark-color);
                color: var(--light-color);
                padding: 3rem 0 2rem;
                margin-top: auto;
            }
            
            .footer-title {
                font-weight: 700;
                margin-bottom: 1.5rem;
                color: var(--primary-color);
            }
            
            .footer-links {
                list-style: none;
                padding: 0;
            }
            
            .footer-links li {
                margin-bottom: 0.8rem;
            }
            
            .footer-links a {
                color: #adb5bd;
                text-decoration: none;
                transition: color 0.3s;
            }
            
            .footer-links a:hover {
                color: var(--light-color);
            }
            
            .social-icons {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }
            
            .social-icon {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: rgba(255, 255, 255, 0.1);
                color: var(--light-color);
                transition: var(--transition);
            }
            
            .social-icon:hover {
                background-color: var(--primary-color);
                transform: translateY(-3px);
            }
            
            .copyright {
                text-align: center;
                padding-top: 2rem;
                margin-top: 2rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: #adb5bd;
            }
            
            /* Chatbot assistant button */
            .chatbot-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: var(--primary-color);
                color: white;
                border-radius: 50px;
                padding: 0.8rem 1.5rem;
                display: flex;
                align-items: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s;
            }
            
            .chatbot-button:hover {
                background-color: var(--secondary-color);
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
            }
            
            .chatbot-icon {
                margin-right: 0.5rem;
            }
            
            /* Auth buttons */
            .auth-buttons .btn {
                min-width: 100px;
                margin-left: 0.5rem;
            }
            
            /* Responsive adjustments */
            @media (max-width: 992px) {
                .hero-title {
                    font-size: 2.5rem;
                }
                
                .hero-subtitle {
                    font-size: 1.2rem;
                }
                
                .hero-section {
                    height: 70vh;
                }
            }
            
            @media (max-width: 768px) {
                .hero-section {
                    height: 60vh;
                }
                
                .hero-buttons .btn {
                    display: block;
                    width: 100%;
                    margin-bottom: 1rem;
                }
                
                .feature-card {
                    margin-bottom: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link active" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Resources</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Assistant</a>
                        </li>
                    </ul>
                    <div class="auth-buttons">
                        <a href="/login" class="btn btn-outline-primary">Login</a>
                        <a href="/register" class="btn btn-primary">Register</a>
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Empowering Complete Health</h1>
                <p class="hero-subtitle">A comprehensive healthcare platform for everyone, offering personalized monitoring and recommendations for conditions like anemia, diabetes, and pregnancy with accessibility in multiple languages.</p>
                <div class="hero-buttons">
                    <a href="/dashboard" class="btn btn-primary me-3">Get Started</a>
                    <a href="#features" class="btn btn-outline-light">Learn More</a>
                </div>
            </div>
            <div class="wave-bottom"></div>
        </section>
        
        <!-- Features Section -->
        <section id="features" class="features-section">
            <div class="container">
                <h2 class="section-title">Our Features</h2>
                <div class="row">
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-clipboard2-pulse"></i>
                            </div>
                            <h3 class="feature-title">Health Tracking</h3>
                            <p class="feature-text">Easily record and monitor vital health metrics for everyone, including specialized tracking for pregnancy, anemia, and diabetes.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-shield-check"></i>
                            </div>
                            <h3 class="feature-title">Risk Assessment</h3>
                            <p class="feature-text">AI-powered risk assessment for health conditions including anemia and diabetes for all users, with additional pregnancy monitoring for women.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-chat-dots"></i>
                            </div>
                            <h3 class="feature-title">Chatbot Assistant</h3>
                            <p class="feature-text">Get immediate answers to all your health questions about anemia, diabetes, and pregnancy in your preferred language.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-bank"></i>
                            </div>
                            <h3 class="feature-title">Government Schemes</h3>
                            <p class="feature-text">Stay informed about government healthcare schemes for all health conditions including diabetes, anemia, and pregnancy care.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer>
            <div class="container">
                <div class="row">
                    <div class="col-md-4">
                        <h4 class="footer-title">NeoMitra</h4>
                        <p>A comprehensive healthcare platform for everyone, offering personalized health tracking, risk assessments, and recommendations for conditions like anemia, diabetes, and pregnancy care, especially designed for rural areas with limited healthcare access.</p>
                        <div class="social-icons">
                            <a href="#" class="social-icon"><i class="bi bi-facebook"></i></a>
                            <a href="#" class="social-icon"><i class="bi bi-twitter"></i></a>
                            <a href="#" class="social-icon"><i class="bi bi-instagram"></i></a>
                            <a href="#" class="social-icon"><i class="bi bi-linkedin"></i></a>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <h4 class="footer-title">Links</h4>
                        <ul class="footer-links">
                            <li><a href="/">Home</a></li>
                            <li><a href="#">About Us</a></li>
                            <li><a href="#">Services</a></li>
                            <li><a href="#">Contact</a></li>
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h4 class="footer-title">Resources</h4>
                        <ul class="footer-links">
                            <li><a href="#">Health Guidelines</a></li>
                            <li><a href="#">Nutritional Advice</a></li>
                            <li><a href="#">Government Schemes</a></li>
                            <li><a href="#">FAQ</a></li>
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h4 class="footer-title">Contact Us</h4>
                        <ul class="footer-links">
                            <li><i class="bi bi-geo-alt me-2"></i> 123 Healthcare St, Medical City</li>
                            <li><i class="bi bi-envelope me-2"></i> info@neomitra.com</li>
                            <li><i class="bi bi-telephone me-2"></i> +91 1234567890</li>
                        </ul>
                    </div>
                </div>
                <div class="copyright">
                    <p>&copy; 2025 NeoMitra. All rights reserved.</p>
                </div>
            </div>
        </footer>
        
        <!-- Chatbot Assistant Button -->
        <div class="chatbot-button">
            <i class="bi bi-chat-dots-fill chatbot-icon"></i>
            NeoMitra Assistant
        </div>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = 'remember_me' in request.form
        
        # Input validation
        if not email or not password:
            error = "Please provide both email and password."
        else:
            # Check if user exists and password is correct
            if email in users and check_password_hash(users[email]['password_hash'], password):
                # Store user info in session
                session['logged_in'] = True
                session['user_email'] = email
                session['username'] = users[email]['username']
                
                # Redirect to dashboard on successful login
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid email or password. Please try again."
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - NeoMitra</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .login-container {
                width: 100%;
                max-width: 450px;
                padding: 2rem;
            }
            
            .login-card {
                background-color: white;
                border-radius: var(--border-radius);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                padding: 2.5rem;
                border: none;
            }
            
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .brand-logo {
                display: flex;
                justify-content: center;
                margin-bottom: 1rem;
            }
            
            .brand-logo i {
                font-size: 3rem;
                color: var(--primary-color);
            }
            
            .login-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--dark-color);
                margin-bottom: 0.5rem;
            }
            
            .login-subtitle {
                color: #6c757d;
                margin-bottom: 0;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-label {
                font-weight: 600;
                color: var(--dark-color);
                margin-bottom: 0.5rem;
            }
            
            .form-control {
                padding: 0.8rem 1rem;
                border-radius: var(--border-radius);
                border: 1px solid #ced4da;
                transition: var(--transition);
            }
            
            .form-control:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 0.25rem rgba(121, 82, 179, 0.25);
            }
            
            .form-check-label {
                color: #6c757d;
            }
            
            .forgot-password {
                color: var(--primary-color);
                text-decoration: none;
                font-weight: 500;
                transition: var(--transition);
            }
            
            .forgot-password:hover {
                color: var(--secondary-color);
                text-decoration: underline;
            }
            
            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
                padding: 0.8rem 2rem;
                font-weight: 600;
                border-radius: 50px;
                transition: all 0.3s;
                width: 100%;
                margin-top: 1rem;
            }
            
            .btn-primary:hover {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            .login-footer {
                text-align: center;
                margin-top: 1.5rem;
                color: #6c757d;
            }
            
            .login-footer a {
                color: var(--primary-color);
                text-decoration: none;
                font-weight: 600;
                transition: var(--transition);
            }
            
            .login-footer a:hover {
                color: var(--secondary-color);
                text-decoration: underline;
            }
            
            .home-link {
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                text-decoration: none;
                margin-top: 2rem;
                transition: var(--transition);
            }
            
            .home-link:hover {
                transform: translateX(-5px);
                color: white;
            }
            
            .home-link i {
                margin-right: 0.5rem;
            }
            
            .alert {
                border-radius: var(--border-radius);
                margin-bottom: 1.5rem;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-card">
                <div class="login-header">
                    <div class="brand-logo">
                        <i class="bi bi-heart-pulse-fill"></i>
                    </div>
                    <h1 class="login-title">Welcome Back</h1>
                    <p class="login-subtitle">Log in to access your NeoMitra account</p>
                </div>
                
                {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
                {% endif %}
                
                <form action="/login" method="post">
                    <div class="form-group">
                        <label for="email" class="form-label">Email Address</label>
                        <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                    </div>
                    
                    <div class="form-group">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <label for="password" class="form-label mb-0">Password</label>
                            <a href="#" class="forgot-password">Forgot Password?</a>
                        </div>
                        <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password" required>
                    </div>
                    
                    <div class="form-check mb-3">
                        <input type="checkbox" class="form-check-input" id="rememberMe" name="remember_me">
                        <label class="form-check-label" for="rememberMe">Remember me</label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Log In</button>
                </form>
                
                <div class="login-footer">
                    <p>Don't have an account? <a href="/register">Register Now</a></p>
                </div>
            </div>
            
            <a href="/" class="home-link">
                <i class="bi bi-arrow-left"></i> Back to Home
            </a>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone_number = request.form.get('phone_number')
        date_of_birth = request.form.get('date_of_birth')
        preferred_language = request.form.get('preferred_language')
        
        # Basic validation
        if not all([first_name, last_name, username, email, password, confirm_password, phone_number, date_of_birth]):
            error = "All fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif len(password) < 8:
            error = "Password must be at least 8 characters long."
        elif email in users:
            error = "Email already registered. Please use a different email."
        else:
            # Create new user
            users[email] = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password_hash': generate_password_hash(password),
                'phone_number': phone_number,
                'date_of_birth': date_of_birth,
                'preferred_language': preferred_language
            }
            
            # Log the user in
            session['logged_in'] = True
            session['user_email'] = email
            session['username'] = username
            
            # Redirect to dashboard
            return redirect(url_for('dashboard'))
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register - NeoMitra</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem 0;
            }
            
            .register-container {
                width: 100%;
                max-width: 700px;
                padding: 2rem;
            }
            
            .register-card {
                background-color: white;
                border-radius: var(--border-radius);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                padding: 2.5rem;
                border: none;
            }
            
            .register-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .brand-logo {
                display: flex;
                justify-content: center;
                margin-bottom: 1rem;
            }
            
            .brand-logo i {
                font-size: 3rem;
                color: var(--primary-color);
            }
            
            .register-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--dark-color);
                margin-bottom: 0.5rem;
            }
            
            .register-subtitle {
                color: #6c757d;
                margin-bottom: 0;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-label {
                font-weight: 600;
                color: var(--dark-color);
                margin-bottom: 0.5rem;
            }
            
            .form-control {
                padding: 0.8rem 1rem;
                border-radius: var(--border-radius);
                border: 1px solid #ced4da;
                transition: var(--transition);
            }
            
            .form-control:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 0.25rem rgba(121, 82, 179, 0.25);
            }
            
            .form-select {
                padding: 0.8rem 1rem;
                border-radius: var(--border-radius);
                border: 1px solid #ced4da;
                transition: var(--transition);
            }
            
            .form-select:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 0.25rem rgba(121, 82, 179, 0.25);
            }
            
            .form-check {
                margin-top: 1rem;
            }
            
            .form-check-label {
                color: #6c757d;
            }
            
            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
                padding: 0.8rem 2rem;
                font-weight: 600;
                border-radius: 50px;
                transition: all 0.3s;
                width: 100%;
                margin-top: 1rem;
            }
            
            .btn-primary:hover {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            .register-footer {
                text-align: center;
                margin-top: 1.5rem;
                color: #6c757d;
            }
            
            .register-footer a {
                color: var(--primary-color);
                text-decoration: none;
                font-weight: 600;
                transition: var(--transition);
            }
            
            .register-footer a:hover {
                color: var(--secondary-color);
                text-decoration: underline;
            }
            
            .home-link {
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                text-decoration: none;
                margin-top: 2rem;
                transition: var(--transition);
            }
            
            .home-link:hover {
                transform: translateX(-5px);
                color: white;
            }
            
            .home-link i {
                margin-right: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="register-container">
            <div class="register-card">
                <div class="register-header">
                    <div class="brand-logo">
                        <i class="bi bi-heart-pulse-fill"></i>
                    </div>
                    <h1 class="register-title">Create Your Account</h1>
                    <p class="register-subtitle">Join NeoMitra for personalized maternal healthcare</p>
                </div>
                
                {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
                {% endif %}
                
                <form action="/register" method="post">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="firstName" class="form-label">First Name</label>
                                <input type="text" class="form-control" id="firstName" name="first_name" placeholder="Enter your first name" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="lastName" class="form-label">Last Name</label>
                                <input type="text" class="form-control" id="lastName" name="last_name" placeholder="Enter your last name" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" class="form-control" id="username" name="username" placeholder="Choose a username" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="email" class="form-label">Email Address</label>
                                <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" name="password" placeholder="Create a password" required>
                                <small class="text-muted">Must be at least 8 characters long</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="confirmPassword" class="form-label">Confirm Password</label>
                                <input type="password" class="form-control" id="confirmPassword" name="confirm_password" placeholder="Confirm your password" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="phoneNumber" class="form-label">Phone Number</label>
                                <input type="tel" class="form-control" id="phoneNumber" name="phone_number" placeholder="Enter your phone number" required>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label for="dateOfBirth" class="form-label">Date of Birth</label>
                                <input type="date" class="form-control" id="dateOfBirth" name="date_of_birth" required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="preferredLanguage" class="form-label">Preferred Language</label>
                        <select class="form-select" id="preferredLanguage" name="preferred_language" required>
                            <option value="en">English</option>
                            <option value="hi">Hindi</option>
                            <option value="ta">Tamil</option>
                            <option value="te">Telugu</option>
                            <option value="bn">Bengali</option>
                            <option value="mr">Marathi</option>
                        </select>
                    </div>
                    
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="termsAgree" name="terms_agree" required>
                        <label class="form-check-label" for="termsAgree">
                            I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
                        </label>
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Register</button>
                </form>
                
                <div class="register-footer">
                    <p>Already have an account? <a href="/login">Login</a></p>
                </div>
            </div>
            
            <a href="/" class="home-link">
                <i class="bi bi-arrow-left"></i> Back to Home
            </a>
        </div>
    </body>
    </html>
    """)

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Get user data from session
    email = session.get('user_email')
    username = session.get('username')
    user_data = users.get(email, {})
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - NeoMitra</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --success-color: #28a745;
                --warning-color: #ffc107;
                --danger-color: #dc3545;
                --info-color: #17a2b8;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                background-color: #f8f9fa;
                color: #333;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .navbar {
                background-color: white;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .navbar-brand {
                display: flex;
                align-items: center;
                font-weight: 700;
                color: var(--primary-color);
                font-size: 1.5rem;
            }
            
            .navbar-brand i {
                margin-right: 0.5rem;
                font-size: 1.8rem;
            }
            
            .main-content {
                flex: 1;
                padding: 2rem 0;
            }
            
            .dashboard-header {
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                color: white;
                padding: 2rem 0;
                margin-bottom: 2rem;
                border-radius: var(--border-radius);
            }
            
            .welcome-message {
                font-size: 2.2rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }
            
            .welcome-subtitle {
                font-size: 1.1rem;
                opacity: 0.9;
            }
            
            .card {
                border: none;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                margin-bottom: 1.5rem;
                transition: var(--transition);
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            
            .card-header {
                padding: 1.2rem 1.5rem;
                background-color: white;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .card-header i {
                font-size: 1.3rem;
                color: var(--primary-color);
                margin-right: 0.8rem;
            }
            
            .card-title {
                display: flex;
                align-items: center;
                margin: 0;
            }
            
            .card-body {
                padding: 1.5rem;
            }
            
            .health-metrics-card .card-body {
                padding: 0;
            }
            
            .metric {
                padding: 1.2rem 1.5rem;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .metric:last-child {
                border-bottom: none;
            }
            
            .metric-label {
                font-weight: 500;
                color: #495057;
            }
            
            .metric-value {
                font-weight: 600;
                color: var(--dark-color);
            }
            
            .metric-value.good {
                color: var(--success-color);
            }
            
            .metric-value.warning {
                color: var(--warning-color);
            }
            
            .metric-value.danger {
                color: var(--danger-color);
            }
            
            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
            }
            
            .btn-primary:hover {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
            }
            
            .upcoming-appointment {
                background-color: rgba(121, 82, 179, 0.05);
                border-radius: var(--border-radius);
                padding: 1.2rem;
                margin-bottom: 1rem;
                border-left: 4px solid var(--primary-color);
            }
            
            .appointment-date {
                font-weight: 600;
                color: var(--primary-color);
                margin-bottom: 0.5rem;
            }
            
            .footer {
                background-color: white;
                padding: 1.5rem 0;
                margin-top: 2rem;
                box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .nav-tabs .nav-link {
                color: #495057;
                font-weight: 500;
            }
            
            .nav-tabs .nav-link.active {
                color: var(--primary-color);
                font-weight: 600;
                border-color: rgba(121, 82, 179, 0.5);
                border-bottom-color: transparent;
            }
            
            .health-tip {
                background-color: rgba(23, 162, 184, 0.1);
                border-radius: var(--border-radius);
                padding: 1.2rem;
                margin-bottom: 1rem;
                border-left: 4px solid var(--info-color);
            }
            
            .health-tip-title {
                font-weight: 600;
                color: var(--info-color);
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
            }
            
            .health-tip-title i {
                margin-right: 0.5rem;
            }
            
            .progress {
                height: 0.8rem;
                border-radius: 1rem;
                margin-top: 0.5rem;
            }
            
            .risk-low {
                background-color: var(--success-color);
            }
            
            .risk-moderate {
                background-color: var(--warning-color);
            }
            
            .risk-high {
                background-color: var(--danger-color);
            }
            
            .quick-action {
                display: flex;
                align-items: center;
                padding: 1rem;
                border-radius: var(--border-radius);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                background-color: white;
                margin-bottom: 1rem;
                transition: var(--transition);
                text-decoration: none;
                color: var(--dark-color);
            }
            
            .quick-action:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                color: var(--primary-color);
            }
            
            .quick-action i {
                font-size: 1.5rem;
                margin-right: 1rem;
                color: var(--primary-color);
            }
            
            .quick-action-title {
                font-weight: 600;
                margin-bottom: 0.2rem;
            }
            
            .quick-action-description {
                font-size: 0.9rem;
                color: #6c757d;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Health Records</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/chatbot">Health Assistant</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Resources</a>
                        </li>
                    </ul>
                    <div class="d-flex align-items-center">
                        <div class="dropdown">
                            <a class="d-flex align-items-center text-decoration-none dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <div class="d-flex align-items-center justify-content-center rounded-circle bg-primary text-white" style="width: 35px; height: 35px; margin-right: 0.5rem;">
                                    {{ username[0].upper() }}
                                </div>
                                <span class="d-none d-sm-inline-block">{{ username }}</span>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                <li><a class="dropdown-item" href="#"><i class="bi bi-person me-2"></i>Profile</a></li>
                                <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i>Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Main Content -->
        <div class="main-content">
            <div class="container">
                <!-- Dashboard Header -->
                <div class="dashboard-header p-4">
                    <div class="container">
                        <h1 class="welcome-message">Welcome, {{ user_data.get('first_name', username) }}!</h1>
                        <p class="welcome-subtitle">Track your health metrics, manage your records, and get personalized recommendations.</p>
                    </div>
                </div>
                
                <!-- Dashboard Content -->
                <div class="row">
                    <!-- Left Column -->
                    <div class="col-lg-8">
                        <!-- Health Metrics -->
                        <div class="card health-metrics-card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-activity"></i>
                                    Health Metrics
                                </h5>
                                <a href="#" class="btn btn-sm btn-outline-primary">Update</a>
                            </div>
                            <div class="card-body">
                                <div class="metric">
                                    <div class="metric-label">Weight</div>
                                    <div class="metric-value">65 kg</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Blood Pressure</div>
                                    <div class="metric-value">120/80 mmHg</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Blood Sugar (Fasting)</div>
                                    <div class="metric-value">98 mg/dL</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Hemoglobin</div>
                                    <div class="metric-value warning">11.2 g/dL</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">BMI</div>
                                    <div class="metric-value">22.5</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Risk Assessment -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-shield-check"></i>
                                    Health Risk Assessment
                                </h5>
                                <a href="#" class="btn btn-sm btn-outline-primary">Details</a>
                            </div>
                            <div class="card-body">
                                <div class="mb-4">
                                    <div class="d-flex justify-content-between mb-2">
                                        <strong>Anemia Risk</strong>
                                        <span class="text-warning">Moderate (45%)</span>
                                    </div>
                                    <div class="progress">
                                        <div class="progress-bar risk-moderate" role="progressbar" style="width: 45%" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                    <p class="text-muted mt-2 small">Based on your hemoglobin levels and other factors</p>
                                </div>
                                
                                <div class="mb-4">
                                    <div class="d-flex justify-content-between mb-2">
                                        <strong>Diabetes Risk</strong>
                                        <span class="text-success">Low (15%)</span>
                                    </div>
                                    <div class="progress">
                                        <div class="progress-bar risk-low" role="progressbar" style="width: 15%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                    <p class="text-muted mt-2 small">Based on your blood sugar levels, BMI, and family history</p>
                                </div>
                                
                                <div class="mb-4">
                                    <div class="d-flex justify-content-between mb-2">
                                        <strong>Hypertension Risk</strong>
                                        <span class="text-success">Low (10%)</span>
                                    </div>
                                    <div class="progress">
                                        <div class="progress-bar risk-low" role="progressbar" style="width: 10%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                                    </div>
                                    <p class="text-muted mt-2 small">Based on your blood pressure readings and lifestyle factors</p>
                                </div>
                                
                                <a href="#" class="btn btn-primary">Take Full Assessment</a>
                            </div>
                        </div>
                        
                        <!-- Recommendations -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-lightbulb"></i>
                                    Personalized Recommendations
                                </h5>
                            </div>
                            <div class="card-body">
                                <div class="health-tip mb-3">
                                    <div class="health-tip-title">
                                        <i class="bi bi-droplet"></i> Addressing Low Hemoglobin
                                    </div>
                                    <p>Your hemoglobin levels indicate mild anemia. Consider increasing your intake of iron-rich foods like spinach, lentils, and lean red meat. Vitamin C helps with iron absorption, so pair these foods with citrus fruits or bell peppers.</p>
                                </div>
                                
                                <div class="health-tip mb-3">
                                    <div class="health-tip-title">
                                        <i class="bi bi-heart"></i> Heart Health
                                    </div>
                                    <p>Maintain your excellent blood pressure by staying physically active. Aim for at least 30 minutes of moderate exercise 5 days a week. Continue to limit salt intake and processed foods.</p>
                                </div>
                                
                                <div class="health-tip">
                                    <div class="health-tip-title">
                                        <i class="bi bi-cup-hot"></i> Hydration
                                    </div>
                                    <p>Proper hydration is essential for overall health. Aim to drink 8-10 glasses of water daily, more if you are physically active or during hot weather.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Right Column -->
                    <div class="col-lg-4">
                        <!-- Quick Actions -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-lightning-charge"></i>
                                    Quick Actions
                                </h5>
                            </div>
                            <div class="card-body">
                                <a href="#" class="quick-action d-block mb-3">
                                    <i class="bi bi-journal-plus"></i>
                                    <div>
                                        <div class="quick-action-title">Record Health Metrics</div>
                                        <p class="quick-action-description">Update your current health measurements</p>
                                    </div>
                                </a>
                                
                                <a href="#" class="quick-action d-block mb-3">
                                    <i class="bi bi-clipboard2-pulse"></i>
                                    <div>
                                        <div class="quick-action-title">Schedule Check-up</div>
                                        <p class="quick-action-description">Book your next health appointment</p>
                                    </div>
                                </a>
                                
                                <a href="#" class="quick-action d-block mb-3">
                                    <i class="bi bi-chat-dots"></i>
                                    <div>
                                        <div class="quick-action-title">Chat with Assistant</div>
                                        <p class="quick-action-description">Get answers to your health questions</p>
                                    </div>
                                </a>
                                
                                <a href="#" class="quick-action d-block">
                                    <i class="bi bi-bank"></i>
                                    <div>
                                        <div class="quick-action-title">Government Schemes</div>
                                        <p class="quick-action-description">Check eligible health programs</p>
                                    </div>
                                </a>
                            </div>
                        </div>
                        
                        <!-- Upcoming Appointments -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-calendar-check"></i>
                                    Upcoming Appointments
                                </h5>
                                <a href="#" class="btn btn-sm btn-outline-primary">Add New</a>
                            </div>
                            <div class="card-body">
                                <div class="upcoming-appointment">
                                    <div class="appointment-date">
                                        <i class="bi bi-calendar-event me-1"></i> April 15, 2025 | 10:30 AM
                                    </div>
                                    <div class="appointment-details">
                                        <strong>General Check-up</strong><br>
                                        <span class="text-muted">Dr. Sarah Johnson</span>
                                    </div>
                                </div>
                                
                                <div class="upcoming-appointment">
                                    <div class="appointment-date">
                                        <i class="bi bi-calendar-event me-1"></i> May 5, 2025 | 2:00 PM
                                    </div>
                                    <div class="appointment-details">
                                        <strong>Blood Test</strong><br>
                                        <span class="text-muted">City Health Lab</span>
                                    </div>
                                </div>
                                
                                <a href="#" class="btn btn-outline-primary w-100 mt-2">View All Appointments</a>
                            </div>
                        </div>
                        
                        <!-- Nutrition Tips -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-egg-fried"></i>
                                    Nutrition Tips
                                </h5>
                            </div>
                            <div class="card-body">
                                <h6 class="mb-3">Foods to Boost Iron Levels:</h6>
                                <ul class="list-group list-group-flush mb-3">
                                    <li class="list-group-item d-flex align-items-center">
                                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                                        <div>
                                            <strong>Spinach and Leafy Greens</strong><br>
                                            <small class="text-muted">High in iron and other essential nutrients</small>
                                        </div>
                                    </li>
                                    <li class="list-group-item d-flex align-items-center">
                                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                                        <div>
                                            <strong>Beans and Lentils</strong><br>
                                            <small class="text-muted">Excellent plant-based sources of iron</small>
                                        </div>
                                    </li>
                                    <li class="list-group-item d-flex align-items-center">
                                        <i class="bi bi-check-circle-fill text-success me-2"></i>
                                        <div>
                                            <strong>Red Meat (Lean)</strong><br>
                                            <small class="text-muted">Contains highly absorbable heme iron</small>
                                        </div>
                                    </li>
                                </ul>
                                <a href="#" class="btn btn-outline-primary w-100">View Nutrition Guide</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <footer class="footer mt-auto">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong class="text-primary">NeoMitra</strong> &copy; 2025. All rights reserved.
                    </div>
                    <div>
                        <a href="#" class="text-muted me-3">Privacy Policy</a>
                        <a href="#" class="text-muted me-3">Terms of Service</a>
                        <a href="#" class="text-muted">Contact Us</a>
                    </div>
                </div>
            </div>
        </footer>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """, username=username, user_data=user_data)

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect('/')

@app.route('/health-records')
def health_records():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Records - NeoMitra</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f7ff;
                min-height: 100vh;
            }
            
            .navbar {
                background-color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            
            .navbar-brand {
                display: flex;
                align-items: center;
                font-weight: 700;
                color: var(--primary-color);
            }
            
            .navbar-brand i {
                margin-right: 0.5rem;
            }
            
            .sidebar {
                background: white;
                box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
                min-height: calc(100vh - 56px);
            }
            
            .sidebar-link {
                display: block;
                padding: 0.75rem 1.25rem;
                color: #6c757d;
                text-decoration: none;
                transition: var(--transition);
                position: relative;
            }
            
            .sidebar-link.active {
                color: var(--primary-color);
                background-color: rgba(121, 82, 179, 0.05);
                font-weight: 600;
            }
            
            .sidebar-link.active::before {
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                height: 100%;
                width: 4px;
                background-color: var(--primary-color);
            }
            
            .sidebar-link:hover {
                color: var(--primary-color);
                background-color: rgba(121, 82, 179, 0.05);
            }
            
            .sidebar-link i {
                margin-right: 0.5rem;
            }
            
            .main-content {
                padding: 2rem;
            }
            
            .page-title {
                color: var(--dark-color);
                font-weight: 600;
                margin-bottom: 1.5rem;
            }
            
            .card {
                border: none;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                margin-bottom: 1.5rem;
                transition: var(--transition);
            }
            
            .card:hover {
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            }
            
            .card-header {
                background-color: white;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1.25rem;
            }
            
            .card-title {
                color: var(--dark-color);
                font-weight: 600;
                margin-bottom: 0;
            }
            
            .card-body {
                padding: 1.5rem;
            }
            
            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
            }
            
            .btn-primary:hover {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
            }
            
            .btn-outline-primary {
                color: var(--primary-color);
                border-color: var(--primary-color);
            }
            
            .btn-outline-primary:hover {
                background-color: var(--primary-color);
                color: white;
            }
            
            .form-label {
                font-weight: 500;
                color: var(--dark-color);
            }
            
            .form-control:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 0.25rem rgba(121, 82, 179, 0.25);
            }
            
            .form-check-input:checked {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
            }
            
            .health-record-list {
                margin-bottom: 1.5rem;
            }
            
            .health-record-item {
                background-color: white;
                border-radius: var(--border-radius);
                padding: 1rem;
                box-shadow: var(--box-shadow);
                margin-bottom: 1rem;
            }
            
            .health-record-date {
                font-size: 0.875rem;
                color: #6c757d;
                margin-bottom: 0.5rem;
            }
            
            .health-data {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            }
            
            .health-data-item {
                background-color: rgba(121, 82, 179, 0.1);
                color: var(--primary-color);
                padding: 0.25rem 0.75rem;
                border-radius: 50px;
                font-size: 0.875rem;
                font-weight: 500;
            }
            
            .microphone-container {
                background-color: white;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                padding: 1.5rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 1.5rem;
            }
            
            .microphone-btn {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background-color: var(--primary-color);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                cursor: pointer;
                margin-bottom: 1rem;
                transition: all 0.3s;
            }
            
            .microphone-btn:hover {
                transform: scale(1.05);
                background-color: var(--secondary-color);
            }
            
            .microphone-btn.active {
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% {
                    box-shadow: 0 0 0 0 rgba(121, 82, 179, 0.7);
                }
                70% {
                    box-shadow: 0 0 0 20px rgba(121, 82, 179, 0);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(121, 82, 179, 0);
                }
            }
            
            .microphone-status {
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            
            .microphone-transcript {
                max-height: 100px;
                overflow-y: auto;
                width: 100%;
                padding: 1rem;
                background-color: #f8f9fa;
                border-radius: var(--border-radius);
                font-style: italic;
                color: #6c757d;
            }
            
            .voice-help {
                margin-top: 1rem;
                font-size: 0.875rem;
                color: #6c757d;
            }
            
            .voice-help strong {
                color: var(--dark-color);
            }
            
            .voice-examples {
                font-size: 0.875rem;
                color: #6c757d;
                margin-top: 0.5rem;
            }
            
            .voice-examples code {
                background-color: #f8f9fa;
                padding: 0.15rem 0.3rem;
                border-radius: 3px;
                color: var(--primary-color);
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/health-records">Health Records</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/risk-assessment">Risk Assessment</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/resources">Resources</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/chatbot">Assistant</a>
                        </li>
                    </ul>
                    <div class="d-flex align-items-center">
                        <span class="me-3">{{ session.get('username', '') }}</span>
                        <a href="/logout" class="btn btn-outline-danger btn-sm">Logout</a>
                    </div>
                </div>
            </div>
        </nav>
        
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-3 col-xl-2 p-0">
                    <div class="sidebar">
                        <a href="/dashboard" class="sidebar-link">
                            <i class="bi bi-house-door"></i> Dashboard
                        </a>
                        <a href="/health-records" class="sidebar-link active">
                            <i class="bi bi-clipboard-heart"></i> Health Records
                        </a>
                        <a href="/risk-assessment" class="sidebar-link">
                            <i class="bi bi-shield-check"></i> Risk Assessment
                        </a>
                        <a href="/resources" class="sidebar-link">
                            <i class="bi bi-book"></i> Resources
                        </a>
                        <a href="/chatbot" class="sidebar-link">
                            <i class="bi bi-chat-dots"></i> Assistant
                        </a>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-9 col-xl-10">
                    <div class="main-content">
                        <h1 class="page-title">
                            <i class="bi bi-clipboard-heart me-2"></i> Health Records
                        </h1>
                        
                        <div class="row">
                            <div class="col-md-7 col-lg-8">
                                <!-- Health Record Form -->
                                <div class="card">
                                    <div class="card-header">
                                        <h5 class="card-title">
                                            <i class="bi bi-plus-circle"></i>
                                            Add New Health Record
                                        </h5>
                                    </div>
                                    <div class="card-body">
                                        <form>
                                            <div class="row mb-3">
                                                <div class="col-md-6">
                                                    <label for="weight" class="form-label">Weight (kg)</label>
                                                    <input type="number" class="form-control" id="weight" name="weight" step="0.1">
                                                </div>
                                                <div class="col-md-6">
                                                    <label for="height" class="form-label">Height (cm)</label>
                                                    <input type="number" class="form-control" id="height" name="height" step="0.1">
                                                </div>
                                            </div>
                                            
                                            <div class="row mb-3">
                                                <div class="col-md-6">
                                                    <label class="form-label">Blood Pressure (mmHg)</label>
                                                    <div class="input-group">
                                                        <input type="number" class="form-control" id="bp_systolic" name="bp_systolic" placeholder="Systolic">
                                                        <span class="input-group-text">/</span>
                                                        <input type="number" class="form-control" id="bp_diastolic" name="bp_diastolic" placeholder="Diastolic">
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <label for="blood_sugar" class="form-label">Blood Sugar (mg/dL)</label>
                                                    <input type="number" class="form-control" id="blood_sugar" name="blood_sugar" step="0.1">
                                                </div>
                                            </div>
                                            
                                            <div class="row mb-3">
                                                <div class="col-md-6">
                                                    <label for="hemoglobin" class="form-label">Hemoglobin (g/dL)</label>
                                                    <input type="number" class="form-control" id="hemoglobin" name="hemoglobin" step="0.1">
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="form-check mt-4">
                                                        <input class="form-check-input" type="checkbox" id="is_pregnant" name="is_pregnant">
                                                        <label class="form-check-label" for="is_pregnant">I am pregnant</label>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div class="pregnancy-details" style="display: none;">
                                                <div class="row mb-3">
                                                    <div class="col-md-6">
                                                        <label for="pregnancy_week" class="form-label">Pregnancy Week</label>
                                                        <input type="number" class="form-control" id="pregnancy_week" name="pregnancy_week">
                                                    </div>
                                                    <div class="col-md-6">
                                                        <label for="due_date" class="form-label">Due Date</label>
                                                        <input type="date" class="form-control" id="due_date" name="due_date">
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <div class="mb-3">
                                                <label for="existing_conditions" class="form-label">Existing Medical Conditions</label>
                                                <textarea class="form-control" id="existing_conditions" name="existing_conditions" rows="2"></textarea>
                                            </div>
                                            
                                            <div class="mb-3">
                                                <label for="current_medications" class="form-label">Current Medications</label>
                                                <textarea class="form-control" id="current_medications" name="current_medications" rows="2"></textarea>
                                            </div>
                                            
                                            <button type="submit" class="btn btn-primary">Save Health Record</button>
                                        </form>
                                    </div>
                                </div>
                                
                                <!-- Health Records List -->
                                <div class="health-record-list">
                                    <h5 class="mb-3">Recent Health Records</h5>
                                    
                                    <div class="health-record-item">
                                        <div class="health-record-date">
                                            <i class="bi bi-calendar me-1"></i> March 25, 2025
                                        </div>
                                        <div class="health-data">
                                            <div class="health-data-item">Weight: 68kg</div>
                                            <div class="health-data-item">Blood Pressure: 120/80</div>
                                            <div class="health-data-item">Hemoglobin: 13.5 g/dL</div>
                                        </div>
                                        <div class="d-flex justify-content-end">
                                            <button class="btn btn-sm btn-outline-primary">View Details</button>
                                        </div>
                                    </div>
                                    
                                    <div class="health-record-item">
                                        <div class="health-record-date">
                                            <i class="bi bi-calendar me-1"></i> March 10, 2025
                                        </div>
                                        <div class="health-data">
                                            <div class="health-data-item">Weight: 67.5kg</div>
                                            <div class="health-data-item">Blood Pressure: 118/78</div>
                                            <div class="health-data-item">Hemoglobin: 13.2 g/dL</div>
                                        </div>
                                        <div class="d-flex justify-content-end">
                                            <button class="btn btn-sm btn-outline-primary">View Details</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-md-5 col-lg-4">
                                <!-- Voice Input Widget -->
                                <div class="card">
                                    <div class="card-header">
                                        <h5 class="card-title">
                                            <i class="bi bi-mic"></i>
                                            Voice Health Recording
                                        </h5>
                                    </div>
                                    <div class="card-body">
                                        <div class="microphone-container">
                                            <div class="microphone-btn" id="microphoneBtn">
                                                <i class="bi bi-mic"></i>
                                            </div>
                                            <div class="microphone-status" id="microphoneStatus">
                                                Click the microphone to start recording
                                            </div>
                                            <div class="microphone-transcript" id="transcript"></div>
                                        </div>
                                        
                                        <div class="voice-help">
                                            <strong>How to use voice recording:</strong>
                                            <p>Speak clearly and include health metrics with their values.</p>
                                        </div>
                                        
                                        <div class="voice-examples">
                                            Examples:
                                            <ul>
                                                <li><code>"My weight is 70 kg"</code></li>
                                                <li><code>"My blood pressure is 120 over 80"</code></li>
                                                <li><code>"My hemoglobin is 13.5 g/dl"</code></li>
                                                <li><code>"I am pregnant, 20 weeks"</code></li>
                                            </ul>
                                        </div>
                                        
                                        <div id="extractedDataContainer" class="mt-3" style="display: none;">
                                            <h6>Extracted Health Data</h6>
                                            <div id="extractedData" class="p-3 bg-light rounded"></div>
                                            <button id="saveExtractedData" class="btn btn-primary btn-sm mt-2">Save to Health Record</button>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Health Tips -->
                                <div class="card mt-3">
                                    <div class="card-header">
                                        <h5 class="card-title">
                                            <i class="bi bi-lightbulb"></i>
                                            Health Tips
                                        </h5>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-3">
                                            <strong>Regular Monitoring</strong>
                                            <p class="small text-muted">Keep track of your health metrics regularly to identify trends and potential issues early.</p>
                                        </div>
                                        <div class="mb-3">
                                            <strong>Balanced Diet</strong>
                                            <p class="small text-muted">Maintain a balanced diet rich in vegetables, fruits, lean proteins, and whole grains to support overall health.</p>
                                        </div>
                                        <div>
                                            <strong>Stay Hydrated</strong>
                                            <p class="small text-muted">Drink adequate water throughout the day to support proper bodily functions and maintain energy levels.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- JavaScript to handle voice recognition -->
        <script src="/static/js/voice-recognition.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Toggle pregnancy details based on checkbox
                const isPregnantCheckbox = document.getElementById('is_pregnant');
                const pregnancyDetails = document.querySelector('.pregnancy-details');
                
                isPregnantCheckbox.addEventListener('change', function() {
                    pregnancyDetails.style.display = this.checked ? 'block' : 'none';
                });
                
                // Voice recognition setup
                const microphoneBtn = document.getElementById('microphoneBtn');
                const microphoneStatus = document.getElementById('microphoneStatus');
                const transcriptElement = document.getElementById('transcript');
                const extractedDataContainer = document.getElementById('extractedDataContainer');
                const extractedDataElement = document.getElementById('extractedData');
                const saveExtractedDataBtn = document.getElementById('saveExtractedData');
                
                let voiceRecognition = null;
                let healthDataExtractor = null;
                let lastExtractedData = null;
                
                // Initialize voice recognition
                try {
                    voiceRecognition = new VoiceRecognition('en-US');
                    healthDataExtractor = new HealthDataExtractor();
                    
                    voiceRecognition.onStart(function() {
                        microphoneBtn.classList.add('active');
                        microphoneStatus.textContent = 'Listening...';
                        transcriptElement.textContent = '';
                        extractedDataContainer.style.display = 'none';
                    });
                    
                    voiceRecognition.onResult(function(transcript, confidence) {
                        transcriptElement.textContent = transcript;
                        
                        // Process transcript with our backend NLP
                        processTranscript(transcript);
                    });
                    
                    voiceRecognition.onEnd(function() {
                        microphoneBtn.classList.remove('active');
                        microphoneStatus.textContent = 'Click the microphone to start recording';
                    });
                    
                    voiceRecognition.onError(function(error) {
                        microphoneStatus.textContent = 'Error: ' + error;
                        microphoneBtn.classList.remove('active');
                    });
                } catch (error) {
                    console.error('Error initializing voice recognition:', error);
                    microphoneStatus.textContent = 'Speech recognition not supported';
                    microphoneBtn.disabled = true;
                }
                
                // Microphone button click handler
                microphoneBtn.addEventListener('click', function() {
                    if (!voiceRecognition) return;
                    
                    if (voiceRecognition.isListening) {
                        voiceRecognition.stop();
                    } else {
                        voiceRecognition.start();
                    }
                });
                
                // Process transcript with backend NLP
                function processTranscript(transcript) {
                    // Show loading state
                    microphoneStatus.textContent = 'Processing...';
                    
                    // Call our backend API
                    fetch('/api/voice/process', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            transcript: transcript,
                            language: 'en'
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Processed data:', data);
                        
                        if (data.success && Object.keys(data.extracted_data).length > 0) {
                            // Show extracted data
                            lastExtractedData = data.extracted_data;
                            displayExtractedData(data.extracted_data);
                            extractedDataContainer.style.display = 'block';
                        } else {
                            microphoneStatus.textContent = 'No health data detected. Try again.';
                        }
                    })
                    .catch(error => {
                        console.error('Error processing voice input:', error);
                        microphoneStatus.textContent = 'Error processing voice input';
                    });
                }
                
                // Display extracted data
                function displayExtractedData(data) {
                    let html = '';
                    
                    for (const [key, value] of Object.entries(data)) {
                        const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        html += `<div><strong>${formattedKey}:</strong> ${value}</div>`;
                    }
                    
                    extractedDataElement.innerHTML = html;
                    microphoneStatus.textContent = 'Health data extracted successfully';
                }
                
                // Save extracted data to form
                saveExtractedDataBtn.addEventListener('click', function() {
                    if (!lastExtractedData) return;
                    
                    // Map extracted data to form fields
                    if (lastExtractedData.weight) {
                        document.getElementById('weight').value = lastExtractedData.weight;
                    }
                    
                    if (lastExtractedData.height) {
                        document.getElementById('height').value = lastExtractedData.height;
                    }
                    
                    if (lastExtractedData.blood_pressure_systolic) {
                        document.getElementById('bp_systolic').value = lastExtractedData.blood_pressure_systolic;
                    }
                    
                    if (lastExtractedData.blood_pressure_diastolic) {
                        document.getElementById('bp_diastolic').value = lastExtractedData.blood_pressure_diastolic;
                    }
                    
                    if (lastExtractedData.blood_sugar) {
                        document.getElementById('blood_sugar').value = lastExtractedData.blood_sugar;
                    }
                    
                    if (lastExtractedData.hemoglobin) {
                        document.getElementById('hemoglobin').value = lastExtractedData.hemoglobin;
                    }
                    
                    if (lastExtractedData.is_pregnant !== undefined) {
                        document.getElementById('is_pregnant').checked = lastExtractedData.is_pregnant;
                        document.querySelector('.pregnancy-details').style.display = lastExtractedData.is_pregnant ? 'block' : 'none';
                    }
                    
                    if (lastExtractedData.pregnancy_week) {
                        document.getElementById('pregnancy_week').value = lastExtractedData.pregnancy_week;
                    }
                    
                    microphoneStatus.textContent = 'Data transferred to form';
                    extractedDataContainer.style.display = 'none';
                });
            });
        </script>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

@app.route('/chatbot')
def chatbot():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Assistant - NeoMitra</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                background-color: #f8f9fa;
                color: #333;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .navbar {
                background-color: white;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .navbar-brand {
                display: flex;
                align-items: center;
                font-weight: 700;
                color: var(--primary-color);
                font-size: 1.5rem;
            }
            
            .navbar-brand i {
                margin-right: 0.5rem;
                font-size: 1.8rem;
            }
            
            .main-content {
                flex: 1;
                padding: 2rem 0;
            }
            
            .chatbot-container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                overflow: hidden;
                display: flex;
                flex-direction: column;
                height: 70vh;
            }
            
            .chatbot-header {
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                color: white;
                padding: 1.5rem;
                display: flex;
                align-items: center;
            }
            
            .chatbot-avatar {
                width: 50px;
                height: 50px;
                background-color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 1rem;
            }
            
            .chatbot-avatar i {
                font-size: 1.8rem;
                color: var(--primary-color);
            }
            
            .chatbot-title {
                margin: 0;
                font-size: 1.5rem;
                font-weight: 600;
            }
            
            .chatbot-subtitle {
                margin: 0;
                font-size: 0.9rem;
                opacity: 0.8;
            }
            
            .chatbot-messages {
                flex: 1;
                padding: 1.5rem;
                overflow-y: auto;
                background-color: rgba(121, 82, 179, 0.05);
            }
            
            .message {
                margin-bottom: 1.5rem;
                max-width: 80%;
            }
            
            .message-user {
                margin-left: auto;
                background-color: var(--primary-color);
                color: white;
                border-radius: 18px 18px 0 18px;
                padding: 0.8rem 1.2rem;
            }
            
            .message-bot {
                margin-right: auto;
                background-color: white;
                border-radius: 18px 18px 18px 0;
                padding: 0.8rem 1.2rem;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            
            .chatbot-input {
                padding: 1rem;
                border-top: 1px solid rgba(0, 0, 0, 0.1);
                background-color: white;
            }
            
            .input-group {
                position: relative;
            }
            
            .form-control {
                padding: 0.8rem 1rem;
                border-radius: 25px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                padding-right: 90px;
            }
            
            .form-control:focus {
                box-shadow: 0 0 0 0.25rem rgba(121, 82, 179, 0.25);
                border-color: var(--primary-color);
            }
            
            .send-button {
                position: absolute;
                right: 5px;
                top: 5px;
                background-color: var(--primary-color);
                border: none;
                border-radius: 50%;
                width: 38px;
                height: 38px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                z-index: 10;
            }
            
            .send-button:hover {
                background-color: var(--secondary-color);
            }
            
            .mic-button {
                position: absolute;
                right: 50px;
                top: 5px;
                background-color: transparent;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 50%;
                width: 38px;
                height: 38px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary-color);
                z-index: 10;
            }
            
            .mic-button:hover {
                background-color: rgba(121, 82, 179, 0.1);
            }
            
            .mic-button.active {
                background-color: var(--primary-color);
                color: white;
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            
            .topic-suggestions {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 1rem;
            }
            
            .topic-chip {
                background-color: rgba(121, 82, 179, 0.1);
                color: var(--primary-color);
                padding: 0.5rem 0.8rem;
                border-radius: 50px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: var(--transition);
            }
            
            .topic-chip:hover {
                background-color: rgba(121, 82, 179, 0.2);
            }
            
            .footer {
                background-color: white;
                padding: 1rem 0;
                margin-top: 2rem;
                box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Health Records</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/chatbot">Health Assistant</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Resources</a>
                        </li>
                    </ul>
                    <div class="d-flex align-items-center">
                        <div class="dropdown">
                            <a class="d-flex align-items-center text-decoration-none dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <div class="d-flex align-items-center justify-content-center rounded-circle bg-primary text-white" style="width: 35px; height: 35px; margin-right: 0.5rem;">
                                    {{ username[0].upper() }}
                                </div>
                                <span class="d-none d-sm-inline-block">{{ username }}</span>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                <li><a class="dropdown-item" href="#"><i class="bi bi-person me-2"></i>Profile</a></li>
                                <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i>Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Main Content -->
        <div class="main-content">
            <div class="container">
                <div class="chatbot-container">
                    <div class="chatbot-header">
                        <div class="chatbot-avatar">
                            <i class="bi bi-robot"></i>
                        </div>
                        <div>
                            <h2 class="chatbot-title">NeoMitra Health Assistant</h2>
                            <p class="chatbot-subtitle">Ask me anything about health, nutrition, and wellness</p>
                        </div>
                    </div>
                    
                    <div class="chatbot-messages" id="chatMessages">
                        <div class="message message-bot">
                            Hello! I'm NeoMitra Health Assistant. I can answer your questions about pregnancy, anemia, diabetes, nutrition, and general health concerns. How can I help you today?
                        </div>
                    </div>
                    
                    <div class="chatbot-input">
                        <div class="input-group">
                            <input type="text" class="form-control" id="messageInput" placeholder="Type your message here..." autocomplete="off">
                            <button class="mic-button" id="micButton" title="Voice input">
                                <i class="bi bi-mic"></i>
                            </button>
                            <button class="send-button" id="sendButton" title="Send message">
                                <i class="bi bi-send"></i>
                            </button>
                        </div>
                        
                        <div class="topic-suggestions">
                            <div class="topic-chip" onclick="suggestTopic('What are signs of anemia?')">Signs of anemia</div>
                            <div class="topic-chip" onclick="suggestTopic('How to manage blood sugar levels?')">Managing blood sugar</div>
                            <div class="topic-chip" onclick="suggestTopic('Iron-rich foods for anemia')">Iron-rich foods</div>
                            <div class="topic-chip" onclick="suggestTopic('Pregnancy nutrition tips')">Pregnancy nutrition</div>
                            <div class="topic-chip" onclick="suggestTopic('Exercise recommendations')">Exercise tips</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <footer class="footer mt-auto">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong class="text-primary">NeoMitra</strong> &copy; 2025. All rights reserved.
                    </div>
                    <div>
                        <a href="#" class="text-muted me-3">Privacy Policy</a>
                        <a href="#" class="text-muted me-3">Terms of Service</a>
                        <a href="#" class="text-muted">Contact Us</a>
                    </div>
                </div>
            </div>
        </footer>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        
        <script>
            // DOM Elements
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            const micButton = document.getElementById('micButton');
            
            // Function to add a message to the chat
            function addMessage(message, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.classList.add(isUser ? 'message-user' : 'message-bot');
                messageDiv.textContent = message;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // Function to send a message
            function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    addMessage(message, true);
                    messageInput.value = '';
                    
                    // Send the message to the API and get a response
                    fetch('/api/chatbot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            // Add the bot's response to the chat
                            setTimeout(() => {
                                addMessage(data.response, false);
                            }, 500);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        setTimeout(() => {
                            addMessage("I'm sorry, I'm having trouble connecting. Please try again later.", false);
                        }, 500);
                    });
                }
            }
            
            // Function for suggested topics
            function suggestTopic(topic) {
                messageInput.value = topic;
                messageInput.focus();
            }
            
            // Event listeners
            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // Voice input functionality (simplified for demo)
            let isRecording = false;
            
            micButton.addEventListener('click', () => {
                isRecording = !isRecording;
                if (isRecording) {
                    micButton.classList.add('active');
                    // In a real implementation, this would start voice recording
                    setTimeout(() => {
                        // Simulate ending the recording after 3 seconds
                        isRecording = false;
                        micButton.classList.remove('active');
                        messageInput.value = "This is a simulated voice message.";
                        messageInput.focus();
                    }, 3000);
                } else {
                    micButton.classList.remove('active');
                    // In a real implementation, this would stop voice recording
                }
            });
        </script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/resources')
def resources():
    # If not logged in, allow viewing but with limited content
    logged_in = session.get('logged_in', False)
    username = session.get('username', 'Guest')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Resources - NeoMitra</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --light-color: #f8f9fa;
                --dark-color: #212529;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                background-color: #f8f9fa;
                color: #333;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .navbar {
                background-color: white;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            .navbar-brand {
                display: flex;
                align-items: center;
                font-weight: 700;
                color: var(--primary-color);
                font-size: 1.5rem;
            }
            
            .navbar-brand i {
                margin-right: 0.5rem;
                font-size: 1.8rem;
            }
            
            .main-content {
                flex: 1;
                padding: 2rem 0;
            }
            
            .page-header {
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                color: white;
                padding: 2.5rem 0;
                margin-bottom: 2.5rem;
            }
            
            .page-title {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }
            
            .page-subtitle {
                font-size: 1.1rem;
                opacity: 0.9;
                max-width: 800px;
            }
            
            .card {
                border: none;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                margin-bottom: 1.5rem;
                transition: var(--transition);
                overflow: hidden;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            
            .card-img-top {
                height: 180px;
                object-fit: cover;
            }
            
            .card-body {
                padding: 1.5rem;
            }
            
            .card-title {
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: var(--dark-color);
            }
            
            .card-text {
                color: #6c757d;
                margin-bottom: 1rem;
            }
            
            .card-footer {
                padding: 1rem 1.5rem;
                background-color: white;
                border-top: 1px solid rgba(0, 0, 0, 0.05);
            }
            
            .btn-primary {
                background-color: var(--primary-color);
                border-color: var(--primary-color);
                padding: 0.5rem 1rem;
                font-weight: 500;
                border-radius: 50px;
                transition: all 0.3s;
            }
            
            .btn-primary:hover {
                background-color: var(--secondary-color);
                border-color: var(--secondary-color);
                transform: translateY(-2px);
            }
            
            .btn-outline-primary {
                border-color: var(--primary-color);
                color: var(--primary-color);
                padding: 0.5rem 1rem;
                font-weight: 500;
                border-radius: 50px;
                transition: all 0.3s;
            }
            
            .btn-outline-primary:hover {
                background-color: var(--primary-color);
                color: white;
                transform: translateY(-2px);
            }
            
            .resource-category {
                margin-bottom: 3rem;
            }
            
            .category-title {
                margin-bottom: 1.5rem;
                color: var(--primary-color);
                font-weight: 600;
                display: flex;
                align-items: center;
            }
            
            .category-title i {
                margin-right: 0.5rem;
                font-size: 1.5rem;
            }
            
            .topic-filter {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-bottom: 2rem;
            }
            
            .topic-badge {
                background-color: rgba(121, 82, 179, 0.1);
                color: var(--primary-color);
                padding: 0.5rem 1rem;
                border-radius: 50px;
                font-size: 0.9rem;
                cursor: pointer;
                transition: var(--transition);
                border: 1px solid transparent;
            }
            
            .topic-badge:hover,
            .topic-badge.active {
                background-color: var(--primary-color);
                color: white;
            }
            
            .resource-card {
                border: none;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                margin-bottom: 1.5rem;
                transition: var(--transition);
                overflow: hidden;
                height: 100%;
            }
            
            .locked-indicator {
                position: absolute;
                top: 10px;
                right: 10px;
                background-color: rgba(0, 0, 0, 0.5);
                color: white;
                padding: 0.3rem 0.6rem;
                border-radius: 50px;
                font-size: 0.8rem;
                display: flex;
                align-items: center;
            }
            
            .locked-indicator i {
                margin-right: 0.3rem;
            }
            
            .footer {
                background-color: white;
                padding: 1.5rem 0;
                margin-top: 2rem;
                box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Home</a>
                        </li>
                        {% if logged_in %}
                        <li class="nav-item">
                            <a class="nav-link" href="/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Health Records</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/chatbot">Health Assistant</a>
                        </li>
                        {% endif %}
                        <li class="nav-item">
                            <a class="nav-link active" href="/resources">Resources</a>
                        </li>
                    </ul>
                    <div class="d-flex align-items-center">
                        {% if logged_in %}
                        <div class="dropdown">
                            <a class="d-flex align-items-center text-decoration-none dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <div class="d-flex align-items-center justify-content-center rounded-circle bg-primary text-white" style="width: 35px; height: 35px; margin-right: 0.5rem;">
                                    {{ username[0].upper() }}
                                </div>
                                <span class="d-none d-sm-inline-block">{{ username }}</span>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                <li><a class="dropdown-item" href="#"><i class="bi bi-person me-2"></i>Profile</a></li>
                                <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i>Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
                            </ul>
                        </div>
                        {% else %}
                        <a href="/login" class="btn btn-outline-primary me-2">Login</a>
                        <a href="/register" class="btn btn-primary">Register</a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Page Header -->
        <header class="page-header">
            <div class="container">
                <h1 class="page-title">Health Resources</h1>
                <p class="page-subtitle">Access comprehensive information about anemia, diabetes, pregnancy care, nutrition, and government healthcare schemes.</p>
            </div>
        </header>
        
        <!-- Main Content -->
        <div class="main-content">
            <div class="container">
                <!-- Topic Filter -->
                <div class="topic-filter">
                    <div class="topic-badge active">All Topics</div>
                    <div class="topic-badge">Anemia</div>
                    <div class="topic-badge">Diabetes</div>
                    <div class="topic-badge">Pregnancy</div>
                    <div class="topic-badge">Nutrition</div>
                    <div class="topic-badge">Government Schemes</div>
                </div>
                
                <!-- Medical Guidelines -->
                <div class="resource-category">
                    <h2 class="category-title">
                        <i class="bi bi-journal-medical"></i>
                        Health Guidelines
                    </h2>
                    <div class="row">
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                <img src="https://images.unsplash.com/photo-1505751172876-fa1923c5c528?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YW5lbWlhfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Anemia Management">
                                <div class="card-body">
                                    <h5 class="card-title">Understanding and Managing Anemia</h5>
                                    <p class="card-text">Learn about the causes, symptoms, and treatment options for anemia, a condition affecting both men and women.</p>
                                </div>
                                <div class="card-footer">
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                {% if not logged_in %}
                                <div class="locked-indicator">
                                    <i class="bi bi-lock-fill"></i> Login to Access
                                </div>
                                {% endif %}
                                <img src="https://images.unsplash.com/photo-1584362917165-526a968579e6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZGlhYmV0ZXN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Diabetes Care">
                                <div class="card-body">
                                    <h5 class="card-title">Comprehensive Diabetes Management</h5>
                                    <p class="card-text">Essential guidelines for managing blood sugar levels, understanding medication, and making lifestyle changes.</p>
                                </div>
                                <div class="card-footer">
                                    {% if logged_in %}
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                    {% else %}
                                    <a href="/login" class="btn btn-primary">Login to Access</a>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                <img src="https://images.unsplash.com/photo-1516726817505-f5ed825624d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHJlZ25hbmN5fGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Pregnancy Care">
                                <div class="card-body">
                                    <h5 class="card-title">Pregnancy Care Guidelines</h5>
                                    <p class="card-text">Essential information for a healthy pregnancy, including prenatal care, nutrition, and managing common concerns.</p>
                                </div>
                                <div class="card-footer">
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Nutrition Advice -->
                <div class="resource-category">
                    <h2 class="category-title">
                        <i class="bi bi-egg-fried"></i>
                        Nutrition Resources
                    </h2>
                    <div class="row">
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                <img src="https://images.unsplash.com/photo-1576097449402-94a548bc8de1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGVhbHRoeSUyMGZvb2R8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Iron-Rich Foods">
                                <div class="card-body">
                                    <h5 class="card-title">Iron-Rich Foods for Anemia Prevention</h5>
                                    <p class="card-text">A comprehensive guide to foods high in iron and strategies to enhance iron absorption in your diet.</p>
                                </div>
                                <div class="card-footer">
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                {% if not logged_in %}
                                <div class="locked-indicator">
                                    <i class="bi bi-lock-fill"></i> Login to Access
                                </div>
                                {% endif %}
                                <img src="https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZGlhYmV0ZXMlMjBmb29kfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Diabetic Diet">
                                <div class="card-body">
                                    <h5 class="card-title">Diabetes-Friendly Meal Planning</h5>
                                    <p class="card-text">Learn how to create balanced meals that help manage blood sugar levels, including recipe ideas and sample meal plans.</p>
                                </div>
                                <div class="card-footer">
                                    {% if logged_in %}
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                    {% else %}
                                    <a href="/login" class="btn btn-primary">Login to Access</a>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGhlYWx0aHklMjBmb29kfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Pregnancy Nutrition">
                                <div class="card-body">
                                    <h5 class="card-title">Optimal Nutrition During Pregnancy</h5>
                                    <p class="card-text">Essential nutritional guidance for each trimester of pregnancy, focusing on critical nutrients for maternal and fetal health.</p>
                                </div>
                                <div class="card-footer">
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Government Schemes -->
                <div class="resource-category">
                    <h2 class="category-title">
                        <i class="bi bi-bank"></i>
                        Government Healthcare Schemes
                    </h2>
                    <div class="row">
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8aG9zcGl0YWx8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Janani Suraksha Yojana">
                                <div class="card-body">
                                    <h5 class="card-title">Janani Suraksha Yojana (JSY)</h5>
                                    <p class="card-text">Details about this scheme which promotes institutional delivery among poor pregnant women with cash assistance and support.</p>
                                </div>
                                <div class="card-footer">
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                <img src="https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZG9jdG9yfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Ayushman Bharat">
                                <div class="card-body">
                                    <h5 class="card-title">Ayushman Bharat Health Scheme</h5>
                                    <p class="card-text">Information about India's national health protection scheme providing coverage for secondary and tertiary care hospitalization.</p>
                                </div>
                                <div class="card-footer">
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-4 mb-4">
                            <div class="card resource-card">
                                {% if not logged_in %}
                                <div class="locked-indicator">
                                    <i class="bi bi-lock-fill"></i> Login to Access
                                </div>
                                {% endif %}
                                <img src="https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fG1lZGljaW5lfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60" class="card-img-top" alt="Pradhan Mantri Jan Arogya Yojana">
                                <div class="card-body">
                                    <h5 class="card-title">Pradhan Mantri Jan Arogya Yojana (PM-JAY)</h5>
                                    <p class="card-text">A detailed guide to eligibility, benefits, and application process for this flagship health insurance scheme.</p>
                                </div>
                                <div class="card-footer">
                                    {% if logged_in %}
                                    <a href="#" class="btn btn-outline-primary">Read More</a>
                                    {% else %}
                                    <a href="/login" class="btn btn-primary">Login to Access</a>
                                    {% endif %}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <footer class="footer mt-auto">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong class="text-primary">NeoMitra</strong> &copy; 2025. All rights reserved.
                    </div>
                    <div>
                        <a href="#" class="text-muted me-3">Privacy Policy</a>
                        <a href="#" class="text-muted me-3">Terms of Service</a>
                        <a href="#" class="text-muted">Contact Us</a>
                    </div>
                </div>
            </div>
        </footer>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        
        <script>
            // Topic filter functionality
            const topicBadges = document.querySelectorAll('.topic-badge');
            
            topicBadges.forEach(badge => {
                badge.addEventListener('click', () => {
                    // Remove active class from all badges
                    topicBadges.forEach(b => b.classList.remove('active'));
                    
                    // Add active class to clicked badge
                    badge.classList.add('active');
                    
                    // In a real application, this would filter the resources
                    // For now, we're just toggling the active state
                });
            });
        </script>
    </body>
    </html>
    """, logged_in=logged_in, username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)