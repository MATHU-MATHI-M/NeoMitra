const mongoose = require('mongoose');

const healthRecordSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  recordDate: {
    type: Date,
    default: Date.now
  },
  isPregnant: {
    type: Boolean,
    default: false
  },
  pregnancyWeek: {
    type: Number,
    min: 1,
    max: 44
  },
  dueDate: {
    type: Date
  },
  weight: {
    type: Number, // in kg
    min: 20,
    max: 200
  },
  height: {
    type: Number, // in cm
    min: 100,
    max: 250
  },
  bloodPressureSystolic: {
    type: Number,
    min: 70,
    max: 220
  },
  bloodPressureDiastolic: {
    type: Number,
    min: 40,
    max: 120
  },
  bloodSugar: {
    type: Number, // mg/dL
    min: 30,
    max: 500
  },
  hemoglobin: {
    type: Number, // g/dL
    min: 5,
    max: 20
  },
  previousPregnancies: {
    type: Number,
    default: 0,
    min: 0
  },
  previousComplications: {
    type: String,
    trim: true
  },
  existingConditions: {
    type: String,
    trim: true
  },
  currentMedications: {
    type: String,
    trim: true
  }
}, {
  timestamps: true
});

const HealthRecord = mongoose.model('HealthRecord', healthRecordSchema);

module.exports = HealthRecord;