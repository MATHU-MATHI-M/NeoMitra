const mongoose = require('mongoose');

const governmentSchemeSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Scheme name is required'],
    trim: true
  },
  description: {
    type: String,
    required: [true, 'Scheme description is required'],
    trim: true
  },
  eligibilityCriteria: {
    type: String,
    required: [true, 'Eligibility criteria is required'],
    trim: true
  },
  benefits: {
    type: String,
    required: [true, 'Benefits information is required'],
    trim: true
  },
  applicationProcess: {
    type: String,
    required: [true, 'Application process information is required'],
    trim: true
  },
  documentsRequired: {
    type: String,
    required: [true, 'Documents required information is needed'],
    trim: true
  },
  schemeUrl: {
    type: String,
    trim: true
  },
  regions: {
    type: [String],
    default: ['All']
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
});

const GovernmentScheme = mongoose.model('GovernmentScheme', governmentSchemeSchema);

module.exports = GovernmentScheme;