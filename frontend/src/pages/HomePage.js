import React from 'react';
import { Container, Row, Col, Card, Button, Carousel } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaHeartbeat, FaChartLine, FaFileAlt, FaInfoCircle, FaComments } from 'react-icons/fa';

const HomePage = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero bg-primary text-white py-5">
        <Container>
          <Row className="align-items-center">
            <Col lg={6} className="mb-4 mb-lg-0">
              <h1 className="display-4 fw-bold mb-3">Empowering Maternal Healthcare</h1>
              <p className="lead mb-4">
                NeoMitra provides comprehensive maternal health resources, pregnancy risk assessment, 
                and awareness about government healthcare schemes.
              </p>
              <div className="d-flex gap-3">
                <Button as={Link} to="/register" variant="light" size="lg" className="text-primary fw-bold">
                  Get Started
                </Button>
                <Button as={Link} to="/about" variant="outline-light" size="lg">
                  Learn More
                </Button>
              </div>
            </Col>
            <Col lg={6}>
              <img 
                src="/images/hero-image.svg" 
                alt="Maternal healthcare illustration" 
                className="img-fluid" 
              />
            </Col>
          </Row>
        </Container>
      </section>

      {/* Features Section */}
      <section className="features py-5">
        <Container>
          <div className="text-center mb-5">
            <h2 className="display-5 fw-bold">How NeoMitra Helps You</h2>
            <p className="lead">Comprehensive tools for maternal healthcare and awareness</p>
          </div>
          
          <Row className="g-4">
            <Col md={4}>
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="text-center p-4">
                  <div className="feature-icon bg-primary text-white rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center" style={{ width: '80px', height: '80px' }}>
                    <FaHeartbeat size={30} />
                  </div>
                  <Card.Title className="fw-bold">Health Tracking</Card.Title>
                  <Card.Text>
                    Easily record and monitor your health parameters throughout pregnancy.
                  </Card.Text>
                  <Link to="/health-records" className="btn btn-outline-primary mt-3">
                    Track Health
                  </Link>
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={4}>
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="text-center p-4">
                  <div className="feature-icon bg-primary text-white rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center" style={{ width: '80px', height: '80px' }}>
                    <FaChartLine size={30} />
                  </div>
                  <Card.Title className="fw-bold">Risk Assessment</Card.Title>
                  <Card.Text>
                    AI-powered assessment of pregnancy risks and anemia detection.
                  </Card.Text>
                  <Link to="/risk-assessment" className="btn btn-outline-primary mt-3">
                    Check Risks
                  </Link>
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={4}>
              <Card className="h-100 border-0 shadow-sm">
                <Card.Body className="text-center p-4">
                  <div className="feature-icon bg-primary text-white rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center" style={{ width: '80px', height: '80px' }}>
                    <FaFileAlt size={30} />
                  </div>
                  <Card.Title className="fw-bold">Government Schemes</Card.Title>
                  <Card.Text>
                    Information about government healthcare schemes for mothers.
                  </Card.Text>
                  <Link to="/health-schemes" className="btn btn-outline-primary mt-3">
                    Explore Schemes
                  </Link>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials py-5 bg-light">
        <Container>
          <div className="text-center mb-5">
            <h2 className="display-5 fw-bold">What Mothers Say</h2>
            <p className="lead">Hear from mothers who have benefited from NeoMitra</p>
          </div>
          
          <Carousel className="testimonial-carousel" indicators={true} controls={true}>
            <Carousel.Item>
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4 p-md-5">
                  <div className="d-flex flex-column align-items-center">
                    <div className="testimonial-image rounded-circle overflow-hidden mb-3" style={{ width: '100px', height: '100px' }}>
                      <img 
                        src="/images/testimonial-1.jpg" 
                        alt="Testimonial" 
                        className="img-fluid" 
                      />
                    </div>
                    <p className="text-center mb-3">
                      "NeoMitra helped me understand my pregnancy risks and guided me through proper nutrition. The anemia prevention tips were invaluable during my pregnancy journey."
                    </p>
                    <div className="text-center">
                      <h5 className="mb-1">Priya Sharma</h5>
                      <p className="text-muted mb-0">Mother of two, Delhi</p>
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Carousel.Item>
            
            <Carousel.Item>
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4 p-md-5">
                  <div className="d-flex flex-column align-items-center">
                    <div className="testimonial-image rounded-circle overflow-hidden mb-3" style={{ width: '100px', height: '100px' }}>
                      <img 
                        src="/images/testimonial-2.jpg" 
                        alt="Testimonial" 
                        className="img-fluid" 
                      />
                    </div>
                    <p className="text-center mb-3">
                      "The chatbot assistant answered all my questions about pregnancy complications. I also discovered government schemes that I was eligible for, which helped me financially."
                    </p>
                    <div className="text-center">
                      <h5 className="mb-1">Lakshmi Devi</h5>
                      <p className="text-muted mb-0">Expectant mother, Chennai</p>
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Carousel.Item>
            
            <Carousel.Item>
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4 p-md-5">
                  <div className="d-flex flex-column align-items-center">
                    <div className="testimonial-image rounded-circle overflow-hidden mb-3" style={{ width: '100px', height: '100px' }}>
                      <img 
                        src="/images/testimonial-3.jpg" 
                        alt="Testimonial" 
                        className="img-fluid" 
                      />
                    </div>
                    <p className="text-center mb-3">
                      "Being able to access healthcare information in my native language made a huge difference. The risk assessment alerted me to potential anemia risks which my doctor confirmed later."
                    </p>
                    <div className="text-center">
                      <h5 className="mb-1">Fatima Khan</h5>
                      <p className="text-muted mb-0">Mother of one, Mumbai</p>
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Carousel.Item>
          </Carousel>
        </Container>
      </section>

      {/* CTA Section */}
      <section className="cta py-5 bg-primary text-white">
        <Container className="text-center">
          <h2 className="display-5 fw-bold mb-4">Ready to Take Care of Your Health?</h2>
          <p className="lead mb-4">
            Join NeoMitra today and access comprehensive maternal healthcare tools and resources.
          </p>
          <Button as={Link} to="/register" variant="light" size="lg" className="text-primary fw-bold px-5">
            Register Now
          </Button>
        </Container>
      </section>
    </div>
  );
};

export default HomePage;