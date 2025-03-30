/**
 * Voice Recognition Module for NeoMitra
 * Enables voice-assisted health logging with natural language processing
 */

class VoiceRecognition {
    constructor(language = 'en-US') {
        this.recognition = null;
        this.isListening = false;
        this.language = language;
        this.transcript = '';
        this.confidence = 0;
        this.onResultCallback = null;
        this.onStartCallback = null;
        this.onEndCallback = null;
        this.onErrorCallback = null;
        
        this.initRecognition();
    }
    
    initRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = this.language;
            
            this.recognition.onstart = () => {
                this.isListening = true;
                if (this.onStartCallback) this.onStartCallback();
            };
            
            this.recognition.onresult = (event) => {
                const last = event.results.length - 1;
                this.transcript = event.results[last][0].transcript;
                this.confidence = event.results[last][0].confidence;
                
                if (event.results[last].isFinal && this.onResultCallback) {
                    this.onResultCallback(this.transcript, this.confidence);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                if (this.onErrorCallback) this.onErrorCallback(event.error);
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                if (this.onEndCallback) this.onEndCallback();
            };
        } else {
            console.error('Speech recognition not supported in this browser');
        }
    }
    
    setLanguage(language) {
        this.language = language;
        if (this.recognition) {
            this.recognition.lang = language;
        }
    }
    
    start() {
        if (this.recognition) {
            this.recognition.start();
        } else {
            console.error('Speech recognition not initialized');
        }
    }
    
    stop() {
        if (this.recognition) {
            this.recognition.stop();
        }
    }
    
    onResult(callback) {
        this.onResultCallback = callback;
    }
    
    onStart(callback) {
        this.onStartCallback = callback;
    }
    
    onEnd(callback) {
        this.onEndCallback = callback;
    }
    
    onError(callback) {
        this.onErrorCallback = callback;
    }
}

/**
 * Health Data Extractor
 * Processes natural language input to extract health-related data
 */
class HealthDataExtractor {
    constructor() {
        // Keywords for different health metrics
        this.weightKeywords = ['weight', 'kilogram', 'kg', 'pounds', 'lbs'];
        this.heightKeywords = ['height', 'centimeter', 'cm', 'feet', 'foot', 'inches', 'inch'];
        this.bloodPressureKeywords = ['blood pressure', 'bp', 'systolic', 'diastolic', 'mmhg'];
        this.bloodSugarKeywords = ['blood sugar', 'glucose', 'mg/dl', 'mmol'];
        this.hemoglobinKeywords = ['hemoglobin', 'hb', 'g/dl'];
        
        // Keywords for pregnancy status
        this.pregnancyKeywords = ['pregnant', 'pregnancy', 'expecting', 'trimester', 'weeks pregnant'];
        
        // Keywords for symptoms
        this.symptomKeywords = [
            'fever', 'headache', 'nausea', 'vomiting', 'dizziness', 'fatigue',
            'pain', 'cramp', 'swelling', 'bleeding', 'cough', 'sore throat',
            'rash', 'shortness of breath', 'chest pain', 'abdominal pain'
        ];
    }
    
    extractData(text) {
        const lowercaseText = text.toLowerCase();
        const data = {
            weight: this.extractWeight(lowercaseText),
            height: this.extractHeight(lowercaseText),
            bloodPressure: this.extractBloodPressure(lowercaseText),
            bloodSugar: this.extractBloodSugar(lowercaseText),
            hemoglobin: this.extractHemoglobin(lowercaseText),
            isPregnant: this.checkPregnancyStatus(lowercaseText),
            pregnancyWeek: this.extractPregnancyWeek(lowercaseText),
            symptoms: this.extractSymptoms(lowercaseText)
        };
        
        return data;
    }
    
    extractWeight(text) {
        // Look for weight values with units
        const weightRegex = /(\d+\.?\d*)\s*(kg|kilogram|pounds|lbs)/i;
        const match = text.match(weightRegex);
        
        if (match) {
            const value = parseFloat(match[1]);
            const unit = match[2].toLowerCase();
            
            // Convert to kg if in pounds
            if (unit === 'pounds' || unit === 'lbs') {
                return (value * 0.453592).toFixed(2);
            }
            
            return value.toFixed(2);
        }
        
        return null;
    }
    
    extractHeight(text) {
        // Look for height in cm
        const cmRegex = /(\d+\.?\d*)\s*(cm|centimeter)/i;
        const cmMatch = text.match(cmRegex);
        
        if (cmMatch) {
            return parseFloat(cmMatch[1]).toFixed(2);
        }
        
        // Look for height in feet and inches
        const feetInchesRegex = /(\d+\.?\d*)\s*feet\s*(?:and)?\s*(\d+\.?\d*)\s*inch/i;
        const feetInchesMatch = text.match(feetInchesRegex);
        
        if (feetInchesMatch) {
            const feet = parseFloat(feetInchesMatch[1]);
            const inches = parseFloat(feetInchesMatch[2]);
            const totalCm = (feet * 30.48) + (inches * 2.54);
            return totalCm.toFixed(2);
        }
        
        return null;
    }
    
    extractBloodPressure(text) {
        // Look for blood pressure as systolic/diastolic
        const bpRegex = /(\d+)[\/\s-]+(\d+)\s*(?:mmhg|blood pressure|bp)/i;
        const match = text.match(bpRegex);
        
        if (match) {
            return {
                systolic: parseInt(match[1]),
                diastolic: parseInt(match[2])
            };
        }
        
        return null;
    }
    
    extractBloodSugar(text) {
        // Look for blood sugar values with units
        const bsRegex = /(\d+\.?\d*)\s*(?:mg\/dl|mmol|blood sugar|glucose)/i;
        const match = text.match(bsRegex);
        
        if (match) {
            return parseFloat(match[1]).toFixed(2);
        }
        
        return null;
    }
    
    extractHemoglobin(text) {
        // Look for hemoglobin values with units
        const hbRegex = /(\d+\.?\d*)\s*(?:g\/dl|hemoglobin|hb)/i;
        const match = text.match(hbRegex);
        
        if (match) {
            return parseFloat(match[1]).toFixed(2);
        }
        
        return null;
    }
    
    checkPregnancyStatus(text) {
        for (const keyword of this.pregnancyKeywords) {
            if (text.includes(keyword)) {
                return true;
            }
        }
        
        return false;
    }
    
    extractPregnancyWeek(text) {
        // Look for pregnancy week
        const weekRegex = /(\d+)\s*(?:weeks?|wks?)\s*(?:pregnant|pregnancy|gestation)/i;
        const match = text.match(weekRegex);
        
        if (match) {
            return parseInt(match[1]);
        }
        
        return null;
    }
    
    extractSymptoms(text) {
        const foundSymptoms = [];
        
        for (const symptom of this.symptomKeywords) {
            if (text.includes(symptom)) {
                foundSymptoms.push(symptom);
            }
        }
        
        return foundSymptoms.length > 0 ? foundSymptoms : null;
    }
}

// Make classes available globally
window.VoiceRecognition = VoiceRecognition;
window.HealthDataExtractor = HealthDataExtractor;