from flask import render_template, url_for, flash, redirect, request, jsonify, session, g
from flask_login import login_user, current_user, logout_user, login_required
from flask_babel import get_locale, _
from app import app, db, babel
from models import User, HealthRecord, RiskAssessment, GovernmentScheme, MedicalGuideline
from models import NutritionAdvice, ChatbotConversation
from forms import (LoginForm, RegistrationForm, HealthRecordForm, RiskAssessmentForm,
                  ProfileUpdateForm, ChangePasswordForm)
from chatbot import get_chatbot_response
from ml_models import predict_pregnancy_risk, predict_anemia_risk
from datetime import datetime
import uuid


def get_locale():
    # If a user is logged in, use their preferred language
    if current_user.is_authenticated:
        return current_user.preferred_language
    # Otherwise try to guess the language from the user accept
    # header the browser transmits or use the default
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or 'en'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=_('Home - NeoMitra'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash(_('Login unsuccessful. Please check email and password'), 'danger')
    
    return render_template('login.html', title=_('Login'), form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            date_of_birth=form.date_of_birth.data,
            preferred_language=form.preferred_language.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Your account has been created! You can now log in.'), 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title=_('Register'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    # Get the most recent health record and risk assessment for the user
    health_record = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
        HealthRecord.record_date.desc()).first()
    risk_assessment = RiskAssessment.query.filter_by(user_id=current_user.id).order_by(
        RiskAssessment.assessment_date.desc()).first()
    
    return render_template('dashboard.html', title=_('Dashboard'), 
                          health_record=health_record, risk_assessment=risk_assessment)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.address = form.address.data
        current_user.preferred_language = form.preferred_language.data
        db.session.commit()
        flash(_('Your profile has been updated!'), 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone_number.data = current_user.phone_number
        form.date_of_birth.data = current_user.date_of_birth
        form.address.data = current_user.address
        form.preferred_language.data = current_user.preferred_language
    
    return render_template('profile.html', title=_('Profile'), form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash(_('Your password has been updated!'), 'success')
            return redirect(url_for('profile'))
        else:
            flash(_('Current password is incorrect.'), 'danger')
    
    return render_template('change_password.html', title=_('Change Password'), form=form)


@app.route('/health_records', methods=['GET', 'POST'])
@login_required
def health_records():
    form = HealthRecordForm()
    if form.validate_on_submit():
        health_record = HealthRecord(
            user_id=current_user.id,
            is_pregnant=form.is_pregnant.data,
            pregnancy_week=form.pregnancy_week.data if form.is_pregnant.data else None,
            due_date=form.due_date.data if form.is_pregnant.data else None,
            weight=form.weight.data,
            height=form.height.data,
            blood_pressure_systolic=form.blood_pressure_systolic.data,
            blood_pressure_diastolic=form.blood_pressure_diastolic.data,
            blood_sugar=form.blood_sugar.data,
            hemoglobin=form.hemoglobin.data,
            previous_pregnancies=form.previous_pregnancies.data,
            previous_complications=form.previous_complications.data,
            existing_conditions=form.existing_conditions.data,
            current_medications=form.current_medications.data
        )
        db.session.add(health_record)
        db.session.commit()
        flash(_('Your health record has been saved!'), 'success')
        return redirect(url_for('health_records'))
    
    # Get all health records for the user
    user_health_records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
        HealthRecord.record_date.desc()).all()
    
    return render_template('health_records.html', title=_('Health Records'), 
                          form=form, health_records=user_health_records)


@app.route('/risk_assessment', methods=['GET', 'POST'])
@login_required
def risk_assessment():
    form = RiskAssessmentForm()
    if form.validate_on_submit():
        # Collect form data for ML prediction
        assessment_data = {
            'age_above_35': form.age_above_35.data,
            'multiple_pregnancy': form.multiple_pregnancy.data,
            'previous_csection': form.previous_csection.data,
            'previous_preterm_birth': form.previous_preterm_birth.data,
            'previous_miscarriage': form.previous_miscarriage.data,
            'diabetes': form.diabetes.data,
            'hypertension': form.hypertension.data,
            'heart_disease': form.heart_disease.data,
            'kidney_disease': form.kidney_disease.data,
            'autoimmune_disease': form.autoimmune_disease.data,
            'gestational_diabetes': form.gestational_diabetes.data,
            'preeclampsia': form.preeclampsia.data,
            'placenta_previa': form.placenta_previa.data,
            'bleeding': form.bleeding.data,
            'smoking': form.smoking.data,
            'alcohol': form.alcohol.data,
            'drug_use': form.drug_use.data,
            'fatigue': form.fatigue.data,
            'dizzy_spells': form.dizzy_spells.data,
            'pale_skin': form.pale_skin.data,
            'shortness_of_breath': form.shortness_of_breath.data,
            'poor_diet': form.poor_diet.data,
            'recent_blood_loss': form.recent_blood_loss.data
        }
        
        # Get the latest health record if available
        latest_health_record = HealthRecord.query.filter_by(user_id=current_user.id).order_by(
            HealthRecord.record_date.desc()).first()
        
        # If we have a health record, add relevant data to assessment
        if latest_health_record:
            assessment_data['hemoglobin'] = latest_health_record.hemoglobin
            assessment_data['age'] = (datetime.now().date() - current_user.date_of_birth).days // 365
            assessment_data['previous_pregnancies'] = latest_health_record.previous_pregnancies
        
        # Make predictions using the ML models
        pregnancy_risk = predict_pregnancy_risk(assessment_data)
        anemia_risk = predict_anemia_risk(assessment_data)
        
        # Determine risk factors and recommendations
        risk_factors = []
        recommendations = []
        
        # Handle pregnancy risk factors
        if assessment_data['age_above_35']:
            risk_factors.append(_("Age above 35"))
            recommendations.append(_("Regular prenatal checkups with special monitoring"))
        
        if assessment_data['multiple_pregnancy']:
            risk_factors.append(_("Multiple pregnancy"))
            recommendations.append(_("Increased nutrition and more frequent monitoring"))
        
        if assessment_data['previous_csection'] or assessment_data['previous_preterm_birth']:
            risk_factors.append(_("Previous pregnancy complications"))
            recommendations.append(_("Close monitoring by specialist"))
        
        if any([assessment_data['diabetes'], assessment_data['hypertension'], 
                assessment_data['heart_disease'], assessment_data['kidney_disease']]):
            risk_factors.append(_("Pre-existing medical conditions"))
            recommendations.append(_("Consultation with specialist for condition management during pregnancy"))
        
        # Handle anemia risk factors
        if assessment_data['fatigue'] or assessment_data['dizzy_spells'] or assessment_data['pale_skin']:
            risk_factors.append(_("Anemia symptoms"))
            recommendations.append(_("Iron-rich diet and possible iron supplements"))
        
        if assessment_data['poor_diet']:
            risk_factors.append(_("Poor nutrition"))
            recommendations.append(_("Dietary consultation and nutrient-rich meal planning"))
        
        # Create a new risk assessment record
        new_assessment = RiskAssessment(
            user_id=current_user.id,
            pregnancy_risk_score=pregnancy_risk,
            anemia_risk_score=anemia_risk,
            risk_factors=", ".join(risk_factors),
            recommendations=", ".join(recommendations),
            follow_up_required=pregnancy_risk > 50 or anemia_risk > 50
        )
        db.session.add(new_assessment)
        db.session.commit()
        
        flash(_('Your risk assessment has been completed!'), 'success')
        return redirect(url_for('risk_assessment'))
    
    # Get all risk assessments for the user
    user_assessments = RiskAssessment.query.filter_by(user_id=current_user.id).order_by(
        RiskAssessment.assessment_date.desc()).all()
    
    return render_template('risk_assessment.html', title=_('Risk Assessment'), 
                          form=form, assessments=user_assessments)


@app.route('/health_schemes')
def health_schemes():
    schemes = GovernmentScheme.query.all()
    return render_template('health_schemes.html', title=_('Government Health Schemes'), schemes=schemes)


@app.route('/medical_guidelines')
def medical_guidelines():
    guidelines = MedicalGuideline.query.all()
    return render_template('medical_guidelines.html', title=_('Medical Guidelines'), guidelines=guidelines)


@app.route('/anemia_prevention')
def anemia_prevention():
    nutritional_advice = NutritionAdvice.query.filter(
        NutritionAdvice.title.like('%anemia%')).all()
    return render_template('anemia_prevention.html', title=_('Anemia Prevention'), advice=nutritional_advice)


@app.route('/nutrition')
def nutrition():
    all_advice = NutritionAdvice.query.all()
    return render_template('nutrition.html', title=_('Nutrition Advice'), advice=all_advice)


@app.route('/chatbot')
def chatbot_page():
    # Generate a session ID if one doesn't exist
    if 'chatbot_session_id' not in session:
        session['chatbot_session_id'] = str(uuid.uuid4())
    
    return render_template('chatbot.html', title=_('NeoMitra Assistant'))


@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    data = request.json
    user_message = data.get('message', '')
    
    # Get the chatbot response
    bot_response = get_chatbot_response(user_message)
    
    # Save the conversation
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
    
    conversation = ChatbotConversation(
        user_id=user_id,
        session_id=session.get('chatbot_session_id', str(uuid.uuid4())),
        user_message=user_message,
        bot_response=bot_response
    )
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({
        'response': bot_response
    })


@app.route('/api/voice_to_text', methods=['POST'])
def voice_to_text():
    # This is just a placeholder route for handling voice input from the frontend
    # In a real implementation, you would process audio data here
    return jsonify({'success': True})


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# Add some sample data to the database for initial testing
def insert_sample_data():
    # Only add data if the tables are empty
    if GovernmentScheme.query.count() == 0:
        schemes = [
            GovernmentScheme(
                name='Pradhan Mantri Matru Vandana Yojana (PMMVY)',
                description='A maternity benefit program run by the government of India.',
                eligibility_criteria='First live birth for women 19 years and above',
                benefits='₹5,000 in three installments',
                application_process='Apply through Anganwadi centers or health facilities',
                documents_required='Aadhaar card, bank account details, MCP card'
            ),
            GovernmentScheme(
                name='Janani Suraksha Yojana (JSY)',
                description='A safe motherhood intervention under the National Health Mission.',
                eligibility_criteria='Pregnant women belonging to BPL households',
                benefits='Cash assistance for institutional delivery',
                application_process='Register at local health center',
                documents_required='BPL card, Aadhaar card, bank account details'
            ),
            GovernmentScheme(
                name='Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (AB-PMJAY)',
                description='Health insurance scheme providing coverage up to ₹5 lakhs per family per year.',
                eligibility_criteria='Economically vulnerable families as per SECC database',
                benefits='Free healthcare services at empanelled hospitals',
                application_process='Visit common service center or health facility with required documents',
                documents_required='Aadhaar card, ration card, income certificate'
            )
        ]
        db.session.bulk_save_objects(schemes)
        db.session.commit()
    
    if MedicalGuideline.query.count() == 0:
        guidelines = [
            MedicalGuideline(
                title='Prenatal Care Guidelines',
                category='Pregnancy',
                content='Regular prenatal visits are crucial for monitoring both maternal and fetal health. '
                        'First trimester: monthly visits. Second trimester: visits every 2-3 weeks. '
                        'Third trimester: weekly visits. Report any unusual symptoms immediately.'
            ),
            MedicalGuideline(
                title='Managing Anemia During Pregnancy',
                category='Anemia',
                content='Anemia during pregnancy is common and can lead to complications if not managed. '
                        'Consume iron-rich foods like spinach, beans, and fortified cereals. '
                        'Take iron supplements as prescribed. Get regular hemoglobin tests.'
            ),
            MedicalGuideline(
                title='Signs of High-Risk Pregnancy',
                category='High-Risk Pregnancy',
                content='Watch for these warning signs: severe headaches, vision changes, sudden swelling, '
                        'abdominal pain, vaginal bleeding, decreased fetal movement, fever above 100.4°F, '
                        'or difficulty breathing. Seek immediate medical attention if you experience any of these.'
            )
        ]
        db.session.bulk_save_objects(guidelines)
        db.session.commit()
    
    if NutritionAdvice.query.count() == 0:
        nutrition_advice = [
            NutritionAdvice(
                title='First Trimester Nutrition',
                pregnancy_stage='First Trimester',
                description='Focus on quality nutrition despite potential morning sickness.',
                food_recommendations='Folate-rich foods (leafy greens, fortified cereals), small frequent meals, '
                                   'ginger for nausea, plenty of water',
                foods_to_avoid='Raw meat, unpasteurized dairy, high-mercury fish, excessive caffeine'
            ),
            NutritionAdvice(
                title='Second Trimester Nutrition',
                pregnancy_stage='Second Trimester',
                description='Increase calorie intake slightly to support growing baby.',
                food_recommendations='Calcium-rich foods (dairy, fortified plant milks), protein (legumes, lean meat), '
                                   'iron-rich foods (spinach, beans), vitamin C sources',
                foods_to_avoid='Raw seafood, alcohol, excessive sugar'
            ),
            NutritionAdvice(
                title='Third Trimester Nutrition',
                pregnancy_stage='Third Trimester',
                description='Focus on nutrient-dense foods as baby\'s growth accelerates.',
                food_recommendations='Omega-3 fatty acids (fatty fish, walnuts), fiber (whole grains, fruits), '
                                   'vitamin D (fortified milk, sunshine), small frequent meals',
                foods_to_avoid='Processed foods high in sodium, caffeine'
            ),
            NutritionAdvice(
                title='Preventing Anemia Through Diet',
                pregnancy_stage=None,
                description='Dietary approaches to prevent and manage anemia during pregnancy.',
                food_recommendations='Iron-rich foods (red meat, spinach, lentils, fortified cereals), '
                                   'vitamin C with meals to enhance iron absorption (citrus fruits, tomatoes, bell peppers), '
                                   'cooking in iron pots',
                foods_to_avoid='Tea and coffee with meals (inhibit iron absorption), excessive dairy with iron-rich meals'
            )
        ]
        db.session.bulk_save_objects(nutrition_advice)
        db.session.commit()
