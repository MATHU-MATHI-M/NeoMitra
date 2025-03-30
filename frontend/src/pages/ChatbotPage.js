import React, { useState, useEffect, useRef } from 'react';
import { Container, Row, Col, Card, Form, Button, Dropdown } from 'react-bootstrap';
import axios from 'axios';
import './ChatbotPage.css';

const ChatbotPage = ({ user }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hello! I'm NeoMitra Assistant. How can I help you with your maternal health questions today?",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  
  const endOfMessagesRef = useRef(null);
  const languageOptions = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi' },
    { code: 'ta', name: 'Tamil' },
    { code: 'te', name: 'Telugu' },
    { code: 'bn', name: 'Bengali' },
    { code: 'mr', name: 'Marathi' }
  ];
  
  // Scroll to the bottom of the chat when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const handleSendMessage = async (e) => {
    e?.preventDefault();
    
    if (!inputMessage.trim()) return;
    
    const userMessage = {
      id: new Date().getTime(),
      sender: 'user',
      text: inputMessage,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    
    try {
      // In a real app, send request to the server
      // For now, simulate API call with timeout
      setTimeout(async () => {
        const botResponse = {
          id: new Date().getTime() + 1,
          sender: 'bot',
          text: await getMockBotResponse(inputMessage, selectedLanguage),
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        
        setMessages(prevMessages => [...prevMessages, botResponse]);
        setIsLoading(false);
      }, 1000);
      
      // In a real implementation, this would be:
      /*
      const response = await axios.post('/api/chatbot', {
        message: inputMessage,
        language: selectedLanguage
      });
      
      const botResponse = {
        id: new Date().getTime() + 1,
        sender: 'bot',
        text: response.data.response,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages(prevMessages => [...prevMessages, botResponse]);
      setIsLoading(false);
      */
      
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorResponse = {
        id: new Date().getTime() + 1,
        sender: 'bot',
        text: 'Sorry, I encountered an error processing your request. Please try again later.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true
      };
      
      setMessages(prevMessages => [...prevMessages, errorResponse]);
      setIsLoading(false);
    }
  };
  
  const getMockBotResponse = (message, language) => {
    // Mock responses for demonstration
    const lowercaseMessage = message.toLowerCase();
    
    if (lowercaseMessage.includes('hello') || lowercaseMessage.includes('hi')) {
      return "Hello! How are you feeling today?";
    } else if (lowercaseMessage.includes('pain') || lowercaseMessage.includes('hurt')) {
      return "I'm sorry to hear you're experiencing pain. Could you tell me where the pain is located and how severe it is on a scale of 1-10? If you're experiencing severe pain, please contact your healthcare provider immediately.";
    } else if (lowercaseMessage.includes('diet') || lowercaseMessage.includes('food') || lowercaseMessage.includes('eat')) {
      return "For a healthy pregnancy, focus on a balanced diet with plenty of fruits, vegetables, whole grains, lean proteins, and dairy. It's important to get enough folate, iron, calcium, and protein. Would you like specific recommendations for any nutrient?";
    } else if (lowercaseMessage.includes('anemia') || lowercaseMessage.includes('iron')) {
      return "Anemia during pregnancy is common and often caused by iron deficiency. To prevent or treat it, include iron-rich foods like leafy greens, beans, red meat, and fortified cereals in your diet. Your doctor may also recommend iron supplements. Regular check-ups to monitor your hemoglobin levels are important.";
    } else if (lowercaseMessage.includes('government') || lowercaseMessage.includes('scheme') || lowercaseMessage.includes('benefit')) {
      return "There are several government healthcare schemes available for pregnant women, including Janani Suraksha Yojana (JSY), Pradhan Mantri Matru Vandana Yojana (PMMVY), and Janani Shishu Suraksha Karyakram (JSSK). These provide financial assistance, free check-ups, and other benefits. Would you like more details about any of these programs?";
    } else if (lowercaseMessage.includes('exercise') || lowercaseMessage.includes('workout')) {
      return "Regular, moderate exercise during pregnancy is beneficial. Walking, swimming, prenatal yoga, and stationary cycling are good options. Always consult your healthcare provider before starting any exercise routine during pregnancy. Avoid high-impact activities and exercises that risk falling or abdominal injury.";
    } else {
      return "Thank you for your message. I understand you're asking about " + message + ". Could you provide more details so I can give you the most helpful information?";
    }
  };
  
  const handleVoiceInput = () => {
    // Toggle recording state
    setIsRecording(!isRecording);
    
    if (!isRecording) {
      // Start recording - in a real implementation, this would use the Web Speech API
      // For now, just simulate voice input
      setTimeout(() => {
        setInputMessage("Tell me about anemia during pregnancy");
        setIsRecording(false);
      }, 2000);
    } else {
      // Stop recording
      setIsRecording(false);
    }
  };
  
  const handleLanguageChange = (code) => {
    setSelectedLanguage(code);
  };
  
  return (
    <div className="chatbot-page">
      <Container>
        <Row className="justify-content-center">
          <Col lg={8}>
            <div className="chatbot-header">
              <h2 className="chatbot-title">NeoMitra Assistant</h2>
              <p className="chatbot-subtitle">Ask me anything about your maternal health journey</p>
            </div>
            
            <Card className="chatbot-card">
              <Card.Body className="p-0">
                <div className="chat-header">
                  <div className="chat-avatar">
                    <div className="avatar-circle">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-robot" viewBox="0 0 16 16">
                        <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5ZM3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.58 26.58 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.933.933 0 0 1-.765.935c-.845.147-2.34.346-4.235.346-1.895 0-3.39-.2-4.235-.346A.933.933 0 0 1 3 9.219V8.062Zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a24.767 24.767 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25.286 25.286 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135Z"/>
                        <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2V1.866ZM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5Z"/>
                      </svg>
                    </div>
                  </div>
                  <div className="chat-info">
                    <div className="chat-name">NeoMitra Assistant</div>
                    <div className="chat-status">Online</div>
                  </div>
                  <div className="language-selector">
                    <Dropdown>
                      <Dropdown.Toggle variant="outline-secondary" id="language-dropdown" className="language-dropdown">
                        {languageOptions.find(lang => lang.code === selectedLanguage)?.name || 'Language'}
                      </Dropdown.Toggle>
                      <Dropdown.Menu>
                        {languageOptions.map(lang => (
                          <Dropdown.Item 
                            key={lang.code} 
                            onClick={() => handleLanguageChange(lang.code)}
                            active={selectedLanguage === lang.code}
                          >
                            {lang.name}
                          </Dropdown.Item>
                        ))}
                      </Dropdown.Menu>
                    </Dropdown>
                  </div>
                </div>
                
                <div className="chat-messages">
                  {messages.map(message => (
                    <div 
                      key={message.id} 
                      className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'} ${message.isError ? 'error-message' : ''}`}
                    >
                      {message.sender === 'bot' && (
                        <div className="message-avatar">
                          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" className="bi bi-robot" viewBox="0 0 16 16">
                            <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5ZM3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.58 26.58 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.933.933 0 0 1-.765.935c-.845.147-2.34.346-4.235.346-1.895 0-3.39-.2-4.235-.346A.933.933 0 0 1 3 9.219V8.062Zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a24.767 24.767 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25.286 25.286 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135Z"/>
                            <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2V1.866ZM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5Z"/>
                          </svg>
                        </div>
                      )}
                      <div className="message-content">
                        <div className="message-text">{message.text}</div>
                        <div className="message-time">{message.time}</div>
                      </div>
                    </div>
                  ))}
                  
                  {isLoading && (
                    <div className="message bot-message typing-indicator">
                      <div className="message-avatar">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" className="bi bi-robot" viewBox="0 0 16 16">
                          <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5ZM3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.58 26.58 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.933.933 0 0 1-.765.935c-.845.147-2.34.346-4.235.346-1.895 0-3.39-.2-4.235-.346A.933.933 0 0 1 3 9.219V8.062Zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a24.767 24.767 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25.286 25.286 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135Z"/>
                          <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2V1.866ZM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5Z"/>
                        </svg>
                      </div>
                      <div className="message-content">
                        <div className="typing-dots">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Empty div for scrolling to bottom */}
                  <div ref={endOfMessagesRef} />
                </div>
                
                <div className="chat-input-area">
                  <Form onSubmit={handleSendMessage}>
                    <div className="input-group">
                      <Button 
                        variant={isRecording ? "danger" : "secondary"}
                        className="voice-btn"
                        onClick={handleVoiceInput}
                        aria-label="Voice Input"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-mic" viewBox="0 0 16 16">
                          <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z"/>
                          <path d="M10 8a2 2 0 1 1-4 0V3a2 2 0 1 1 4 0v5zM8 0a3 3 0 0 0-3 3v5a3 3 0 0 0 6 0V3a3 3 0 0 0-3-3z"/>
                        </svg>
                        {isRecording && <span className="recording-pulse"></span>}
                      </Button>
                      <Form.Control
                        type="text"
                        placeholder="Type your message here..."
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        disabled={isLoading || isRecording}
                      />
                      <Button 
                        variant="primary" 
                        type="submit" 
                        disabled={!inputMessage.trim() || isLoading || isRecording}
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-send" viewBox="0 0 16 16">
                          <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07Zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493Z"/>
                        </svg>
                      </Button>
                    </div>
                  </Form>
                </div>
              </Card.Body>
            </Card>
            
            <div className="chatbot-info mt-4">
              <div className="info-card">
                <div className="info-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-info-circle" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                    <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                  </svg>
                </div>
                <div className="info-text">
                  This chatbot provides general maternal health information. For emergencies, please contact your healthcare provider immediately.
                </div>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default ChatbotPage;