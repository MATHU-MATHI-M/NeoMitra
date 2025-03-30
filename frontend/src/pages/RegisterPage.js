import React, { useState } from 'react';
import { Container, Row, Col, Form, Button, Card, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { FaUser, FaEnvelope, FaLock, FaPhone, FaCalendarAlt, FaLanguage, FaUserPlus } from 'react-icons/fa';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    phoneNumber: '',
    dateOfBirth: '',
    preferredLanguage: 'en'
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const { 
    username, 
    email, 
    password, 
    confirmPassword, 
    firstName, 
    lastName, 
    phoneNumber, 
    dateOfBirth, 
    preferredLanguage 
  } = formData;

  const onChange = e => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const onSubmit = async e => {
    e.preventDefault();
    setError(null);
    
    // Basic validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }
    
    try {
      setLoading(true);
      
      // This is a placeholder for the actual registration API call
      // Will be replaced with the real implementation later
      console.log('Registration form submitted:', formData);
      
      // Simulate API call
      setTimeout(() => {
        // Redirect to login after registration
        navigate('/login');
        setLoading(false);
      }, 1500);
      
    } catch (err) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Container>
      <Row className="justify-content-center my-5">
        <Col md={10} lg={8}>
          <Card className="border-0 shadow-sm">
            <Card.Body className="p-4 p-md-5">
              <div className="text-center mb-4">
                <h2 className="fw-bold">Create an Account</h2>
                <p className="text-muted">Join NeoMitra to access maternal healthcare services</p>
              </div>
              
              {error && <Alert variant="danger">{error}</Alert>}
              
              <Form onSubmit={onSubmit}>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="username">
                      <Form.Label>Username</Form.Label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <FaUser />
                        </span>
                        <Form.Control
                          type="text"
                          name="username"
                          placeholder="Choose a username"
                          value={username}
                          onChange={onChange}
                          required
                        />
                      </div>
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="email">
                      <Form.Label>Email Address</Form.Label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <FaEnvelope />
                        </span>
                        <Form.Control
                          type="email"
                          name="email"
                          placeholder="Enter your email"
                          value={email}
                          onChange={onChange}
                          required
                        />
                      </div>
                    </Form.Group>
                  </Col>
                </Row>
                
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="password">
                      <Form.Label>Password</Form.Label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <FaLock />
                        </span>
                        <Form.Control
                          type="password"
                          name="password"
                          placeholder="Create password (min. 8 characters)"
                          value={password}
                          onChange={onChange}
                          required
                        />
                      </div>
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="confirmPassword">
                      <Form.Label>Confirm Password</Form.Label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <FaLock />
                        </span>
                        <Form.Control
                          type="password"
                          name="confirmPassword"
                          placeholder="Confirm your password"
                          value={confirmPassword}
                          onChange={onChange}
                          required
                        />
                      </div>
                    </Form.Group>
                  </Col>
                </Row>
                
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="firstName">
                      <Form.Label>First Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="firstName"
                        placeholder="Enter your first name"
                        value={firstName}
                        onChange={onChange}
                        required
                      />
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="lastName">
                      <Form.Label>Last Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="lastName"
                        placeholder="Enter your last name"
                        value={lastName}
                        onChange={onChange}
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>
                
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="phoneNumber">
                      <Form.Label>Phone Number</Form.Label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <FaPhone />
                        </span>
                        <Form.Control
                          type="tel"
                          name="phoneNumber"
                          placeholder="Enter your phone number"
                          value={phoneNumber}
                          onChange={onChange}
                          required
                        />
                      </div>
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="dateOfBirth">
                      <Form.Label>Date of Birth</Form.Label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <FaCalendarAlt />
                        </span>
                        <Form.Control
                          type="date"
                          name="dateOfBirth"
                          value={dateOfBirth}
                          onChange={onChange}
                          required
                        />
                      </div>
                    </Form.Group>
                  </Col>
                </Row>
                
                <Form.Group className="mb-4" controlId="preferredLanguage">
                  <Form.Label>Preferred Language</Form.Label>
                  <div className="input-group">
                    <span className="input-group-text">
                      <FaLanguage />
                    </span>
                    <Form.Select 
                      name="preferredLanguage" 
                      value={preferredLanguage}
                      onChange={onChange}
                      required
                    >
                      <option value="en">English</option>
                      <option value="hi">Hindi</option>
                      <option value="ta">Tamil</option>
                      <option value="te">Telugu</option>
                      <option value="bn">Bengali</option>
                      <option value="mr">Marathi</option>
                    </Form.Select>
                  </div>
                </Form.Group>
                
                <Form.Group className="mb-4">
                  <Form.Check
                    type="checkbox"
                    id="termsCheckbox"
                    label={
                      <span>
                        I agree to the <Link to="#" className="text-decoration-none">Terms of Service</Link> and <Link to="#" className="text-decoration-none">Privacy Policy</Link>
                      </span>
                    }
                    required
                  />
                </Form.Group>
                
                <Button 
                  variant="primary" 
                  type="submit" 
                  className="w-100 mb-3" 
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Creating your account...
                    </>
                  ) : (
                    <>
                      <FaUserPlus className="me-2" /> Register
                    </>
                  )}
                </Button>
                
                <div className="text-center mt-4">
                  <p className="mb-0">
                    Already have an account? <Link to="/login" className="text-decoration-none">Sign In</Link>
                  </p>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default RegisterPage;