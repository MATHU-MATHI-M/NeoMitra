/**
 * Chatbot Assistant for NeoMitra
 * Provides a floating chatbot interface for user assistance
 */

class ChatbotAssistant {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.createChatbotElement();
        this.initEventListeners();
    }

    createChatbotElement() {
        // Create the chatbot container
        this.chatbotContainer = document.createElement('div');
        this.chatbotContainer.className = 'chatbot-container';
        this.chatbotContainer.innerHTML = `
            <div class="chatbot-icon" id="chatbotIcon">
                <i class="bi bi-chat-dots-fill"></i>
            </div>

            <div class="chatbot-window" id="chatbotWindow" style="display: none;">
                <div class="chatbot-header">
                    <div class="chatbot-title">
                        <i class="bi bi-robot"></i>
                        NeoMitra Assistant
                    </div>
                    <div class="chatbot-controls">
                        <button class="chatbot-minimize-btn" id="chatbotMinimizeBtn">
                            <i class="bi bi-dash"></i>
                        </button>
                    </div>
                </div>
                <div class="chatbot-messages" id="chatbotMessages">
                    <div class="chat-message bot-message">
                        <div class="message-content">
                            Hello! I'm NeoMitra Assistant. How can I help you today?
                        </div>
                    </div>
                </div>
                <div class="chatbot-input">
                    <input type="text" id="chatbotInput" placeholder="Type your message here...">
                    <button id="chatbotSendBtn">
                        <i class="bi bi-send-fill"></i>
                    </button>
                </div>
            </div>
        `;

        // Add chatbot styles
        const style = document.createElement('style');
        style.textContent = `
            .chatbot-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .chatbot-icon {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: #7952b3;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                transition: all 0.3s;
            }

            .chatbot-icon i {
                font-size: 24px;
            }

            .chatbot-icon:hover {
                transform: scale(1.05);
                background-color: #6f42c1;
            }

            .chatbot-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .chatbot-header {
                background-color: #7952b3;
                color: white;
                padding: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .chatbot-title {
                display: flex;
                align-items: center;
                font-weight: 600;
            }

            .chatbot-title i {
                margin-right: 8px;
                font-size: 18px;
            }

            .chatbot-controls button {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                font-size: 18px;
            }

            .chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                background-color: #f8f9fa;
            }

            .chat-message {
                margin-bottom: 15px;
                display: flex;
                flex-direction: column;
            }

            .user-message {
                align-items: flex-end;
            }

            .bot-message {
                align-items: flex-start;
            }

            .message-content {
                padding: 12px 15px;
                border-radius: 20px;
                max-width: 80%;
                word-wrap: break-word;
            }

            .user-message .message-content {
                background-color: #7952b3;
                color: white;
            }

            .bot-message .message-content {
                background-color: #e9ecef;
                color: #212529;
            }

            .chatbot-input {
                padding: 15px;
                background-color: white;
                display: flex;
                border-top: 1px solid #dee2e6;
            }

            .chatbot-input input {
                flex: 1;
                padding: 10px 15px;
                border: 1px solid #ced4da;
                border-radius: 30px;
                outline: none;
            }

            .chatbot-input input:focus {
                border-color: #7952b3;
            }

            .chatbot-input button {
                background-color: #7952b3;
                color: white;
                border: none;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-left: 10px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s;
            }

            .chatbot-input button:hover {
                background-color: #6f42c1;
            }

            .chatbot-input button i {
                font-size: 16px;
            }

            @media (max-width: 576px) {
                .chatbot-window {
                    width: 300px;
                    height: 450px;
                    bottom: 70px;
                    right: 0;
                }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(this.chatbotContainer);
    }

    initEventListeners() {
        // Open/close chatbot
        const chatbotIcon = document.getElementById('chatbotIcon');
        const chatbotWindow = document.getElementById('chatbotWindow');
        const chatbotMinimizeBtn = document.getElementById('chatbotMinimizeBtn');
        
        chatbotIcon.addEventListener('click', () => {
            this.isOpen = !this.isOpen;
            chatbotWindow.style.display = this.isOpen ? 'flex' : 'none';
        });
        
        chatbotMinimizeBtn.addEventListener('click', () => {
            this.isOpen = false;
            chatbotWindow.style.display = 'none';
        });
        
        // Send message
        const chatbotInput = document.getElementById('chatbotInput');
        const chatbotSendBtn = document.getElementById('chatbotSendBtn');
        
        const sendMessage = () => {
            const message = chatbotInput.value.trim();
            if (message) {
                this.addUserMessage(message);
                chatbotInput.value = '';
                
                // Process the message and get response
                this.processMessage(message);
            }
        };
        
        chatbotSendBtn.addEventListener('click', sendMessage);
        
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    addUserMessage(message) {
        const chatbotMessages = document.getElementById('chatbotMessages');
        
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message user-message';
        messageElement.innerHTML = `
            <div class="message-content">
                ${message}
            </div>
        `;
        
        chatbotMessages.appendChild(messageElement);
        this.scrollToBottom();
        
        this.messages.push({
            role: 'user',
            content: message
        });
    }
    
    addBotMessage(message) {
        const chatbotMessages = document.getElementById('chatbotMessages');
        
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message bot-message';
        messageElement.innerHTML = `
            <div class="message-content">
                ${message}
            </div>
        `;
        
        chatbotMessages.appendChild(messageElement);
        this.scrollToBottom();
        
        this.messages.push({
            role: 'bot',
            content: message
        });
    }
    
    scrollToBottom() {
        const chatbotMessages = document.getElementById('chatbotMessages');
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    processMessage(message) {
        // Show typing indicator
        this.showTypingIndicator();
        
        // Call the API
        fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                language: 'en'
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            this.removeTypingIndicator();
            
            // Add bot response
            this.addBotMessage(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            this.removeTypingIndicator();
            this.addBotMessage('Sorry, I encountered an error. Please try again later.');
        });
    }
    
    showTypingIndicator() {
        const chatbotMessages = document.getElementById('chatbotMessages');
        
        const typingElement = document.createElement('div');
        typingElement.className = 'chat-message bot-message typing-indicator';
        typingElement.id = 'typingIndicator';
        typingElement.innerHTML = `
            <div class="message-content">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        `;
        
        chatbotMessages.appendChild(typingElement);
        this.scrollToBottom();
        
        // Add typing indicator styles
        const style = document.createElement('style');
        style.textContent = `
            .typing-indicator .message-content {
                padding: 12px 15px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .typing-indicator .dot {
                width: 8px;
                height: 8px;
                background-color: #6c757d;
                border-radius: 50%;
                margin: 0 3px;
                animation: typing-animation 1.5s infinite ease-in-out;
            }
            
            .typing-indicator .dot:nth-child(1) {
                animation-delay: 0s;
            }
            
            .typing-indicator .dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-indicator .dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing-animation {
                0%, 60%, 100% {
                    transform: translateY(0);
                }
                30% {
                    transform: translateY(-6px);
                }
            }
        `;
        
        if (!document.getElementById('typingIndicatorStyle')) {
            style.id = 'typingIndicatorStyle';
            document.head.appendChild(style);
        }
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const chatbot = new ChatbotAssistant();
});