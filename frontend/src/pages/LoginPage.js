import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginPage.css';

const LoginPage = ({ login, user }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  
  useEffect(() => {
    // If user is already logged in, redirect to dashboard
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!email || !password) {
      setError('Please provide both email and password');
      return;
    }
    
    try {
      setLoading(true);
      
      // For demonstration purposes - in a real app, this would be an API call
      // Mock login functionality for now
      setTimeout(() => {
        // Simulate successful login
        const userData = {
          id: 1,
          username: 'testuser',
          email: email,
          firstName: 'Test',
          lastName: 'User',
          token: 'mock-jwt-token',
        };
        
        login(userData);
        setLoading(false);
        navigate('/dashboard');
      }, 1500);
      
      // In a real implementation, this would be:
      /*
      const response = await axios.post('/api/auth/login', {
        email,
        password,
        rememberMe
      });
      
      login(response.data);
      navigate('/dashboard');
      */
      
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.message || 'Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="login-page">
      <Container>
        <Row className="justify-content-center">
          <Col md={8} lg={6} xl={5}>
            <div className="text-center mb-4">
              <h2 className="auth-title">Welcome Back</h2>
              <p className="auth-subtitle">Log in to access your personalized healthcare journey</p>
            </div>
            
            <Card className="auth-card">
              <Card.Body className="p-4">
                {error && (
                  <Alert variant="danger" className="mb-4">
                    {error}
                  </Alert>
                )}
                
                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label>Email Address</Form.Label>
                    <Form.Control
                      type="email"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </Form.Group>
                  
                  <Form.Group className="mb-4">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                      type="password"
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </Form.Group>
                  
                  <Form.Group className="mb-4 d-flex justify-content-between align-items-center">
                    <Form.Check
                      type="checkbox"
                      label="Remember me"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                    />
                    <Link to="/forgot-password" className="forgot-password">
                      Forgot Password?
                    </Link>
                  </Form.Group>
                  
                  <Button
                    variant="primary"
                    type="submit"
                    className="w-100 login-btn"
                    disabled={loading}
                  >
                    {loading ? 'Logging in...' : 'Log In'}
                  </Button>
                </Form>
              </Card.Body>
            </Card>
            
            <div className="text-center mt-4">
              <p className="auth-redirect">
                Don't have an account?{' '}
                <Link to="/register" className="auth-link">
                  Sign up now
                </Link>
              </p>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default LoginPage;