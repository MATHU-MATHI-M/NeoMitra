import os
from flask import Flask, send_from_directory, jsonify, render_template_string, redirect, url_for

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

# Home page with gradient background like in the provided screenshot
@app.route('/')
def home():
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
                <h1 class="hero-title">Empowering Maternal Health</h1>
                <p class="hero-subtitle">A comprehensive healthcare platform for monitoring, assessing, and improving maternal health with a focus on high-risk pregnancies and anemia prevention.</p>
                <div class="hero-buttons">
                    <a href="/register" class="btn btn-primary me-3">Get Started</a>
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
                            <p class="feature-text">Easily record and monitor vital health metrics throughout your pregnancy journey.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-shield-check"></i>
                            </div>
                            <h3 class="feature-title">Risk Assessment</h3>
                            <p class="feature-text">AI-powered risk assessment for pregnancy complications and anemia with personalized recommendations.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-chat-dots"></i>
                            </div>
                            <h3 class="feature-title">Chatbot Assistant</h3>
                            <p class="feature-text">Get immediate answers to your maternal health questions in your preferred language.</p>
                        </div>
                    </div>
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="bi bi-bank"></i>
                            </div>
                            <h3 class="feature-title">Government Schemes</h3>
                            <p class="feature-text">Stay informed about government healthcare schemes available for pregnant women.</p>
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
                        <p>A maternal healthcare platform focused on high-risk pregnancy detection and anemia prevention, especially for rural areas with limited healthcare access.</p>
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

@app.route('/login')
def login():
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
                
                <form action="#" method="post">
                    <div class="form-group">
                        <label for="email" class="form-label">Email Address</label>
                        <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email">
                    </div>
                    
                    <div class="form-group">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <label for="password" class="form-label mb-0">Password</label>
                            <a href="#" class="forgot-password">Forgot Password?</a>
                        </div>
                        <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password">
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
    </body>
    </html>
    """)

@app.route('/register')
def register():
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
                
                <form action="#" method="post">
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
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)