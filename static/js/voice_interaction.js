document.addEventListener('DOMContentLoaded', function() {
    // Initialize Web Speech API functionality
    initializeVoiceInteraction();
});

// Function to initialize voice interaction
function initializeVoiceInteraction() {
    // Check if browser supports speech recognition
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        console.warn('Speech Recognition API is not supported in this browser');
        hideVoiceFeatures();
        return;
    }

    // Elements
    const voiceSearchButton = document.getElementById('voice-search-button');
    const voiceInputButtons = document.querySelectorAll('.voice-input-button');
    const languageSelector = document.getElementById('language-selector');

    // Create speech recognition object
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    // Configure recognition
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = languageSelector ? languageSelector.value : 'en-US';

    // Update language if selector changes
    if (languageSelector) {
        languageSelector.addEventListener('change', function() {
            const langMap = {
                'en': 'en-US',
                'hi': 'hi-IN',
                'ta': 'ta-IN',
                'te': 'te-IN',
                'bn': 'bn-IN',
                'mr': 'mr-IN'
            };
            recognition.lang = langMap[this.value] || 'en-US';
        });
    }

    // Handle voice search button
    if (voiceSearchButton) {
        voiceSearchButton.addEventListener('click', function() {
            startVoiceRecognition(recognition, 'search-query');
        });
    }

    // Handle all voice input buttons
    voiceInputButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetInputId = this.getAttribute('data-target');
            startVoiceRecognition(recognition, targetInputId);
        });
    });

    // Add voice input to text fields
    addVoiceInputToTextFields();
}

// Function to start voice recognition
function startVoiceRecognition(recognition, targetElementId) {
    const targetElement = document.getElementById(targetElementId);
    if (!targetElement) {
        console.error('Target element not found:', targetElementId);
        return;
    }

    // Show visual feedback
    showListeningAnimation(targetElement);

    // Define recognition event handlers
    recognition.onstart = function() {
        console.log('Voice recognition started');
    };

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        targetElement.value = transcript;
        hideListeningAnimation(targetElement);
        
        // Trigger input event to activate any listeners
        const inputEvent = new Event('input', {
            bubbles: true,
            cancelable: true,
        });
        targetElement.dispatchEvent(inputEvent);
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        hideListeningAnimation(targetElement);
        showErrorNotification('Could not recognize speech. Please try again.');
    };

    recognition.onend = function() {
        hideListeningAnimation(targetElement);
    };

    // Start recognition
    try {
        recognition.start();
    } catch (error) {
        console.error('Error starting speech recognition:', error);
        hideListeningAnimation(targetElement);
    }
}

// Function to add voice input buttons to all text fields
function addVoiceInputToTextFields() {
    const textInputs = document.querySelectorAll('input[type="text"], input[type="search"], textarea');
    
    textInputs.forEach(input => {
        // Skip if input already has voice input or is hidden/disabled
        if (input.parentElement.querySelector('.voice-input-button') || 
            input.disabled || 
            input.readOnly || 
            input.type === 'hidden') {
            return;
        }
        
        // Create voice input button
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'voice-input-button btn btn-sm btn-light';
        button.setAttribute('data-target', input.id);
        button.innerHTML = '<i class="fas fa-microphone"></i>';
        button.title = 'Voice input';
        
        // Add button after input in a wrapper
        if (!input.parentElement.classList.contains('input-group')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'input-group';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
        }
        
        const inputGroup = input.parentElement;
        const buttonWrapper = document.createElement('div');
        buttonWrapper.className = 'input-group-append';
        buttonWrapper.appendChild(button);
        inputGroup.appendChild(buttonWrapper);
        
        // Add click event
        button.addEventListener('click', function() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                
                startVoiceRecognition(recognition, input.id);
            } else {
                showErrorNotification('Speech recognition is not supported in your browser');
            }
        });
    });
}

// Function to hide voice features if not supported
function hideVoiceFeatures() {
    const voiceButtons = document.querySelectorAll('.voice-input-button, #voice-search-button');
    voiceButtons.forEach(button => {
        button.style.display = 'none';
    });
}

// Function to show listening animation
function showListeningAnimation(targetElement) {
    // Create and add listening indicator
    const indicator = document.createElement('div');
    indicator.className = 'listening-indicator';
    indicator.innerHTML = `
        <div class="listening-ripple">
            <div class="listening-wave"></div>
            <div class="listening-wave"></div>
            <div class="listening-wave"></div>
        </div>
        <span>Listening...</span>
    `;
    
    // Position the indicator near the target element
    const rect = targetElement.getBoundingClientRect();
    indicator.style.top = (rect.bottom + window.scrollY + 5) + 'px';
    indicator.style.left = (rect.left + window.scrollX) + 'px';
    
    // Add to body
    document.body.appendChild(indicator);
    
    // Add active class to the target input
    targetElement.classList.add('voice-active');
}

// Function to hide listening animation
function hideListeningAnimation(targetElement) {
    const indicator = document.querySelector('.listening-indicator');
    if (indicator) {
        indicator.remove();
    }
    
    // Remove active class from the target input
    targetElement.classList.remove('voice-active');
}

// Function to show error notification
function showErrorNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'voice-error-notification';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Voice-to-text for scheme search
function initializeSchemeSearch() {
    const searchInput = document.getElementById('scheme-search');
    const searchButton = document.getElementById('scheme-search-button');
    const schemeCards = document.querySelectorAll('.scheme-card');
    
    if (!searchInput || !schemeCards.length) return;
    
    function filterSchemes() {
        const query = searchInput.value.toLowerCase();
        let matchFound = false;
        
        schemeCards.forEach(card => {
            const title = card.querySelector('h5').textContent.toLowerCase();
            const description = card.querySelector('.card-text').textContent.toLowerCase();
            const content = title + ' ' + description;
            
            if (content.includes(query) || query === '') {
                card.style.display = 'block';
                matchFound = true;
                
                // Highlight matching text
                if (query !== '') {
                    highlightText(card, query);
                } else {
                    // Remove highlights
                    card.innerHTML = card.innerHTML.replace(/<mark>(.*?)<\/mark>/g, '$1');
                }
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show no results message if needed
        const noResults = document.getElementById('no-results');
        if (noResults) {
            noResults.style.display = matchFound ? 'none' : 'block';
        }
    }
    
    // Highlight matching text
    function highlightText(element, query) {
        const title = element.querySelector('h5');
        const description = element.querySelector('.card-text');
        
        // Remove existing highlights
        title.innerHTML = title.innerHTML.replace(/<mark>(.*?)<\/mark>/g, '$1');
        description.innerHTML = description.innerHTML.replace(/<mark>(.*?)<\/mark>/g, '$1');
        
        // Add new highlights
        const regex = new RegExp(query, 'gi');
        title.innerHTML = title.innerHTML.replace(regex, match => `<mark>${match}</mark>`);
        description.innerHTML = description.innerHTML.replace(regex, match => `<mark>${match}</mark>`);
    }
    
    // Event listeners
    searchInput.addEventListener('input', filterSchemes);
    
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    searchInput.value = transcript;
                    filterSchemes();
                };
                
                recognition.start();
            }
        });
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSchemeSearch);
} else {
    initializeSchemeSearch();
}
