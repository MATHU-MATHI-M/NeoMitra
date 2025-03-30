import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './RegisterPage.css';

const RegisterPage = ({ login }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    phone: '',
    dob: '',
    language: 'en'
  });
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
  
  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }
    
    // Check that all required fields are filled
    const requiredFields = ['username', 'email', 'password', 'firstName', 'lastName', 'phone', 'dob'];
    for (const field of requiredFields) {
      if (!formData[field]) {
        setError(`Please fill in all required fields (${field} is missing)`);
        return false;
      }
    }
    
    return true;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!validateForm()) {
      return;
    }
    
    try {
      setLoading(true);
      
      // For demonstration purposes - in a real app, this would be an API call
      // Mock registration functionality for now
      setTimeout(() => {
        // Simulate successful registration
        const userData = {
          id: 1,
          username: formData.username,
          email: formData.email,
          firstName: formData.firstName,
          lastName: formData.lastName,
          token: 'mock-jwt-token',
        };
        
        login(userData);
        setLoading(false);
        navigate('/dashboard');
      }, 1500);
      
      // In a real implementation, this would be:
      /*
      const response = await axios.post('/api/auth/register', {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
        phone_number: formData.phone,
        date_of_birth: formData.dob,
        preferred_language: formData.language
      });
      
      login(response.data);
      navigate('/dashboard');
      */
      
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
    }
  };
  
  return (
    <div className="register-page">
      <Container>
        <Row className="justify-content-center">
          <Col md={10} lg={8}>
            <div className="text-center mb-4">
              <h2 className="auth-title">Create Your Account</h2>
              <p className="auth-subtitle">Join NeoMitra and start your maternal health journey</p>
            </div>
            
            <Card className="auth-card">
              <Card.Body className="p-4">
                {error && (
                  <Alert variant="danger" className="mb-4">
                    {error}
                  </Alert>
                )}
                
                <Form onSubmit={handleSubmit}>
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Username</Form.Label>
                        <Form.Control
                          type="text"
                          placeholder="Choose a username"
                          name="username"
                          value={formData.username}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                    
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control
                          type="email"
                          placeholder="Enter your email"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                          type="password"
                          placeholder="Create a password"
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          required
                        />
                        <Form.Text className="text-muted">
                          Password must be at least 8 characters long
                        </Form.Text>
                      </Form.Group>
                    </Col>
                    
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control
                          type="password"
                          placeholder="Confirm your password"
                          name="confirmPassword"
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>First Name</Form.Label>
                        <Form.Control
                          type="text"
                          placeholder="Enter your first name"
                          name="firstName"
                          value={formData.firstName}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                    
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control
                          type="text"
                          placeholder="Enter your last name"
                          name="lastName"
                          value={formData.lastName}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Row>
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Phone Number</Form.Label>
                        <Form.Control
                          type="tel"
                          placeholder="Enter your phone number"
                          name="phone"
                          value={formData.phone}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                    
                    <Col md={6}>
                      <Form.Group className="mb-3">
                        <Form.Label>Date of Birth</Form.Label>
                        <Form.Control
                          type="date"
                          name="dob"
                          value={formData.dob}
                          onChange={handleChange}
                          required
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  
                  <Form.Group className="mb-4">
                    <Form.Label>Preferred Language</Form.Label>
                    <Form.Select
                      name="language"
                      value={formData.language}
                      onChange={handleChange}
                    >
                      <option value="en">English</option>
                      <option value="hi">Hindi</option>
                      <option value="ta">Tamil</option>
                      <option value="te">Telugu</option>
                      <option value="bn">Bengali</option>
                      <option value="mr">Marathi</option>
                    </Form.Select>
                  </Form.Group>
                  
                  <Form.Group className="mb-4">
                    <Form.Check
                      type="checkbox"
                      label="I agree to the Terms of Service and Privacy Policy"
                      required
                    />
                  </Form.Group>
                  
                  <Button
                    variant="primary"
                    type="submit"
                    className="w-100 register-btn"
                    disabled={loading}
                  >
                    {loading ? 'Creating Account...' : 'Create Account'}
                  </Button>
                </Form>
              </Card.Body>
            </Card>
            
            <div className="text-center mt-4">
              <p className="auth-redirect">
                Already have an account?{' '}
                <Link to="/login" className="auth-link">
                  Log in
                </Link>
              </p>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default RegisterPage;