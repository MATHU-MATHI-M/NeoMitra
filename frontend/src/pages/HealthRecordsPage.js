import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Tab, Nav, Alert, Table } from 'react-bootstrap';
import './HealthRecordsPage.css';

const HealthRecordsPage = ({ user }) => {
  const [activeTab, setActiveTab] = useState('records');
  const [showForm, setShowForm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formSuccess, setFormSuccess] = useState(false);
  
  // Mock health records data - in a real app, this would come from API
  const [healthRecords, setHealthRecords] = useState([
    {
      id: 1,
      date: '2025-03-01',
      weight: 65.4,
      height: 162,
      bmi: 24.9,
      blood_pressure: '120/80',
      blood_sugar: 5.4,
      hemoglobin: 11.8,
      pregnancy_week: 20,
      notes: 'Regular checkup, everything looks normal.'
    },
    {
      id: 2,
      date: '2025-03-15',
      weight: 66.2,
      height: 162,
      bmi: 25.2,
      blood_pressure: '118/76',
      blood_sugar: 5.6,
      hemoglobin: 11.5,
      pregnancy_week: 22,
      notes: 'Mild anemia detected, iron supplements recommended.'
    },
    {
      id: 3,
      date: '2025-03-29',
      weight: 67.0,
      height: 162,
      bmi: 25.5,
      blood_pressure: '125/82',
      blood_sugar: 5.3,
      hemoglobin: 11.9,
      pregnancy_week: 24,
      notes: 'Hemoglobin improving with supplements. Continue current regimen.'
    }
  ]);
  
  // Form state for adding health record
  const [formData, setFormData] = useState({
    weight: '',
    height: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    blood_sugar: '',
    hemoglobin: '',
    pregnancy_week: '',
    is_pregnant: true,
    previous_pregnancies: '',
    previous_complications: '',
    existing_conditions: '',
    current_medications: '',
    notes: ''
  });
  
  // Handle form input changes
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  // Calculate BMI
  const calculateBMI = (weight, height) => {
    if (!weight || !height) return '';
    // BMI = weight (kg) / (height (m))^2
    const heightInMeters = height / 100;
    return (weight / (heightInMeters * heightInMeters)).toFixed(1);
  };
  
  // Get BMI category
  const getBMICategory = (bmi) => {
    if (!bmi) return '';
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal';
    if (bmi < 30) return 'Overweight';
    return 'Obese';
  };
  
  // Format date for display
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };
  
  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Calculate BMI
    const bmi = calculateBMI(parseFloat(formData.weight), parseFloat(formData.height));
    
    // Format blood pressure
    const bloodPressure = `${formData.blood_pressure_systolic}/${formData.blood_pressure_diastolic}`;
    
    // For demonstration, simulate API call with timeout
    setTimeout(() => {
      // Create new health record
      const newRecord = {
        id: healthRecords.length + 1,
        date: new Date().toISOString().split('T')[0],
        weight: parseFloat(formData.weight),
        height: parseFloat(formData.height),
        bmi: parseFloat(bmi),
        blood_pressure: bloodPressure,
        blood_sugar: parseFloat(formData.blood_sugar) || null,
        hemoglobin: parseFloat(formData.hemoglobin) || null,
        pregnancy_week: parseInt(formData.pregnancy_week) || null,
        notes: formData.notes
      };
      
      // Add record to state (in a real app, this would be handled by API)
      setHealthRecords([newRecord, ...healthRecords]);
      
      // Reset form and show success message
      setFormData({
        weight: '',
        height: '',
        blood_pressure_systolic: '',
        blood_pressure_diastolic: '',
        blood_sugar: '',
        hemoglobin: '',
        pregnancy_week: '',
        is_pregnant: true,
        previous_pregnancies: '',
        previous_complications: '',
        existing_conditions: '',
        current_medications: '',
        notes: ''
      });
      setIsSubmitting(false);
      setFormSuccess(true);
      setShowForm(false);
      setActiveTab('records');
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setFormSuccess(false);
      }, 3000);
      
      // In a real app, this would be an API call:
      /*
      const response = await axios.post('/api/health-records', {
        ...formData,
        blood_pressure: bloodPressure,
        bmi: bmi
      });
      
      // Add new record to state
      setHealthRecords([response.data, ...healthRecords]);
      setIsSubmitting(false);
      setFormSuccess(true);
      setShowForm(false);
      setActiveTab('records');
      */
    }, 1500);
  };
  
  return (
    <div className="health-records-page">
      <Container>
        <div className="records-header">
          <div>
            <h2 className="records-title">Health Records</h2>
            <p className="records-subtitle">Track and manage your maternal health information</p>
          </div>
          {!showForm && (
            <Button 
              variant="primary" 
              className="add-record-btn"
              onClick={() => setShowForm(true)}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-plus-lg me-2" viewBox="0 0 16 16">
                <path fillRule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
              </svg>
              Add New Record
            </Button>
          )}
        </div>
        
        {formSuccess && (
          <Alert variant="success" className="mb-4">
            Health record added successfully!
          </Alert>
        )}
        
        {showForm ? (
          <Card className="form-card">
            <Card.Body>
              <div className="form-header">
                <h3 className="form-title">Add New Health Record</h3>
                <Button 
                  variant="link" 
                  className="close-btn"
                  onClick={() => setShowForm(false)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-x-lg" viewBox="0 0 16 16">
                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                  </svg>
                </Button>
              </div>
              
              <Form onSubmit={handleSubmit}>
                <div className="form-section">
                  <h4 className="section-title">Pregnancy Information</h4>
                  <Row>
                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Pregnancy Week</Form.Label>
                        <Form.Control
                          type="number"
                          min="1"
                          max="42"
                          name="pregnancy_week"
                          value={formData.pregnancy_week}
                          onChange={handleChange}
                          placeholder="Enter current week"
                        />
                      </Form.Group>
                    </Col>
                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Previous Pregnancies</Form.Label>
                        <Form.Control
                          type="number"
                          min="0"
                          name="previous_pregnancies"
                          value={formData.previous_pregnancies}
                          onChange={handleChange}
                          placeholder="Number of previous pregnancies"
                        />
                      </Form.Group>
                    </Col>
                    <Col md={4}>
                      <Form.Group className="mb-3">
                        <Form.Label>Pregnancy Status</Form.Label>
                        <Form.Check
                          type="checkbox"
                          label="Currently Pregnant"
                          name="is_pregnant"
                          checked={formData.is_pregnant}
                          onChange={handleChange}
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Form.Group className="mb-3">
                    <Form.Label>Previous Complications</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={2}
                      name="previous_complications"
                      value={formData.previous_complications}
                      onChange={handleChange}
                      placeholder="Enter any previous pregnancy complications"
                    />
                  </Form.Group>
                </div>
                
                <div className="form-section">
                  <h4 className="section-title">Vital Measurements</h4>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Weight (kg) *</Form.Label>
                        <Form.Control
                          type="number"
                          step="0.1"
                          name="weight"
                          value={formData.weight}
                          onChange={handleChange}
                          placeholder="Enter your weight in kg"
                          required
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Height (cm) *</Form.Label>
                        <Form.Control
                          type="number"
                          step="0.1"
                          name="height"
                          value={formData.height}
                          onChange={handleChange}
                          placeholder="Enter your height in cm"
                          required
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Row>
                    <Col md={6}>
                      <Form.Label>Blood Pressure (mmHg)</Form.Label>
                      <Row>
                        <Col>
                          <Form.Group className="mb-3">
                            <Form.Control
                              type="number"
                              name="blood_pressure_systolic"
                              value={formData.blood_pressure_systolic}
                              onChange={handleChange}
                              placeholder="Systolic"
                            />
                          </Form.Group>
                        </Col>
                        <Col xs="auto" className="d-flex align-items-center">
                          <span>/</span>
                        </Col>
                        <Col>
                          <Form.Group className="mb-3">
                            <Form.Control
                              type="number"
                              name="blood_pressure_diastolic"
                              value={formData.blood_pressure_diastolic}
                              onChange={handleChange}
                              placeholder="Diastolic"
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                    </Col>
                    <Col md={6}>
                      <Row>
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>Blood Sugar (mg/dL)</Form.Label>
                            <Form.Control
                              type="number"
                              step="0.1"
                              name="blood_sugar"
                              value={formData.blood_sugar}
                              onChange={handleChange}
                              placeholder="Enter blood sugar"
                            />
                          </Form.Group>
                        </Col>
                        <Col md={6}>
                          <Form.Group className="mb-3">
                            <Form.Label>Hemoglobin (g/dL)</Form.Label>
                            <Form.Control
                              type="number"
                              step="0.1"
                              name="hemoglobin"
                              value={formData.hemoglobin}
                              onChange={handleChange}
                              placeholder="Enter hemoglobin"
                            />
                          </Form.Group>
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                </div>
                
                <div className="form-section">
                  <h4 className="section-title">Medical Information</h4>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Existing Conditions</Form.Label>
                        <Form.Control
                          as="textarea"
                          rows={3}
                          name="existing_conditions"
                          value={formData.existing_conditions}
                          onChange={handleChange}
                          placeholder="Enter any existing medical conditions"
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Current Medications</Form.Label>
                        <Form.Control
                          as="textarea"
                          rows={3}
                          name="current_medications"
                          value={formData.current_medications}
                          onChange={handleChange}
                          placeholder="Enter any medications you are currently taking"
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Form.Group className="mb-3">
                    <Form.Label>Notes</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      name="notes"
                      value={formData.notes}
                      onChange={handleChange}
                      placeholder="Enter any additional notes or concerns"
                    />
                  </Form.Group>
                </div>
                
                <div className="form-actions">
                  <Button 
                    variant="secondary" 
                    onClick={() => setShowForm(false)}
                    className="me-2"
                  >
                    Cancel
                  </Button>
                  
                  <Button 
                    variant="primary" 
                    type="submit"
                    disabled={isSubmitting || !formData.weight || !formData.height}
                  >
                    {isSubmitting ? 'Saving...' : 'Save Health Record'}
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        ) : (
          <Card className="records-card">
            <Card.Body>
              <Tab.Container activeKey={activeTab} onSelect={(key) => setActiveTab(key)}>
                <Nav variant="tabs" className="records-tabs">
                  <Nav.Item>
                    <Nav.Link eventKey="records">Records History</Nav.Link>
                  </Nav.Item>
                  <Nav.Item>
                    <Nav.Link eventKey="summary">Health Summary</Nav.Link>
                  </Nav.Item>
                  <Nav.Item>
                    <Nav.Link eventKey="charts">Health Trends</Nav.Link>
                  </Nav.Item>
                </Nav>
                
                <Tab.Content className="mt-4">
                  <Tab.Pane eventKey="records">
                    {healthRecords.length === 0 ? (
                      <div className="no-records">
                        <p>No health records found. Start tracking your health by adding a record.</p>
                        <Button 
                          variant="primary" 
                          onClick={() => setShowForm(true)}
                        >
                          Add First Record
                        </Button>
                      </div>
                    ) : (
                      <div className="records-table-container">
                        <Table responsive className="records-table">
                          <thead>
                            <tr>
                              <th>Date</th>
                              <th>Week</th>
                              <th>Weight (kg)</th>
                              <th>BMI</th>
                              <th>Blood Pressure</th>
                              <th>Hemoglobin</th>
                              <th>Notes</th>
                              <th>Actions</th>
                            </tr>
                          </thead>
                          <tbody>
                            {healthRecords.map(record => (
                              <tr key={record.id}>
                                <td>{formatDate(record.date)}</td>
                                <td>{record.pregnancy_week || '-'}</td>
                                <td>{record.weight}</td>
                                <td>
                                  {record.bmi}
                                  <div className="bmi-category">{getBMICategory(record.bmi)}</div>
                                </td>
                                <td>{record.blood_pressure || '-'}</td>
                                <td>{record.hemoglobin || '-'}</td>
                                <td>
                                  <div className="record-notes">
                                    {record.notes || 'No notes'}
                                  </div>
                                </td>
                                <td>
                                  <Button variant="link" size="sm" className="action-btn">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                                      <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                                      <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                                    </svg>
                                  </Button>
                                  <Button variant="link" size="sm" className="action-btn">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-pencil" viewBox="0 0 16 16">
                                      <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                                    </svg>
                                  </Button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </Table>
                      </div>
                    )}
                  </Tab.Pane>
                  
                  <Tab.Pane eventKey="summary">
                    <div className="health-summary">
                      {healthRecords.length === 0 ? (
                        <div className="no-records">
                          <p>No health records found to generate a summary. Please add a health record first.</p>
                          <Button 
                            variant="primary" 
                            onClick={() => setShowForm(true)}
                          >
                            Add First Record
                          </Button>
                        </div>
                      ) : (
                        <>
                          <Row>
                            <Col md={6} lg={3} className="mb-4">
                              <div className="summary-card">
                                <div className="summary-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-calendar-heart" viewBox="0 0 16 16">
                                    <path fillRule="evenodd" d="M4 .5a.5.5 0 0 0-1 0V1H2a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-1V.5a.5.5 0 0 0-1 0V1H4V.5ZM1 14V4h14v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1Zm7-6.507c1.664-1.711 5.825 1.283 0 5.132-5.825-3.85-1.664-6.843 0-5.132Z"/>
                                  </svg>
                                </div>
                                <div className="summary-title">Pregnancy Week</div>
                                <div className="summary-value">{healthRecords[0].pregnancy_week || '-'}</div>
                                <div className="summary-label">Current Week</div>
                              </div>
                            </Col>
                            
                            <Col md={6} lg={3} className="mb-4">
                              <div className="summary-card">
                                <div className="summary-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-heart-pulse" viewBox="0 0 16 16">
                                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053.918 3.995.78 5.323 1.508 7H.43c-2.128-5.697 4.165-8.83 7.394-5.857.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17c3.23-2.974 9.522.159 7.394 5.856h-1.078c.728-1.677.59-3.005.108-3.947C13.486.878 10.4.28 8.717 2.01L8 2.748ZM2.212 10h1.315C4.593 11.183 6.05 12.458 8 13.795c1.949-1.337 3.407-2.612 4.473-3.795h1.315c-1.265 1.566-3.14 3.25-5.788 5-2.648-1.75-4.523-3.434-5.788-5Z"/>
                                    <path d="M10.464 3.314a.5.5 0 0 0-.945.049L7.921 8.956 6.464 5.314a.5.5 0 0 0-.88-.091L3.732 8H.5a.5.5 0 0 0 0 1H4a.5.5 0 0 0 .416-.223l1.473-2.209 1.647 4.118a.5.5 0 0 0 .945-.049l1.598-5.593 1.457 3.642A.5.5 0 0 0 12 9h3.5a.5.5 0 0 0 0-1h-3.162l-1.874-4.686Z"/>
                                  </svg>
                                </div>
                                <div className="summary-title">Blood Pressure</div>
                                <div className="summary-value">
                                  {healthRecords[0].blood_pressure || '-'}
                                </div>
                                <div className="summary-label">Latest Reading</div>
                              </div>
                            </Col>
                            
                            <Col md={6} lg={3} className="mb-4">
                              <div className="summary-card">
                                <div className="summary-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-droplet" viewBox="0 0 16 16">
                                    <path fillRule="evenodd" d="M7.21.8C7.69.295 8 0 8 0c.109.363.234.708.371 1.038.812 1.946 2.073 3.35 3.197 4.6C12.878 7.096 14 8.345 14 10a6 6 0 0 1-12 0C2 6.668 5.58 2.517 7.21.8zm.413 1.021A31.25 31.25 0 0 0 5.794 3.99c-.726.95-1.436 2.008-1.96 3.07C3.304 8.133 3 9.138 3 10a5 5 0 0 0 10 0c0-1.201-.796-2.157-2.181-3.7l-.03-.032C9.75 5.11 8.5 3.72 7.623 1.82z"/>
                                    <path fillRule="evenodd" d="M4.553 7.776c.82-1.641 1.717-2.753 2.093-3.13l.708.708c-.29.29-1.128 1.311-1.907 2.87l-.894-.448z"/>
                                  </svg>
                                </div>
                                <div className="summary-title">Hemoglobin</div>
                                <div className="summary-value">
                                  {healthRecords[0].hemoglobin ? `${healthRecords[0].hemoglobin} g/dL` : '-'}
                                </div>
                                <div className="summary-label">Latest Reading</div>
                              </div>
                            </Col>
                            
                            <Col md={6} lg={3} className="mb-4">
                              <div className="summary-card">
                                <div className="summary-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-weight" viewBox="0 0 16 16">
                                    <path d="M12 1c.993 0 1.91.326 2.656.88L12 5.4 9.896 2.1l-.209-.207A5.002 5.002 0 0 1 12 1zm-8 0c.993 0 1.91.326 2.656.88L8 5.4 5.896 2.1l-.209-.207A5.002 5.002 0 0 1 8 1zm0 13a4.992 4.992 0 0 1-3.202-1.172L6.5 9.49l.907 1.049L8 13.234l.593-2.195.907-1.05 1.7 3.338A4.992 4.992 0 0 1 8 14z"/>
                                    <path d="M4.343 2.343l1.06 1.06A3.003 3.003 0 0 0 4 6c0 .593.173 1.146.47 1.614l.338.45a3.02 3.02 0 0 0 2.566 1.435c1.055.044 2.144-.401 2.574-1.435l.089-.148c.297-.469.47-1.022.47-1.615 0-1.082-.57-2.025-1.4-2.546l1.06-1.06a4.978 4.978 0 0 1 1.88 3.359c0 .938-.25 1.833-.7 2.6l-.345.577a4.979 4.979 0 0 1-4.134 2.39c-2.050 0-3.75-1.6-3.902-3.635a4.99 4.99 0 0 1 1.098-3.533l.019-.025a4.975 4.975 0 0 1 1.348-1.243zM8 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm-.5 3a.5.5 0 0 1 1 0v1.5a.5.5 0 0 1-1 0V4.5z"/>
                                  </svg>
                                </div>
                                <div className="summary-title">Weight</div>
                                <div className="summary-value">
                                  {healthRecords[0].weight} kg
                                </div>
                                <div className="summary-label">BMI: {healthRecords[0].bmi} ({getBMICategory(healthRecords[0].bmi)})</div>
                              </div>
                            </Col>
                          </Row>
                          
                          <div className="health-insights">
                            <h4 className="insights-title">Health Insights</h4>
                            <div className="insights-content">
                              <div className="insight-item">
                                <div className="insight-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" className="bi bi-info-circle" viewBox="0 0 16 16">
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                                  </svg>
                                </div>
                                <div className="insight-text">
                                  <p>Your hemoglobin levels are within the normal range for pregnancy. Continue maintaining a balanced diet rich in iron.</p>
                                </div>
                              </div>
                              <div className="insight-item">
                                <div className="insight-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" className="bi bi-graph-up" viewBox="0 0 16 16">
                                    <path fillRule="evenodd" d="M0 0h1v15h15v1H0V0Zm14.817 3.113a.5.5 0 0 1 .07.704l-4.5 5.5a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61 4.15-5.073a.5.5 0 0 1 .704-.07Z"/>
                                  </svg>
                                </div>
                                <div className="insight-text">
                                  <p>Your weight gain is on track for your stage of pregnancy. Continue with your current dietary habits.</p>
                                </div>
                              </div>
                              <div className="insight-item">
                                <div className="insight-icon">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" className="bi bi-heart-pulse" viewBox="0 0 16 16">
                                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053.918 3.995.78 5.323 1.508 7H.43c-2.128-5.697 4.165-8.83 7.394-5.857.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17c3.23-2.974 9.522.159 7.394 5.856h-1.078c.728-1.677.59-3.005.108-3.947C13.486.878 10.4.28 8.717 2.01L8 2.748ZM2.212 10h1.315C4.593 11.183 6.05 12.458 8 13.795c1.949-1.337 3.407-2.612 4.473-3.795h1.315c-1.265 1.566-3.14 3.25-5.788 5-2.648-1.75-4.523-3.434-5.788-5Z"/>
                                    <path d="M10.464 3.314a.5.5 0 0 0-.945.049L7.921 8.956 6.464 5.314a.5.5 0 0 0-.88-.091L3.732 8H.5a.5.5 0 0 0 0 1H4a.5.5 0 0 0 .416-.223l1.473-2.209 1.647 4.118a.5.5 0 0 0 .945-.049l1.598-5.593 1.457 3.642A.5.5 0 0 0 12 9h3.5a.5.5 0 0 0 0-1h-3.162l-1.874-4.686Z"/>
                                  </svg>
                                </div>
                                <div className="insight-text">
                                  <p>Your blood pressure is in the normal range. Maintain a low-sodium diet and regular physical activity as recommended by your healthcare provider.</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  </Tab.Pane>
                  
                  <Tab.Pane eventKey="charts">
                    <div className="health-charts">
                      {healthRecords.length === 0 ? (
                        <div className="no-records">
                          <p>No health records found to generate charts. Please add a health record first.</p>
                          <Button 
                            variant="primary" 
                            onClick={() => setShowForm(true)}
                          >
                            Add First Record
                          </Button>
                        </div>
                      ) : (
                        <div className="charts-placeholder">
                          <div className="chart-info">
                            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" className="bi bi-bar-chart" viewBox="0 0 16 16">
                              <path d="M4 11H2v3h2v-3zm5-4H7v7h2V7zm5-5v12h-2V2h2zm-2-1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1h-2zM6 7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm-5 4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3z"/>
                            </svg>
                            <p className="chart-text">Health trend charts will be generated as you add more health records over time.</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </Tab.Pane>
                </Tab.Content>
              </Tab.Container>
            </Card.Body>
          </Card>
        )}
      </Container>
    </div>
  );
};

export default HealthRecordsPage;