/**
 * Voice Recognition Module for NeoMitra Healthcare Platform
 * This module enables voice-based health data logging with natural language processing
 */

class VoiceRecognition {
    constructor(processingEndpoint = '/process_voice_recording') {
        this.recognition = null;
        this.isListening = false;
        this.transcripts = [];
        this.processingEndpoint = processingEndpoint;
        this.setupRecognition();
        this.speechSynthesis = window.speechSynthesis;
    }

    setupRecognition() {
        // Check if browser supports speech recognition
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('Speech recognition not supported in this browser');
            return;
        }

        // Initialize SpeechRecognition object
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = document.documentElement.lang || 'en-US';

        // Set up event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI(true);
            console.log('Voice recognition started');
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateUI(false);
            console.log('Voice recognition ended');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                    this.transcripts.push(transcript.trim());
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update UI with transcripts
            this.updateTranscriptUI(finalTranscript, interimTranscript);

            // If we have a final transcript, process it
            if (finalTranscript) {
                this.processTranscript(finalTranscript);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            this.isListening = false;
            this.updateUI(false);
            
            // Attempt to restart if there was a temporary error
            if (event.error === 'network' || event.error === 'service-not-allowed') {
                setTimeout(() => this.start(), 1000);
            }
        };
    }

    start() {
        if (!this.recognition) {
            this.setupRecognition();
            if (!this.recognition) return; // Still not available
        }

        try {
            this.recognition.start();
            this.speak("I'm listening. You can tell me about your health data now.");
        } catch (e) {
            console.error('Error starting speech recognition:', e);
            // If already started, stop and start again
            if (e.name === 'InvalidStateError') {
                this.recognition.stop();
                setTimeout(() => this.start(), 200);
            }
        }
    }

    stop() {
        if (this.recognition) {
            try {
                this.recognition.stop();
                this.speak("Voice input stopped.");
            } catch (e) {
                console.error('Error stopping speech recognition:', e);
            }
        }
    }

    updateUI(isListening) {
        // Find UI elements
        const startButton = document.getElementById('startVoiceButton');
        const stopButton = document.getElementById('stopVoiceButton');
        const statusIndicator = document.getElementById('voiceStatusIndicator');
        
        if (startButton && stopButton) {
            startButton.disabled = isListening;
            stopButton.disabled = !isListening;
        }
        
        if (statusIndicator) {
            statusIndicator.className = isListening 
                ? 'status-indicator active' 
                : 'status-indicator';
            statusIndicator.textContent = isListening 
                ? 'Listening...' 
                : 'Not listening';
        }
    }

    updateTranscriptUI(finalTranscript, interimTranscript) {
        const transcriptElement = document.getElementById('voiceTranscript');
        const interimElement = document.getElementById('interimTranscript');
        
        if (transcriptElement && finalTranscript) {
            const p = document.createElement('p');
            p.textContent = finalTranscript;
            transcriptElement.appendChild(p);
            transcriptElement.scrollTop = transcriptElement.scrollHeight;
        }
        
        if (interimElement) {
            interimElement.textContent = interimTranscript;
        }
    }

    processTranscript(transcript) {
        // Send the transcript to the server for NLP processing
        fetch(this.processingEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ transcript }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Processed data:', data);
            this.handleProcessedData(data);
        })
        .catch(error => {
            console.error('Error processing transcript:', error);
        });
    }

    handleProcessedData(data) {
        // Handle the processed data
        if (data.success) {
            // Update UI with extracted health data
            this.updateExtractedDataUI(data.extractedData);
            
            // Provide voice feedback
            if (data.response) {
                this.speak(data.response);
            }
            
            // If data was successfully saved
            if (data.dataSaved) {
                this.showSuccessMessage(data.message || "Health data successfully saved!");
            }
        } else {
            // Handle error
            this.showErrorMessage(data.message || "Could not process your health data.");
            this.speak("I'm sorry, I couldn't understand your health data. Can you please try again?");
        }
    }

    updateExtractedDataUI(extractedData) {
        // Find the container to display extracted data
        const container = document.getElementById('extractedHealthData');
        if (!container) return;
        
        // Clear previous data
        container.innerHTML = '';
        
        // Create a table for the extracted data
        const table = document.createElement('table');
        table.className = 'table table-striped mt-3';
        
        // Add headers
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        const headerKeys = document.createElement('th');
        headerKeys.textContent = 'Health Metric';
        const headerValues = document.createElement('th');
        headerValues.textContent = 'Value';
        headerRow.appendChild(headerKeys);
        headerRow.appendChild(headerValues);
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Add body with data
        const tbody = document.createElement('tbody');
        
        for (const key in extractedData) {
            if (extractedData.hasOwnProperty(key)) {
                const row = document.createElement('tr');
                
                const keyCell = document.createElement('td');
                keyCell.textContent = this.formatMetricName(key);
                
                const valueCell = document.createElement('td');
                valueCell.textContent = extractedData[key];
                
                row.appendChild(keyCell);
                row.appendChild(valueCell);
                tbody.appendChild(row);
            }
        }
        
        table.appendChild(tbody);
        container.appendChild(table);
        
        // Show the container if hidden
        container.style.display = 'block';
    }
    
    formatMetricName(key) {
        // Convert camelCase to Title Case with spaces
        return key
            .replace(/([A-Z])/g, ' $1')
            .replace(/^./, str => str.toUpperCase())
            .trim();
    }

    showSuccessMessage(message) {
        this.showMessage(message, 'success');
    }
    
    showErrorMessage(message) {
        this.showMessage(message, 'danger');
    }
    
    showMessage(message, type) {
        // Find or create alert container
        let alertContainer = document.getElementById('voiceAlertContainer');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.id = 'voiceAlertContainer';
            alertContainer.className = 'mt-3';
            
            // Find a place to insert it
            const extractedData = document.getElementById('extractedHealthData');
            if (extractedData) {
                extractedData.parentNode.insertBefore(alertContainer, extractedData);
            } else {
                document.getElementById('voiceTranscript').parentNode.appendChild(alertContainer);
            }
        }
        
        // Create alert
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Add to container
        alertContainer.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
    
    speak(text) {
        if (!this.speechSynthesis) return;
        
        // Cancel any ongoing speech
        this.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = document.documentElement.lang || 'en-US';
        
        // Find a female voice if available
        const voices = this.speechSynthesis.getVoices();
        const femaleVoice = voices.find(voice => voice.name.includes('female'));
        if (femaleVoice) utterance.voice = femaleVoice;
        
        this.speechSynthesis.speak(utterance);
    }
    
    // Public method to clear transcripts
    clearTranscripts() {
        this.transcripts = [];
        const transcriptElement = document.getElementById('voiceTranscript');
        if (transcriptElement) {
            transcriptElement.innerHTML = '';
        }
        const interimElement = document.getElementById('interimTranscript');
        if (interimElement) {
            interimElement.textContent = '';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Create global instance
    window.voiceRecognition = new VoiceRecognition();
    
    // Set up event listeners for voice control buttons
    const startButton = document.getElementById('startVoiceButton');
    if (startButton) {
        startButton.addEventListener('click', () => {
            window.voiceRecognition.start();
        });
    }
    
    const stopButton = document.getElementById('stopVoiceButton');
    if (stopButton) {
        stopButton.addEventListener('click', () => {
            window.voiceRecognition.stop();
        });
    }
    
    const clearButton = document.getElementById('clearVoiceButton');
    if (clearButton) {
        clearButton.addEventListener('click', () => {
            window.voiceRecognition.clearTranscripts();
            
            // Also clear extracted data
            const extractedData = document.getElementById('extractedHealthData');
            if (extractedData) {
                extractedData.innerHTML = '';
                extractedData.style.display = 'none';
            }
        });
    }
});