import React, { useState, useEffect } from 'react';
import { Navbar, Nav, Container, Button, NavDropdown } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { FaUser, FaSignOutAlt, FaHeartbeat, FaChartLine, FaFileAlt, FaComments } from 'react-icons/fa';

const Header = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();
  
  useEffect(() => {
    // Check if user is logged in
    const userToken = localStorage.getItem('userToken');
    setIsAuthenticated(!!userToken);
  }, []);
  
  const handleLogout = () => {
    // Clear user data from local storage
    localStorage.removeItem('userToken');
    localStorage.removeItem('userData');
    
    // Update authentication state
    setIsAuthenticated(false);
    
    // Redirect to login page
    navigate('/login');
  };
  
  return (
    <Navbar bg="primary" variant="dark" expand="lg" className="py-3 shadow-sm" sticky="top">
      <Container>
        <Navbar.Brand as={Link} to="/" className="d-flex align-items-center">
          <img 
            src="/logo.svg" 
            alt="NeoMitra Logo" 
            width="30" 
            height="30" 
            className="me-2" 
          />
          <span className="fw-bold">NeoMitra</span>
        </Navbar.Brand>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/" className="mx-2">Home</Nav.Link>
            
            {isAuthenticated ? (
              <>
                <Nav.Link as={Link} to="/health-records" className="mx-2">
                  <FaHeartbeat className="me-1" /> Health Records
                </Nav.Link>
                
                <Nav.Link as={Link} to="/risk-assessment" className="mx-2">
                  <FaChartLine className="me-1" /> Risk Assessment
                </Nav.Link>
                
                <Nav.Link as={Link} to="/health-schemes" className="mx-2">
                  <FaFileAlt className="me-1" /> Govt Schemes
                </Nav.Link>
                
                <Nav.Link as={Link} to="/chatbot" className="mx-2">
                  <FaComments className="me-1" /> Chatbot
                </Nav.Link>
                
                <NavDropdown 
                  title={
                    <span>
                      <FaUser className="me-1" /> Profile
                    </span>
                  } 
                  id="basic-nav-dropdown" 
                  align="end"
                  className="mx-2"
                >
                  <NavDropdown.Item as={Link} to="/profile">My Profile</NavDropdown.Item>
                  <NavDropdown.Item as={Link} to="/settings">Settings</NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item onClick={handleLogout}>
                    <FaSignOutAlt className="me-2" /> Logout
                  </NavDropdown.Item>
                </NavDropdown>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/about" className="mx-2">About</Nav.Link>
                <Nav.Link as={Link} to="/contact" className="mx-2">Contact</Nav.Link>
                <Button 
                  as={Link} 
                  to="/login" 
                  variant="outline-light" 
                  className="ms-3 me-2"
                >
                  Login
                </Button>
                <Button 
                  as={Link} 
                  to="/register" 
                  variant="light" 
                  className="text-primary"
                >
                  Register
                </Button>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;