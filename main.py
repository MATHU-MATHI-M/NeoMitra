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
def process_voice_api():
    """
    API endpoint to process voice transcripts and extract health data using NLP
    """
    data = request.json
    
    if not data or 'transcript' not in data:
        return jsonify({"error": "No transcript provided"}), 400

# Routes for Nutrition page subpages
@app.route('/nutrition/meal-planner')
def meal_planner():
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Meal Planner - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .meal-card {
                border-radius: 12px;
                overflow: hidden;
                transition: all 0.3s ease;
                margin-bottom: 1.5rem;
            }
            .meal-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .meal-img {
                height: 180px;
                object-fit: cover;
            }
            .meal-planner-week {
                background-color: rgba(var(--bs-primary-rgb), 0.1);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 2rem;
            }
            .meal-day {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            .meal-time {
                font-weight: 600;
                color: var(--bs-primary);
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
            }
            .meal-time i {
                margin-right: 0.5rem;
            }
            /* Floating chatbot button */
            .chatbot-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: var(--bs-primary);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s;
            }
            .chatbot-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
            }
            .chatbot-popup {
                position: fixed;
                bottom: 90px;
                right: 20px;
                width: 350px;
                height: 500px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
                z-index: 999;
                display: none;
                flex-direction: column;
                overflow: hidden;
            }
            .chatbot-header {
                background-color: var(--bs-primary);
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
            }
            .chatbot-input {
                border-top: 1px solid #e0e0e0;
                padding: 10px;
                display: flex;
            }
            .chatbot-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin-right: 10px;
            }
            .message {
                margin-bottom: 10px;
                max-width: 80%;
            }
            .user-message {
                background-color: var(--bs-primary);
                color: white;
                padding: 10px 15px;
                border-radius: 18px 18px 0 18px;
                align-self: flex-end;
                margin-left: auto;
            }
            .bot-message {
                background-color: #f1f1f1;
                color: #333;
                padding: 10px 15px;
                border-radius: 18px 18px 18px 0;
                align-self: flex-start;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link active">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Personalized Meal Plan</h2>
                        <div>
                            <a href="/nutrition" class="btn btn-outline-primary me-2">
                                <i class="bi bi-arrow-left me-2"></i>
                                Back to Nutrition Guide
                            </a>
                            <a href="/nutrition/shopping-list" class="btn btn-primary">
                                <i class="bi bi-cart me-2"></i>
                                Get Shopping List
                            </a>
                        </div>
                    </div>
                    
                    <div class="alert alert-primary mt-4">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-info-circle-fill me-2 fs-4"></i>
                            <div>
                                <strong>Personalized for your needs</strong>
                                <p class="mb-0">This meal plan is customized based on your health profile, considering your pregnancy stage and hemoglobin levels to provide optimal nutrition.</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Weekly Meal Planner -->
                    <h4 class="mt-4 mb-3">Week of March 30 - April 5, 2025</h4>
                    
                    <!-- Monday -->
                    <div class="meal-planner-week">
                        <h5><i class="bi bi-calendar-date me-2"></i>Monday</h5>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-sunrise"></i> Breakfast
                                    </div>
                                    <p><strong>Spinach and Feta Omelette</strong></p>
                                    <ul class="small">
                                        <li>2 eggs</li>
                                        <li>1 cup fresh spinach</li>
                                        <li>30g feta cheese</li>
                                        <li>Whole grain toast</li>
                                        <li>1 orange</li>
                                    </ul>
                                    <div class="text-muted small">High in iron, protein, and vitamin C</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-sun"></i> Lunch
                                    </div>
                                    <p><strong>Lentil & Vegetable Soup</strong></p>
                                    <ul class="small">
                                        <li>1 cup cooked lentils</li>
                                        <li>Mixed vegetables (carrots, celery, onions)</li>
                                        <li>Whole grain roll</li>
                                        <li>Side salad with olive oil dressing</li>
                                    </ul>
                                    <div class="text-muted small">Rich in iron, fiber, and plant-based protein</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-moon"></i> Dinner
                                    </div>
                                    <p><strong>Grilled Salmon with Quinoa</strong></p>
                                    <ul class="small">
                                        <li>150g salmon fillet</li>
                                        <li>1/2 cup cooked quinoa</li>
                                        <li>Steamed broccoli</li>
                                        <li>Lemon-herb sauce</li>
                                    </ul>
                                    <div class="text-muted small">Excellent source of omega-3 fatty acids and protein</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row mt-2">
                            <div class="col-md-6">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-cup-hot"></i> Snacks
                                    </div>
                                    <ul>
                                        <li><strong>Mid-morning:</strong> Greek yogurt with mixed berries and honey</li>
                                        <li><strong>Afternoon:</strong> Handful of mixed nuts and dried apricots</li>
                                    </ul>
                                    <div class="text-muted small">Good sources of protein, calcium, and iron</div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-droplet-fill"></i> Hydration
                                    </div>
                                    <p><strong>Aim for 8-10 glasses of fluid:</strong></p>
                                    <ul>
                                        <li>Water (6-8 glasses)</li>
                                        <li>Lemon water (1 glass)</li>
                                        <li>Herbal tea (1 glass)</li>
                                    </ul>
                                    <div class="text-muted small">Adequate hydration is essential for blood volume expansion during pregnancy</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tuesday -->
                    <div class="meal-planner-week">
                        <h5><i class="bi bi-calendar-date me-2"></i>Tuesday</h5>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-sunrise"></i> Breakfast
                                    </div>
                                    <p><strong>Oatmeal with Fortified Toppings</strong></p>
                                    <ul class="small">
                                        <li>1 cup cooked oatmeal</li>
                                        <li>1 tbsp ground flaxseeds</li>
                                        <li>1 tbsp chia seeds</li>
                                        <li>Mixed berries</li>
                                        <li>1 tbsp honey</li>
                                    </ul>
                                    <div class="text-muted small">High in fiber, omega-3 fatty acids, and antioxidants</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-sun"></i> Lunch
                                    </div>
                                    <p><strong>Chicken and Spinach Wrap</strong></p>
                                    <ul class="small">
                                        <li>100g grilled chicken breast</li>
                                        <li>Whole grain wrap</li>
                                        <li>Fresh spinach</li>
                                        <li>Red bell peppers</li>
                                        <li>Hummus spread</li>
                                    </ul>
                                    <div class="text-muted small">Good source of lean protein and iron</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="meal-day">
                                    <div class="meal-time">
                                        <i class="bi bi-moon"></i> Dinner
                                    </div>
                                    <p><strong>Beef and Vegetable Stir-Fry</strong></p>
                                    <ul class="small">
                                        <li>100g lean beef strips</li>
                                        <li>Stir-fried vegetables (broccoli, carrots, snow peas)</li>
                                        <li>Brown rice</li>
                                        <li>Ginger-soy sauce</li>
                                    </ul>
                                    <div class="text-muted small">Excellent source of heme iron and vitamin C</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card mt-4">
                        <div class="card-header">
                            <h5 class="card-title">Dietary Notes & Recommendations</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h6><i class="bi bi-check-circle-fill text-success me-2"></i>Focus on Iron-Rich Foods</h6>
                                    <p>Based on your health profile, we've included plenty of iron-rich foods to help prevent anemia. Combining vitamin C with iron-rich foods enhances iron absorption.</p>
                                    
                                    <h6><i class="bi bi-check-circle-fill text-success me-2"></i>Protein Requirements</h6>
                                    <p>During pregnancy, your protein needs increase. This meal plan provides adequate protein from both animal and plant sources.</p>
                                </div>
                                <div class="col-md-6">
                                    <h6><i class="bi bi-check-circle-fill text-success me-2"></i>Calcium-Rich Foods</h6>
                                    <p>Calcium is essential for your baby's bone development. We've included various calcium sources like dairy products, fortified plant milks, and leafy greens.</p>
                                    
                                    <h6><i class="bi bi-check-circle-fill text-success me-2"></i>Portion Size Flexibility</h6>
                                    <p>Adjust portion sizes based on your hunger levels. Listen to your body's signals and eat until you're comfortably full.</p>
                                </div>
                            </div>
                            
                            <div class="alert alert-warning mt-3">
                                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                                <strong>Important Note:</strong> This meal plan is a general guide. Always consult with your healthcare provider or a registered dietitian for personalized nutrition advice.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Floating Chatbot Button -->
        <div class="chatbot-button" onclick="toggleChatbot()">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        
        <!-- Chatbot Popup -->
        <div class="chatbot-popup" id="chatbotPopup">
            <div class="chatbot-header">
                <div>
                    <i class="bi bi-robot me-2"></i>
                    NeoMitra Assistant
                </div>
                <button class="btn-close btn-close-white" onclick="toggleChatbot()"></button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="message bot-message">
                    Hello! I'm your NeoMitra nutrition assistant. How can I help you with your meal plan today?
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" id="chatbotInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                <button class="btn btn-primary" onclick="sendMessage()">
                    <i class="bi bi-send"></i>
                </button>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Chatbot functionality
            let chatbotOpen = false;
            
            function toggleChatbot() {
                chatbotOpen = !chatbotOpen;
                document.getElementById('chatbotPopup').style.display = chatbotOpen ? 'flex' : 'none';
                if (chatbotOpen) {
                    document.getElementById('chatbotInput').focus();
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('chatbotInput');
                const message = input.value.trim();
                
                if (message) {
                    // Add user message
                    addMessage(message, 'user');
                    input.value = '';
                    
                    // Simulate bot response
                    setTimeout(() => {
                        let response = '';
                        
                        if (message.toLowerCase().includes('iron')) {
                            response = "Iron-rich foods in your meal plan include spinach, lentils, lean red meat, and fortified cereals. These are important for preventing anemia, especially during pregnancy.";
                        } else if (message.toLowerCase().includes('portion')) {
                            response = "Portion sizes should be adjusted based on your individual needs. Generally, fill half your plate with vegetables, a quarter with protein, and a quarter with whole grains.";
                        } else if (message.toLowerCase().includes('substitute') || message.toLowerCase().includes('alternative')) {
                            response = "You can substitute ingredients based on your preferences or dietary restrictions. For example, if you don't eat fish, you can replace salmon with tofu or legumes for protein.";
                        } else if (message.toLowerCase().includes('vegetarian') || message.toLowerCase().includes('vegan')) {
                            response = "For a vegetarian version of this meal plan, you can replace meat with plant-based proteins like tofu, tempeh, legumes, and quinoa. Make sure to include vitamin B12 supplementation for vegan diets.";
                        } else {
                            response = "Thank you for your question about the meal plan. Is there something specific you'd like to know about nutrition during pregnancy or how to adapt these recipes?";
                        }
                        
                        addMessage(response, 'bot');
                    }, 1000);
                }
            }
            
            function addMessage(text, sender) {
                const messagesContainer = document.getElementById('chatbotMessages');
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                messageElement.textContent = text;
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """, username=session.get('username', 'User'))
    
@app.route('/nutrition/shopping-list')
def shopping_list():
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shopping List - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .shopping-category {
                margin-bottom: 2rem;
            }
            .shopping-item {
                padding: 1rem;
                border-radius: 8px;
                background-color: white;
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                transition: all 0.2s;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .shopping-item:hover {
                box-shadow: 0 5px 10px rgba(0,0,0,0.1);
            }
            .shopping-item label {
                margin: 0;
                display: flex;
                align-items: center;
                width: 100%;
                cursor: pointer;
            }
            .item-checkbox {
                margin-right: 1rem;
                width: 20px;
                height: 20px;
            }
            .item-info {
                flex: 1;
            }
            .item-quantity {
                color: #6c757d;
                font-size: 0.9rem;
                margin-left: auto;
                padding-left: 10px;
            }
            .item-checked {
                text-decoration: line-through;
                opacity: 0.6;
            }
            .print-section {
                background-color: rgba(var(--bs-primary-rgb), 0.1);
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 2rem;
            }
            .list-stats {
                display: flex;
                justify-content: space-between;
                margin-bottom: 1rem;
            }
            .stat-item {
                text-align: center;
                padding: 1rem;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .stat-number {
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--bs-primary);
            }
            .stat-label {
                font-size: 0.9rem;
                color: #6c757d;
            }
            /* Floating chatbot button */
            .chatbot-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: var(--bs-primary);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s;
            }
            .chatbot-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
            }
            .chatbot-popup {
                position: fixed;
                bottom: 90px;
                right: 20px;
                width: 350px;
                height: 500px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
                z-index: 999;
                display: none;
                flex-direction: column;
                overflow: hidden;
            }
            .chatbot-header {
                background-color: var(--bs-primary);
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
            }
            .chatbot-input {
                border-top: 1px solid #e0e0e0;
                padding: 10px;
                display: flex;
            }
            .chatbot-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin-right: 10px;
            }
            .message {
                margin-bottom: 10px;
                max-width: 80%;
            }
            .user-message {
                background-color: var(--bs-primary);
                color: white;
                padding: 10px 15px;
                border-radius: 18px 18px 0 18px;
                align-self: flex-end;
                margin-left: auto;
            }
            .bot-message {
                background-color: #f1f1f1;
                color: #333;
                padding: 10px 15px;
                border-radius: 18px 18px 18px 0;
                align-self: flex-start;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link active">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Shopping List</h2>
                        <div>
                            <a href="/nutrition" class="btn btn-outline-primary me-2">
                                <i class="bi bi-arrow-left me-2"></i>
                                Back to Nutrition Guide
                            </a>
                            <a href="/nutrition/meal-planner" class="btn btn-outline-primary me-2">
                                <i class="bi bi-calendar-week me-2"></i>
                                View Meal Plan
                            </a>
                            <button class="btn btn-primary" onclick="window.print()">
                                <i class="bi bi-printer me-2"></i>
                                Print List
                            </button>
                        </div>
                    </div>
                    
                    <div class="print-section mt-4">
                        <div class="row">
                            <div class="col-md-8">
                                <h5>Weekly Shopping List: March 30 - April 5, 2025</h5>
                                <p>This shopping list is generated based on your personalized meal plan, focusing on iron-rich foods to support your current health needs.</p>
                            </div>
                            <div class="col-md-4 text-end">
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" id="showCheckedItems" checked>
                                    <label class="form-check-label" for="showCheckedItems">Show checked items</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row mt-3">
                            <div class="col-md-4">
                                <div class="stat-item">
                                    <div class="stat-number">32</div>
                                    <div class="stat-label">Total Items</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="stat-item">
                                    <div class="stat-number">15</div>
                                    <div class="stat-label">Iron-Rich Items</div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="stat-item">
                                    <div class="stat-number">12</div>
                                    <div class="stat-label">Vitamin-Rich Items</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <!-- Produce Section -->
                            <div class="shopping-category">
                                <h4><i class="bi bi-flower1 text-success me-2"></i>Produce</h4>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Fresh Spinach</div>
                                        <div class="item-quantity">2 bunches</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Broccoli</div>
                                        <div class="item-quantity">1 head</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Carrots</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Bell Peppers (assorted colors)</div>
                                        <div class="item-quantity">3</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Onions</div>
                                        <div class="item-quantity">3</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Garlic</div>
                                        <div class="item-quantity">1 head</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Lemons</div>
                                        <div class="item-quantity">2</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Mixed Berries</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Oranges</div>
                                        <div class="item-quantity">4</div>
                                    </label>
                                </div>
                            </div>
                            
                            <!-- Proteins Section -->
                            <div class="shopping-category">
                                <h4><i class="bi bi-egg me-2 text-warning"></i>Proteins</h4>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Eggs</div>
                                        <div class="item-quantity">1 dozen</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Chicken Breast</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Salmon Fillets</div>
                                        <div class="item-quantity">300g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Lean Beef</div>
                                        <div class="item-quantity">250g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Tofu (firm)</div>
                                        <div class="item-quantity">1 block</div>
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <!-- Grains & Legumes Section -->
                            <div class="shopping-category">
                                <h4><i class="bi bi-grid me-2 text-warning"></i>Grains & Legumes</h4>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Lentils (dry)</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Quinoa</div>
                                        <div class="item-quantity">250g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Brown Rice</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Whole Grain Bread</div>
                                        <div class="item-quantity">1 loaf</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Rolled Oats</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Whole Grain Wraps</div>
                                        <div class="item-quantity">1 pack</div>
                                    </label>
                                </div>
                            </div>
                            
                            <!-- Dairy & Alternatives Section -->
                            <div class="shopping-category">
                                <h4><i class="bi bi-cup me-2 text-info"></i>Dairy & Alternatives</h4>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Greek Yogurt</div>
                                        <div class="item-quantity">500g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Feta Cheese</div>
                                        <div class="item-quantity">200g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Milk (low-fat)</div>
                                        <div class="item-quantity">1L</div>
                                    </label>
                                </div>
                            </div>
                            
                            <!-- Pantry Items Section -->
                            <div class="shopping-category">
                                <h4><i class="bi bi-basket me-2 text-secondary"></i>Pantry Items</h4>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Olive Oil</div>
                                        <div class="item-quantity">1 bottle</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Flaxseeds</div>
                                        <div class="item-quantity">100g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Chia Seeds</div>
                                        <div class="item-quantity">100g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Mixed Nuts</div>
                                        <div class="item-quantity">250g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Dried Apricots</div>
                                        <div class="item-quantity">100g</div>
                                    </label>
                                </div>
                                
                                <div class="shopping-item">
                                    <label>
                                        <input type="checkbox" class="item-checkbox">
                                        <div class="item-info">Honey</div>
                                        <div class="item-quantity">1 jar</div>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Floating Chatbot Button -->
        <div class="chatbot-button" onclick="toggleChatbot()">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        
        <!-- Chatbot Popup -->
        <div class="chatbot-popup" id="chatbotPopup">
            <div class="chatbot-header">
                <div>
                    <i class="bi bi-robot me-2"></i>
                    NeoMitra Assistant
                </div>
                <button class="btn-close btn-close-white" onclick="toggleChatbot()"></button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="message bot-message">
                    Hello! I'm your NeoMitra shopping assistant. Need help finding alternatives or understanding why certain items are on your list?
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" id="chatbotInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                <button class="btn btn-primary" onclick="sendMessage()">
                    <i class="bi bi-send"></i>
                </button>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Shopping list functionality
            document.addEventListener('DOMContentLoaded', function() {
                const checkboxes = document.querySelectorAll('.item-checkbox');
                const showCheckedItems = document.getElementById('showCheckedItems');
                
                // Handle checkbox changes
                checkboxes.forEach(checkbox => {
                    checkbox.addEventListener('change', function() {
                        const item = this.closest('.shopping-item');
                        if (this.checked) {
                            item.classList.add('item-checked');
                        } else {
                            item.classList.remove('item-checked');
                        }
                        updateVisibility();
                    });
                });
                
                // Handle show/hide toggle
                showCheckedItems.addEventListener('change', updateVisibility);
                
                function updateVisibility() {
                    const hideChecked = !showCheckedItems.checked;
                    document.querySelectorAll('.item-checked').forEach(item => {
                        item.style.display = hideChecked ? 'none' : 'flex';
                    });
                }
            });
            
            // Chatbot functionality
            let chatbotOpen = false;
            
            function toggleChatbot() {
                chatbotOpen = !chatbotOpen;
                document.getElementById('chatbotPopup').style.display = chatbotOpen ? 'flex' : 'none';
                if (chatbotOpen) {
                    document.getElementById('chatbotInput').focus();
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('chatbotInput');
                const message = input.value.trim();
                
                if (message) {
                    // Add user message
                    addMessage(message, 'user');
                    input.value = '';
                    
                    // Simulate bot response
                    setTimeout(() => {
                        let response = '';
                        
                        if (message.toLowerCase().includes('iron')) {
                            response = "Iron-rich foods on your shopping list include spinach, lentils, lean beef, and dried apricots. These are important for preventing anemia, especially during pregnancy.";
                        } else if (message.toLowerCase().includes('substitute') || message.toLowerCase().includes('alternative')) {
                            response = "You can substitute any items based on availability. For example, if spinach is not available, you can use kale or swiss chard as an alternative source of iron and other nutrients.";
                        } else if (message.toLowerCase().includes('vegetarian') || message.toLowerCase().includes('vegan')) {
                            response = "For a vegetarian shopping list, you can skip the meat and fish items and add more plant-based proteins like chickpeas, black beans, and meat alternatives. Make sure to include vitamin B12 supplementation for vegan diets.";
                        } else if (message.toLowerCase().includes('budget') || message.toLowerCase().includes('cheap')) {
                            response = "To make this shopping list more budget-friendly, you can prioritize seasonal produce, buy in bulk when possible, and replace some fresh items with frozen alternatives, which are often more affordable and just as nutritious.";
                        } else {
                            response = "Thank you for your question about the shopping list. Is there something specific you'd like to know about certain ingredients or how to modify the list to suit your needs?";
                        }
                        
                        addMessage(response, 'bot');
                    }, 1000);
                }
            }
            
            function addMessage(text, sender) {
                const messagesContainer = document.getElementById('chatbotMessages');
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                messageElement.textContent = text;
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

# Routes for government scheme details
@app.route('/scheme/<scheme_id>')
def scheme_details(scheme_id):
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Dictionary of scheme details
    schemes = {
        'pmsma': {
            'name': 'Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA)',
            'logo': 'https://via.placeholder.com/150x150?text=PMSMA',
            'description': 'The Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA) is an initiative to provide free antenatal care to pregnant women on the 9th of every month throughout the country. The program aims to improve the quality and coverage of antenatal care, including early detection and management of high-risk pregnancies.',
            'eligibility': [
                'All pregnant women',
                'No income criteria',
                'Special focus on rural, tribal, and urban slum areas',
                'Priority for women who have not received antenatal care'
            ],
            'benefits': [
                'Free comprehensive antenatal check-ups by specialists/physicians',
                'Free screening for anemia, blood pressure, blood sugar, and other pregnancy complications',
                'Free ultrasound scans',
                'Identification and follow-up of high-risk pregnancies',
                'Counseling on nutrition, birth preparedness, and complications readiness'
            ],
            'process': [
                'Visit your nearest health facility (Primary Health Center, Community Health Center, or District Hospital) on the 9th of any month',
                'Bring any existing health records and your Mother and Child Protection (MCP) card if available',
                'Register at the facility for the check-up',
                'Complete the check-up with the available specialists'
            ],
            'documents': [
                'Identity proof (Aadhaar card, voter ID, or any government-issued ID)',
                'Address proof',
                'Previous medical/pregnancy records (if available)',
                'Mother and Child Protection (MCP) card (if already issued)'
            ],
            'contact': {
                'website': 'https://www.pmsma.nhp.gov.in/',
                'helpline': '1800-180-1104',
                'email': 'pmsma@gov.in'
            }
        },
        'jsy': {
            'name': 'Janani Suraksha Yojana (JSY)',
            'logo': 'https://via.placeholder.com/150x150?text=JSY',
            'description': 'Janani Suraksha Yojana (JSY) is a safe motherhood intervention under the National Health Mission. It promotes institutional delivery among pregnant women, especially those from low-income households, to reduce maternal and neonatal mortality by providing cash assistance.',
            'eligibility': [
                'Pregnant women from Below Poverty Line (BPL) families',
                'Scheduled Caste/Scheduled Tribe women',
                'Women from rural areas delivering in public health facilities',
                'In urban areas, BPL women who deliver in public or accredited private institutions'
            ],
            'benefits': [
                'Cash assistance of ₹1,400 in rural areas and ₹1,000 in urban areas for non-high focus states',
                'Cash assistance of ₹1,000 in rural areas and ₹600 in urban areas for high focus states',
                'Free delivery services including cesarean section',
                'Free transport from home to institution and back',
                'Free diet during stay in the facility'
            ],
            'process': [
                'Register at the nearest Anganwadi center or with ASHA worker during pregnancy',
                'Carry out at least three antenatal check-ups',
                'Deliver at a government health facility or an accredited private institution',
                'Submit the required documents after delivery to claim the cash assistance'
            ],
            'documents': [
                'BPL card or SC/ST certificate',
                'Identity proof (Aadhaar card, voter ID)',
                'Mother and Child Protection (MCP) card',
                'ANC check-up records',
                'Birth certificate of the child'
            ],
            'contact': {
                'website': 'https://nhm.gov.in/index1.php?lang=1&level=3&sublinkid=841&lid=309',
                'helpline': '1800-180-1104',
                'email': 'jsy@gov.in'
            }
        },
        'pmjay': {
            'name': 'Pradhan Mantri Jan Arogya Yojana (PMJAY)',
            'logo': 'https://via.placeholder.com/150x150?text=PMJAY',
            'description': 'Pradhan Mantri Jan Arogya Yojana (PMJAY), also known as Ayushman Bharat, is a health insurance scheme that aims to provide free access to healthcare for low-income earners in the country. The scheme provides a cover of ₹5 lakhs per family per year for secondary and tertiary care hospitalization.',
            'eligibility': [
                'Families identified through Socio-Economic Caste Census (SECC) data',
                'No cap on family size and age of members',
                'Covers both rural and urban families who fall under the deprivation criteria',
                'Families covered under existing RSBY scheme'
            ],
            'benefits': [
                'Health coverage up to ₹5 lakh per family per year',
                'Coverage for pre and post-hospitalization expenses',
                'All pre-existing conditions covered from day one',
                'Cashless and paperless access to services',
                'More than 1,393 procedures covered, including maternal health services'
            ],
            'process': [
                'Check eligibility through PMJAY website or app',
                'Visit the nearest empaneled hospital with valid identification',
                'Get verified through your Aadhaar number or ration card',
                'After verification, receive treatment without paying anything upfront'
            ],
            'documents': [
                'Aadhaar card (preferred) or alternative government ID',
                'PMJAY e-card (if already issued)',
                'Proof of residence',
                'BPL card or ration card (if applicable)'
            ],
            'contact': {
                'website': 'https://pmjay.gov.in/',
                'helpline': '14555 or 1800-111-565',
                'email': 'pmjay@nha.gov.in'
            }
        },
        'rbsk': {
            'name': 'Rashtriya Bal Swasthya Karyakram (RBSK)',
            'logo': 'https://via.placeholder.com/150x150?text=RBSK',
            'description': 'Rashtriya Bal Swasthya Karyakram (RBSK) is a child health screening and early intervention service program under the National Health Mission. It aims to identify and manage children from birth to 18 years for 4 Ds - Defects at birth, Diseases, Deficiencies, and Developmental delays including disabilities.',
            'eligibility': [
                'All children from birth to 18 years of age',
                'Children enrolled in anganwadis',
                'Students in government and government-aided schools',
                'Out-of-school children'
            ],
            'benefits': [
                'Free health screening for early detection of 4 Ds',
                'Free referral support, treatment, and management at tertiary facilities',
                'Free surgeries for birth defects like congenital heart disease, club foot, etc.',
                'Child health screening and intervention services',
                'Provision of mobility aids, hearing aids, and other assistive devices as needed'
            ],
            'process': [
                'Children are screened at birthing facilities, anganwadis, or schools by RBSK mobile health teams',
                'If any health condition is detected, the child is referred to higher facilities',
                'District Early Intervention Centers (DEICs) provide comprehensive management and follow-up',
                'Regular follow-ups are conducted to monitor progress'
            ],
            'documents': [
                'Birth certificate or age proof',
                'Identity card of parent/guardian',
                'Address proof',
                'RBSK health card (if already issued)'
            ],
            'contact': {
                'website': 'https://nhm.gov.in/index1.php?lang=1&level=4&sublinkid=1190&lid=583',
                'helpline': '1800-180-1104',
                'email': 'rbsk@gov.in'
            }
        },
        'npcdcs': {
            'name': 'National Programme for Prevention and Control of Diabetes',
            'logo': 'https://via.placeholder.com/150x150?text=NPCDCS',
            'description': 'The National Programme for Prevention and Control of Cancer, Diabetes, Cardiovascular Diseases and Stroke (NPCDCS) aims to prevent and control major non-communicable diseases (NCDs) through health promotion, early diagnosis, and management of common NCDs. It has a special focus on diabetes management and prevention.',
            'eligibility': [
                'All citizens, with a focus on those at risk of diabetes and other NCDs',
                'Individuals with a family history of diabetes',
                'People with obesity, high blood pressure, or sedentary lifestyle',
                'Pregnant women for gestational diabetes screening'
            ],
            'benefits': [
                'Free screening for diabetes and other NCDs',
                'Free or subsidized treatment for diagnosed cases',
                'Regular follow-up and monitoring',
                'Health education and counseling on lifestyle modification',
                'Support for management of complications'
            ],
            'process': [
                'Visit the nearest NCD clinic or health center for screening',
                'Complete the risk assessment form',
                'Undergo free blood sugar testing and other relevant examinations',
                'If diagnosed, register for treatment and follow-up services',
                'Attend regular check-ups as advised by healthcare providers'
            ],
            'documents': [
                'Identity proof',
                'Address proof',
                'Previous medical records (if available)',
                'Family history documentation (if available)'
            ],
            'contact': {
                'website': 'https://npcdcs.nhp.gov.in/',
                'helpline': '1800-180-1104',
                'email': 'npcdcs@gov.in'
            }
        }
    }
    
    # Get the scheme details or return 404 if not found
    scheme = schemes.get(scheme_id)
    if not scheme:
        return render_template_string("Scheme not found"), 404
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ scheme.name }} - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .scheme-banner {
                background-color: rgba(var(--bs-primary-rgb), 0.1);
                border-radius: 12px;
                padding: 30px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 30px;
            }
            .scheme-logo {
                max-width: 150px;
                max-height: 150px;
                border-radius: 10px;
            }
            .scheme-header h2 {
                margin-bottom: 10px;
            }
            .scheme-meta {
                display: flex;
                gap: 15px;
                margin-top: 15px;
            }
            .scheme-meta-item {
                display: flex;
                align-items: center;
                font-size: 0.9rem;
                color: #6c757d;
            }
            .scheme-meta-item i {
                margin-right: 5px;
                font-size: 1.1rem;
                color: var(--bs-primary);
            }
            .section-card {
                margin-bottom: 20px;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            .section-header {
                background-color: var(--bs-primary);
                color: white;
                padding: 15px 20px;
                font-weight: 600;
                display: flex;
                align-items: center;
            }
            .section-header i {
                margin-right: 10px;
                font-size: 1.2rem;
            }
            .section-body {
                padding: 20px;
                background-color: white;
            }
            .list-custom {
                padding-left: 0;
                list-style: none;
            }
            .list-custom li {
                position: relative;
                padding-left: 30px;
                margin-bottom: 10px;
                line-height: 1.5;
            }
            .list-custom li:before {
                content: '\\2713';
                position: absolute;
                left: 0;
                top: 0;
                color: var(--bs-primary);
                font-weight: bold;
            }
            .process-step {
                display: flex;
                margin-bottom: 15px;
            }
            .step-number {
                width: 30px;
                height: 30px;
                background-color: var(--bs-primary);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                margin-right: 15px;
                flex-shrink: 0;
            }
            .step-content {
                flex: 1;
            }
            .contact-item {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            .contact-icon {
                width: 40px;
                height: 40px;
                background-color: rgba(var(--bs-primary-rgb), 0.1);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 15px;
                color: var(--bs-primary);
                font-size: 1.2rem;
            }
            .apply-section {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 30px;
                text-align: center;
            }
            .print-section {
                display: flex;
                justify-content: center;
                margin-top: 30px;
                padding: 15px;
                border-top: 1px solid #e0e0e0;
            }
            /* Floating chatbot button */
            .chatbot-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: var(--bs-primary);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s;
            }
            .chatbot-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
            }
            .chatbot-popup {
                position: fixed;
                bottom: 90px;
                right: 20px;
                width: 350px;
                height: 500px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
                z-index: 999;
                display: none;
                flex-direction: column;
                overflow: hidden;
            }
            .chatbot-header {
                background-color: var(--bs-primary);
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
            }
            .chatbot-input {
                border-top: 1px solid #e0e0e0;
                padding: 10px;
                display: flex;
            }
            .chatbot-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin-right: 10px;
            }
            .message {
                margin-bottom: 10px;
                max-width: 80%;
            }
            .user-message {
                background-color: var(--bs-primary);
                color: white;
                padding: 10px 15px;
                border-radius: 18px 18px 0 18px;
                align-self: flex-end;
                margin-left: auto;
            }
            .bot-message {
                background-color: #f1f1f1;
                color: #333;
                padding: 10px 15px;
                border-radius: 18px 18px 18px 0;
                align-self: flex-start;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link active">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Government Scheme Details</h2>
                        <div>
                            <a href="/government_schemes" class="btn btn-outline-primary">
                                <i class="bi bi-arrow-left me-2"></i>
                                Back to Schemes
                            </a>
                        </div>
                    </div>
                    
                    <!-- Scheme Banner -->
                    <div class="scheme-banner">
                        <img src="{{ scheme.logo }}" alt="{{ scheme.name }} Logo" class="scheme-logo">
                        <div class="scheme-header">
                            <h2>{{ scheme.name }}</h2>
                            <p class="text-muted">Government of India Initiative</p>
                            <div class="scheme-meta">
                                <div class="scheme-meta-item">
                                    <i class="bi bi-check-circle-fill"></i>
                                    <span>Official Program</span>
                                </div>
                                <div class="scheme-meta-item">
                                    <i class="bi bi-people-fill"></i>
                                    <span>Nationwide Coverage</span>
                                </div>
                                <div class="scheme-meta-item">
                                    <i class="bi bi-star-fill"></i>
                                    <span>High Priority Scheme</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-8">
                            <!-- Description Section -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-info-circle"></i>
                                    About the Scheme
                                </div>
                                <div class="section-body">
                                    <p>{{ scheme.description }}</p>
                                </div>
                            </div>
                            
                            <!-- Eligibility Section -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-person-check"></i>
                                    Eligibility Criteria
                                </div>
                                <div class="section-body">
                                    <ul class="list-custom">
                                        {% for item in scheme.eligibility %}
                                        <li>{{ item }}</li>
                                        {% endfor %}
                                    </ul>
                                </div>
                            </div>
                            
                            <!-- Benefits Section -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-gift"></i>
                                    Benefits
                                </div>
                                <div class="section-body">
                                    <ul class="list-custom">
                                        {% for item in scheme.benefits %}
                                        <li>{{ item }}</li>
                                        {% endfor %}
                                    </ul>
                                </div>
                            </div>
                            
                            <!-- Application Process Section -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-clipboard-check"></i>
                                    How to Apply
                                </div>
                                <div class="section-body">
                                    {% for item in scheme.process %}
                                    <div class="process-step">
                                        <div class="step-number">{{ loop.index }}</div>
                                        <div class="step-content">{{ item }}</div>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4">
                            <!-- Required Documents -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-file-earmark-text"></i>
                                    Required Documents
                                </div>
                                <div class="section-body">
                                    <ul class="list-custom">
                                        {% for item in scheme.documents %}
                                        <li>{{ item }}</li>
                                        {% endfor %}
                                    </ul>
                                </div>
                            </div>
                            
                            <!-- Contact Information -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-telephone"></i>
                                    Contact Information
                                </div>
                                <div class="section-body">
                                    <div class="contact-item">
                                        <div class="contact-icon">
                                            <i class="bi bi-globe"></i>
                                        </div>
                                        <div>
                                            <strong>Website</strong><br>
                                            <a href="{{ scheme.contact.website }}" target="_blank">{{ scheme.contact.website }}</a>
                                        </div>
                                    </div>
                                    
                                    <div class="contact-item">
                                        <div class="contact-icon">
                                            <i class="bi bi-telephone"></i>
                                        </div>
                                        <div>
                                            <strong>Helpline</strong><br>
                                            {{ scheme.contact.helpline }}
                                        </div>
                                    </div>
                                    
                                    <div class="contact-item">
                                        <div class="contact-icon">
                                            <i class="bi bi-envelope"></i>
                                        </div>
                                        <div>
                                            <strong>Email</strong><br>
                                            <a href="mailto:{{ scheme.contact.email }}">{{ scheme.contact.email }}</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Nearby Facilities -->
                            <div class="section-card">
                                <div class="section-header">
                                    <i class="bi bi-geo-alt"></i>
                                    Nearby Application Centers
                                </div>
                                <div class="section-body">
                                    <p>Based on your location, here are the nearest facilities where you can apply for this scheme:</p>
                                    
                                    <div class="list-group">
                                        <a href="#" class="list-group-item list-group-item-action">
                                            <div class="d-flex w-100 justify-content-between">
                                                <h6 class="mb-1">Primary Health Center, Sector 10</h6>
                                                <small>1.2 km</small>
                                            </div>
                                            <small class="text-muted">Open 9:00 AM - 5:00 PM</small>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action">
                                            <div class="d-flex w-100 justify-content-between">
                                                <h6 class="mb-1">Community Health Center, Main Road</h6>
                                                <small>3.5 km</small>
                                            </div>
                                            <small class="text-muted">Open 8:00 AM - 8:00 PM</small>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action">
                                            <div class="d-flex w-100 justify-content-between">
                                                <h6 class="mb-1">District Hospital, Central Area</h6>
                                                <small>5.8 km</small>
                                            </div>
                                            <small class="text-muted">Open 24 hours</small>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Apply Section -->
                            <div class="apply-section">
                                <h5 class="mb-3">Ready to Apply?</h5>
                                <p>Our NeoMitra assistant can help you complete the application process step by step.</p>
                                <button class="btn btn-primary" id="applyButton">
                                    <i class="bi bi-pencil-square me-2"></i>
                                    Start Application Process
                                </button>
                            </div>
                            
                            <!-- Print Section -->
                            <div class="print-section">
                                <button class="btn btn-outline-primary" onclick="window.print()">
                                    <i class="bi bi-printer me-2"></i>
                                    Print Scheme Details
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Floating Chatbot Button -->
        <div class="chatbot-button" onclick="toggleChatbot()">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        
        <!-- Chatbot Popup -->
        <div class="chatbot-popup" id="chatbotPopup">
            <div class="chatbot-header">
                <div>
                    <i class="bi bi-robot me-2"></i>
                    NeoMitra Assistant
                </div>
                <button class="btn-close btn-close-white" onclick="toggleChatbot()"></button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="message bot-message">
                    Hello! I can help you understand and apply for the {{ scheme.name }}. What would you like to know about this scheme?
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" id="chatbotInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                <button class="btn btn-primary" onclick="sendMessage()">
                    <i class="bi bi-send"></i>
                </button>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Chatbot functionality
            let chatbotOpen = false;
            
            function toggleChatbot() {
                chatbotOpen = !chatbotOpen;
                document.getElementById('chatbotPopup').style.display = chatbotOpen ? 'flex' : 'none';
                if (chatbotOpen) {
                    document.getElementById('chatbotInput').focus();
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            // Apply button also opens chatbot
            document.getElementById('applyButton').addEventListener('click', function() {
                if (!chatbotOpen) toggleChatbot();
                setTimeout(() => {
                    addMessage("I want to apply for this scheme. Can you guide me through the process?", 'user');
                    setTimeout(() => {
                        addMessage("I'd be happy to help you apply for the {{ scheme.name }}. Let's start with checking your eligibility. Could you please tell me if you meet these criteria: {{ scheme.eligibility[0] }}?", 'bot');
                    }, 1000);
                }, 500);
            });
            
            function sendMessage() {
                const input = document.getElementById('chatbotInput');
                const message = input.value.trim();
                
                if (message) {
                    // Add user message
                    addMessage(message, 'user');
                    input.value = '';
                    
                    // Simulate bot response
                    setTimeout(() => {
                        let response = '';
                        
                        if (message.toLowerCase().includes('eligibility') || message.toLowerCase().includes('qualify')) {
                            response = "To be eligible for {{ scheme.name }}, you should meet these criteria: {% for item in scheme.eligibility %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}.";
                        } else if (message.toLowerCase().includes('document') || message.toLowerCase().includes('paper')) {
                            response = "You'll need the following documents: {% for item in scheme.documents %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}.";
                        } else if (message.toLowerCase().includes('benefit') || message.toLowerCase().includes('advantage')) {
                            response = "This scheme provides several benefits including: {% for item in scheme.benefits %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}.";
                        } else if (message.toLowerCase().includes('apply') || message.toLowerCase().includes('how to')) {
                            response = "To apply, follow these steps: {% for item in scheme.process %}{{ loop.index }}. {{ item }}{% if not loop.last %}, {% endif %}{% endfor %}.";
                        } else if (message.toLowerCase().includes('contact') || message.toLowerCase().includes('helpline')) {
                            response = "You can contact the scheme administrators via: Helpline: {{ scheme.contact.helpline }}, Email: {{ scheme.contact.email }}, or visit their website: {{ scheme.contact.website }}.";
                        } else {
                            response = "Thank you for your question about {{ scheme.name }}. Is there something specific about the eligibility, benefits, application process, or required documents that you'd like to know?";
                        }
                        
                        addMessage(response, 'bot');
                    }, 1000);
                }
            }
            
            function addMessage(text, sender) {
                const messagesContainer = document.getElementById('chatbotMessages');
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                messageElement.textContent = text;
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """, scheme=scheme, username=session.get('username', 'User'))
    
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

# Index page as landing page
@app.route('/')
def index():
    # Go directly to home page showing website features
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NeoMitra - Complete Health Platform</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #7952b3;
                --secondary-color: #6f42c1;
                --border-radius: 8px;
                --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                --transition: all 0.3s ease;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .navbar {
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 0.8rem 1rem;
            }
            
            .navbar-brand {
                display: flex;
                align-items: center;
                font-weight: 700;
                font-size: 1.5rem;
            }
            
            .navbar-brand i {
                margin-right: 0.5rem;
                font-size: 1.8rem;
            }
            
            .hero-section {
                position: relative;
                height: 80vh;
                background: linear-gradient(135deg, #7952b3 0%, #1e88e5 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
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
            
            .wave-bottom {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 100px;
                background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="1" d="M0,96L80,112C160,128,320,160,480,160C640,160,800,128,960,128C1120,128,1280,160,1360,176L1440,192L1440,320L1360,320C1280,320,1120,320,960,320C800,320,640,320,480,320C320,320,80,320L0,320Z"></path></svg>') no-repeat;
                background-size: 100% 100%;
            }
            
            .features-section {
                padding: 5rem 0;
            }
            
            .section-title {
                text-align: center;
                margin-bottom: 3rem;
                color: var(--primary-color);
                font-weight: 700;
            }
            
            .feature-card {
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
            
            .about-section {
                padding: 5rem 0;
                background-color: #f8f9fa;
            }
            
            .about-img {
                max-width: 100%;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
            }
            
            .how-it-works {
                padding: 5rem 0;
            }
            
            .step-card {
                text-align: center;
                padding: 2rem;
                transition: var(--transition);
            }
            
            .step-number {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background-color: var(--primary-color);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 1.5rem;
                margin: 0 auto 1.5rem;
            }
            
            .testimonials {
                padding: 5rem 0;
                background-color: #f8f9fa;
            }
            
            .testimonial-card {
                padding: 2rem;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                margin-bottom: 2rem;
                position: relative;
            }
            
            .testimonial-text {
                font-style: italic;
                margin-bottom: 1.5rem;
            }
            
            .testimonial-author {
                display: flex;
                align-items: center;
            }
            
            .testimonial-author img {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                margin-right: 1rem;
            }
            
            .author-info h5 {
                margin-bottom: 0.2rem;
                font-weight: 600;
            }
            
            .author-info p {
                margin-bottom: 0;
                font-size: 0.9rem;
                opacity: 0.7;
            }
            
            .quote-icon {
                position: absolute;
                top: -15px;
                right: 20px;
                font-size: 3rem;
                color: var(--primary-color);
                opacity: 0.2;
            }
            
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
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light bg-white">
            <div class="container">
                <a class="navbar-brand text-primary" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link active text-dark" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="/health_records">Health Records</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="/risk_assessment">Risk Assessment</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="/government_schemes">Government Schemes</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="/nutrition">Nutrition Guide</a>
                        </li>
                    </ul>
                    <div class="d-flex">
                        <a href="/login" class="btn btn-outline-primary me-2">Login</a>
                        <a href="/register" class="btn btn-primary">Register</a>
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Hero Section -->
        <section class="hero-section text-light">
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
                            <p>Easily record and monitor vital health metrics for everyone, including specialized tracking for pregnancy, anemia, and diabetes.</p>
                            <a href="/health_records" class="btn btn-sm btn-primary mt-3">Learn More</a>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-shield-check"></i>
                            </div>
                            <h3 class="feature-title">Risk Assessment</h3>
                            <p>AI-powered risk assessment for health conditions including anemia and diabetes for all users, with additional pregnancy monitoring for women.</p>
                            <a href="/risk_assessment" class="btn btn-sm btn-primary mt-3">Learn More</a>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-chat-dots"></i>
                            </div>
                            <h3 class="feature-title">Chatbot Assistant</h3>
                            <p>Get immediate answers to all your health questions about anemia, diabetes, and pregnancy in your preferred language.</p>
                            <a href="/chatbot" class="btn btn-sm btn-primary mt-3">Try It Now</a>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-bank"></i>
                            </div>
                            <h3 class="feature-title">Government Schemes</h3>
                            <p>Stay informed about government healthcare schemes for all health conditions including diabetes, anemia, and pregnancy care.</p>
                            <a href="/government_schemes" class="btn btn-sm btn-primary mt-3">View Schemes</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- About Section -->
        <section class="about-section">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-6 mb-4 mb-lg-0">
                        <h2 class="section-title text-start">About NeoMitra</h2>
                        <p class="mb-4">NeoMitra is a comprehensive healthcare platform designed to provide accessible healthcare information and services to everyone, particularly in areas with limited healthcare access.</p>
                        <p class="mb-4">Our platform offers personalized health tracking, risk assessments for various conditions, and localized information in multiple languages to ensure that healthcare knowledge is available to all, regardless of location or language barriers.</p>
                        <div class="d-flex flex-wrap gap-2">
                            <div class="badge bg-primary p-2 rounded-pill"><i class="bi bi-translate me-1"></i> Multiple Languages</div>
                            <div class="badge bg-primary p-2 rounded-pill"><i class="bi bi-shield-check me-1"></i> Data Security</div>
                            <div class="badge bg-primary p-2 rounded-pill"><i class="bi bi-hand-thumbs-up me-1"></i> User Friendly</div>
                            <div class="badge bg-primary p-2 rounded-pill"><i class="bi bi-heart-pulse me-1"></i> Health Focused</div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <img src="https://source.unsplash.com/random/600x400/?healthcare" alt="Healthcare" class="about-img img-fluid">
                    </div>
                </div>
            </div>
        </section>
        
        <!-- How It Works -->
        <section class="how-it-works">
            <div class="container">
                <h2 class="section-title">How It Works</h2>
                <div class="row">
                    <div class="col-md-4 mb-4 mb-md-0">
                        <div class="step-card">
                            <div class="step-number">1</div>
                            <h4>Create Account</h4>
                            <p>Register with basic information to get started with personalized health tracking.</p>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4 mb-md-0">
                        <div class="step-card">
                            <div class="step-number">2</div>
                            <h4>Enter Health Data</h4>
                            <p>Input your health metrics and medical history for personalized assessments.</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="step-card">
                            <div class="step-number">3</div>
                            <h4>Get Insights</h4>
                            <p>Receive personalized recommendations, risk assessments, and health guidance.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Testimonials -->
        <section class="testimonials">
            <div class="container">
                <h2 class="section-title">What Our Users Say</h2>
                <div class="row">
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="testimonial-card">
                            <div class="quote-icon">
                                <i class="bi bi-quote"></i>
                            </div>
                            <p class="testimonial-text">"NeoMitra has been a lifesaver for me during my pregnancy. The health tracking and risk assessment features have kept me informed and connected to healthcare resources."</p>
                            <div class="testimonial-author">
                                <img src="https://randomuser.me/api/portraits/women/45.jpg" alt="User">
                                <div class="author-info">
                                    <h5>Priya Sharma</h5>
                                    <p>Delhi, India</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="testimonial-card">
                            <div class="quote-icon">
                                <i class="bi bi-quote"></i>
                            </div>
                            <p class="testimonial-text">"As someone with diabetes, the nutrition guide and health tracking features have helped me manage my condition better. The localized information in my native language is incredibly helpful."</p>
                            <div class="testimonial-author">
                                <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="User">
                                <div class="author-info">
                                    <h5>Rajesh Kumar</h5>
                                    <p>Chennai, India</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6 mb-4">
                        <div class="testimonial-card">
                            <div class="quote-icon">
                                <i class="bi bi-quote"></i>
                            </div>
                            <p class="testimonial-text">"The information about government schemes has been invaluable for our village health center. We've been able to help many families access healthcare benefits they didn't know existed."</p>
                            <div class="testimonial-author">
                                <img src="https://randomuser.me/api/portraits/women/68.jpg" alt="User">
                                <div class="author-info">
                                    <h5>Lakshmi Devi</h5>
                                    <p>Health Worker, Rajasthan</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Call to Action -->
        <section class="bg-primary text-light py-5">
            <div class="container text-center">
                <h2 class="mb-4">Ready to take control of your health?</h2>
                <p class="lead mb-4">Join thousands of users who are already benefiting from NeoMitra's comprehensive health platform.</p>
                <div class="d-flex justify-content-center gap-3">
                    <a href="/register" class="btn btn-light btn-lg">Register Now</a>
                    <a href="/learn_more" class="btn btn-outline-light btn-lg">Learn More</a>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer class="bg-dark text-light py-5">
            <div class="container">
                <div class="row">
                    <div class="col-md-4 mb-4 mb-md-0">
                        <h4 class="mb-4"><i class="bi bi-heart-pulse-fill me-2"></i>NeoMitra</h4>
                        <p>A comprehensive healthcare platform for everyone, offering personalized health tracking, risk assessments, and recommendations for various health conditions.</p>
                        <div class="d-flex gap-3 mt-4">
                            <a href="#" class="text-light fs-5"><i class="bi bi-facebook"></i></a>
                            <a href="#" class="text-light fs-5"><i class="bi bi-twitter"></i></a>
                            <a href="#" class="text-light fs-5"><i class="bi bi-instagram"></i></a>
                            <a href="#" class="text-light fs-5"><i class="bi bi-linkedin"></i></a>
                        </div>
                    </div>
                    <div class="col-md-2 mb-4 mb-md-0">
                        <h5 class="mb-4">Quick Links</h5>
                        <ul class="list-unstyled">
                            <li class="mb-2"><a href="/" class="text-light text-decoration-none">Home</a></li>
                            <li class="mb-2"><a href="/about" class="text-light text-decoration-none">About Us</a></li>
                            <li class="mb-2"><a href="/services" class="text-light text-decoration-none">Services</a></li>
                            <li class="mb-2"><a href="/contact" class="text-light text-decoration-none">Contact</a></li>
                        </ul>
                    </div>
                    <div class="col-md-3 mb-4 mb-md-0">
                        <h5 class="mb-4">Health Resources</h5>
                        <ul class="list-unstyled">
                            <li class="mb-2"><a href="/health_records" class="text-light text-decoration-none">Health Records</a></li>
                            <li class="mb-2"><a href="/risk_assessment" class="text-light text-decoration-none">Risk Assessment</a></li>
                            <li class="mb-2"><a href="/government_schemes" class="text-light text-decoration-none">Government Schemes</a></li>
                            <li class="mb-2"><a href="/nutrition" class="text-light text-decoration-none">Nutrition Guide</a></li>
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h5 class="mb-4">Contact Us</h5>
                        <ul class="list-unstyled">
                            <li class="mb-2"><i class="bi bi-geo-alt me-2"></i>123 Healthcare St, Medical City</li>
                            <li class="mb-2"><i class="bi bi-envelope me-2"></i>info@neomitra.com</li>
                            <li class="mb-2"><i class="bi bi-telephone me-2"></i>+91 1234567890</li>
                        </ul>
                    </div>
                </div>
                <hr class="my-4">
                <p class="text-center mb-0">&copy; 2025 NeoMitra. All rights reserved.</p>
            </div>
        </footer>
        
        <!-- Chatbot Button -->
        <div class="chatbot-button" onclick="window.location.href='/chatbot'">
            <i class="bi bi-chat-dots-fill chatbot-icon"></i>
            Ask NeoMitra
        </div>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

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
        <nav class="navbar navbar-expand-lg navbar-light bg-white">
            <div class="container">
                <a class="navbar-brand text-primary" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link active text-dark" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="#">Resources</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="#">Assistant</a>
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

@app.route('/risk_assessment')
def risk_assessment():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Risk Assessment - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .form-check-input:checked {
                background-color: var(--bs-primary);
                border-color: var(--bs-primary);
            }
            .result-card {
                border-radius: 8px;
                margin-bottom: 1.5rem;
            }
            .risk-high {
                background-color: rgba(220, 53, 69, 0.1);
                border-left: 4px solid #dc3545;
            }
            .risk-moderate {
                background-color: rgba(255, 193, 7, 0.1);
                border-left: 4px solid #ffc107;
            }
            .risk-low {
                background-color: rgba(25, 135, 84, 0.1);
                border-left: 4px solid #198754;
            }
            .assessment-type-card {
                border-radius: 10px;
                border: 2px solid transparent;
                padding: 20px;
                margin-bottom: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .assessment-type-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .assessment-type-card.active {
                border-color: var(--bs-primary);
                background-color: rgba(var(--bs-primary-rgb), 0.05);
            }
            .assessment-icon {
                width: 60px;
                height: 60px;
                background-color: rgba(var(--bs-primary-rgb), 0.1);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 15px;
                font-size: 24px;
                color: var(--bs-primary);
            }
            .assessment-forms {
                display: none;
            }
            .assessment-forms.active {
                display: block;
            }
            .assessment-summary {
                background-color: rgba(var(--bs-primary-rgb), 0.05);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            /* Floating chatbot button */
            .chatbot-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: var(--bs-primary);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                cursor: pointer;
                z-index: 1000;
                transition: all 0.3s;
            }
            .chatbot-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
            }
            .chatbot-popup {
                position: fixed;
                bottom: 90px;
                right: 20px;
                width: 350px;
                height: 500px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
                z-index: 999;
                display: none;
                flex-direction: column;
                overflow: hidden;
            }
            .chatbot-header {
                background-color: var(--bs-primary);
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
            }
            .chatbot-input {
                border-top: 1px solid #e0e0e0;
                padding: 10px;
                display: flex;
            }
            .chatbot-input input {
                flex: 1;
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin-right: 10px;
            }
            .message {
                margin-bottom: 10px;
                max-width: 80%;
            }
            .user-message {
                background-color: var(--bs-primary);
                color: white;
                padding: 10px 15px;
                border-radius: 18px 18px 0 18px;
                align-self: flex-end;
                margin-left: auto;
            }
            .bot-message {
                background-color: #f1f1f1;
                color: #333;
                padding: 10px 15px;
                border-radius: 18px 18px 18px 0;
                align-self: flex-start;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link text-dark">
                                    <i class="bi bi-speedometer2 text-primary me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link text-dark">
                                    <i class="bi bi-journal-medical text-primary me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link active bg-primary">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link text-dark">
                                    <i class="bi bi-calendar-check text-primary me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link text-dark">
                                    <i class="bi bi-egg-fried text-primary me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link text-dark">
                                    <i class="bi bi-bank text-primary me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Health Risk Assessment</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <div class="assessment-summary mt-4">
                        <h5>Choose Your Health Assessment</h5>
                        <p>Select the type of health assessment you'd like to complete to get personalized insights and recommendations.</p>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-md-4 mb-4">
                            <div class="assessment-type-card active" id="pregnancy-card" onclick="selectAssessmentType('pregnancy')">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="assessment-icon">
                                        <i class="bi bi-heart"></i>
                                    </div>
                                    <div>
                                        <h5 class="mb-1">High-Risk Pregnancy</h5>
                                        <p class="mb-0 text-muted">Identify pregnancy-related risks early</p>
                                    </div>
                                </div>
                                <p>Evaluates factors that might lead to pregnancy complications, helping you take preventive measures early.</p>
                            </div>
                        </div>
                        
                        <div class="col-md-4 mb-4">
                            <div class="assessment-type-card" id="anemia-card" onclick="selectAssessmentType('anemia')">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="assessment-icon">
                                        <i class="bi bi-droplet"></i>
                                    </div>
                                    <div>
                                        <h5 class="mb-1">Anemia Prevention</h5>
                                        <p class="mb-0 text-muted">Check your risk for anemia</p>
                                    </div>
                                </div>
                                <p>Assess your risk for anemia based on symptoms and lifestyle factors, especially important during pregnancy.</p>
                            </div>
                        </div>
                        
                        <div class="col-md-4 mb-4">
                            <div class="assessment-type-card" id="nutrition-card" onclick="selectAssessmentType('nutrition')">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="assessment-icon">
                                        <i class="bi bi-apple"></i>
                                    </div>
                                    <div>
                                        <h5 class="mb-1">Dietary Recommendations</h5>
                                        <p class="mb-0 text-muted">Get personalized nutritional guidance</p>
                                    </div>
                                </div>
                                <p>Analyze your current diet and receive recommendations for optimal nutrition to support your health needs.</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Pregnancy Risk Assessment Form -->
                    <div class="assessment-forms active" id="pregnancy-form">
                        <div class="row">
                            <div class="col-md-7">
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h5 class="card-title">High-Risk Pregnancy Assessment</h5>
                                    </div>
                                    <div class="card-body">
                                        <form id="pregnancyRiskForm">
                                            <h5 class="mb-3">Demographic Information</h5>
                                            <div class="mb-3">
                                                <label class="form-label">Are you over 35 years old?</label>
                                                <div class="d-flex">
                                                    <div class="form-check me-3">
                                                        <input class="form-check-input" type="radio" name="pregAgeAbove35" id="pregAgeAbove35Yes" value="yes">
                                                        <label class="form-check-label" for="pregAgeAbove35Yes">Yes</label>
                                                    </div>
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="radio" name="pregAgeAbove35" id="pregAgeAbove35No" value="no" checked>
                                                        <label class="form-check-label" for="pregAgeAbove35No">No</label>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Pregnancy Factors</h5>
                                            <div class="mb-3">
                                                <label class="form-label">Are you carrying multiple babies (twins, triplets, etc.)?</label>
                                                <div class="d-flex">
                                                    <div class="form-check me-3">
                                                        <input class="form-check-input" type="radio" name="multiplePregnancy" id="multiplePregnancyYes" value="yes">
                                                        <label class="form-check-label" for="multiplePregnancyYes">Yes</label>
                                                    </div>
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="radio" name="multiplePregnancy" id="multiplePregnancyNo" value="no" checked>
                                                        <label class="form-check-label" for="multiplePregnancyNo">No</label>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="previousCSection">
                                                <label class="form-check-label" for="previousCSection">Have you had a previous C-section?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="previousPretermBirth">
                                                <label class="form-check-label" for="previousPretermBirth">Have you had a previous preterm birth?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="previousMiscarriage">
                                                <label class="form-check-label" for="previousMiscarriage">Have you had previous miscarriages?</label>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Medical Conditions</h5>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="pregDiabetes">
                                                <label class="form-check-label" for="pregDiabetes">Do you have pre-existing diabetes?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="pregHypertension">
                                                <label class="form-check-label" for="pregHypertension">Do you have high blood pressure?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="pregThyroid">
                                                <label class="form-check-label" for="pregThyroid">Do you have thyroid disorders?</label>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Current Pregnancy Complications</h5>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="gestationalDiabetes">
                                                <label class="form-check-label" for="gestationalDiabetes">Have you been diagnosed with gestational diabetes?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="preeclampsia">
                                                <label class="form-check-label" for="preeclampsia">Have you been diagnosed with preeclampsia?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="bleeding">
                                                <label class="form-check-label" for="bleeding">Have you experienced vaginal bleeding during this pregnancy?</label>
                                            </div>
                                            
                                            <button type="button" class="btn btn-primary" onclick="calculatePregnancyRisk()">Submit Assessment</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-md-5">
                                <div class="card mb-4" id="pregnancyResultsCard" style="display: none;">
                                    <div class="card-header">
                                        <h5 class="card-title">Pregnancy Risk Assessment Results</h5>
                                    </div>
                                    <div class="card-body">
                                        <div class="result-card p-3 risk-moderate">
                                            <h5>Pregnancy Risk</h5>
                                            <div class="d-flex justify-content-between align-items-center mb-2">
                                                <span>Risk Level:</span>
                                                <span class="badge bg-warning" id="pregnancyRiskLevel">Moderate</span>
                                            </div>
                                            <div class="progress mb-3">
                                                <div class="progress-bar bg-warning" role="progressbar" style="width: 65%" id="pregnancyRiskBar"></div>
                                            </div>
                                            <div id="pregnancyRecommendations">
                                                <h6>Recommendations:</h6>
                                                <ul>
                                                    <li>Regular prenatal check-ups every 2 weeks</li>
                                                    <li>Monitor blood pressure daily</li>
                                                    <li>Follow a balanced diet rich in iron and folic acid</li>
                                                    <li>Moderate physical activity as recommended by your doctor</li>
                                                </ul>
                                            </div>
                                        </div>
                                        
                                        <div class="mt-4">
                                            <a href="#" class="btn btn-outline-primary me-2">
                                                <i class="bi bi-download me-1"></i> Download Report
                                            </a>
                                            <a href="#" class="btn btn-outline-primary">
                                                <i class="bi bi-share me-1"></i> Share with Doctor
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h5 class="card-title">About Pregnancy Risk Assessment</h5>
                                    </div>
                                    <div class="card-body">
                                        <p>This assessment helps identify factors that may increase the risk of pregnancy complications.</p>
                                        <p>Early identification of high-risk pregnancies allows for closer monitoring and specialized care when needed.</p>
                                        <p>The assessment considers your medical history, current health status, and pregnancy-specific factors.</p>
                                        <p>Based on your responses, you'll receive personalized recommendations to help ensure a healthy pregnancy.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Anemia Risk Assessment Form -->
                    <div class="assessment-forms" id="anemia-form">
                        <div class="row">
                            <div class="col-md-7">
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h5 class="card-title">Anemia Risk Assessment</h5>
                                    </div>
                                    <div class="card-body">
                                        <form id="anemiaRiskForm">
                                            <h5 class="mb-3">Physical Symptoms</h5>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="fatigue">
                                                <label class="form-check-label" for="fatigue">Do you often feel fatigued or weak?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="dizzySpells">
                                                <label class="form-check-label" for="dizzySpells">Do you experience dizziness or fainting?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="paleSkin">
                                                <label class="form-check-label" for="paleSkin">Have you noticed that your skin is paler than usual?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="shortnessOfBreath">
                                                <label class="form-check-label" for="shortnessOfBreath">Do you experience shortness of breath during normal activities?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="headaches">
                                                <label class="form-check-label" for="headaches">Do you frequently have headaches?</label>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Dietary Factors</h5>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="poorDiet">
                                                <label class="form-check-label" for="poorDiet">Do you have limited access to iron-rich foods?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="vegetarianVegan">
                                                <label class="form-check-label" for="vegetarianVegan">Are you vegetarian or vegan?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="lowProtein">
                                                <label class="form-check-label" for="lowProtein">Is your diet low in protein?</label>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Medical Factors</h5>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="heavyPeriods">
                                                <label class="form-check-label" for="heavyPeriods">Do you have heavy menstrual periods?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="recentBloodLoss">
                                                <label class="form-check-label" for="recentBloodLoss">Have you experienced any recent blood loss?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="chronicDisease">
                                                <label class="form-check-label" for="chronicDisease">Do you have any chronic diseases (kidney disease, rheumatoid arthritis, etc.)?</label>
                                            </div>
                                            
                                            <button type="button" class="btn btn-primary" onclick="calculateAnemiaRisk()">Submit Assessment</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-md-5">
                                <div class="card mb-4" id="anemiaResultsCard" style="display: none;">
                                    <div class="card-header">
                                        <h5 class="card-title">Anemia Risk Assessment Results</h5>
                                    </div>
                                    <div class="card-body">
                                        <div class="result-card p-3 risk-high">
                                            <h5>Anemia Risk</h5>
                                            <div class="d-flex justify-content-between align-items-center mb-2">
                                                <span>Risk Level:</span>
                                                <span class="badge bg-danger" id="anemiaRiskLevel">High</span>
                                            </div>
                                            <div class="progress mb-3">
                                                <div class="progress-bar bg-danger" role="progressbar" style="width: 85%" id="anemiaRiskBar"></div>
                                            </div>
                                            <div id="anemiaRecommendations">
                                                <h6>Recommendations:</h6>
                                                <ul>
                                                    <li>Immediate hemoglobin test recommended</li>
                                                    <li>Increase intake of iron-rich foods (leafy greens, meat, beans)</li>
                                                    <li>Consider iron supplements (consult with healthcare provider)</li>
                                                    <li>Follow up with healthcare provider within 1 week</li>
                                                    <li>Check for eligible government health schemes for free treatment</li>
                                                </ul>
                                            </div>
                                        </div>
                                        
                                        <div class="mt-4">
                                            <a href="#" class="btn btn-outline-primary me-2">
                                                <i class="bi bi-download me-1"></i> Download Report
                                            </a>
                                            <a href="#" class="btn btn-outline-primary">
                                                <i class="bi bi-share me-1"></i> Share with Doctor
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h5 class="card-title">About Anemia Risk Assessment</h5>
                                    </div>
                                    <div class="card-body">
                                        <p>Anemia is a condition where you don't have enough healthy red blood cells to carry adequate oxygen to your body's tissues.</p>
                                        <p>This assessment helps identify risk factors for anemia, which is particularly important during pregnancy.</p>
                                        <p>Early detection and treatment of anemia can prevent complications like fatigue, weakness, and in pregnant women, preterm delivery and low birth weight.</p>
                                        <p>After completing the assessment, you'll receive personalized recommendations to help maintain healthy hemoglobin levels.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Nutrition Assessment Form -->
                    <div class="assessment-forms" id="nutrition-form">
                        <div class="row">
                            <div class="col-md-7">
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h5 class="card-title">Dietary Assessment</h5>
                                    </div>
                                    <div class="card-body">
                                        <form id="nutritionAssessmentForm">
                                            <h5 class="mb-3">Current Diet</h5>
                                            <div class="mb-3">
                                                <label class="form-label">How many servings of fruits do you consume daily?</label>
                                                <select class="form-select" id="fruitServings">
                                                    <option value="0">None</option>
                                                    <option value="1">1 serving</option>
                                                    <option value="2">2 servings</option>
                                                    <option value="3">3 servings</option>
                                                    <option value="4">4 or more servings</option>
                                                </select>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">How many servings of vegetables do you consume daily?</label>
                                                <select class="form-select" id="vegetableServings">
                                                    <option value="0">None</option>
                                                    <option value="1">1 serving</option>
                                                    <option value="2">2 servings</option>
                                                    <option value="3">3 servings</option>
                                                    <option value="4">4 or more servings</option>
                                                </select>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">How often do you consume iron-rich foods (leafy greens, red meat, beans)?</label>
                                                <select class="form-select" id="ironFoods">
                                                    <option value="rarely">Rarely or never</option>
                                                    <option value="sometimes">1-2 times per week</option>
                                                    <option value="often">3-4 times per week</option>
                                                    <option value="daily">Daily</option>
                                                </select>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">How often do you consume calcium-rich foods (dairy, fortified plant milk, etc.)?</label>
                                                <select class="form-select" id="calciumFoods">
                                                    <option value="rarely">Rarely or never</option>
                                                    <option value="sometimes">1-2 times per week</option>
                                                    <option value="often">3-4 times per week</option>
                                                    <option value="daily">Daily</option>
                                                </select>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Dietary Restrictions</h5>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="vegetarian">
                                                <label class="form-check-label" for="vegetarian">Are you vegetarian?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="vegan">
                                                <label class="form-check-label" for="vegan">Are you vegan?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="glutenFree">
                                                <label class="form-check-label" for="glutenFree">Do you follow a gluten-free diet?</label>
                                            </div>
                                            <div class="mb-3 form-check">
                                                <input type="checkbox" class="form-check-input" id="dairyFree">
                                                <label class="form-check-label" for="dairyFree">Do you avoid dairy products?</label>
                                            </div>
                                            
                                            <h5 class="mb-3 mt-4">Eating Habits</h5>
                                            <div class="mb-3">
                                                <label class="form-label">How many meals do you typically eat per day?</label>
                                                <select class="form-select" id="mealsPerDay">
                                                    <option value="1-2">1-2 meals</option>
                                                    <option value="3">3 meals</option>
                                                    <option value="4-5">4-5 meals (including snacks)</option>
                                                    <option value="6+">6 or more meals</option>
                                                </select>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label">Do you often skip meals?</label>
                                                <select class="form-select" id="skipMeals">
                                                    <option value="never">Never</option>
                                                    <option value="sometimes">Sometimes</option>
                                                    <option value="often">Often</option>
                                                    <option value="daily">Daily</option>
                                                </select>
                                            </div>
                                            
                                            <button type="button" class="btn btn-primary" onclick="calculateNutritionRecommendations()">Submit Assessment</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-md-5">
                                <div class="card mb-4" id="nutritionResultsCard" style="display: none;">
                                    <div class="card-header">
                                        <h5 class="card-title">Dietary Recommendations</h5>
                                    </div>
                                    <div class="card-body">
                                        <div class="mb-4">
                                            <h5>Diet Quality Analysis</h5>
                                            <div class="progress mb-3">
                                                <div class="progress-bar bg-info" role="progressbar" style="width: 70%" id="dietQualityBar"></div>
                                            </div>
                                            <p id="dietQualityMessage">Based on your responses, your diet provides moderate nutritional support. There are several areas where improvements can be made.</p>
                                        </div>
                                        
                                        <div id="nutritionRecommendations">
                                            <h6>Personalized Recommendations:</h6>
                                            <ul>
                                                <li>Increase your daily fruit intake to at least 2-3 servings</li>
                                                <li>Add more leafy greens to your meals for iron and folate</li>
                                                <li>Consider including a vitamin C source with iron-rich foods to improve absorption</li>
                                                <li>Ensure adequate protein intake through a variety of sources</li>
                                                <li>Stay well-hydrated with at least 8 glasses of water daily</li>
                                            </ul>
                                        </div>
                                        
                                        <div class="mt-4">
                                            <a href="/nutrition/meal-planner" class="btn btn-primary w-100">
                                                <i class="bi bi-calendar-check me-2"></i>
                                                View Personalized Meal Plan
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card mb-4">
                                    <div class="card-header">
                                        <h5 class="card-title">About Dietary Assessment</h5>
                                    </div>
                                    <div class="card-body">
                                        <p>This assessment analyzes your current diet and eating habits to provide personalized nutritional recommendations.</p>
                                        <p>Good nutrition is essential for overall health and is particularly important during pregnancy, when managing anemia, or other health conditions.</p>
                                        <p>The recommendations consider your dietary preferences, restrictions, and current eating patterns.</p>
                                        <p>After completing the assessment, you'll receive tailored advice on how to optimize your diet for your specific health needs.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Floating Chatbot Button -->
        <div class="chatbot-button" onclick="toggleChatbot()">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        
        <!-- Chatbot Popup -->
        <div class="chatbot-popup" id="chatbotPopup">
            <div class="chatbot-header">
                <div>
                    <i class="bi bi-robot me-2"></i>
                    NeoMitra Assistant
                </div>
                <button class="btn-close btn-close-white" onclick="toggleChatbot()"></button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="message bot-message">
                    Hello! I'm your health assessment assistant. How can I help you understand the different assessments available?
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" id="chatbotInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                <button class="btn btn-primary" onclick="sendMessage()">
                    <i class="bi bi-send"></i>
                </button>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Assessment type selection
            function selectAssessmentType(type) {
                // Hide all forms
                document.querySelectorAll('.assessment-forms').forEach(form => {
                    form.classList.remove('active');
                });
                
                // Remove active class from all cards
                document.querySelectorAll('.assessment-type-card').forEach(card => {
                    card.classList.remove('active');
                });
                
                // Show selected form and activate card
                document.getElementById(type + '-form').classList.add('active');
                document.getElementById(type + '-card').classList.add('active');
            }
            
            // Risk calculation functions
            function calculatePregnancyRisk() {
                // In a real application, this would send data to the server for processing
                document.getElementById('pregnancyResultsCard').style.display = 'block';
                document.getElementById('pregnancyResultsCard').scrollIntoView({ behavior: 'smooth' });
                
                // Store assessment results in session
                sessionStorage.setItem('pregnancy_risk_level', 'Moderate');
                sessionStorage.setItem('pregnancy_risk_score', '65');
            }
            
            function calculateAnemiaRisk() {
                // In a real application, this would send data to the server for processing
                document.getElementById('anemiaResultsCard').style.display = 'block';
                document.getElementById('anemiaResultsCard').scrollIntoView({ behavior: 'smooth' });
                
                // Store assessment results in session
                sessionStorage.setItem('anemia_risk_level', 'High');
                sessionStorage.setItem('anemia_risk_score', '85');
            }
            
            function calculateNutritionRecommendations() {
                // In a real application, this would send data to the server for processing
                document.getElementById('nutritionResultsCard').style.display = 'block';
                document.getElementById('nutritionResultsCard').scrollIntoView({ behavior: 'smooth' });
            }
            
            // Chatbot functionality
            let chatbotOpen = false;
            
            function toggleChatbot() {
                chatbotOpen = !chatbotOpen;
                document.getElementById('chatbotPopup').style.display = chatbotOpen ? 'flex' : 'none';
                if (chatbotOpen) {
                    document.getElementById('chatbotInput').focus();
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('chatbotInput');
                const message = input.value.trim();
                
                if (message) {
                    // Add user message
                    addMessage(message, 'user');
                    input.value = '';
                    
                    // Simulate bot response
                    setTimeout(() => {
                        let response = '';
                        
                        if (message.toLowerCase().includes('pregnancy') || message.toLowerCase().includes('high-risk')) {
                            response = "The High-Risk Pregnancy assessment evaluates factors that might lead to pregnancy complications. It considers your age, medical history, previous pregnancy outcomes, and current health status to identify potential risks.";
                        } else if (message.toLowerCase().includes('anemia')) {
                            response = "The Anemia Prevention assessment looks at symptoms and risk factors for anemia, which is especially important during pregnancy. It evaluates physical symptoms, dietary habits, and medical factors that might contribute to low hemoglobin levels.";
                        } else if (message.toLowerCase().includes('diet') || message.toLowerCase().includes('nutrition')) {
                            response = "The Dietary Recommendations assessment analyzes your current eating habits, nutritional intake, and dietary restrictions to provide personalized nutrition guidance. This helps ensure you're getting all the essential nutrients needed, especially during pregnancy.";
                        } else if (message.toLowerCase().includes('result') || message.toLowerCase().includes('recommendation')) {
                            response = "After completing an assessment, you'll receive personalized results and recommendations based on your responses. These include risk levels for certain conditions and specific actions you can take to maintain or improve your health.";
                        } else {
                            response = "You can choose from three different health assessments: High-Risk Pregnancy Detection, Anemia Prevention, and Dietary Recommendations. Each provides personalized insights based on your specific situation. Which assessment are you most interested in learning about?";
                        }
                        
                        addMessage(response, 'bot');
                    }, 1000);
                }
            }
            
            function addMessage(text, sender) {
                const messagesContainer = document.getElementById('chatbotMessages');
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                messageElement.textContent = text;
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/government_schemes')
def government_schemes():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Government Schemes - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .scheme-card {
                transition: all 0.3s ease;
                margin-bottom: 1.5rem;
            }
            .scheme-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .scheme-logo {
                max-width: 80px;
                max-height: 80px;
            }
            .scheme-badge {
                position: absolute;
                top: 10px;
                right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link text-dark">
                                    <i class="bi bi-calendar-check text-primary me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link text-dark">
                                    <i class="bi bi-egg-fried text-primary me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link active bg-primary">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                            <li>
                                <a href="/chatbot" class="nav-link text-dark">
                                    <i class="bi bi-chat-dots text-primary me-2"></i>
                                    Chatbot Assistant
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Government Healthcare Schemes</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-md-8">
                            <!-- Schemes List -->
                            <div class="mb-4">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <h4>Available Schemes</h4>
                                    <div class="input-group" style="max-width: 300px;">
                                        <input type="text" class="form-control" placeholder="Search schemes" id="searchSchemes">
                                        <button class="btn btn-outline-primary" type="button">
                                            <i class="bi bi-search"></i>
                                        </button>
                                    </div>
                                </div>
                                
                                <div class="card scheme-card position-relative">
                                    <span class="badge bg-success scheme-badge">Recommended</span>
                                    <div class="card-body d-flex">
                                        <img src="https://via.placeholder.com/80x80?text=PMSMA" alt="PMSMA Logo" class="scheme-logo me-3">
                                        <div>
                                            <h5 class="card-title text-light">Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA)</h5>
                                            <p class="card-text text-light">Provides free antenatal care to pregnant women on the 9th of every month with the aim of detecting high-risk pregnancies.</p>
                                            <div class="d-flex flex-wrap gap-2 mb-2">
                                                <span class="badge bg-primary">Pregnancy Care</span>
                                                <span class="badge bg-info">Free Check-ups</span>
                                                <span class="badge bg-secondary">All Districts</span>
                                            </div>
                                            <a href="/scheme/pmsma" class="btn btn-sm btn-primary">View Details</a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card scheme-card position-relative mt-3">
                                    <span class="badge bg-success scheme-badge">Recommended</span>
                                    <div class="card-body d-flex">
                                        <img src="https://via.placeholder.com/80x80?text=JSY" alt="JSY Logo" class="scheme-logo me-3">
                                        <div>
                                            <h5 class="card-title text-light">Janani Suraksha Yojana (JSY)</h5>
                                            <p class="card-text text-light">Promotes institutional delivery among poor pregnant women with cash assistance, reducing maternal and infant mortality.</p>
                                            <div class="d-flex flex-wrap gap-2 mb-2">
                                                <span class="badge bg-primary">Pregnancy Care</span>
                                                <span class="badge bg-info">Cash Benefits</span>
                                                <span class="badge bg-secondary">National</span>
                                            </div>
                                            <a href="/scheme/jsy" class="btn btn-sm btn-primary">View Details</a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card scheme-card mt-3">
                                    <div class="card-body d-flex">
                                        <img src="https://via.placeholder.com/80x80?text=PMJAY" alt="PMJAY Logo" class="scheme-logo me-3">
                                        <div>
                                            <h5 class="card-title text-light">Pradhan Mantri Jan Arogya Yojana (PMJAY)</h5>
                                            <p class="card-text text-light">Health insurance scheme providing coverage up to ₹5 lakhs per family per year for secondary and tertiary care hospitalization.</p>
                                            <div class="d-flex flex-wrap gap-2 mb-2">
                                                <span class="badge bg-primary">Health Insurance</span>
                                                <span class="badge bg-info">All Conditions</span>
                                                <span class="badge bg-secondary">National</span>
                                            </div>
                                            <a href="/scheme/pmjay" class="btn btn-sm btn-primary">View Details</a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card scheme-card mt-3">
                                    <div class="card-body d-flex">
                                        <img src="https://via.placeholder.com/80x80?text=RBSK" alt="RBSK Logo" class="scheme-logo me-3">
                                        <div>
                                            <h5 class="card-title text-light">Rashtriya Bal Swasthya Karyakram (RBSK)</h5>
                                            <p class="card-text text-light">Child health screening and early intervention services for children from birth to 18 years to provide comprehensive care.</p>
                                            <div class="d-flex flex-wrap gap-2 mb-2">
                                                <span class="badge bg-primary">Child Health</span>
                                                <span class="badge bg-info">Screening</span>
                                                <span class="badge bg-secondary">National</span>
                                            </div>
                                            <a href="/scheme/rbsk" class="btn btn-sm btn-primary">View Details</a>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="card scheme-card mt-3">
                                    <div class="card-body d-flex">
                                        <img src="https://via.placeholder.com/80x80?text=NPCDCS" alt="NPCDCS Logo" class="scheme-logo me-3">
                                        <div>
                                            <h5 class="card-title text-light">National Programme for Prevention and Control of Diabetes</h5>
                                            <p class="card-text text-light">Provides free screening, diagnosis, and management of diabetes and related non-communicable diseases.</p>
                                            <div class="d-flex flex-wrap gap-2 mb-2">
                                                <span class="badge bg-primary">Diabetes</span>
                                                <span class="badge bg-info">Free Treatment</span>
                                                <span class="badge bg-secondary">National</span>
                                            </div>
                                            <a href="/scheme/npcdcs" class="btn btn-sm btn-primary">View Details</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4">
                            <!-- Eligibility Checker -->
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title">Eligibility Checker</h5>
                                </div>
                                <div class="card-body">
                                    <p>Find out which government schemes you are eligible for based on your profile.</p>
                                    <form>
                                        <div class="mb-3">
                                            <label class="form-label">Category</label>
                                            <select class="form-select">
                                                <option>General</option>
                                                <option>SC/ST</option>
                                                <option>OBC</option>
                                                <option>BPL</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Annual Income</label>
                                            <select class="form-select">
                                                <option>Below ₹1 Lakh</option>
                                                <option>₹1-3 Lakhs</option>
                                                <option>₹3-5 Lakhs</option>
                                                <option>Above ₹5 Lakhs</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Health Condition</label>
                                            <select class="form-select">
                                                <option>Pregnancy</option>
                                                <option>Anemia</option>
                                                <option>Diabetes</option>
                                                <option>Hypertension</option>
                                                <option>General Health</option>
                                            </select>
                                        </div>
                                        <button type="button" class="btn btn-primary w-100">Check Eligibility</button>
                                    </form>
                                </div>
                            </div>
                            
                            <!-- Need Help -->
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title">Need Help?</h5>
                                </div>
                                <div class="card-body">
                                    <p>Having trouble understanding or applying for government schemes?</p>
                                    <div class="d-grid gap-2">
                                        <a href="/chatbot" class="btn btn-outline-primary">
                                            <i class="bi bi-chat-dots me-2"></i>
                                            Ask Our Assistant
                                        </a>
                                        <a href="/contact" class="btn btn-outline-primary">
                                            <i class="bi bi-telephone me-2"></i>
                                            Contact Support
                                        </a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Resources -->
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title">Useful Resources</h5>
                                </div>
                                <div class="card-body">
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item d-flex align-items-center">
                                            <i class="bi bi-file-earmark-text me-2 text-primary"></i>
                                            <a href="#" class="text-decoration-none">How to Apply for Health Schemes</a>
                                        </li>
                                        <li class="list-group-item d-flex align-items-center">
                                            <i class="bi bi-file-earmark-text me-2 text-primary"></i>
                                            <a href="#" class="text-decoration-none">Required Documents Checklist</a>
                                        </li>
                                        <li class="list-group-item d-flex align-items-center">
                                            <i class="bi bi-file-earmark-text me-2 text-primary"></i>
                                            <a href="#" class="text-decoration-none">Nearest Application Centers</a>
                                        </li>
                                        <li class="list-group-item d-flex align-items-center">
                                            <i class="bi bi-file-earmark-text me-2 text-primary"></i>
                                            <a href="#" class="text-decoration-none">Application Status Tracker</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/profile')
def profile():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #333;
            }
            .nav-link {
                color: #333;
            }
            .nav-link.active {
                background-color: var(--bs-primary);
                color: white;
            }
            .nav-link:hover {
                color: var(--bs-primary);
            }
            .dropdown-toggle, .fs-4.fw-bold.text-primary {
                color: var(--bs-primary) !important;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #333;
            }
            .profile-header {
                padding: 2rem 0;
                margin-bottom: 2rem;
                border-radius: 10px;
                background-color: #ffffff;
            }
            .avatar-upload {
                position: relative;
                max-width: 150px;
                margin: 0 auto;
            }
            .avatar-edit {
                position: absolute;
                right: 5px;
                bottom: 5px;
                width: 36px;
                height: 36px;
                border-radius: 100%;
                background: var(--bs-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
            }
            .avatar-preview {
                width: 150px;
                height: 150px;
                position: relative;
                border-radius: 100%;
                overflow: hidden;
                background: #666;
                border: 5px solid var(--bs-primary);
            }
            .avatar-preview img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                            <li>
                                <a href="/chatbot" class="nav-link">
                                    <i class="bi bi-chat-dots me-2"></i>
                                    Chatbot Assistant
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item active" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Your Profile</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <div class="row">
                        <div class="col-lg-4">
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title">Profile Picture</h5>
                                </div>
                                <div class="card-body text-center">
                                    <div class="avatar-upload">
                                        <div class="avatar-edit">
                                            <label for="imageUpload" class="text-white">
                                                <i class="bi bi-pencil"></i>
                                            </label>
                                            <input type='file' id="imageUpload" accept=".png, .jpg, .jpeg" style="display: none;" />
                                        </div>
                                        <div class="avatar-preview">
                                            <img src="https://via.placeholder.com/150" alt="Profile Picture" id="imagePreview">
                                        </div>
                                    </div>
                                    <h4 class="mt-3">{{ username }}</h4>
                                    <p class="text-muted">Member since {{ user_data.get('created_at', 'January 2023') }}</p>
                                </div>
                            </div>
                            
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title">Account Security</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <label class="form-label">Password</label>
                                        <div class="d-flex justify-content-between align-items-center">
                                            <span>••••••••</span>
                                            <button class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#changePasswordModal">Change</button>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Two-Factor Authentication</label>
                                        <div class="d-flex justify-content-between align-items-center">
                                            <span class="text-danger">Not enabled</span>
                                            <button class="btn btn-sm btn-outline-primary">Enable</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-lg-8">
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title">Personal Information</h5>
                                </div>
                                <div class="card-body">
                                    <form id="profileForm">
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label for="firstName" class="form-label">First Name</label>
                                                <input type="text" class="form-control" id="firstName" value="{{ user_data.get('first_name', '') }}">
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label for="lastName" class="form-label">Last Name</label>
                                                <input type="text" class="form-control" id="lastName" value="{{ user_data.get('last_name', '') }}">
                                            </div>
                                        </div>
                                        
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label for="email" class="form-label">Email Address</label>
                                                <input type="email" class="form-control" id="email" value="{{ user_data.get('email', '') }}">
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label for="phone" class="form-label">Phone Number</label>
                                                <input type="tel" class="form-control" id="phone" value="{{ user_data.get('phone', '') }}">
                                            </div>
                                        </div>
                                        
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label for="dob" class="form-label">Date of Birth</label>
                                                <input type="date" class="form-control" id="dob" value="{{ user_data.get('dob', '') }}">
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label for="gender" class="form-label">Gender</label>
                                                <select class="form-select" id="gender">
                                                    <option value="female" {{ 'selected' if user_data.get('gender') == 'female' else '' }}>Female</option>
                                                    <option value="male" {{ 'selected' if user_data.get('gender') == 'male' else '' }}>Male</option>
                                                    <option value="other" {{ 'selected' if user_data.get('gender') == 'other' else '' }}>Other</option>
                                                    <option value="prefer_not_to_say" {{ 'selected' if user_data.get('gender') == 'prefer_not_to_say' else '' }}>Prefer not to say</option>
                                                </select>
                                            </div>
                                        </div>
                                        
                                        <div class="mb-3">
                                            <label for="address" class="form-label">Address</label>
                                            <textarea class="form-control" id="address" rows="3">{{ user_data.get('address', '') }}</textarea>
                                        </div>
                                        
                                        <div class="row">
                                            <div class="col-md-6 mb-3">
                                                <label for="preferredLanguage" class="form-label">Preferred Language</label>
                                                <select class="form-select" id="preferredLanguage">
                                                    <option value="en" {{ 'selected' if user_data.get('preferred_language') == 'en' else '' }}>English</option>
                                                    <option value="hi" {{ 'selected' if user_data.get('preferred_language') == 'hi' else '' }}>Hindi</option>
                                                    <option value="ta" {{ 'selected' if user_data.get('preferred_language') == 'ta' else '' }}>Tamil</option>
                                                    <option value="te" {{ 'selected' if user_data.get('preferred_language') == 'te' else '' }}>Telugu</option>
                                                    <option value="mr" {{ 'selected' if user_data.get('preferred_language') == 'mr' else '' }}>Marathi</option>
                                                    <option value="bn" {{ 'selected' if user_data.get('preferred_language') == 'bn' else '' }}>Bengali</option>
                                                </select>
                                            </div>
                                            <div class="col-md-6 mb-3">
                                                <label for="emergencyContact" class="form-label">Emergency Contact</label>
                                                <input type="tel" class="form-control" id="emergencyContact" value="{{ user_data.get('emergency_contact', '') }}">
                                            </div>
                                        </div>
                                        
                                        <div class="text-end">
                                            <button type="button" class="btn btn-primary" onclick="saveProfile()">Save Changes</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                            
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title">Healthcare Provider Details</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <label for="primaryDoctor" class="form-label">Primary Doctor/OBGYN</label>
                                        <input type="text" class="form-control" id="primaryDoctor" value="{{ user_data.get('primary_doctor', '') }}">
                                    </div>
                                    <div class="mb-3">
                                        <label for="healthcareCenter" class="form-label">Healthcare Center</label>
                                        <input type="text" class="form-control" id="healthcareCenter" value="{{ user_data.get('healthcare_center', '') }}">
                                    </div>
                                    <div class="mb-3">
                                        <label for="healthInsurance" class="form-label">Health Insurance ID</label>
                                        <input type="text" class="form-control" id="healthInsurance" value="{{ user_data.get('health_insurance', '') }}">
                                    </div>
                                    <div class="text-end">
                                        <button type="button" class="btn btn-primary" onclick="saveHealthcareInfo()">Save Healthcare Info</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Change Password Modal -->
        <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="changePasswordModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="changePasswordModalLabel">Change Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="changePasswordForm">
                            <div class="mb-3">
                                <label for="currentPassword" class="form-label">Current Password</label>
                                <input type="password" class="form-control" id="currentPassword" required>
                            </div>
                            <div class="mb-3">
                                <label for="newPassword" class="form-label">New Password</label>
                                <input type="password" class="form-control" id="newPassword" required minlength="8">
                                <div class="form-text">Password must be at least 8 characters long and include a mix of letters, numbers, and symbols.</div>
                            </div>
                            <div class="mb-3">
                                <label for="confirmPassword" class="form-label">Confirm New Password</label>
                                <input type="password" class="form-control" id="confirmPassword" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="changePassword()">Update Password</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Preview profile image before upload
            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        document.getElementById('imagePreview').src = e.target.result;
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }
            
            document.getElementById('imageUpload').addEventListener('change', function() {
                readURL(this);
            });
            
            // Save profile information
            function saveProfile() {
                // Get form data
                const formData = {
                    firstName: document.getElementById('firstName').value,
                    lastName: document.getElementById('lastName').value,
                    email: document.getElementById('email').value,
                    phone: document.getElementById('phone').value,
                    dob: document.getElementById('dob').value,
                    gender: document.getElementById('gender').value,
                    address: document.getElementById('address').value,
                    preferredLanguage: document.getElementById('preferredLanguage').value,
                    emergencyContact: document.getElementById('emergencyContact').value
                };
                
                // Normally this would be sent to the server
                // For demo purposes, we'll just show a success message
                alert('Profile updated successfully!');
            }
            
            // Save healthcare information
            function saveHealthcareInfo() {
                // Get healthcare form data
                const healthcareData = {
                    primaryDoctor: document.getElementById('primaryDoctor').value,
                    healthcareCenter: document.getElementById('healthcareCenter').value,
                    healthInsurance: document.getElementById('healthInsurance').value
                };
                
                // Normally this would be sent to the server
                // For demo purposes, we'll just show a success message
                alert('Healthcare information updated successfully!');
            }
            
            // Change password
            function changePassword() {
                const currentPassword = document.getElementById('currentPassword').value;
                const newPassword = document.getElementById('newPassword').value;
                const confirmPassword = document.getElementById('confirmPassword').value;
                
                // Validate passwords match
                if (newPassword !== confirmPassword) {
                    alert('New passwords do not match!');
                    return;
                }
                
                // Normally this would be sent to the server for validation and updating
                // For demo purposes, we'll just show a success message
                alert('Password updated successfully!');
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
            }
        </script>
        
        <!-- Floating Chatbot Button -->
        <div class="position-fixed bottom-0 end-0 p-3">
            <a href="/chatbot" class="btn btn-primary rounded-circle shadow-lg p-3">
                <i class="bi bi-chat-dots-fill fs-4"></i>
            </a>
        </div>
    </body>
    </html>
    """, username=session.get('username', 'User'), user_data={})

@app.route('/process_voice_recording', methods=['POST'])
def process_voice_recording():
    """
    Process voice transcripts and extract health data using NLP
    """
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400
    
    # Get transcript from request
    data = request.get_json()
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({"success": False, "message": "No transcript provided"}), 400
    
    # Example of basic NLP to extract health data
    extracted_data = {}
    
    # Check for weight
    weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|kilograms?|kilos)', transcript, re.IGNORECASE)
    if weight_match:
        extracted_data['weight'] = float(weight_match.group(1))
    
    # Check for blood pressure
    bp_match = re.search(r'(\d+)[\/\\](\d+)', transcript)
    if bp_match:
        extracted_data['bloodPressure'] = f"{bp_match.group(1)}/{bp_match.group(2)}"
    
    # Check for blood sugar
    sugar_match = re.search(r'blood sugar (?:is|of|at)?\s*(\d+(?:\.\d+)?)', transcript, re.IGNORECASE)
    if sugar_match:
        extracted_data['bloodSugar'] = float(sugar_match.group(1))
    
    # Check for hemoglobin
    hb_match = re.search(r'(?:hemoglobin|hb) (?:is|of|at)?\s*(\d+(?:\.\d+)?)', transcript, re.IGNORECASE)
    if hb_match:
        extracted_data['hemoglobin'] = float(hb_match.group(1))
    
    # Check for glucose
    glucose_match = re.search(r'glucose (?:is|of|at)?\s*(\d+(?:\.\d+)?)', transcript, re.IGNORECASE)
    if glucose_match:
        extracted_data['glucose'] = float(glucose_match.group(1))
    
    # Check for heart rate
    hr_match = re.search(r'(?:heart rate|pulse) (?:is|of|at)?\s*(\d+)', transcript, re.IGNORECASE)
    if hr_match:
        extracted_data['heartRate'] = int(hr_match.group(1))
    
    # Check for temperature
    temp_match = re.search(r'temperature (?:is|of|at)?\s*(\d+(?:\.\d+)?)', transcript, re.IGNORECASE)
    if temp_match:
        extracted_data['temperature'] = float(temp_match.group(1))
    
    # Check for pregnancy week
    preg_week_match = re.search(r'(\d+)(?:st|nd|rd|th)? week (?:of pregnancy|pregnant)', transcript, re.IGNORECASE)
    if preg_week_match:
        extracted_data['pregnancyWeek'] = int(preg_week_match.group(1))
    
    # Check for due date
    due_date_match = re.search(r'due date (?:is|of)?\s*(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})', transcript, re.IGNORECASE)
    if due_date_match:
        day = int(due_date_match.group(1))
        month = int(due_date_match.group(2))
        year = int(due_date_match.group(3))
        if year < 100:  # Convert 2-digit year to 4-digit
            year += 2000
        extracted_data['dueDate'] = f"{year}-{month:02d}-{day:02d}"
    
    # Check for symptoms
    symptoms = []
    symptom_patterns = [
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(headache|migraine)', 'headache'),
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(nausea|vomiting)', 'nausea'),
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(fatigue|tired|exhaustion)', 'fatigue'),
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(dizziness|vertigo|lightheaded)', 'dizziness'),
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(swelling|edema)', 'swelling'),
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(cramps|contractions)', 'cramps'),
        (r'(?:have|having|experiencing|suffering from|feeling)?\s*(?:a|some|bad|severe)?\s*(backache|back pain)', 'back pain')
    ]
    
    for pattern, symptom_name in symptom_patterns:
        if re.search(pattern, transcript, re.IGNORECASE):
            symptoms.append(symptom_name)
    
    if symptoms:
        extracted_data['symptoms'] = ', '.join(symptoms)
    
    response_message = ""
    
    if extracted_data:
        # Format a readable response
        readable_data = []
        for key, value in extracted_data.items():
            # Format camelCase to normal text
            formatted_key = ''.join([' ' + c.lower() if c.isupper() else c for c in key]).strip()
            readable_data.append(f"{formatted_key}: {value}")
        
        response_message = f"I've recorded the following health data: {', '.join(readable_data)}"
        
        return jsonify({
            "success": True,
            "extractedData": extracted_data,
            "response": response_message,
            "dataSaved": True,
            "message": "Health data saved successfully!"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Could not extract any health data from your input. Please try again with specific health measurements like weight, blood pressure, or symptoms."
        })

@app.route('/voice_input', methods=['GET'])
def voice_input_page():
    """
    Page for voice-assisted health logging
    """
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Voice Health Logging - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #333;
            }
            .nav-link {
                color: #333;
            }
            .nav-link.active {
                background-color: var(--bs-primary);
                color: white;
            }
            .nav-link:hover {
                color: var(--bs-primary);
            }
            .dropdown-toggle, .fs-4.fw-bold.text-primary {
                color: var(--bs-primary) !important;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #333;
            }
            .voice-container {
                border-radius: 15px;
                background-color: rgba(var(--bs-primary-rgb), 0.05);
                padding: 2rem;
                margin-bottom: 2rem;
                color: #333;
            }
            .status-indicator {
                display: inline-block;
                width: 15px;
                height: 15px;
                border-radius: 50%;
                background-color: #dc3545;
                margin-right: 0.5rem;
            }
            .status-indicator.active {
                background-color: #28a745;
                animation: pulse 1.5s infinite;
            }
            .voice-transcript {
                max-height: 250px;
                overflow-y: auto;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 1rem;
                margin-top: 1rem;
            }
            .voice-transcript p {
                margin-bottom: 0.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            .voice-tutorial {
                background-color: rgba(var(--bs-info-rgb), 0.1);
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 2rem;
            }
            .voice-button {
                min-width: 100px;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                            <li>
                                <a href="/voice_input" class="nav-link active">
                                    <i class="bi bi-mic-fill me-2"></i>
                                    Voice Health Logging
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Voice Health Logging</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-lg-8">
                            <!-- Voice Input Card -->
                            <div class="voice-container">
                                <h4 class="mb-4">
                                    <i class="bi bi-mic-fill me-2"></i>
                                    Record Health Data Using Voice
                                </h4>
                                
                                <div class="d-flex align-items-center mb-3">
                                    <div>
                                        <span class="status-indicator" id="voiceStatusIndicator"></span>
                                        <span id="voiceStatus">Not listening</span>
                                    </div>
                                </div>
                                
                                <div class="d-flex gap-2 mb-4">
                                    <button class="btn btn-primary voice-button" id="startVoiceButton">
                                        <i class="bi bi-mic-fill me-2"></i>
                                        Start
                                    </button>
                                    <button class="btn btn-danger voice-button" id="stopVoiceButton" disabled>
                                        <i class="bi bi-mic-mute-fill me-2"></i>
                                        Stop
                                    </button>
                                    <button class="btn btn-secondary voice-button" id="clearVoiceButton">
                                        <i class="bi bi-trash me-2"></i>
                                        Clear
                                    </button>
                                </div>
                                
                                <h5>What you're saying:</h5>
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <p id="interimTranscript" class="fst-italic text-muted"></p>
                                    </div>
                                </div>
                                
                                <h5>Recorded Statements:</h5>
                                <div class="voice-transcript mb-4" id="voiceTranscript"></div>
                                
                                <div id="extractedHealthData"></div>
                            </div>
                        </div>
                        
                        <div class="col-lg-4">
                            <!-- Tutorial Card -->
                            <div class="voice-tutorial">
                                <h5>How To Use Voice Logging</h5>
                                <ol class="mt-3">
                                    <li class="mb-2">Click the <strong>Start</strong> button and allow microphone access if prompted.</li>
                                    <li class="mb-2">Speak clearly about your health measurements or symptoms.</li>
                                    <li class="mb-2">Click <strong>Stop</strong> when you're done.</li>
                                    <li class="mb-2">Review the extracted health data for accuracy.</li>
                                </ol>
                                
                                <h6 class="mt-4">Example Phrases:</h6>
                                <ul>
                                    <li>"My weight is 65 kg"</li>
                                    <li>"My blood pressure is 120/80"</li>
                                    <li>"My blood sugar is 95"</li>
                                    <li>"My hemoglobin level is 13.5"</li>
                                    <li>"I'm in my 24th week of pregnancy"</li>
                                    <li>"I'm experiencing headaches and fatigue"</li>
                                </ul>
                                
                                <div class="alert alert-info mt-3">
                                    <i class="bi bi-info-circle me-2"></i>
                                    All your health data will be saved to your medical record after verification.
                                </div>
                            </div>
                            
                            <!-- Quick Access Card -->
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title">Quick Access</h5>
                                </div>
                                <div class="card-body">
                                    <div class="list-group list-group-flush">
                                        <a href="/health-records" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>View Health Records</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="/chatbot" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Ask Health Assistant</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script src="/static/js/voice-recognition.js"></script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/settings')
def settings():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Settings - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #333;
            }
            .nav-link {
                color: #333;
            }
            .nav-link.active {
                background-color: var(--bs-primary);
                color: white;
            }
            .nav-link:hover {
                color: var(--bs-primary);
            }
            .dropdown-toggle, .fs-4.fw-bold.text-primary {
                color: var(--bs-primary) !important;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
                background-color: #ffffff;
                color: #333;
            }
            .settings-card {
                transition: all 0.3s ease;
                border-radius: 10px;
                margin-bottom: 20px;
                background-color: #ffffff;
                color: #333;
            }
            .form-switch .form-check-input {
                width: 3em;
                height: 1.5em;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                            <li>
                                <a href="/chatbot" class="nav-link">
                                    <i class="bi bi-chat-dots me-2"></i>
                                    Chatbot Assistant
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item active" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Settings</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-lg-8">
                            <!-- Appearance Settings -->
                            <div class="card settings-card">
                                <div class="card-header">
                                    <h5 class="card-title"><i class="bi bi-palette me-2"></i> Appearance</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Theme Mode</h6>
                                            <p class="text-muted mb-0 small">Choose between light and dark mode</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="themeMode" checked>
                                            <label class="form-check-label" for="themeMode">Dark Mode</label>
                                        </div>
                                    </div>
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">High Contrast</h6>
                                            <p class="text-muted mb-0 small">Increase contrast for better visibility</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="highContrast">
                                            <label class="form-check-label" for="highContrast">Off</label>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label for="fontSizeRange" class="form-label">Text Size</label>
                                        <input type="range" class="form-range" min="1" max="3" step="1" id="fontSizeRange" value="2">
                                        <div class="d-flex justify-content-between">
                                            <span>Small</span>
                                            <span>Medium</span>
                                            <span>Large</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Notifications Settings -->
                            <div class="card settings-card">
                                <div class="card-header">
                                    <h5 class="card-title"><i class="bi bi-bell me-2"></i> Notifications</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">App Notifications</h6>
                                            <p class="text-muted mb-0 small">Receive notifications in app</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="appNotifications" checked>
                                            <label class="form-check-label" for="appNotifications">On</label>
                                        </div>
                                    </div>
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Email Notifications</h6>
                                            <p class="text-muted mb-0 small">Receive notifications via email</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="emailNotifications" checked>
                                            <label class="form-check-label" for="emailNotifications">On</label>
                                        </div>
                                    </div>
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">SMS Notifications</h6>
                                            <p class="text-muted mb-0 small">Receive notifications via SMS</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="smsNotifications">
                                            <label class="form-check-label" for="smsNotifications">Off</label>
                                        </div>
                                    </div>
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Health Reminders</h6>
                                            <p class="text-muted mb-0 small">Medication, checkups, and appointments</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="healthReminders" checked>
                                            <label class="form-check-label" for="healthReminders">On</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Privacy Settings -->
                            <div class="card settings-card">
                                <div class="card-header">
                                    <h5 class="card-title"><i class="bi bi-shield-lock me-2"></i> Privacy & Security</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Two-Factor Authentication</h6>
                                            <p class="text-muted mb-0 small">Add an extra layer of security</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="twoFactor">
                                            <label class="form-check-label" for="twoFactor">Off</label>
                                        </div>
                                    </div>
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Data Analytics</h6>
                                            <p class="text-muted mb-0 small">Help improve app by sharing anonymous usage data</p>
                                        </div>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input" type="checkbox" role="switch" id="dataAnalytics" checked>
                                            <label class="form-check-label" for="dataAnalytics">On</label>
                                        </div>
                                    </div>
                                    <div class="mb-3 d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1">Profile Visibility</h6>
                                            <p class="text-muted mb-0 small">Control who can see your profile</p>
                                        </div>
                                        <select class="form-select form-select-sm" style="width: 150px;" id="profileVisibility">
                                            <option value="private">Private</option>
                                            <option value="healthcare">Healthcare Providers</option>
                                            <option value="public">Public</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Language & Region -->
                            <div class="card settings-card">
                                <div class="card-header">
                                    <h5 class="card-title"><i class="bi bi-globe me-2"></i> Language & Region</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <label for="language" class="form-label">Language</label>
                                        <select class="form-select" id="language">
                                            <option value="en">English</option>
                                            <option value="hi">Hindi</option>
                                            <option value="ta">Tamil</option>
                                            <option value="te">Telugu</option>
                                            <option value="mr">Marathi</option>
                                            <option value="bn">Bengali</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="region" class="form-label">Region</label>
                                        <select class="form-select" id="region">
                                            <option value="in">India</option>
                                            <option value="bd">Bangladesh</option>
                                            <option value="np">Nepal</option>
                                            <option value="lk">Sri Lanka</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="text-end mt-4">
                                <button class="btn btn-secondary me-2">Reset to Default</button>
                                <button class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
                            </div>
                        </div>
                        
                        <div class="col-lg-4">
                            <!-- Account Actions -->
                            <div class="card settings-card">
                                <div class="card-header">
                                    <h5 class="card-title"><i class="bi bi-person-gear me-2"></i> Account</h5>
                                </div>
                                <div class="card-body">
                                    <div class="list-group list-group-flush">
                                        <a href="/profile" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Edit Profile</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" data-bs-toggle="modal" data-bs-target="#changePasswordModal">
                                            <span>Change Password</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Linked Accounts</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Data & Privacy</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Help & Support -->
                            <div class="card settings-card">
                                <div class="card-header">
                                    <h5 class="card-title"><i class="bi bi-question-circle me-2"></i> Help & Support</h5>
                                </div>
                                <div class="card-body">
                                    <div class="list-group list-group-flush">
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>FAQs</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Contact Support</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Report a Problem</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                        <a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                            <span>Terms & Policies</span>
                                            <i class="bi bi-chevron-right"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- App Info -->
                            <div class="card settings-card">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <h6 class="mb-0">App Version</h6>
                                        <span class="text-muted">2.5.0</span>
                                    </div>
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <h6 class="mb-0">Last Updated</h6>
                                        <span class="text-muted">March 25, 2025</span>
                                    </div>
                                    <div class="text-center mt-3">
                                        <a href="#" class="btn btn-sm btn-outline-secondary">Check for Updates</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Change Password Modal -->
        <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-labelledby="changePasswordModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="changePasswordModalLabel">Change Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="changePasswordForm">
                            <div class="mb-3">
                                <label for="currentPassword" class="form-label">Current Password</label>
                                <input type="password" class="form-control" id="currentPassword" required>
                            </div>
                            <div class="mb-3">
                                <label for="newPassword" class="form-label">New Password</label>
                                <input type="password" class="form-control" id="newPassword" required minlength="8">
                                <div class="form-text">Password must be at least 8 characters long and include a mix of letters, numbers, and symbols.</div>
                            </div>
                            <div class="mb-3">
                                <label for="confirmPassword" class="form-label">Confirm New Password</label>
                                <input type="password" class="form-control" id="confirmPassword" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="changePassword()">Update Password</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Toggle theme mode
            document.getElementById('themeMode').addEventListener('change', function() {
                if (this.checked) {
                    document.querySelector('label[for="themeMode"]').textContent = 'Dark Mode';
                    // Apply dark mode
                } else {
                    document.querySelector('label[for="themeMode"]').textContent = 'Light Mode';
                    // Apply light mode
                }
            });
            
            // Toggle high contrast
            document.getElementById('highContrast').addEventListener('change', function() {
                if (this.checked) {
                    document.querySelector('label[for="highContrast"]').textContent = 'On';
                    // Apply high contrast
                } else {
                    document.querySelector('label[for="highContrast"]').textContent = 'Off';
                    // Remove high contrast
                }
            });
            
            // Toggle notifications switches labels
            document.querySelectorAll('.form-check-input').forEach(function(switchInput) {
                switchInput.addEventListener('change', function() {
                    const label = document.querySelector(`label[for="${this.id}"]`);
                    if (this.checked) {
                        label.textContent = 'On';
                    } else {
                        label.textContent = 'Off';
                    }
                });
            });
            
            // Save settings
            function saveSettings() {
                // Get settings data
                const settingsData = {
                    themeMode: document.getElementById('themeMode').checked ? 'dark' : 'light',
                    highContrast: document.getElementById('highContrast').checked,
                    fontSize: document.getElementById('fontSizeRange').value,
                    appNotifications: document.getElementById('appNotifications').checked,
                    emailNotifications: document.getElementById('emailNotifications').checked,
                    smsNotifications: document.getElementById('smsNotifications').checked,
                    healthReminders: document.getElementById('healthReminders').checked,
                    twoFactor: document.getElementById('twoFactor').checked,
                    dataAnalytics: document.getElementById('dataAnalytics').checked,
                    profileVisibility: document.getElementById('profileVisibility').value,
                    language: document.getElementById('language').value,
                    region: document.getElementById('region').value
                };
                
                // Normally this would be sent to the server
                // For demo purposes, we'll just show a success message
                alert('Settings saved successfully!');
                console.log(settingsData);
            }
            
            // Change password
            function changePassword() {
                const currentPassword = document.getElementById('currentPassword').value;
                const newPassword = document.getElementById('newPassword').value;
                const confirmPassword = document.getElementById('confirmPassword').value;
                
                // Validate passwords match
                if (newPassword !== confirmPassword) {
                    alert('New passwords do not match!');
                    return;
                }
                
                // Normally this would be sent to the server for validation and updating
                // For demo purposes, we'll just show a success message
                alert('Password updated successfully!');
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                modal.hide();
            }
        </script>
        
        <!-- Floating Chatbot Button -->
        <div class="position-fixed bottom-0 end-0 p-3">
            <a href="/chatbot" class="btn btn-primary rounded-circle shadow-lg p-3">
                <i class="bi bi-chat-dots-fill fs-4"></i>
            </a>
        </div>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/nutrition')
def nutrition():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nutrition Guide - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .food-card {
                border-radius: 12px;
                overflow: hidden;
                transition: all 0.3s ease;
            }
            .food-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .food-img {
                height: 180px;
                object-fit: cover;
            }
            .nutrition-category-card {
                transition: all 0.3s ease;
                cursor: pointer;
                border-radius: 10px;
            }
            .nutrition-category-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .meal-planner {
                background-color: rgba(var(--bs-primary-rgb), 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link active">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                            <li>
                                <a href="/chatbot" class="nav-link">
                                    <i class="bi bi-chat-dots me-2"></i>
                                    Chatbot Assistant
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Nutrition Guide</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <!-- Personalized Meal Plan -->
                    <div class="meal-planner my-4">
                        <div class="row">
                            <div class="col-md-6">
                                <h4 class="mb-3">Your Personalized Nutrition Plan</h4>
                                <p>Based on your health profile and current condition, we've created a customized nutrition plan to help you maintain optimal health.</p>
                                <div class="d-flex gap-2 mt-4">
                                    <a href="/nutrition/meal-planner" class="btn btn-primary">View Full Meal Plan</a>
                                    <a href="/nutrition/shopping-list" class="btn btn-outline-primary">Get Shopping List</a>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100 border-0 bg-transparent">
                                    <div class="card-body">
                                        <h5>Today's Recommendation</h5>
                                        <div class="d-flex align-items-center mb-2">
                                            <i class="bi bi-sunrise fs-5 me-2 text-primary"></i>
                                            <span class="fw-bold">Breakfast:</span>
                                            <span class="ms-2">Oatmeal with nuts, seeds, and berries</span>
                                        </div>
                                        <div class="d-flex align-items-center mb-2">
                                            <i class="bi bi-sun fs-5 me-2 text-primary"></i>
                                            <span class="fw-bold">Lunch:</span>
                                            <span class="ms-2">Spinach salad with lentils and grilled chicken</span>
                                        </div>
                                        <div class="d-flex align-items-center mb-2">
                                            <i class="bi bi-moon fs-5 me-2 text-primary"></i>
                                            <span class="fw-bold">Dinner:</span>
                                            <span class="ms-2">Salmon with roasted vegetables and quinoa</span>
                                        </div>
                                        <div class="d-flex align-items-center">
                                            <i class="bi bi-cup-hot fs-5 me-2 text-primary"></i>
                                            <span class="fw-bold">Snacks:</span>
                                            <span class="ms-2">Greek yogurt with honey, mixed nuts</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Nutrition Categories -->
                    <h4 class="mt-5 mb-3">Nutrition Categories</h4>
                    <div class="row">
                        <div class="col-md-4 mb-4">
                            <div class="card nutrition-category-card h-100">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-droplet-half text-primary fs-1 mb-3"></i>
                                    <h5>Iron-Rich Foods</h5>
                                    <p class="mb-3">Essential for preventing anemia, these foods help maintain healthy blood and energy levels.</p>
                                    <a href="/nutrition/iron-rich" class="btn btn-sm btn-primary">View Foods</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-4">
                            <div class="card nutrition-category-card h-100">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-egg-fried text-primary fs-1 mb-3"></i>
                                    <h5>Protein Sources</h5>
                                    <p class="mb-3">Crucial for muscle development and repair, especially important during pregnancy.</p>
                                    <a href="/nutrition/protein" class="btn btn-sm btn-primary">View Foods</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-4">
                            <div class="card nutrition-category-card h-100">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-flower1 text-primary fs-1 mb-3"></i>
                                    <h5>Folate-Rich Foods</h5>
                                    <p class="mb-3">Important for preventing birth defects and supporting healthy pregnancy development.</p>
                                    <a href="/nutrition/folate" class="btn btn-sm btn-primary">View Foods</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-4">
                            <div class="card nutrition-category-card h-100">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-cup-straw text-primary fs-1 mb-3"></i>
                                    <h5>Low Glycemic Foods</h5>
                                    <p class="mb-3">Helps manage blood sugar levels and prevent gestational diabetes complications.</p>
                                    <a href="/nutrition/low-glycemic" class="btn btn-sm btn-primary">View Foods</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-4">
                            <div class="card nutrition-category-card h-100">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-heart-pulse text-primary fs-1 mb-3"></i>
                                    <h5>Heart-Healthy Foods</h5>
                                    <p class="mb-3">Support cardiovascular health and manage blood pressure during pregnancy.</p>
                                    <a href="/nutrition/heart-healthy" class="btn btn-sm btn-primary">View Foods</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-4">
                            <div class="card nutrition-category-card h-100">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-wrench text-primary fs-1 mb-3"></i>
                                    <h5>Calcium Sources</h5>
                                    <p class="mb-3">Essential for bone development and preventing complications in pregnancy.</p>
                                    <a href="/nutrition/calcium" class="btn btn-sm btn-primary">View Foods</a>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Recommended Foods -->
                    <h4 class="mt-5 mb-3">Recommended Foods for You</h4>
                    <div class="row">
                        <div class="col-lg-3 col-md-6 mb-4">
                            <div class="card food-card h-100">
                                <img src="https://source.unsplash.com/random/300x180/?spinach" class="food-img" alt="Spinach">
                                <div class="card-body">
                                    <h5 class="card-title">Spinach</h5>
                                    <p class="card-text">Rich in iron, folate, and vitamins to help prevent anemia and support fetal development.</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div class="badge bg-success">Iron-Rich</div>
                                        <a href="/nutrition/food/spinach" class="btn btn-sm btn-outline-primary">Details</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-6 mb-4">
                            <div class="card food-card h-100">
                                <img src="https://source.unsplash.com/random/300x180/?lentils" class="food-img" alt="Lentils">
                                <div class="card-body">
                                    <h5 class="card-title">Lentils</h5>
                                    <p class="card-text">Excellent source of plant-based protein, iron, and folate for vegetarians and vegans.</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div class="badge bg-success">Protein</div>
                                        <a href="/nutrition/food/lentils" class="btn btn-sm btn-outline-primary">Details</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-6 mb-4">
                            <div class="card food-card h-100">
                                <img src="https://source.unsplash.com/random/300x180/?salmon" class="food-img" alt="Salmon">
                                <div class="card-body">
                                    <h5 class="card-title">Salmon</h5>
                                    <p class="card-text">Rich in Omega-3 fatty acids that support brain development and heart health.</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div class="badge bg-success">Heart-Healthy</div>
                                        <a href="/nutrition/food/salmon" class="btn btn-sm btn-outline-primary">Details</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-6 mb-4">
                            <div class="card food-card h-100">
                                <img src="https://source.unsplash.com/random/300x180/?yogurt" class="food-img" alt="Greek Yogurt">
                                <div class="card-body">
                                    <h5 class="card-title">Greek Yogurt</h5>
                                    <p class="card-text">High in protein and calcium, supporting bone health and muscle development.</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div class="badge bg-success">Calcium</div>
                                        <a href="/nutrition/food/greek-yogurt" class="btn btn-sm btn-outline-primary">Details</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Nutrition Articles -->
                    <h4 class="mt-5 mb-3">Nutrition Articles</h4>
                    <div class="row">
                        <div class="col-md-6 mb-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">Managing Anemia Through Diet</h5>
                                    <p class="card-text">Learn how to prevent and manage anemia with the right nutritional choices and iron-rich foods.</p>
                                    <a href="/nutrition/article/anemia-diet" class="btn btn-sm btn-primary">Read Article</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 mb-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">Dietary Guidelines for Gestational Diabetes</h5>
                                    <p class="card-text">Practical tips for maintaining stable blood sugar levels during pregnancy through proper nutrition.</p>
                                    <a href="/nutrition/article/gestational-diabetes" class="btn btn-sm btn-primary">Read Article</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/appointments')
def appointments():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Appointments - NeoMitra</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            .sidebar {
                min-height: 100vh;
                border-right: 1px solid #e0e0e0;
            }
            .page-header {
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .appointment-card {
                border-left: 4px solid #7952b3;
                transition: all 0.3s ease;
            }
            .appointment-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .appointment-upcoming {
                border-left-color: #20c997;
            }
            .appointment-past {
                border-left-color: #6c757d;
            }
            .appointment-calendar {
                border-radius: 12px;
                overflow: hidden;
            }
            .calendar-header {
                background-color: #7952b3;
                color: white;
                padding: 15px;
            }
            .calendar-day {
                height: 120px;
                border: 1px solid #e0e0e0;
                padding: 5px;
            }
            .calendar-day-header {
                font-weight: bold;
                text-align: center;
                padding: 10px;
                border: 1px solid #e0e0e0;
            }
            .calendar-day:hover {
                background-color: rgba(121, 82, 179, 0.1);
                cursor: pointer;
            }
            .calendar-day.has-appointment {
                background-color: rgba(32, 201, 151, 0.1);
            }
            .appointment-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-lg-2 col-md-3 p-0 sidebar">
                    <div class="d-flex flex-column p-3">
                        <a href="/" class="d-flex align-items-center mb-3 text-decoration-none">
                            <i class="bi bi-heart-pulse-fill text-primary me-2 fs-4"></i>
                            <span class="fs-4 fw-bold text-primary">NeoMitra</span>
                        </a>
                        <hr>
                        <ul class="nav nav-pills flex-column mb-auto">
                            <li class="nav-item">
                                <a href="/dashboard" class="nav-link">
                                    <i class="bi bi-speedometer2 me-2"></i>
                                    Dashboard
                                </a>
                            </li>
                            <li>
                                <a href="/health-records" class="nav-link">
                                    <i class="bi bi-journal-medical me-2"></i>
                                    Health Records
                                </a>
                            </li>
                            <li>
                                <a href="/risk_assessment" class="nav-link">
                                    <i class="bi bi-shield-check me-2"></i>
                                    Risk Assessment
                                </a>
                            </li>
                            <li>
                                <a href="/appointments" class="nav-link active">
                                    <i class="bi bi-calendar-check me-2"></i>
                                    Appointments
                                </a>
                            </li>
                            <li>
                                <a href="/nutrition" class="nav-link">
                                    <i class="bi bi-egg-fried me-2"></i>
                                    Nutrition Guide
                                </a>
                            </li>
                            <li>
                                <a href="/government_schemes" class="nav-link">
                                    <i class="bi bi-bank me-2"></i>
                                    Government Schemes
                                </a>
                            </li>
                            <li>
                                <a href="/chatbot" class="nav-link">
                                    <i class="bi bi-chat-dots me-2"></i>
                                    Chatbot Assistant
                                </a>
                            </li>
                        </ul>
                        <hr>
                        <div class="dropdown">
                            <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" id="dropdownUser1" data-bs-toggle="dropdown">
                                <img src="https://via.placeholder.com/32" alt="User" width="32" height="32" class="rounded-circle me-2">
                                <strong>{{ username }}</strong>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark text-small shadow" aria-labelledby="dropdownUser1">
                                <li><a class="dropdown-item" href="/profile">Profile</a></li>
                                <li><a class="dropdown-item" href="/settings">Settings</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="/logout">Sign out</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="col-lg-10 col-md-9 p-4">
                    <div class="page-header d-flex justify-content-between align-items-center">
                        <h2>Appointment Management</h2>
                        <a href="/dashboard" class="btn btn-outline-primary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Back to Dashboard
                        </a>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-md-7">
                            <!-- Appointment Calendar -->
                            <div class="appointment-calendar mb-4">
                                <div class="calendar-header d-flex justify-content-between align-items-center">
                                    <button class="btn btn-sm btn-outline-light">
                                        <i class="bi bi-chevron-left"></i>
                                    </button>
                                    <h5 class="mb-0">March 2025</h5>
                                    <button class="btn btn-sm btn-outline-light">
                                        <i class="bi bi-chevron-right"></i>
                                    </button>
                                </div>
                                <div class="calendar-body bg-white">
                                    <div class="row">
                                        <div class="col calendar-day-header">Sun</div>
                                        <div class="col calendar-day-header">Mon</div>
                                        <div class="col calendar-day-header">Tue</div>
                                        <div class="col calendar-day-header">Wed</div>
                                        <div class="col calendar-day-header">Thu</div>
                                        <div class="col calendar-day-header">Fri</div>
                                        <div class="col calendar-day-header">Sat</div>
                                    </div>
                                    <div class="row">
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day">1</div>
                                        <div class="col calendar-day">2</div>
                                    </div>
                                    <div class="row">
                                        <div class="col calendar-day">3</div>
                                        <div class="col calendar-day">4</div>
                                        <div class="col calendar-day">5</div>
                                        <div class="col calendar-day">6</div>
                                        <div class="col calendar-day">7</div>
                                        <div class="col calendar-day">8</div>
                                        <div class="col calendar-day">9</div>
                                    </div>
                                    <div class="row">
                                        <div class="col calendar-day">10</div>
                                        <div class="col calendar-day">11</div>
                                        <div class="col calendar-day">12</div>
                                        <div class="col calendar-day">13</div>
                                        <div class="col calendar-day">14</div>
                                        <div class="col calendar-day has-appointment">
                                            15
                                            <div class="mt-1">
                                                <span class="appointment-dot bg-primary"></span>
                                                <small>10:00 AM</small>
                                            </div>
                                        </div>
                                        <div class="col calendar-day">16</div>
                                    </div>
                                    <div class="row">
                                        <div class="col calendar-day">17</div>
                                        <div class="col calendar-day">18</div>
                                        <div class="col calendar-day">19</div>
                                        <div class="col calendar-day">20</div>
                                        <div class="col calendar-day">21</div>
                                        <div class="col calendar-day">22</div>
                                        <div class="col calendar-day">23</div>
                                    </div>
                                    <div class="row">
                                        <div class="col calendar-day">24</div>
                                        <div class="col calendar-day">25</div>
                                        <div class="col calendar-day">26</div>
                                        <div class="col calendar-day">27</div>
                                        <div class="col calendar-day">28</div>
                                        <div class="col calendar-day has-appointment">
                                            29
                                            <div class="mt-1">
                                                <span class="appointment-dot bg-success"></span>
                                                <small>2:30 PM</small>
                                            </div>
                                        </div>
                                        <div class="col calendar-day">30</div>
                                    </div>
                                    <div class="row">
                                        <div class="col calendar-day">31</div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                        <div class="col calendar-day"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Upcoming Appointments -->
                            <div class="card mb-4">
                                <div class="card-header d-flex justify-content-between align-items-center">
                                    <h5 class="card-title mb-0">Upcoming Appointments</h5>
                                    <a href="/appointments/new" class="btn btn-sm btn-primary">Schedule New</a>
                                </div>
                                <div class="card-body">
                                    <div class="appointment-card appointment-upcoming p-3 mb-3">
                                        <div class="d-flex justify-content-between">
                                            <div>
                                                <h5>Prenatal Check-up</h5>
                                                <p class="mb-0">Dr. Priya Sharma, Obstetrics & Gynecology</p>
                                                <small class="text-muted">City Hospital, Room 305</small>
                                            </div>
                                            <div class="text-end">
                                                <p class="text-success fw-bold mb-0">March 15, 2025</p>
                                                <p class="mb-0">10:00 AM - 11:00 AM</p>
                                                <small class="text-muted">3 days from now</small>
                                            </div>
                                        </div>
                                        <div class="d-flex justify-content-between align-items-center mt-3">
                                            <div>
                                                <span class="badge bg-primary me-2">Prenatal Care</span>
                                                <span class="badge bg-secondary">Regular Check-up</span>
                                            </div>
                                            <div>
                                                <a href="/appointments/123/reschedule" class="btn btn-sm btn-outline-primary">Reschedule</a>
                                                <a href="/appointments/123/cancel" class="btn btn-sm btn-outline-danger">Cancel</a>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="appointment-card appointment-upcoming p-3">
                                        <div class="d-flex justify-content-between">
                                            <div>
                                                <h5>Anemia Follow-up</h5>
                                                <p class="mb-0">Dr. Rajesh Kumar, Hematology</p>
                                                <small class="text-muted">City Hospital, Room 204</small>
                                            </div>
                                            <div class="text-end">
                                                <p class="text-success fw-bold mb-0">March 29, 2025</p>
                                                <p class="mb-0">2:30 PM - 3:15 PM</p>
                                                <small class="text-muted">17 days from now</small>
                                            </div>
                                        </div>
                                        <div class="d-flex justify-content-between align-items-center mt-3">
                                            <div>
                                                <span class="badge bg-primary me-2">Anemia</span>
                                                <span class="badge bg-secondary">Follow-up</span>
                                            </div>
                                            <div>
                                                <a href="/appointments/124/reschedule" class="btn btn-sm btn-outline-primary">Reschedule</a>
                                                <a href="/appointments/124/cancel" class="btn btn-sm btn-outline-danger">Cancel</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Past Appointments -->
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title mb-0">Past Appointments</h5>
                                </div>
                                <div class="card-body">
                                    <div class="appointment-card appointment-past p-3 mb-3">
                                        <div class="d-flex justify-content-between">
                                            <div>
                                                <h5>First Trimester Screening</h5>
                                                <p class="mb-0">Dr. Priya Sharma, Obstetrics & Gynecology</p>
                                                <small class="text-muted">City Hospital, Room 305</small>
                                            </div>
                                            <div class="text-end">
                                                <p class="text-muted fw-bold mb-0">February 14, 2025</p>
                                                <p class="mb-0">9:30 AM - 11:00 AM</p>
                                            </div>
                                        </div>
                                        <div class="d-flex justify-content-between align-items-center mt-3">
                                            <div>
                                                <span class="badge bg-primary me-2">Prenatal Care</span>
                                                <span class="badge bg-secondary">Screening</span>
                                            </div>
                                            <div>
                                                <a href="/appointments/121/view" class="btn btn-sm btn-outline-primary">View Notes</a>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="appointment-card appointment-past p-3">
                                        <div class="d-flex justify-content-between">
                                            <div>
                                                <h5>Initial Hemoglobin Test</h5>
                                                <p class="mb-0">Dr. Rajesh Kumar, Hematology</p>
                                                <small class="text-muted">City Hospital, Lab 102</small>
                                            </div>
                                            <div class="text-end">
                                                <p class="text-muted fw-bold mb-0">January 28, 2025</p>
                                                <p class="mb-0">3:00 PM - 3:30 PM</p>
                                            </div>
                                        </div>
                                        <div class="d-flex justify-content-between align-items-center mt-3">
                                            <div>
                                                <span class="badge bg-primary me-2">Anemia</span>
                                                <span class="badge bg-secondary">Diagnostic</span>
                                            </div>
                                            <div>
                                                <a href="/appointments/120/view" class="btn btn-sm btn-outline-primary">View Notes</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-5">
                            <!-- Schedule New Appointment -->
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title mb-0">Schedule New Appointment</h5>
                                </div>
                                <div class="card-body">
                                    <form>
                                        <div class="mb-3">
                                            <label class="form-label">Appointment Type</label>
                                            <select class="form-select">
                                                <option>Regular Check-up</option>
                                                <option>Anemia Follow-up</option>
                                                <option>Prenatal Care</option>
                                                <option>Ultrasound</option>
                                                <option>Blood Test</option>
                                                <option>Other</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Doctor</label>
                                            <select class="form-select">
                                                <option>Dr. Priya Sharma (Obstetrics & Gynecology)</option>
                                                <option>Dr. Rajesh Kumar (Hematology)</option>
                                                <option>Dr. Meera Patel (General Medicine)</option>
                                                <option>Dr. Sanjay Gupta (Cardiology)</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Preferred Date</label>
                                            <input type="date" class="form-control">
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Preferred Time</label>
                                            <select class="form-select">
                                                <option>Morning (9:00 AM - 12:00 PM)</option>
                                                <option>Afternoon (12:00 PM - 3:00 PM)</option>
                                                <option>Evening (3:00 PM - 6:00 PM)</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Notes (optional)</label>
                                            <textarea class="form-control" rows="3" placeholder="Any specific concerns or questions for the doctor?"></textarea>
                                        </div>
                                        <button type="button" class="btn btn-primary w-100">Schedule Appointment</button>
                                    </form>
                                </div>
                            </div>
                            
                            <!-- Healthcare Providers -->
                            <div class="card mb-4">
                                <div class="card-header">
                                    <h5 class="card-title mb-0">Your Healthcare Providers</h5>
                                </div>
                                <div class="card-body">
                                    <div class="d-flex align-items-center mb-3">
                                        <img src="https://via.placeholder.com/50" alt="Dr. Priya" class="rounded-circle me-3">
                                        <div>
                                            <h6 class="mb-0">Dr. Priya Sharma</h6>
                                            <small class="text-muted">Obstetrics & Gynecology</small>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center mb-3">
                                        <img src="https://via.placeholder.com/50" alt="Dr. Rajesh" class="rounded-circle me-3">
                                        <div>
                                            <h6 class="mb-0">Dr. Rajesh Kumar</h6>
                                            <small class="text-muted">Hematology</small>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center">
                                        <img src="https://via.placeholder.com/50" alt="Dr. Meera" class="rounded-circle me-3">
                                        <div>
                                            <h6 class="mb-0">Dr. Meera Patel</h6>
                                            <small class="text-muted">General Medicine</small>
                                        </div>
                                    </div>
                                    <div class="d-grid mt-3">
                                        <a href="/providers" class="btn btn-sm btn-outline-primary">Manage Healthcare Providers</a>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Reminders & Preparations -->
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title mb-0">Upcoming Appointment Reminders</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <h6>Prenatal Check-up (March 15, 2025)</h6>
                                        <p class="mb-1">Please remember to:</p>
                                        <ul>
                                            <li>Bring your health records</li>
                                            <li>Come with a full bladder for ultrasound</li>
                                            <li>Note down any questions for your doctor</li>
                                            <li>Arrive 15 minutes early for registration</li>
                                        </ul>
                                    </div>
                                    <div>
                                        <h6>Anemia Follow-up (March 29, 2025)</h6>
                                        <p class="mb-1">Please remember to:</p>
                                        <ul>
                                            <li>Fast for 8 hours before the appointment</li>
                                            <li>Bring your previous test results</li>
                                            <li>Track your iron supplement intake</li>
                                            <li>Note any symptoms you've experienced</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """, username=session.get('username', 'User'))

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Get user data from session
    email = session.get('user_email')
    username = session.get('username')
    user_data = users.get(email, {})
    
    # Get health metrics from session if available (updated from health records)
    weight = session.get('weight', '65')
    blood_pressure = session.get('blood_pressure', '120/80')
    blood_sugar = session.get('blood_sugar', '98')
    hemoglobin = session.get('hemoglobin', '11.2')
    bmi = session.get('bmi', '22.5')
    
    # Get risk assessment results if available
    pregnancy_risk_level = session.get('pregnancy_risk_level', 'Moderate')
    pregnancy_risk_score = session.get('pregnancy_risk_score', '65')
    anemia_risk_level = session.get('anemia_risk_level', 'High')
    anemia_risk_score = session.get('anemia_risk_score', '85')
    diabetes_risk_level = session.get('diabetes_risk_level', 'Low') 
    diabetes_risk_score = session.get('diabetes_risk_score', '15')
    
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
        <nav class="navbar navbar-expand-lg navbar-light bg-white">
            <div class="container">
                <a class="navbar-brand text-primary" href="/">
                    <i class="bi bi-heart-pulse-fill"></i> NeoMitra
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="/">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active text-dark" href="/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="#">Health Records</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="/risk_assessment">Risk Assessment</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-dark" href="#">Resources</a>
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
                                <a href="/health-records" class="btn btn-sm btn-outline-primary">Update</a>
                            </div>
                            <div class="card-body">
                                <div class="metric">
                                    <div class="metric-label">Weight</div>
                                    <div class="metric-value">{{ weight }} kg</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Blood Pressure</div>
                                    <div class="metric-value">{{ blood_pressure }} mmHg</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Blood Sugar (Fasting)</div>
                                    <div class="metric-value">{{ blood_sugar }} mg/dL</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Hemoglobin</div>
                                    <div class="metric-value warning">{{ hemoglobin }} g/dL</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">BMI</div>
                                    <div class="metric-value">{{ bmi }}</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Risk Assessment -->
                        <div class="card mb-4">
                            <div class="card-header">
                                <h5 class="card-title">
                                    <i class="bi bi-shield-check"></i>
                                    Completed Health Risk Assessments
                                </h5>
                                <a href="/risk_assessment" class="btn btn-sm btn-outline-primary">Take New Assessment</a>
                            </div>
                            <div class="card-body">
                                <div class="row mb-4">
                                    <div class="col-md-6">
                                        <div class="d-flex align-items-center mb-3">
                                            <div style="width: 15px; height: 15px; background-color: #7952b3; border-radius: 50%; margin-right: 10px;"></div>
                                            <span>Anemia Risk: {{ anemia_risk_level }} ({{ anemia_risk_score }}%)</span>
                                        </div>
                                        <div class="d-flex align-items-center mb-3">
                                            <div style="width: 15px; height: 15px; background-color: #ff6b6b; border-radius: 50%; margin-right: 10px;"></div>
                                            <span>High Risk Pregnancy: {{ pregnancy_risk_level }} ({{ pregnancy_risk_score }}%)</span>
                                        </div>
                                        <div class="d-flex align-items-center mb-3">
                                            <div style="width: 15px; height: 15px; background-color: #20c997; border-radius: 50%; margin-right: 10px;"></div>
                                            <span>Diabetes Risk: {{ diabetes_risk_level }} ({{ diabetes_risk_score }}%)</span>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="chart-container" style="position: relative; height: 200px;">
                                            <canvas id="riskPieChart" width="100%" height="100%"></canvas>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <button class="btn btn-sm btn-outline-primary me-2" onclick="downloadPDF()">
                                            <i class="bi bi-file-earmark-pdf"></i> Download Report
                                        </button>
                                        <div class="btn-group">
                                            <button class="btn btn-sm btn-outline-success dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                                <i class="bi bi-share"></i> Share
                                            </button>
                                            <ul class="dropdown-menu">
                                                <li><a class="dropdown-item" href="#" onclick="shareViaWhatsApp()"><i class="bi bi-whatsapp text-success me-2"></i>WhatsApp</a></li>
                                                <li><a class="dropdown-item" href="#" onclick="shareViaEmail()"><i class="bi bi-envelope text-primary me-2"></i>Email</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                    <a href="/risk_assessment" class="btn btn-primary">Take New Assessment</a>
                                </div>
                            </div>
                        </div>
                        
                        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
                        <script>
                            // Initialize chart once DOM is loaded
                            document.addEventListener('DOMContentLoaded', function() {
                                const ctx = document.getElementById('riskPieChart').getContext('2d');
                                
                                // Get risk data from template variables
                                const riskScores = [
                                    parseInt('{{ anemia_risk_score }}'),
                                    parseInt('{{ pregnancy_risk_score }}'),
                                    parseInt('{{ diabetes_risk_score }}')
                                ];
                                
                                const pieChart = new Chart(ctx, {
                                    type: 'pie',
                                    data: {
                                        labels: ['Anemia Risk', 'Pregnancy Risk', 'Diabetes Risk'],
                                        datasets: [{
                                            data: riskScores,
                                            backgroundColor: [
                                                '#7952b3',
                                                '#ff6b6b',
                                                '#20c997'
                                            ],
                                            borderWidth: 1
                                        }]
                                    },
                                    options: {
                                        responsive: true,
                                        maintainAspectRatio: false,
                                        plugins: {
                                            legend: {
                                                position: 'bottom'
                                            }
                                        }
                                    }
                                });
                            });
                            
                            // Functions for downloading and sharing reports
                            function downloadPDF() {
                                const { jsPDF } = window.jspdf;
                                const doc = new jsPDF();
                                
                                // Add content to PDF
                                doc.setFontSize(22);
                                doc.text('NeoMitra Health Risk Assessment Report', 20, 20);
                                
                                doc.setFontSize(14);
                                doc.text('Assessment Date: ' + new Date().toLocaleDateString(), 20, 30);
                                
                                doc.setFontSize(16);
                                doc.text('Risk Assessment Results:', 20, 40);
                                
                                doc.setFontSize(12);
                                doc.text('Anemia Risk: {{ anemia_risk_level }} ({{ anemia_risk_score }}%)', 25, 50);
                                doc.text('Pregnancy Risk: {{ pregnancy_risk_level }} ({{ pregnancy_risk_score }}%)', 25, 60);
                                doc.text('Diabetes Risk: {{ diabetes_risk_level }} ({{ diabetes_risk_score }}%)', 25, 70);
                                
                                doc.setFontSize(16);
                                doc.text('Health Metrics:', 20, 90);
                                
                                doc.setFontSize(12);
                                doc.text('Weight: {{ weight }} kg', 25, 100);
                                doc.text('Blood Pressure: {{ blood_pressure }} mmHg', 25, 110);
                                doc.text('Blood Sugar: {{ blood_sugar }} mg/dL', 25, 120);
                                doc.text('Hemoglobin: {{ hemoglobin }} g/dL', 25, 130);
                                doc.text('BMI: {{ bmi }}', 25, 140);
                                
                                // Add recommendations based on risk levels
                                doc.setFontSize(16);
                                doc.text('Recommendations:', 20, 160);
                                
                                doc.setFontSize(12);
                                var y = 170;
                                
                                if ('{{ anemia_risk_level }}' === 'High') {
                                    doc.text('• Consult with a healthcare provider about your anemia risk', 25, y);
                                    y += 10;
                                    doc.text('• Increase consumption of iron-rich foods', 25, y);
                                    y += 10;
                                }
                                
                                if ('{{ pregnancy_risk_level }}' === 'High') {
                                    doc.text('• Schedule regular prenatal check-ups', 25, y);
                                    y += 10;
                                    doc.text('• Follow medical advice for high-risk pregnancy management', 25, y);
                                    y += 10;
                                }
                                
                                if ('{{ diabetes_risk_level }}' === 'High') {
                                    doc.text('• Monitor blood sugar levels regularly', 25, y);
                                    y += 10;
                                    doc.text('• Consult with a healthcare provider about diabetes prevention', 25, y);
                                    y += 10;
                                }
                                
                                doc.text('• Maintain a healthy diet and regular exercise routine', 25, y);
                                
                                // Add footer
                                doc.setFontSize(10);
                                doc.text('This report is generated by NeoMitra Health Platform. Please consult with a healthcare provider for medical advice.', 20, 280);
                                
                                // Save the PDF
                                doc.save('NeoMitra_Health_Risk_Report.pdf');
                            }
                            
                            function shareViaWhatsApp() {
                                const message = 'My NeoMitra Health Risk Assessment Results:\n' +
                                    'Anemia Risk: {{ anemia_risk_level }} ({{ anemia_risk_score }}%)\n' +
                                    'Pregnancy Risk: {{ pregnancy_risk_level }} ({{ pregnancy_risk_score }}%)\n' +
                                    'Diabetes Risk: {{ diabetes_risk_level }} ({{ diabetes_risk_score }}%)';
                                
                                const encodedMessage = encodeURIComponent(message);
                                window.open(`https://wa.me/?text=${encodedMessage}`, '_blank');
                            }
                            
                            function shareViaEmail() {
                                const subject = 'My NeoMitra Health Risk Assessment Results';
                                const body = 'My NeoMitra Health Risk Assessment Results:\n' +
                                    'Anemia Risk: {{ anemia_risk_level }} ({{ anemia_risk_score }}%)\n' +
                                    'Pregnancy Risk: {{ pregnancy_risk_level }} ({{ pregnancy_risk_score }}%)\n' +
                                    'Diabetes Risk: {{ diabetes_risk_level }} ({{ diabetes_risk_score }}%)';
                                
                                const mailtoLink = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
                                window.location.href = mailtoLink;
                            }
                        </script>
                        
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
                                <a href="/health-records" class="quick-action d-block mb-3">
                                    <i class="bi bi-journal-plus"></i>
                                    <div>
                                        <div class="quick-action-title">Record Health Metrics</div>
                                        <p class="quick-action-description">Update your current health measurements</p>
                                    </div>
                                </a>
                                
                                <a href="/appointments" class="quick-action d-block mb-3">
                                    <i class="bi bi-clipboard2-pulse"></i>
                                    <div>
                                        <div class="quick-action-title">Schedule Check-up</div>
                                        <p class="quick-action-description">Book your next health appointment</p>
                                    </div>
                                </a>
                                
                                <a href="/chatbot" class="quick-action d-block mb-3">
                                    <i class="bi bi-chat-dots"></i>
                                    <div>
                                        <div class="quick-action-title">Chat with Assistant</div>
                                        <p class="quick-action-description">Get answers to your health questions</p>
                                    </div>
                                </a>
                                
                                <a href="/government_schemes" class="quick-action d-block">
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
                                <a href="/appointments" class="btn btn-sm btn-outline-primary">Add New</a>
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
                                
                                <a href="/appointments" class="btn btn-outline-primary w-100 mt-2">View All Appointments</a>
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
                                <a href="/nutrition" class="btn btn-outline-primary w-100">View Nutrition Guide</a>
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
        
        <!-- Floating Chatbot Button -->
        <div class="chatbot-button" onclick="toggleChatbot()" style="position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px; border-radius: 50%; background-color: var(--primary-color); color: white; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); cursor: pointer; z-index: 1000; transition: all 0.3s;">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        
        <!-- Chatbot Popup -->
        <div id="chatbotPopup" style="position: fixed; bottom: 90px; right: 20px; width: 350px; height: 500px; background-color: white; border-radius: 10px; box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2); z-index: 999; display: none; flex-direction: column; overflow: hidden;">
            <div style="background-color: var(--primary-color); color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <i class="bi bi-robot me-2"></i>
                    NeoMitra Assistant
                </div>
                <button class="btn-close btn-close-white" onclick="toggleChatbot()"></button>
            </div>
            <div id="chatbotMessages" style="flex: 1; padding: 15px; overflow-y: auto;">
                <div style="margin-bottom: 10px; max-width: 80%; background-color: #f1f1f1; color: #333; padding: 10px 15px; border-radius: 18px 18px 18px 0; align-self: flex-start;">
                    Hello! I'm your NeoMitra health assistant. How can I help you today?
                </div>
            </div>
            <div style="border-top: 1px solid #e0e0e0; padding: 10px; display: flex;">
                <input type="text" id="chatbotInput" placeholder="Type your message..." onkeypress="handleChatKeyPress(event)" style="flex: 1; padding: 10px; border: 1px solid #e0e0e0; border-radius: 5px; margin-right: 10px;">
                <button class="btn btn-primary" onclick="sendChatMessage()">
                    <i class="bi bi-send"></i>
                </button>
            </div>
        </div>
        
        <!-- Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        
        <!-- Chatbot Script -->
        <script>
            // Chatbot functionality
            let chatbotOpen = false;
            
            function toggleChatbot() {
                chatbotOpen = !chatbotOpen;
                document.getElementById('chatbotPopup').style.display = chatbotOpen ? 'flex' : 'none';
                if (chatbotOpen) {
                    document.getElementById('chatbotInput').focus();
                }
            }
            
            function handleChatKeyPress(event) {
                if (event.key === 'Enter') {
                    sendChatMessage();
                }
            }
            
            function sendChatMessage() {
                const input = document.getElementById('chatbotInput');
                const message = input.value.trim();
                
                if (message) {
                    // Add user message
                    addChatMessage(message, 'user');
                    input.value = '';
                    
                    // Send to backend API
                    fetch('/api/chatbot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Add bot response
                        addChatMessage(data.response, 'bot');
                    })
                    .catch(error => {
                        console.error('Error processing message:', error);
                        addChatMessage("I'm sorry, I couldn't process your message. Please try again.", 'bot');
                    });
                }
            }
            
            function addChatMessage(text, sender) {
                const messagesContainer = document.getElementById('chatbotMessages');
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                
                if (sender === 'user') {
                    messageElement.style.background = 'var(--primary-color)';
                    messageElement.style.color = 'white';
                    messageElement.style.padding = '10px 15px';
                    messageElement.style.borderRadius = '18px 18px 0 18px';
                    messageElement.style.alignSelf = 'flex-end';
                    messageElement.style.marginLeft = 'auto';
                    messageElement.style.marginBottom = '10px';
                    messageElement.style.maxWidth = '80%';
                } else {
                    messageElement.style.background = '#f1f1f1';
                    messageElement.style.color = '#333';
                    messageElement.style.padding = '10px 15px';
                    messageElement.style.borderRadius = '18px 18px 18px 0';
                    messageElement.style.alignSelf = 'flex-start';
                    messageElement.style.marginBottom = '10px';
                    messageElement.style.maxWidth = '80%';
                }
                
                messageElement.textContent = text;
                messagesContainer.appendChild(messageElement);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        </script>
    </body>
    </html>
    """, username=username, user_data=user_data, 
       weight=weight, blood_pressure=blood_pressure, blood_sugar=blood_sugar, 
       hemoglobin=hemoglobin, bmi=bmi, pregnancy_risk_level=pregnancy_risk_level, 
       pregnancy_risk_score=pregnancy_risk_score, anemia_risk_level=anemia_risk_level, 
       anemia_risk_score=anemia_risk_score, diabetes_risk_level=diabetes_risk_level, 
       diabetes_risk_score=diabetes_risk_score)

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect('/')

@app.route('/health-records', methods=['GET', 'POST'])
def health_records():
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Handle form submission
    if request.method == 'POST':
        # Update session with health metrics
        session['weight'] = request.form.get('weight', '65')
        
        # Combine systolic and diastolic for blood pressure
        bp_systolic = request.form.get('bp_systolic', '120')
        bp_diastolic = request.form.get('bp_diastolic', '80')
        session['blood_pressure'] = f"{bp_systolic}/{bp_diastolic}"
        
        session['blood_sugar'] = request.form.get('blood_sugar', '98')
        session['hemoglobin'] = request.form.get('hemoglobin', '11.2')
        
        # Calculate BMI if height and weight are provided
        weight = float(request.form.get('weight', '0'))
        height = float(request.form.get('height', '0'))
        if weight > 0 and height > 0:
            # BMI = weight(kg) / (height(m))²
            bmi = weight / ((height/100) ** 2)
            session['bmi'] = f"{bmi:.1f}"
        
        # Redirect to dashboard to show updated metrics
        flash('Health records updated successfully!', 'success')
        return redirect('/dashboard')
    
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
                background-color: #212529;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }
            
            .navbar-brand, .nav-link {
                color: white !important;
                font-weight: 600;
            }
            
            .navbar .btn {
                background-color: #ff6b6b;
                border-color: #ff6b6b;
                color: white;
                font-weight: 600;
            }
            
            .navbar .btn:hover {
                background-color: #fa5252;
                border-color: #fa5252;
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
                                        <form action="/health-records" method="POST">
                                            <div class="row mb-3">
                                                <div class="col-md-6">
                                                    <label for="weight" class="form-label">Weight (kg)</label>
                                                    <input type="number" class="form-control" id="weight" name="weight" step="0.1" value="{{ session.get('weight', '65') }}">
                                                </div>
                                                <div class="col-md-6">
                                                    <label for="height" class="form-label">Height (cm)</label>
                                                    <input type="number" class="form-control" id="height" name="height" step="0.1" value="165">
                                                </div>
                                            </div>
                                            
                                            <div class="row mb-3">
                                                <div class="col-md-6">
                                                    <label class="form-label">Blood Pressure (mmHg)</label>
                                                    <div class="input-group">
                                                        <input type="number" class="form-control" id="bp_systolic" name="bp_systolic" placeholder="Systolic" value="{{ session.get('blood_pressure', '120/80').split('/')[0] }}">
                                                        <span class="input-group-text">/</span>
                                                        <input type="number" class="form-control" id="bp_diastolic" name="bp_diastolic" placeholder="Diastolic" value="{{ session.get('blood_pressure', '120/80').split('/')[1] }}">
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <label for="blood_sugar" class="form-label">Blood Sugar (mg/dL)</label>
                                                    <input type="number" class="form-control" id="blood_sugar" name="blood_sugar" step="0.1" value="{{ session.get('blood_sugar', '98') }}">
                                                </div>
                                            </div>
                                            
                                            <div class="row mb-3">
                                                <div class="col-md-6">
                                                    <label for="hemoglobin" class="form-label">Hemoglobin (g/dL)</label>
                                                    <input type="number" class="form-control" id="hemoglobin" name="hemoglobin" step="0.1" value="{{ session.get('hemoglobin', '11.2') }}">
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