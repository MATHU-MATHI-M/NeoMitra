import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Import Bootstrap dark theme
import 'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);