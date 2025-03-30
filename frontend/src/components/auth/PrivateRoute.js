import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

const PrivateRoute = () => {
  const location = useLocation();
  
  // Check if user is authenticated
  // For now we'll use a simple localStorage check
  // This will be enhanced with context API or Redux later
  const isAuthenticated = localStorage.getItem('userToken') !== null;
  
  if (!isAuthenticated) {
    // Redirect to login page if not authenticated
    // Save the current location they were trying to go to
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  // If authenticated, render the child routes
  return <Outlet />;
};

export default PrivateRoute;