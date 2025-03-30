from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms import TextAreaField, IntegerField, FloatField, DateField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from datetime import date
from models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    preferred_language = SelectField('Preferred Language', 
                                    choices=[('en', 'English'), ('hi', 'Hindi'), 
                                             ('ta', 'Tamil'), ('te', 'Telugu'), 
                                             ('bn', 'Bengali'), ('mr', 'Marathi')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')
    
    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth.data > date.today():
            raise ValidationError('Date of birth cannot be in the future.')


class HealthRecordForm(FlaskForm):
    is_pregnant = BooleanField('Are you pregnant?')
    pregnancy_week = IntegerField('Pregnancy Week (if applicable)', validators=[Optional()])
    due_date = DateField('Due Date (if applicable)', validators=[Optional()])
    
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    blood_pressure_systolic = IntegerField('Blood Pressure (Systolic)', validators=[Optional()])
    blood_pressure_diastolic = IntegerField('Blood Pressure (Diastolic)', validators=[Optional()])
    blood_sugar = FloatField('Blood Sugar (mg/dL)', validators=[Optional()])
    hemoglobin = FloatField('Hemoglobin (g/dL)', validators=[Optional()])
    
    previous_pregnancies = IntegerField('Number of Previous Pregnancies', validators=[Optional()])
    previous_complications = TextAreaField('Previous Pregnancy Complications', validators=[Optional()])
    existing_conditions = TextAreaField('Existing Medical Conditions', validators=[Optional()])
    current_medications = TextAreaField('Current Medications', validators=[Optional()])
    
    submit = SubmitField('Save Health Record')


class RiskAssessmentForm(FlaskForm):
    # Common symptoms and risk factors for high-risk pregnancies
    age_above_35 = BooleanField('Are you over 35 years old?')
    multiple_pregnancy = BooleanField('Are you carrying multiple babies (twins, triplets, etc.)?')
    previous_csection = BooleanField('Have you had a previous C-section?')
    previous_preterm_birth = BooleanField('Have you had a previous preterm birth?')
    previous_miscarriage = BooleanField('Have you had previous miscarriages?')
    
    # Medical conditions
    diabetes = BooleanField('Do you have diabetes?')
    hypertension = BooleanField('Do you have high blood pressure?')
    heart_disease = BooleanField('Do you have heart disease?')
    kidney_disease = BooleanField('Do you have kidney disease?')
    autoimmune_disease = BooleanField('Do you have an autoimmune disease?')
    
    # Current pregnancy complications
    gestational_diabetes = BooleanField('Have you been diagnosed with gestational diabetes?')
    preeclampsia = BooleanField('Have you been diagnosed with preeclampsia?')
    placenta_previa = BooleanField('Have you been diagnosed with placenta previa?')
    bleeding = BooleanField('Have you experienced vaginal bleeding during this pregnancy?')
    
    # Lifestyle factors
    smoking = BooleanField('Do you smoke?')
    alcohol = BooleanField('Do you consume alcohol?')
    drug_use = BooleanField('Do you use recreational drugs?')
    
    # Anemia risk factors
    fatigue = BooleanField('Do you often feel fatigued or weak?')
    dizzy_spells = BooleanField('Do you experience dizziness or fainting?')
    pale_skin = BooleanField('Have you noticed that your skin is paler than usual?')
    shortness_of_breath = BooleanField('Do you experience shortness of breath during normal activities?')
    poor_diet = BooleanField('Do you have limited access to iron-rich foods?')
    recent_blood_loss = BooleanField('Have you experienced any recent blood loss?')
    
    additional_notes = TextAreaField('Additional Notes or Concerns', validators=[Optional()])
    submit = SubmitField('Submit Assessment')


class ProfileUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Optional()])
    preferred_language = SelectField('Preferred Language', 
                                    choices=[('en', 'English'), ('hi', 'Hindi'), 
                                             ('ta', 'Tamil'), ('te', 'Telugu'), 
                                             ('bn', 'Bengali'), ('mr', 'Marathi')])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', 
                                     validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
