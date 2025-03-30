import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaFacebook, FaTwitter, FaInstagram, FaYoutube, FaPhone, FaEnvelope, FaMapMarkerAlt } from 'react-icons/fa';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-primary text-white py-5 mt-5">
      <Container>
        <Row className="g-4">
          <Col md={4}>
            <h5 className="fw-bold mb-3">NeoMitra</h5>
            <p className="mb-3">
              Empowering mothers with comprehensive maternal healthcare information, 
              anemia risk assessment, and government scheme awareness.
            </p>
            <div className="d-flex gap-3">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="text-white">
                <FaFacebook size={20} />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-white">
                <FaTwitter size={20} />
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="text-white">
                <FaInstagram size={20} />
              </a>
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" className="text-white">
                <FaYoutube size={20} />
              </a>
            </div>
          </Col>
          
          <Col md={4}>
            <h5 className="fw-bold mb-3">Quick Links</h5>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link to="/about" className="text-white text-decoration-none">About Us</Link>
              </li>
              <li className="mb-2">
                <Link to="/services" className="text-white text-decoration-none">Services</Link>
              </li>
              <li className="mb-2">
                <Link to="/health-schemes" className="text-white text-decoration-none">Government Schemes</Link>
              </li>
              <li className="mb-2">
                <Link to="/faq" className="text-white text-decoration-none">FAQs</Link>
              </li>
              <li className="mb-2">
                <Link to="/privacy-policy" className="text-white text-decoration-none">Privacy Policy</Link>
              </li>
              <li className="mb-2">
                <Link to="/terms" className="text-white text-decoration-none">Terms of Service</Link>
              </li>
            </ul>
          </Col>
          
          <Col md={4}>
            <h5 className="fw-bold mb-3">Contact Us</h5>
            <ul className="list-unstyled">
              <li className="mb-3 d-flex align-items-center">
                <FaMapMarkerAlt className="me-2" />
                <span>123 Healthcare Street, Medical District, Bangalore - 560001</span>
              </li>
              <li className="mb-3 d-flex align-items-center">
                <FaPhone className="me-2" />
                <a href="tel:+918001234567" className="text-white text-decoration-none">+91 8001234567</a>
              </li>
              <li className="mb-3 d-flex align-items-center">
                <FaEnvelope className="me-2" />
                <a href="mailto:info@neomitra.org" className="text-white text-decoration-none">info@neomitra.org</a>
              </li>
            </ul>
          </Col>
        </Row>
        
        <hr className="my-4" />
        
        <div className="text-center">
          <p className="mb-0">
            &copy; {currentYear} NeoMitra. All rights reserved.
          </p>
        </div>
      </Container>
    </footer>
  );
};

export default Footer;