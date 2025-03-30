import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './DashboardPage.css';

const DashboardPage = ({ user }) => {
  // Mock data for dashboard stats - in a real app, this would come from API
  const dashboardData = {
    nextAppointment: {
      date: '2025-04-15',
      time: '10:30 AM',
      doctor: 'Dr. Priya Sharma',
      location: 'Community Health Center, Rajiv Nagar'
    },
    pregnancyDetails: {
      currentWeek: 24,
      dueDate: '2025-09-10',
      trimester: 'Second',
      babySize: 'Size of a corn'
    },
    vitalStats: {
      weight: '62 kg',
      bloodPressure: '118/76',
      lastChecked: '2025-03-25',
      hemoglobin: '11.5 g/dL'
    },
    riskAssessment: {
      lastAssessment: '2025-03-20',
      pregnancyRisk: 'Low',
      anemiaRisk: 'Moderate',
      recommendations: 3
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="dashboard-page">
      <Container>
        <div className="dashboard-header">
          <h2 className="dashboard-title">Welcome, {user?.firstName || 'User'}</h2>
          <p className="dashboard-subtitle">Here's your maternal health summary</p>
        </div>

        <Row className="dashboard-stats">
          {/* Pregnancy Progress */}
          <Col lg={6} className="mb-4">
            <Card className="dashboard-card h-100">
              <Card.Body>
                <Card.Title className="card-title">Pregnancy Progress</Card.Title>
                <div className="pregnancy-progress">
                  <div className="progress-details">
                    <div className="progress-stat">
                      <span className="stat-label">Current Week</span>
                      <span className="stat-value">{dashboardData.pregnancyDetails.currentWeek}</span>
                    </div>
                    <div className="progress-stat">
                      <span className="stat-label">Trimester</span>
                      <span className="stat-value">{dashboardData.pregnancyDetails.trimester}</span>
                    </div>
                    <div className="progress-stat">
                      <span className="stat-label">Due Date</span>
                      <span className="stat-value">{formatDate(dashboardData.pregnancyDetails.dueDate)}</span>
                    </div>
                    <div className="progress-stat">
                      <span className="stat-label">Baby Size</span>
                      <span className="stat-value">{dashboardData.pregnancyDetails.babySize}</span>
                    </div>
                  </div>
                  <div className="progress-bar-container">
                    <div className="progress-bar-wrapper">
                      <div 
                        className="progress-bar-fill" 
                        style={{ width: `${Math.min((dashboardData.pregnancyDetails.currentWeek / 40) * 100, 100)}%` }}
                      ></div>
                    </div>
                    <div className="progress-labels">
                      <span>Week 1</span>
                      <span>Week 40</span>
                    </div>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          {/* Next Appointment */}
          <Col lg={6} className="mb-4">
            <Card className="dashboard-card h-100">
              <Card.Body>
                <Card.Title className="card-title">Next Appointment</Card.Title>
                <div className="appointment-details">
                  <div className="appointment-date">
                    <div className="date-circle">
                      <span className="date-day">{new Date(dashboardData.nextAppointment.date).getDate()}</span>
                      <span className="date-month">{new Date(dashboardData.nextAppointment.date).toLocaleString('default', { month: 'short' })}</span>
                    </div>
                    <div className="appointment-time">{dashboardData.nextAppointment.time}</div>
                  </div>
                  <div className="appointment-info">
                    <p className="info-item">
                      <strong>Doctor:</strong> {dashboardData.nextAppointment.doctor}
                    </p>
                    <p className="info-item">
                      <strong>Location:</strong> {dashboardData.nextAppointment.location}
                    </p>
                    <div className="appointment-actions">
                      <Button variant="outline-primary" size="sm" className="action-btn">Reschedule</Button>
                      <Button variant="outline-secondary" size="sm" className="action-btn">Directions</Button>
                    </div>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>

          {/* Vital Stats */}
          <Col md={6} className="mb-4">
            <Card className="dashboard-card h-100">
              <Card.Body>
                <Card.Title className="card-title">Vital Statistics</Card.Title>
                <div className="vitals-grid">
                  <div className="vital-stat">
                    <span className="vital-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-arrow-up-circle" viewBox="0 0 16 16">
                        <path fillRule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                        <path fillRule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4"/>
                      </svg>
                    </span>
                    <span className="vital-label">Weight</span>
                    <span className="vital-value">{dashboardData.vitalStats.weight}</span>
                  </div>
                  <div className="vital-stat">
                    <span className="vital-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-heart-pulse" viewBox="0 0 16 16">
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053.918 3.995.78 5.323 1.508 7H.43c-2.128-5.697 4.165-8.83 7.394-5.857.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17c3.23-2.974 9.522.159 7.394 5.856h-1.078c.728-1.677.59-3.005.108-3.947C13.486.878 10.4.28 8.717 2.01L8 2.748ZM2.212 10h1.315C4.593 11.183 6.05 12.458 8 13.795c1.949-1.337 3.407-2.612 4.473-3.795h1.315c-1.265 1.566-3.14 3.25-5.788 5-2.648-1.75-4.523-3.434-5.788-5Z"/>
                        <path d="M10.464 3.314a.5.5 0 0 0-.945.049L7.921 8.956 6.464 5.314a.5.5 0 0 0-.88-.091L3.732 8H.5a.5.5 0 0 0 0 1H4a.5.5 0 0 0 .416-.223l1.473-2.209 1.647 4.118a.5.5 0 0 0 .945-.049l1.598-5.593 1.457 3.642A.5.5 0 0 0 12 9h3.5a.5.5 0 0 0 0-1h-3.162l-1.874-4.686Z"/>
                      </svg>
                    </span>
                    <span className="vital-label">Blood Pressure</span>
                    <span className="vital-value">{dashboardData.vitalStats.bloodPressure}</span>
                  </div>
                  <div className="vital-stat">
                    <span className="vital-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-droplet" viewBox="0 0 16 16">
                        <path fillRule="evenodd" d="M7.21.8C7.69.295 8 0 8 0c.109.363.234.708.371 1.038.812 1.946 2.073 3.35 3.197 4.6C12.878 7.096 14 8.345 14 10a6 6 0 0 1-12 0C2 6.668 5.58 2.517 7.21.8zm.413 1.021A31.25 31.25 0 0 0 5.794 3.99c-.726.95-1.436 2.008-1.96 3.07C3.304 8.133 3 9.138 3 10a5 5 0 0 0 10 0c0-1.201-.796-2.157-2.181-3.7l-.03-.032C9.75 5.11 8.5 3.72 7.623 1.82z"/>
                        <path fillRule="evenodd" d="M4.553 7.776c.82-1.641 1.717-2.753 2.093-3.13l.708.708c-.29.29-1.128 1.311-1.907 2.87l-.894-.448z"/>
                      </svg>
                    </span>
                    <span className="vital-label">Hemoglobin</span>
                    <span className="vital-value">{dashboardData.vitalStats.hemoglobin}</span>
                  </div>
                  <div className="vital-stat">
                    <span className="vital-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-calendar-check" viewBox="0 0 16 16">
                        <path d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                        <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                      </svg>
                    </span>
                    <span className="vital-label">Last Checked</span>
                    <span className="vital-value">{formatDate(dashboardData.vitalStats.lastChecked)}</span>
                  </div>
                </div>
                <div className="card-actions">
                  <Link to="/health-records">
                    <Button variant="primary" className="w-100">View Full Health Records</Button>
                  </Link>
                </div>
              </Card.Body>
            </Card>
          </Col>

          {/* Risk Assessment */}
          <Col md={6} className="mb-4">
            <Card className="dashboard-card h-100">
              <Card.Body>
                <Card.Title className="card-title">Risk Assessment</Card.Title>
                <div className="risk-details">
                  <div className="risk-date">Last assessed: {formatDate(dashboardData.riskAssessment.lastAssessment)}</div>
                  <div className="risk-status-grid">
                    <div className="risk-status">
                      <div className="risk-label">Pregnancy Risk</div>
                      <div className={`risk-badge ${dashboardData.riskAssessment.pregnancyRisk.toLowerCase()}`}>
                        {dashboardData.riskAssessment.pregnancyRisk}
                      </div>
                    </div>
                    <div className="risk-status">
                      <div className="risk-label">Anemia Risk</div>
                      <div className={`risk-badge ${dashboardData.riskAssessment.anemiaRisk.toLowerCase()}`}>
                        {dashboardData.riskAssessment.anemiaRisk}
                      </div>
                    </div>
                  </div>
                  <div className="recommendations-preview">
                    <div className="recommendations-header">
                      <span className="recommendations-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-lightbulb" viewBox="0 0 16 16">
                          <path d="M2 6a6 6 0 1 1 10.174 4.31c-.203.196-.359.4-.453.619l-.762 1.769A.5.5 0 0 1 10.5 13a.5.5 0 0 1 0 1 .5.5 0 0 1 0 1l-.224.447a1 1 0 0 1-.894.553H6.618a1 1 0 0 1-.894-.553L5.5 15a.5.5 0 0 1 0-1 .5.5 0 0 1 0-1 .5.5 0 0 1-.46-.302l-.761-1.77a1.964 1.964 0 0 0-.453-.618A5.984 5.984 0 0 1 2 6zm6-5a5 5 0 0 0-3.479 8.592c.263.254.514.564.676.941L5.83 12h4.342l.632-1.467c.162-.377.413-.687.676-.941A5 5 0 0 0 8 1z"/>
                        </svg>
                      </span>
                      <span className="recommendations-title">You have {dashboardData.riskAssessment.recommendations} new recommendations</span>
                    </div>
                  </div>
                  <div className="card-actions">
                    <Link to="/risk-assessment">
                      <Button variant="primary" className="w-100">View Full Assessment</Button>
                    </Link>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Quick Actions */}
        <div className="quick-actions">
          <h3 className="section-title">Quick Actions</h3>
          <Row>
            <Col md={3} sm={6} className="mb-3">
              <Link to="/chatbot" className="quick-action-link">
                <div className="quick-action">
                  <div className="quick-action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-chat-dots" viewBox="0 0 16 16">
                      <path d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
                      <path d="m2.165 15.803.02-.004c1.83-.363 2.948-.842 3.468-1.105A9.06 9.06 0 0 0 8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6a10.437 10.437 0 0 1-.524 2.318l-.003.011a10.722 10.722 0 0 1-.244.637c-.079.186.074.394.273.362a21.673 21.673 0 0 0 .693-.125zm.8-3.108a1 1 0 0 0-.287-.801C1.618 10.83 1 9.468 1 8c0-3.192 3.004-6 7-6s7 2.808 7 6c0 3.193-3.004 6-7 6a8.06 8.06 0 0 1-2.088-.272 1 1 0 0 0-.711.074c-.387.196-1.24.57-2.634.893a10.97 10.97 0 0 0 .398-2z"/>
                    </svg>
                  </div>
                  <div className="quick-action-text">Chat with Assistant</div>
                </div>
              </Link>
            </Col>
            <Col md={3} sm={6} className="mb-3">
              <Link to="/health-records" className="quick-action-link">
                <div className="quick-action">
                  <div className="quick-action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-clipboard2-pulse" viewBox="0 0 16 16">
                      <path d="M9.5 0a.5.5 0 0 1 .5.5.5.5 0 0 0 .5.5.5.5 0 0 1 .5.5V2a.5.5 0 0 1-.5.5h-5A.5.5 0 0 1 5 2v-.5a.5.5 0 0 1 .5-.5.5.5 0 0 0 .5-.5.5.5 0 0 1 .5-.5h3Z"/>
                      <path d="M3 2.5a.5.5 0 0 1 .5-.5H4a.5.5 0 0 0 0-1h-.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1H12a.5.5 0 0 0 0 1h.5a.5.5 0 0 1 .5.5v12a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5v-12Z"/>
                      <path d="M9.979 5.356a.5.5 0 0 0-.968.04L7.92 10.49l-.94-3.135a.5.5 0 0 0-.926-.08L4.69 10H4.5a.5.5 0 0 0 0 1H5a.5.5 0 0 0 .447-.276l.936-1.873 1.138 3.793a.5.5 0 0 0 .968-.04L9.58 7.51l.94 3.135A.5.5 0 0 0 11 11h.5a.5.5 0 0 0 0-1h-.128z"/>
                    </svg>
                  </div>
                  <div className="quick-action-text">Update Health Data</div>
                </div>
              </Link>
            </Col>
            <Col md={3} sm={6} className="mb-3">
              <Link to="/risk-assessment" className="quick-action-link">
                <div className="quick-action">
                  <div className="quick-action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-shield-check" viewBox="0 0 16 16">
                      <path d="M5.338 1.59a61.44 61.44 0 0 0-2.837.856.481.481 0 0 0-.328.39c-.554 4.157.726 7.19 2.253 9.188a10.725 10.725 0 0 0 2.287 2.233c.346.244.652.42.893.533.12.057.218.095.293.118a.55.55 0 0 0 .101.025.615.615 0 0 0 .1-.025c.076-.023.174-.061.294-.118.24-.113.547-.29.893-.533a10.726 10.726 0 0 0 2.287-2.233c1.527-1.997 2.807-5.031 2.253-9.188a.48.48 0 0 0-.328-.39c-.651-.213-1.75-.56-2.837-.855C9.552 1.29 8.531 1.067 8 1.067c-.53 0-1.552.223-2.662.524zM5.072.56C6.157.265 7.31 0 8 0s1.843.265 2.928.56c1.11.3 2.229.655 2.887.87a1.54 1.54 0 0 1 1.044 1.262c.596 4.477-.787 7.795-2.465 9.99a11.775 11.775 0 0 1-2.517 2.453 7.159 7.159 0 0 1-1.048.625c-.28.132-.581.24-.829.24s-.548-.108-.829-.24a7.158 7.158 0 0 1-1.048-.625 11.777 11.777 0 0 1-2.517-2.453C1.928 10.487.545 7.169 1.141 2.692A1.54 1.54 0 0 1 2.185 1.43 62.456 62.456 0 0 1 5.072.56z"/>
                      <path d="M10.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                    </svg>
                  </div>
                  <div className="quick-action-text">New Risk Assessment</div>
                </div>
              </Link>
            </Col>
            <Col md={3} sm={6} className="mb-3">
              <Link to="/profile" className="quick-action-link">
                <div className="quick-action">
                  <div className="quick-action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-person-gear" viewBox="0 0 16 16">
                      <path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm.256 7a4.474 4.474 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10c.26 0 .507.009.74.025.226-.341.496-.65.804-.918C9.077 9.038 8.564 9 8 9c-5 0-6 3-6 4s1 1 1 1h5.256Zm3.63-4.54c.18-.613 1.048-.613 1.229 0l.043.148a.64.64 0 0 0 .921.382l.136-.074c.561-.306 1.175.308.87.869l-.075.136a.64.64 0 0 0 .382.92l.149.045c.612.18.612 1.048 0 1.229l-.15.043a.64.64 0 0 0-.38.921l.074.136c.305.561-.309 1.175-.87.87l-.136-.075a.64.64 0 0 0-.92.382l-.045.149c-.18.612-1.048.612-1.229 0l-.043-.15a.64.64 0 0 0-.921-.38l-.136.074c-.561.305-1.175-.309-.87-.87l.075-.136a.64.64 0 0 0-.382-.92l-.148-.045c-.613-.18-.613-1.048 0-1.229l.148-.043a.64.64 0 0 0 .382-.921l-.074-.136c-.306-.561.308-1.175.869-.87l.136.075a.64.64 0 0 0 .92-.382l.045-.148ZM14 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0Z"/>
                    </svg>
                  </div>
                  <div className="quick-action-text">Edit Profile</div>
                </div>
              </Link>
            </Col>
          </Row>
        </div>
      </Container>
    </div>
  );
};

export default DashboardPage;