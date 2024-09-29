const chatbotToggle = document.querySelector('.chatbot-toggle');
const chatbot = document.querySelector('.chatbot');
const closeChatbot = document.querySelector('.close-chatbot');
const messagesContainer = document.querySelector('.messages');
const inputField = document.querySelector('.chatbot-input input');
const sendButton = document.querySelector('.chatbot-input button');

// Toggle chatbot open and close
chatbotToggle.addEventListener('click', () => {
    chatbot.classList.toggle('open');
});

closeChatbot.addEventListener('click', () => {
    chatbot.classList.remove('open');
});

// Function to send message to backend
function sendMessage(message) {
    // Replace with your actual backend URL and endpoint
    fetch('http://localhost:3000/chat', {  // Ensure this URL matches your backend API
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),  // Send user message to backend
    })
    .then(response => response.json())
    .then(data => {
        displayMessage('Bot', data.response);  // Display bot's response
    })
    .catch(error => console.error('Error:', error));
}

// Function to display message in the chat window
function displayMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;  // Scroll to bottom
}

// Event listener for send button
sendButton.addEventListener('click', () => {
    const userMessage = inputField.value.trim();
    if (userMessage) {
        displayMessage('You', userMessage);
        sendMessage(userMessage);  // Send message to backend
        inputField.value = '';  // Clear input field
    }
});

// Optionally, allow pressing 'Enter' to send the message
inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});
