import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Navbar, Container, Nav, Button } from 'react-bootstrap';
import './Header.css';

const Header = ({ user, logout }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <Navbar expand="lg" variant="dark" className="main-navbar" fixed="top">
      <Container>
        <Navbar.Brand as={Link} to="/" className="brand">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="brand-icon">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="#6c5ce7" stroke="#a29bfe" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span className="ms-2">NeoMitra</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/" className="nav-link">Home</Nav.Link>
            
            {user ? (
              <>
                <Nav.Link as={Link} to="/dashboard" className="nav-link">Dashboard</Nav.Link>
                <Nav.Link as={Link} to="/health-records" className="nav-link">Health Records</Nav.Link>
                <Nav.Link as={Link} to="/risk-assessment" className="nav-link">Risk Assessment</Nav.Link>
                <Nav.Link as={Link} to="/chatbot" className="nav-link">Chatbot</Nav.Link>
                <Button 
                  variant="outline-light" 
                  className="ms-3 logout-btn"
                  onClick={handleLogout}
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/login" className="nav-link">Login</Nav.Link>
                <Nav.Link as={Link} to="/register" className="nav-link register-link">Register</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;