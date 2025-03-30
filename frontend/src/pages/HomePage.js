import React, { useEffect } from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  useEffect(() => {
    // Trigger animations when component mounts
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate');
        }
      });
    }, { threshold: 0.1 });

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));

    return () => {
      animatedElements.forEach(el => observer.unobserve(el));
    };
  }, []);

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <Container>
          <Row className="align-items-center">
            <Col lg={6} className="mb-5 mb-lg-0">
              <div className="hero-content">
                <h1 className="hero-title">
                  Empowering <span className="highlight">Maternal Health</span> in Every Village
                </h1>
                <p className="hero-subtitle">
                  NeoMitra provides accessible healthcare information, risk assessment tools, and
                  personalized guidance for expectant mothers in rural areas.
                </p>
                <div className="hero-buttons">
                  <Link to="/register">
                    <Button variant="primary" size="lg" className="me-3">
                      Get Started
                    </Button>
                  </Link>
                  <Link to="/login">
                    <Button variant="outline-light" size="lg">
                      Sign In
                    </Button>
                  </Link>
                </div>
              </div>
            </Col>
            <Col lg={6}>
              <div className="hero-image-container">
                <svg width="100%" height="100%" viewBox="0 0 800 600" fill="none" xmlns="http://www.w3.org/2000/svg" className="hero-image">
                  {/* A simple SVG illustration of a mother and child */}
                  <circle cx="400" cy="300" r="200" fill="#6c5ce7" fillOpacity="0.1" />
                  <path d="M300,250 Q400,150 500,250 T700,250" stroke="#6c5ce7" strokeWidth="3" fill="none" />
                  <circle cx="350" cy="240" r="50" fill="#a29bfe" />
                  <circle cx="450" cy="240" r="70" fill="#6c5ce7" />
                </svg>
              </div>
            </Col>
          </Row>
        </Container>
      </section>
      
      {/* Features Section */}
      <section className="features-section">
        <Container>
          <h2 className="section-title text-center mb-5">Our Key Features</h2>
          <Row>
            <Col md={4} className="mb-4">
              <Card className="feature-card animate-on-scroll">
                <Card.Body className="text-center">
                  <div className="feature-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" className="bi bi-heart-pulse" viewBox="0 0 16 16">
                      <path fillRule="evenodd" d="M8 2.748v-.717A1.5 1.5 0 0 0 9.5 3.5v8.75a.75.75 0 0 1-.094.12l-1.78.178-.178 1.178h-.031a.75.75 0 0 1-1.05 0h-.03l-.18-1.178-1.78-.178A.75.75 0 0 1 4.5 12.25v-8.5a1.5 1.5 0 0 1 1.5-1.5h1.594c.83 0 1.576.498 1.906 1.27l.6 1.405 1.5-.629a1.5 1.5 0 0 1 2.122.82l.818 2.454a.75.75 0 0 0 .662.547l1.6.132a.75.75 0 0 1 0 1.5l-1.599.133a.75.75 0 0 0-.662.547l-.825 2.453a1.5 1.5 0 0 1-2.121.819l-1.5-.63-.599 1.42a2.25 2.25 0 0 1-2.094 1.358H6zm3.99 1.5c-.177 0-.348.03-.5.085V1.5h.75a.75.75 0 0 1 .75.75v1.998ZM4.5 1.5a.5.5 0 0 0-.5.5v2.918l1.5 1.5v-4.5a.5.5 0 0 0-.59-.493c-.142.052-.289.084-.41.094ZM3.493 3.5a.5.5 0 0 1-.319.94l-.21-.17zm-2.29 4.025a.75.75 0 0 0 .543.905l1.68.339a.75.75 0 0 1 .609.6l.438 2.43a.75.75 0 0 0 1.472 0l.44-2.43a.75.75 0 0 1 .608-.6l1.681-.339a.75.75 0 0 0 0-1.45l-1.68-.34a.75.75 0 0 1-.61-.6l-.438-2.429a.75.75 0 0 0-1.472 0L4.415 7.11a.75.75 0 0 1-.608.601l-1.681.338a.75.75 0 0 0-.544.905z"/>
                    </svg>
                  </div>
                  <Card.Title className="feature-title">Risk Assessment</Card.Title>
                  <Card.Text>
                    AI-powered tools to identify high-risk pregnancies and anemia, enabling early intervention and care.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="feature-card animate-on-scroll">
                <Card.Body className="text-center">
                  <div className="feature-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" className="bi bi-translate" viewBox="0 0 16 16">
                      <path d="M4.545 6.714 4.11 8H3l1.862-5h1.284L8 8H6.833l-.435-1.286H4.545zm1.634-.736L5.5 3.956h-.049l-.679 2.022H6.18z"/>
                      <path d="M0 2a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v3h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-3H2a2 2 0 0 1-2-2V2zm2-1a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H2zm7.138 9.995c.193.301.402.583.63.846-.748.575-1.673 1.001-2.768 1.292.178.217.451.635.555.867 1.125-.359 2.08-.844 2.886-1.494.777.665 1.739 1.165 2.93 1.472.133-.254.414-.673.629-.89-1.125-.253-2.057-.694-2.82-1.284.681-.747 1.222-1.651 1.621-2.757H14V8h-3v1.047h.765c-.318.844-.74 1.546-1.272 2.13a6.066 6.066 0 0 1-.415-.492 1.988 1.988 0 0 1-.94.31z"/>
                    </svg>
                  </div>
                  <Card.Title className="feature-title">Multilingual Support</Card.Title>
                  <Card.Text>
                    Access health information in multiple local languages, making maternal care accessible for all.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4">
              <Card className="feature-card animate-on-scroll">
                <Card.Body className="text-center">
                  <div className="feature-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" className="bi bi-chat-dots" viewBox="0 0 16 16">
                      <path d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>
                      <path d="m2.165 15.803.02-.004c1.83-.363 2.948-.842 3.468-1.105A9.06 9.06 0 0 0 8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6a10.437 10.437 0 0 1-.524 2.318l-.003.011a10.722 10.722 0 0 1-.244.637c-.079.186.074.394.273.362a21.673 21.673 0 0 0 .693-.125zm.8-3.108a1 1 0 0 0-.287-.801C1.618 10.83 1 9.468 1 8c0-3.192 3.004-6 7-6s7 2.808 7 6c0 3.193-3.004 6-7 6a8.06 8.06 0 0 1-2.088-.272 1 1 0 0 0-.711.074c-.387.196-1.24.57-2.634.893a10.97 10.97 0 0 0 .398-2z"/>
                    </svg>
                  </div>
                  <Card.Title className="feature-title">Interactive Chatbot</Card.Title>
                  <Card.Text>
                    Get immediate answers to maternal health questions with our voice and text-based assistant.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
      
      {/* Call to Action */}
      <section className="cta-section">
        <Container>
          <div className="cta-container animate-on-scroll">
            <h2 className="cta-title">Ready to take charge of your maternal health journey?</h2>
            <p className="cta-text">Join thousands of women who are experiencing safer pregnancies with NeoMitra's guidance.</p>
            <Link to="/register">
              <Button variant="primary" size="lg" className="cta-button">
                Join NeoMitra Now
              </Button>
            </Link>
          </div>
        </Container>
      </section>
    </div>
  );
};

export default HomePage;