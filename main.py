import os
from flask import Flask, send_from_directory, jsonify, render_template_string

app = Flask(__name__)

# Health check endpoint
@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "NeoMitra API is running"})

# Chatbot endpoint (mock for now)
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    return jsonify({
        "response": "Hello! I'm NeoMitra Assistant. I can help you with your maternal health questions.",
        "status": "success"
    })

# Simple placeholder HTML for testing the server
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NeoMitra - Maternal Healthcare Platform</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #121212;
                color: #ffffff;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
                text-align: center;
            }
            header {
                background-color: #7952b3;
                padding: 1rem;
                margin-bottom: 2rem;
            }
            h1 {
                color: #ffffff;
                margin: 0;
            }
            .hero {
                background-color: #1e1e1e;
                padding: 3rem 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .hero h2 {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #7952b3;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;
            }
            .feature {
                background-color: #1e1e1e;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            .feature h3 {
                color: #7952b3;
                margin-top: 0;
            }
            footer {
                padding: 1rem;
                background-color: #1e1e1e;
                margin-top: 2rem;
            }
            .btn {
                background-color: #7952b3;
                color: white;
                border: none;
                padding: 0.8rem 1.5rem;
                font-size: 1rem;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
                text-decoration: none;
                display: inline-block;
                margin: 0.5rem;
            }
            .btn:hover {
                background-color: #6742a3;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>NeoMitra</h1>
        </header>
        
        <div class="container">
            <div class="hero">
                <h2>Empowering Maternal Health</h2>
                <p>A comprehensive healthcare platform for monitoring, assessing, and improving maternal health with a focus on high-risk pregnancies and anemia prevention.</p>
                <a href="#" class="btn">Get Started</a>
                <a href="#" class="btn">Learn More</a>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>Health Tracking</h3>
                    <p>Easily record and monitor vital health metrics throughout your pregnancy journey.</p>
                </div>
                <div class="feature">
                    <h3>Risk Assessment</h3>
                    <p>AI-powered risk assessment for pregnancy complications and anemia with personalized recommendations.</p>
                </div>
                <div class="feature">
                    <h3>Chatbot Assistant</h3>
                    <p>Get immediate answers to your maternal health questions in your preferred language.</p>
                </div>
                <div class="feature">
                    <h3>Government Schemes</h3>
                    <p>Stay informed about government healthcare schemes available for pregnant women.</p>
                </div>
            </div>
        </div>
        
        <footer>
            <p>&copy; 2025 NeoMitra. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)