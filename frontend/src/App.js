import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ChatbotPage from './pages/ChatbotPage';
import HealthRecordsPage from './pages/HealthRecordsPage';
import RiskAssessmentPage from './pages/RiskAssessmentPage';
import PrivateRoute from './components/auth/PrivateRoute';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app-container">
      <Header user={user} logout={logout} />
      <main className="content-container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage login={login} user={user} />} />
          <Route path="/register" element={<RegisterPage login={login} />} />
          <Route path="/dashboard" element={
            <PrivateRoute user={user}>
              <DashboardPage user={user} />
            </PrivateRoute>
          } />
          <Route path="/chatbot" element={
            <PrivateRoute user={user}>
              <ChatbotPage user={user} />
            </PrivateRoute>
          } />
          <Route path="/health-records" element={
            <PrivateRoute user={user}>
              <HealthRecordsPage user={user} />
            </PrivateRoute>
          } />
          <Route path="/risk-assessment" element={
            <PrivateRoute user={user}>
              <RiskAssessmentPage user={user} />
            </PrivateRoute>
          } />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;