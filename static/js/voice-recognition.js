/**
 * Voice Recognition Module for NeoMitra
 * Provides speech-to-text functionality for health data logging
 */

class VoiceRecognition {
    constructor(language = 'en-US') {
        this.language = language;
        this.isListening = false;
        this.recognition = null;
        this.initSpeechRecognition();
    }

    initSpeechRecognition() {
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            // Initialize the Web Speech API
            const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognitionAPI();
            
            // Configure recognition
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = this.language;
            
            // Set up callbacks
            this.recognition.onstart = () => {
                this.isListening = true;
                if (this.onStartCallback) this.onStartCallback();
            };
            
            this.recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                
                const confidence = event.results[0][0].confidence;
                
                if (event.results[0].isFinal && this.onResultCallback) {
                    this.onResultCallback(transcript, confidence);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isListening = false;
                if (this.onErrorCallback) this.onErrorCallback(event.error);
            };
            
            this.recognition.onend = () => {
                this.isListening = false;
                if (this.onEndCallback) this.onEndCallback();
            };
        } else {
            console.error('Speech Recognition API not supported in this browser.');
            throw new Error('Speech Recognition not supported');
        }
    }

    start() {
        if (!this.recognition) {
            throw new Error('Speech Recognition not initialized');
        }
        
        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start speech recognition:', error);
        }
    }

    stop() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }

    setLanguage(language) {
        this.language = language;
        if (this.recognition) {
            this.recognition.lang = language;
        }
    }

    onStart(callback) {
        this.onStartCallback = callback;
    }

    onResult(callback) {
        this.onResultCallback = callback;
    }

    onError(callback) {
        this.onErrorCallback = callback;
    }

    onEnd(callback) {
        this.onEndCallback = callback;
    }
}

/**
 * Health Data Extractor
 * Parses voice transcripts to extract health-related information
 */
class HealthDataExtractor {
    constructor() {
        this.patterns = {
            weight: /\b(weight|weigh|weighs)\s+is\s+(\d+(?:\.\d+)?)\s*(kg|kilograms?|pounds?|lbs?)\b/i,
            height: /\b(height|tall)\s+is\s+(\d+(?:\.\d+)?)\s*(cm|centimeters?|meters?|m|feet|foot|ft|inches?|in)\b/i,
            blood_pressure: /\b(blood\s+pressure|bp)\s+is\s+(\d+)\s*(?:over|\/)\s*(\d+)\b/i,
            hemoglobin: /\b(hemoglobin|hb|haemoglobin)\s+is\s+(\d+(?:\.\d+)?)\b/i,
            blood_sugar: /\b(blood\s+sugar|glucose|sugar\s+level)\s+is\s+(\d+(?:\.\d+)?)\b/i,
            pregnancy: /\b(i\s*am|i'm)\s+(pregnant)\b/i,
            pregnancy_week: /\b(pregnant|pregnancy).+?(\d+)\s*(weeks?|wks?)\b/i
        };
    }

    extract(transcript) {
        const extractedData = {};
        
        // Extract weight
        const weightMatch = transcript.match(this.patterns.weight);
        if (weightMatch) {
            let weight = parseFloat(weightMatch[2]);
            const unit = weightMatch[3].toLowerCase();
            
            // Convert to kg if needed
            if (unit.startsWith('lb') || unit.startsWith('pound')) {
                weight = weight * 0.453592; // Convert lbs to kg
            }
            
            extractedData.weight = weight;
        }
        
        // Extract height
        const heightMatch = transcript.match(this.patterns.height);
        if (heightMatch) {
            let height = parseFloat(heightMatch[2]);
            const unit = heightMatch[3].toLowerCase();
            
            // Convert to cm if needed
            if (unit === 'm' || unit.startsWith('meter')) {
                height = height * 100; // Convert meters to cm
            } else if (unit === 'ft' || unit.startsWith('foot') || unit.startsWith('feet')) {
                height = height * 30.48; // Convert feet to cm
            } else if (unit === 'in' || unit.startsWith('inch')) {
                height = height * 2.54; // Convert inches to cm
            }
            
            extractedData.height = height;
        }
        
        // Extract blood pressure
        const bpMatch = transcript.match(this.patterns.blood_pressure);
        if (bpMatch) {
            extractedData.blood_pressure_systolic = parseInt(bpMatch[2]);
            extractedData.blood_pressure_diastolic = parseInt(bpMatch[3]);
        }
        
        // Extract hemoglobin
        const hbMatch = transcript.match(this.patterns.hemoglobin);
        if (hbMatch) {
            extractedData.hemoglobin = parseFloat(hbMatch[2]);
        }
        
        // Extract blood sugar
        const bsMatch = transcript.match(this.patterns.blood_sugar);
        if (bsMatch) {
            extractedData.blood_sugar = parseFloat(bsMatch[2]);
        }
        
        // Extract pregnancy status
        const pregnancyMatch = transcript.match(this.patterns.pregnancy);
        if (pregnancyMatch) {
            extractedData.is_pregnant = true;
        }
        
        // Extract pregnancy week
        const pregnancyWeekMatch = transcript.match(this.patterns.pregnancy_week);
        if (pregnancyWeekMatch) {
            extractedData.pregnancy_week = parseInt(pregnancyWeekMatch[2]);
        }
        
        return extractedData;
    }
}