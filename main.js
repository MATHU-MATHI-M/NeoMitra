const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();

// Initialize body parser
app.use(express.json());

// Serve static assets (if in production)
app.use(express.static(path.join(__dirname, 'frontend/public')));

// Root route - Serve React app
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/public', 'index.html'));
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'NeoMitra API is running' });
});

// Port setup
const PORT = process.env.PORT || 5000;

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

// Export the Express app
module.exports = { app };