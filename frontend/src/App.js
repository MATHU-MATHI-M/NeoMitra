import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';

// Layout components
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';

// Page components
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import NotFoundPage from './pages/NotFoundPage';

// Auth components
import PrivateRoute from './components/auth/PrivateRoute';

// Styles
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App = () => {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100">
        <Header />
        <main className="flex-grow-1">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            {/* Protected Routes */}
            <Route element={<PrivateRoute />}>
              <Route path="/dashboard" element={<div>Dashboard</div>} />
              <Route path="/health-records" element={<div>Health Records</div>} />
              <Route path="/risk-assessment" element={<div>Risk Assessment</div>} />
              <Route path="/health-schemes" element={<div>Government Schemes</div>} />
              <Route path="/chatbot" element={<div>Chatbot</div>} />
              <Route path="/profile" element={<div>Profile</div>} />
              <Route path="/settings" element={<div>Settings</div>} />
            </Route>
            
            {/* 404 Route */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;