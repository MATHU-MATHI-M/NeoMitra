from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    preferred_language = db.Column(db.String(10), default="en")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    health_records = db.relationship('HealthRecord', backref='user', lazy=True)
    risk_assessments = db.relationship('RiskAssessment', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'


class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Pregnancy details
    is_pregnant = db.Column(db.Boolean, default=False)
    pregnancy_week = db.Column(db.Integer, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    
    # Health metrics
    weight = db.Column(db.Float, nullable=True)  # in kg
    height = db.Column(db.Float, nullable=True)  # in cm
    blood_pressure_systolic = db.Column(db.Integer, nullable=True)
    blood_pressure_diastolic = db.Column(db.Integer, nullable=True)
    blood_sugar = db.Column(db.Float, nullable=True)
    hemoglobin = db.Column(db.Float, nullable=True)
    
    # Medical history
    previous_pregnancies = db.Column(db.Integer, default=0)
    previous_complications = db.Column(db.Text, nullable=True)
    existing_conditions = db.Column(db.Text, nullable=True)
    current_medications = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<HealthRecord {self.id} for User {self.user_id}>'


class RiskAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Risk scores (0-100)
    pregnancy_risk_score = db.Column(db.Float, nullable=True)
    anemia_risk_score = db.Column(db.Float, nullable=True)
    
    # Assessment details
    risk_factors = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    follow_up_required = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<RiskAssessment {self.id} for User {self.user_id}>'


class GovernmentScheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    application_process = db.Column(db.Text, nullable=False)
    documents_required = db.Column(db.Text, nullable=False)
    scheme_url = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f'<GovernmentScheme {self.name}>'


class MedicalGuideline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MedicalGuideline {self.title}>'


class NutritionAdvice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    pregnancy_stage = db.Column(db.String(50), nullable=True)  # trimester or postpartum
    description = db.Column(db.Text, nullable=False)
    food_recommendations = db.Column(db.Text, nullable=False)
    foods_to_avoid = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<NutritionAdvice {self.title}>'


class ChatbotConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<ChatbotConversation {self.id}>'
