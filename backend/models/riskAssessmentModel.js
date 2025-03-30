const mongoose = require('mongoose');

const riskAssessmentSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  assessmentDate: {
    type: Date,
    default: Date.now
  },
  pregnancyRiskScore: {
    type: Number,
    min: 0,
    max: 100
  },
  anemiaRiskScore: {
    type: Number,
    min: 0,
    max: 100
  },
  riskFactors: {
    // Demographic risks
    ageAbove35: { type: Boolean, default: false },
    multiplePregnancy: { type: Boolean, default: false },
    previousCSection: { type: Boolean, default: false },
    previousPretermBirth: { type: Boolean, default: false },
    previousMiscarriage: { type: Boolean, default: false },
    
    // Medical conditions
    diabetes: { type: Boolean, default: false },
    hypertension: { type: Boolean, default: false },
    heartDisease: { type: Boolean, default: false },
    kidneyDisease: { type: Boolean, default: false },
    autoimmuneDisease: { type: Boolean, default: false },
    
    // Pregnancy complications
    gestationalDiabetes: { type: Boolean, default: false },
    preeclampsia: { type: Boolean, default: false },
    placentaPrevia: { type: Boolean, default: false },
    bleeding: { type: Boolean, default: false },
    
    // Lifestyle factors
    smoking: { type: Boolean, default: false },
    alcohol: { type: Boolean, default: false },
    drugUse: { type: Boolean, default: false },
    
    // Anemia risk factors
    fatigue: { type: Boolean, default: false },
    dizzySpells: { type: Boolean, default: false },
    paleSkin: { type: Boolean, default: false },
    shortnessOfBreath: { type: Boolean, default: false },
    poorDiet: { type: Boolean, default: false },
    recentBloodLoss: { type: Boolean, default: false }
  },
  recommendations: {
    type: [String]
  },
  followUpRequired: {
    type: Boolean,
    default: false
  },
  additionalNotes: {
    type: String,
    trim: true
  }
}, {
  timestamps: true
});

const RiskAssessment = mongoose.model('RiskAssessment', riskAssessmentSchema);

module.exports = RiskAssessment;