const express = require('express');
const path = require('path');
const cors = require('cors');
const mongoose = require('mongoose');
const compression = require('compression');
const helmet = require('helmet');
const morgan = require('morgan');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Create Express app
const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(compression());
app.use(helmet({
  contentSecurityPolicy: false,
  crossOriginEmbedderPolicy: false
}));
app.use(morgan('dev'));

// Connect to MongoDB
// Using a connection string compatible with older MongoDB versions
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/NeoMitra', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  // These options help with compatibility for older MongoDB versions
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
})
  .then(() => {
    console.log('MongoDB Connected');
  })
  .catch((err) => {
    console.error('MongoDB Connection Error:', err);
    console.log('Continuing without database connection. Some features may not work.');
  });

// Define routes
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'success', message: 'API is healthy' });
});

// Serve static assets in production
if (process.env.NODE_ENV === 'production') {
  // Set static folder
  app.use(express.static('frontend/build'));
  
  // Any route that is not an API route will be redirected to index.html
  app.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'frontend', 'build', 'index.html'));
  });
}

// Port setup
const PORT = process.env.PORT || 5001;

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Access the application at http://localhost:${PORT}`);
  console.log(`Access the application at http://localhost:${PORT}`);
  console.log(`Access the application at http://localhost:${PORT}`);
});