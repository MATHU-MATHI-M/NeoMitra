document.addEventListener('DOMContentLoaded', function() {
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const voiceButton = document.getElementById('voice-button');
    const minimizeButton = document.getElementById('minimize-chatbot');
    const expandButton = document.getElementById('expand-chatbot');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    
    let isListening = false;
    let recognition = null;
    
    // Initialize Web Speech API if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            isListening = true;
            voiceButton.classList.add('listening');
            voiceButton.innerHTML = '<i class="fas fa-microphone-alt"></i>';
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };
        
        recognition.onend = function() {
            isListening = false;
            voiceButton.classList.remove('listening');
            voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            isListening = false;
            voiceButton.classList.remove('listening');
            voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
            
            addBotMessage("I couldn't hear you clearly. Please try again or type your message.");
        };
    } else {
        // Hide voice button if not supported
        if (voiceButton) {
            voiceButton.style.display = 'none';
        }
    }
    
    // Add greeting message when chatbot loads
    function addWelcomeMessage() {
        setTimeout(() => {
            addBotMessage("Hello! I'm the NeoMitra Assistant. I can help you with questions about pregnancy, anemia prevention, health schemes, and more. How can I assist you today?");
        }, 500);
    }
    
    // Add a user message to the chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message user-message';
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Add a bot message to the chat
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message bot-message';
        
        // Show typing indicator
        messageElement.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Replace typing indicator with actual message after a delay
        setTimeout(() => {
            messageElement.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>${formatMessage(message)}</p>
                </div>
            `;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }
    
    // Format message with markdown-like syntax
    function formatMessage(message) {
        // Bold text between ** **
        message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text between * *
        message = message.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convert line breaks to <br>
        message = message.replace(/\n/g, '<br>');
        
        return message;
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // Send a message to the chatbot API
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        userInput.value = '';
        
        // Send message to server
        fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Add bot response to chat
            addBotMessage(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addBotMessage("I'm sorry, I'm having trouble connecting. Please try again later.");
        });
    }
    
    // Toggle voice recognition
    function toggleVoiceRecognition() {
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }
    
    // Toggle chatbot visibility
    function toggleChatbot() {
        if (chatbotContainer.classList.contains('minimized')) {
            chatbotContainer.classList.remove('minimized');
        } else {
            chatbotContainer.classList.add('minimized');
        }
    }
    
    // Event listeners
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    if (voiceButton) {
        voiceButton.addEventListener('click', toggleVoiceRecognition);
    }
    
    if (minimizeButton) {
        minimizeButton.addEventListener('click', function() {
            chatbotContainer.classList.add('minimized');
        });
    }
    
    if (expandButton) {
        expandButton.addEventListener('click', function() {
            chatbotContainer.classList.remove('minimized');
        });
    }
    
    if (chatbotToggle) {
        chatbotToggle.addEventListener('click', toggleChatbot);
    }
    
    // Add welcome message when chat loads
    if (chatMessages) {
        addWelcomeMessage();
    }
    
    // Make chatbot draggable
    if (chatbotContainer) {
        makeDraggable(chatbotContainer);
    }
});

// Make an element draggable
function makeDraggable(element) {
    const header = element.querySelector('.chatbot-header');
    if (!header) return;
    
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    
    header.onmousedown = dragMouseDown;
    
    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        
        // Get the mouse cursor position at startup
        pos3 = e.clientX;
        pos4 = e.clientY;
        
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }
    
    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        
        // Calculate the new cursor position
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        
        // Set the element's new position
        element.style.top = (element.offsetTop - pos2) + "px";
        element.style.left = (element.offsetLeft - pos1) + "px";
        
        // Ensure the chatbot stays within the viewport
        const rect = element.getBoundingClientRect();
        if (rect.left < 0) element.style.left = "0px";
        if (rect.top < 0) element.style.top = "0px";
        if (rect.right > window.innerWidth) element.style.left = (window.innerWidth - rect.width) + "px";
        if (rect.bottom > window.innerHeight) element.style.top = (window.innerHeight - rect.height) + "px";
    }
    
    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
