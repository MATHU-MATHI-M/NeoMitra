import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Accordion } from 'react-bootstrap';
import './RiskAssessmentPage.css';

const RiskAssessmentPage = ({ user }) => {
  const [activeTab, setActiveTab] = useState('pregnancy');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [assessmentResults, setAssessmentResults] = useState(null);
  
  // Form state for pregnancy risk assessment
  const [pregnancyForm, setPregnancyForm] = useState({
    age_above_35: false,
    multiple_pregnancy: false,
    previous_csection: false,
    previous_preterm_birth: false,
    previous_miscarriage: false,
    diabetes: false,
    hypertension: false,
    heart_disease: false,
    kidney_disease: false,
    autoimmune_disease: false,
    gestational_diabetes: false,
    preeclampsia: false,
    placenta_previa: false,
    bleeding: false,
    smoking: false,
    alcohol: false,
    drug_use: false,
    additional_notes: ''
  });
  
  // Form state for anemia risk assessment
  const [anemiaForm, setAnemiaForm] = useState({
    fatigue: false,
    dizzy_spells: false,
    pale_skin: false,
    shortness_of_breath: false,
    poor_diet: false,
    recent_blood_loss: false,
    hemoglobin_level: '',
    diet_low_iron: false,
    heavy_periods: false,
    pregnancy_close: false,
    additional_notes: ''
  });
  
  // Handle form input changes for pregnancy risk assessment
  const handlePregnancyChange = (e) => {
    const { name, value, type, checked } = e.target;
    setPregnancyForm({
      ...pregnancyForm,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  // Handle form input changes for anemia risk assessment
  const handleAnemiaChange = (e) => {
    const { name, value, type, checked } = e.target;
    setAnemiaForm({
      ...anemiaForm,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // For demonstration, calculate mock risk scores
    setTimeout(() => {
      // Calculate mock pregnancy risk score
      const pregnancyRiskFactors = Object.entries(pregnancyForm)
        .filter(([key, value]) => value === true && key !== 'additional_notes')
        .map(([key]) => key);
      
      const pregnancyRiskScore = pregnancyRiskFactors.length * 6;
      
      // Calculate mock anemia risk score
      const anemiaRiskFactors = Object.entries(anemiaForm)
        .filter(([key, value]) => value === true && key !== 'additional_notes' && key !== 'hemoglobin_level')
        .map(([key]) => key);
      
      let anemiaRiskScore = anemiaRiskFactors.length * 8;
      
      // Adjust based on hemoglobin level if provided
      if (anemiaForm.hemoglobin_level) {
        const hemoglobin = parseFloat(anemiaForm.hemoglobin_level);
        if (hemoglobin < 9) {
          anemiaRiskScore += 40;
        } else if (hemoglobin < 11) {
          anemiaRiskScore += 20;
        } else if (hemoglobin < 12) {
          anemiaRiskScore += 10;
        }
      }
      
      // Prepare recommendations based on risk factors
      const pregnancyRecommendations = getPregnancyRecommendations(pregnancyRiskFactors, pregnancyRiskScore);
      const anemiaRecommendations = getAnemiaRecommendations(anemiaRiskFactors, anemiaRiskScore, anemiaForm.hemoglobin_level);
      
      // Set assessment results
      setAssessmentResults({
        pregnancyRisk: {
          score: pregnancyRiskScore,
          level: getRiskLevel(pregnancyRiskScore),
          factors: pregnancyRiskFactors,
          recommendations: pregnancyRecommendations
        },
        anemiaRisk: {
          score: anemiaRiskScore,
          level: getRiskLevel(anemiaRiskScore),
          factors: anemiaRiskFactors,
          recommendations: anemiaRecommendations
        },
        date: new Date().toISOString()
      });
      
      setShowResults(true);
      setIsSubmitting(false);
      
      // In a real app, this would be an API call:
      /*
      const response = await axios.post('/api/risk-assessment', {
        pregnancy_assessment: pregnancyForm,
        anemia_assessment: anemiaForm
      });
      
      setAssessmentResults(response.data);
      setShowResults(true);
      setIsSubmitting(false);
      */
    }, 1500);
  };
  
  // Calculate risk level based on score
  const getRiskLevel = (score) => {
    if (score < 30) return 'Low';
    if (score < 60) return 'Moderate';
    return 'High';
  };
  
  // Get pregnancy risk recommendations
  const getPregnancyRecommendations = (riskFactors, riskScore) => {
    const recommendations = [];
    
    if (riskScore >= 60) {
      recommendations.push('Schedule a consultation with a high-risk pregnancy specialist (perinatologist) within the next week.');
      recommendations.push('Increase the frequency of your prenatal checkups to every 2 weeks or as advised by your doctor.');
    } else if (riskScore >= 30) {
      recommendations.push('Consult with your healthcare provider about your risk factors at your next prenatal visit.');
      recommendations.push('Consider more frequent monitoring of your pregnancy.');
    } else {
      recommendations.push('Continue with your regular prenatal care schedule.');
    }
    
    if (riskFactors.includes('hypertension') || riskFactors.includes('preeclampsia')) {
      recommendations.push('Monitor your blood pressure regularly at home and report any significant changes to your healthcare provider.');
      recommendations.push('Follow a low-sodium diet and stay well-hydrated.');
    }
    
    if (riskFactors.includes('diabetes') || riskFactors.includes('gestational_diabetes')) {
      recommendations.push('Monitor your blood sugar levels as directed by your healthcare provider.');
      recommendations.push('Follow a balanced diet plan suitable for gestational diabetes.');
    }
    
    if (riskFactors.includes('smoking') || riskFactors.includes('alcohol') || riskFactors.includes('drug_use')) {
      recommendations.push('Seek support to stop smoking, drinking alcohol, or using recreational drugs during pregnancy.');
      recommendations.push('Join a support group or program for pregnant women trying to quit harmful substances.');
    }
    
    if (riskFactors.includes('bleeding') || riskFactors.includes('placenta_previa')) {
      recommendations.push('Rest as much as possible and avoid strenuous activities.');
      recommendations.push('Contact your healthcare provider immediately if you experience any bleeding.');
    }
    
    return recommendations;
  };
  
  // Get anemia risk recommendations
  const getAnemiaRecommendations = (riskFactors, riskScore, hemoglobinLevel) => {
    const recommendations = [];
    
    if (riskScore >= 60) {
      recommendations.push('Consult with your doctor immediately about starting iron supplementation.');
      recommendations.push('Schedule a follow-up blood test within 2 weeks to monitor your hemoglobin levels.');
    } else if (riskScore >= 30) {
      recommendations.push('Discuss iron supplementation with your healthcare provider at your next visit.');
      recommendations.push('Increase iron-rich foods in your diet and consider scheduling another hemoglobin test.');
    } else {
      recommendations.push('Continue with a balanced diet that includes iron-rich foods.');
    }
    
    if (hemoglobinLevel && parseFloat(hemoglobinLevel) < 11) {
      recommendations.push('Your hemoglobin level indicates potential anemia. Consult with your healthcare provider for appropriate treatment.');
    }
    
    if (riskFactors.includes('diet_low_iron') || riskFactors.includes('poor_diet')) {
      recommendations.push('Include more iron-rich foods in your diet such as spinach, beans, lentils, red meat, and fortified cereals.');
      recommendations.push('Pair iron-rich foods with vitamin C sources to improve absorption.');
    }
    
    if (riskFactors.includes('fatigue') || riskFactors.includes('dizzy_spells') || riskFactors.includes('shortness_of_breath')) {
      recommendations.push('Rest adequately and avoid overexertion.');
      recommendations.push('Report any worsening symptoms to your healthcare provider.');
    }
    
    return recommendations;
  };
  
  return (
    <div className="risk-assessment-page">
      <Container>
        <div className="assessment-header text-center">
          <h2 className="assessment-title">Risk Assessment</h2>
          <p className="assessment-subtitle">
            Evaluate your pregnancy and anemia risks to receive personalized recommendations
          </p>
        </div>
        
        {showResults ? (
          <div className="assessment-results">
            <Card className="results-card mb-4">
              <Card.Body>
                <div className="results-header">
                  <h3 className="results-title">Your Assessment Results</h3>
                  <div className="results-date">
                    Assessed on: {new Date(assessmentResults.date).toLocaleDateString()}
                  </div>
                </div>
                
                <Row className="risk-scores">
                  <Col md={6} className="mb-4">
                    <div className="risk-score-card">
                      <div className="score-header">
                        <h4 className="score-title">Pregnancy Risk</h4>
                        <div className={`risk-badge ${assessmentResults.pregnancyRisk.level.toLowerCase()}`}>
                          {assessmentResults.pregnancyRisk.level}
                        </div>
                      </div>
                      <div className="score-progress">
                        <div className="progress-bar-wrapper">
                          <div 
                            className="progress-bar-fill" 
                            style={{ width: `${Math.min(assessmentResults.pregnancyRisk.score, 100)}%` }}
                          ></div>
                        </div>
                        <div className="progress-labels">
                          <span>Low Risk</span>
                          <span>Moderate</span>
                          <span>High Risk</span>
                        </div>
                      </div>
                    </div>
                  </Col>
                  
                  <Col md={6} className="mb-4">
                    <div className="risk-score-card">
                      <div className="score-header">
                        <h4 className="score-title">Anemia Risk</h4>
                        <div className={`risk-badge ${assessmentResults.anemiaRisk.level.toLowerCase()}`}>
                          {assessmentResults.anemiaRisk.level}
                        </div>
                      </div>
                      <div className="score-progress">
                        <div className="progress-bar-wrapper">
                          <div 
                            className="progress-bar-fill" 
                            style={{ width: `${Math.min(assessmentResults.anemiaRisk.score, 100)}%` }}
                          ></div>
                        </div>
                        <div className="progress-labels">
                          <span>Low Risk</span>
                          <span>Moderate</span>
                          <span>High Risk</span>
                        </div>
                      </div>
                    </div>
                  </Col>
                </Row>
                
                <div className="results-section mb-4">
                  <h4 className="section-title">Recommendations</h4>
                  
                  <Accordion defaultActiveKey="0">
                    <Accordion.Item eventKey="0">
                      <Accordion.Header>Pregnancy Care Recommendations</Accordion.Header>
                      <Accordion.Body>
                        <ul className="recommendations-list">
                          {assessmentResults.pregnancyRisk.recommendations.map((rec, index) => (
                            <li key={index} className="recommendation-item">{rec}</li>
                          ))}
                        </ul>
                      </Accordion.Body>
                    </Accordion.Item>
                    
                    <Accordion.Item eventKey="1">
                      <Accordion.Header>Anemia Prevention Recommendations</Accordion.Header>
                      <Accordion.Body>
                        <ul className="recommendations-list">
                          {assessmentResults.anemiaRisk.recommendations.map((rec, index) => (
                            <li key={index} className="recommendation-item">{rec}</li>
                          ))}
                        </ul>
                      </Accordion.Body>
                    </Accordion.Item>
                  </Accordion>
                </div>
                
                <div className="results-actions">
                  <Button 
                    variant="primary" 
                    className="action-btn me-3"
                    onClick={() => window.print()}
                  >
                    Print Results
                  </Button>
                  <Button 
                    variant="outline-primary" 
                    className="action-btn"
                    onClick={() => setShowResults(false)}
                  >
                    Take Another Assessment
                  </Button>
                </div>
              </Card.Body>
            </Card>
            
            <div className="disclaimer-card">
              <div className="disclaimer-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-info-circle" viewBox="0 0 16 16">
                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                  <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                </svg>
              </div>
              <div className="disclaimer-text">
                <p>This risk assessment is for informational purposes only and should not replace professional medical advice. Always consult with your healthcare provider about your specific situation.</p>
              </div>
            </div>
          </div>
        ) : (
          <Card className="assessment-card">
            <Card.Body>
              <div className="assessment-tabs">
                <div 
                  className={`tab ${activeTab === 'pregnancy' ? 'active' : ''}`}
                  onClick={() => setActiveTab('pregnancy')}
                >
                  Pregnancy Risk
                </div>
                <div 
                  className={`tab ${activeTab === 'anemia' ? 'active' : ''}`}
                  onClick={() => setActiveTab('anemia')}
                >
                  Anemia Risk
                </div>
              </div>
              
              <Form onSubmit={handleSubmit}>
                {activeTab === 'pregnancy' && (
                  <div className="tab-content">
                    <div className="tab-section">
                      <h4 className="section-title">Medical History</h4>
                      <Row>
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="age_above_35"
                            name="age_above_35"
                            label="Are you over 35 years old?"
                            checked={pregnancyForm.age_above_35}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="multiple_pregnancy"
                            name="multiple_pregnancy"
                            label="Are you carrying multiple babies (twins, triplets, etc.)?"
                            checked={pregnancyForm.multiple_pregnancy}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="previous_csection"
                            name="previous_csection"
                            label="Have you had a previous C-section?"
                            checked={pregnancyForm.previous_csection}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="previous_preterm_birth"
                            name="previous_preterm_birth"
                            label="Have you had a previous preterm birth?"
                            checked={pregnancyForm.previous_preterm_birth}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                        </Col>
                        
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="previous_miscarriage"
                            name="previous_miscarriage"
                            label="Have you had previous miscarriages?"
                            checked={pregnancyForm.previous_miscarriage}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="diabetes"
                            name="diabetes"
                            label="Do you have diabetes?"
                            checked={pregnancyForm.diabetes}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="hypertension"
                            name="hypertension"
                            label="Do you have high blood pressure?"
                            checked={pregnancyForm.hypertension}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="heart_disease"
                            name="heart_disease"
                            label="Do you have heart disease?"
                            checked={pregnancyForm.heart_disease}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                        </Col>
                      </Row>
                    </div>
                    
                    <div className="tab-section">
                      <h4 className="section-title">Current Pregnancy</h4>
                      <Row>
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="gestational_diabetes"
                            name="gestational_diabetes"
                            label="Have you been diagnosed with gestational diabetes?"
                            checked={pregnancyForm.gestational_diabetes}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="preeclampsia"
                            name="preeclampsia"
                            label="Have you been diagnosed with preeclampsia?"
                            checked={pregnancyForm.preeclampsia}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="placenta_previa"
                            name="placenta_previa"
                            label="Have you been diagnosed with placenta previa?"
                            checked={pregnancyForm.placenta_previa}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                        </Col>
                        
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="bleeding"
                            name="bleeding"
                            label="Have you experienced vaginal bleeding during this pregnancy?"
                            checked={pregnancyForm.bleeding}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="smoking"
                            name="smoking"
                            label="Do you smoke?"
                            checked={pregnancyForm.smoking}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="alcohol"
                            name="alcohol"
                            label="Do you consume alcohol?"
                            checked={pregnancyForm.alcohol}
                            onChange={handlePregnancyChange}
                            className="mb-3"
                          />
                        </Col>
                      </Row>
                    </div>
                    
                    <Form.Group className="mb-4">
                      <Form.Label>Additional Notes or Concerns</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={3}
                        name="additional_notes"
                        value={pregnancyForm.additional_notes}
                        onChange={handlePregnancyChange}
                        placeholder="Enter any additional information that might be relevant..."
                      />
                    </Form.Group>
                  </div>
                )}
                
                {activeTab === 'anemia' && (
                  <div className="tab-content">
                    <div className="tab-section">
                      <h4 className="section-title">Symptoms</h4>
                      <Row>
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="fatigue"
                            name="fatigue"
                            label="Do you often feel fatigued or weak?"
                            checked={anemiaForm.fatigue}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="dizzy_spells"
                            name="dizzy_spells"
                            label="Do you experience dizziness or fainting?"
                            checked={anemiaForm.dizzy_spells}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="pale_skin"
                            name="pale_skin"
                            label="Have you noticed that your skin is paler than usual?"
                            checked={anemiaForm.pale_skin}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                        </Col>
                        
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="shortness_of_breath"
                            name="shortness_of_breath"
                            label="Do you experience shortness of breath during normal activities?"
                            checked={anemiaForm.shortness_of_breath}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="poor_diet"
                            name="poor_diet"
                            label="Do you have limited access to iron-rich foods?"
                            checked={anemiaForm.poor_diet}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="recent_blood_loss"
                            name="recent_blood_loss"
                            label="Have you experienced any recent blood loss?"
                            checked={anemiaForm.recent_blood_loss}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                        </Col>
                      </Row>
                    </div>
                    
                    <div className="tab-section">
                      <h4 className="section-title">Risk Factors</h4>
                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>Hemoglobin Level (g/dL) (if known)</Form.Label>
                            <Form.Control
                              type="number"
                              step="0.1"
                              name="hemoglobin_level"
                              value={anemiaForm.hemoglobin_level}
                              onChange={handleAnemiaChange}
                              placeholder="Enter your latest hemoglobin reading"
                            />
                          </Form.Group>
                          
                          <Form.Check 
                            type="checkbox"
                            id="diet_low_iron"
                            name="diet_low_iron"
                            label="Is your diet low in iron-rich foods?"
                            checked={anemiaForm.diet_low_iron}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                        </Col>
                        
                        <Col md={6}>
                          <Form.Check 
                            type="checkbox"
                            id="heavy_periods"
                            name="heavy_periods"
                            label="Did you have heavy menstrual periods before pregnancy?"
                            checked={anemiaForm.heavy_periods}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                          
                          <Form.Check 
                            type="checkbox"
                            id="pregnancy_close"
                            name="pregnancy_close"
                            label="Is this pregnancy less than 1 year after a previous pregnancy?"
                            checked={anemiaForm.pregnancy_close}
                            onChange={handleAnemiaChange}
                            className="mb-3"
                          />
                        </Col>
                      </Row>
                    </div>
                    
                    <Form.Group className="mb-4">
                      <Form.Label>Additional Notes or Concerns</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={3}
                        name="additional_notes"
                        value={anemiaForm.additional_notes}
                        onChange={handleAnemiaChange}
                        placeholder="Enter any additional information that might be relevant..."
                      />
                    </Form.Group>
                  </div>
                )}
                
                <div className="form-actions">
                  <Button 
                    variant="secondary" 
                    onClick={() => setActiveTab(activeTab === 'pregnancy' ? 'anemia' : 'pregnancy')}
                    className="me-2"
                  >
                    {activeTab === 'pregnancy' ? 'Next: Anemia Risk' : 'Back to Pregnancy Risk'}
                  </Button>
                  
                  <Button 
                    variant="primary" 
                    type="submit"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Processing Assessment...' : 'Submit Assessment'}
                  </Button>
                </div>
                
                <div className="assessment-note mt-4">
                  <Alert variant="info">
                    <small>This risk assessment tool is for informational purposes only and should not replace professional medical advice. Always consult your healthcare provider.</small>
                  </Alert>
                </div>
              </Form>
            </Card.Body>
          </Card>
        )}
      </Container>
    </div>
  );
};

export default RiskAssessmentPage;