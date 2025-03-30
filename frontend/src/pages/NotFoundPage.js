import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <Container className="py-5 text-center fade-in">
      <Row className="justify-content-center">
        <Col md={8}>
          <svg width="150" height="150" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="mb-4 text-muted">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h1 className="display-4 mb-4">Page Not Found</h1>
          <p className="lead mb-5">
            We couldn't find the page you were looking for. 
            It might have been removed, renamed, or did not exist in the first place.
          </p>
          <Button as={Link} to="/" size="lg">
            Return to Home
          </Button>
        </Col>
      </Row>
    </Container>
  );
};

export default NotFoundPage;