const express = require('express');
const path = require('path');
const cors = require('cors');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the frontend/public directory
app.use(express.static(path.join(__dirname, 'frontend/public')));

// API routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'NeoMitra API is running' });
});

// For any other GET request, send the index.html file
// This enables client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/public', 'index.html'));
});

// Port setup
const PORT = process.env.PORT || 5000;

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`NeoMitra server running on port ${PORT}`);
  console.log(`Visit http://localhost:${PORT} to view the application`);
});

// Export the Express app
module.exports = { app };