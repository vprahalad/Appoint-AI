const chatbotToggle = document.querySelector('.chatbot-toggle');
const chatbot = document.querySelector('.chatbot');
const closeChatbot = document.querySelector('.close-chatbot');
const messagesContainer = document.querySelector('.messages');
const inputField = document.querySelector('.chatbot-input input');
const sendButton = document.querySelector('.chatbot-input button');

chatbotToggle.addEventListener('click', () => {
    chatbot.classList.toggle('open');
});

closeChatbot.addEventListener('click', () => {
    chatbot.classList.remove('open');
});

function sendMessage(message) {
    fetch('http://localhost:3000/chat', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),  
    })
    .then(response => response.json())
    .then(data => {
        displayMessage('Bot', data.response); 
    })
    .catch(error => console.error('Error:', error));
}

function displayMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight; 
}


sendButton.addEventListener('click', () => {
    const userMessage = inputField.value.trim();
    if (userMessage) {
        displayMessage('You', userMessage);
        sendMessage(userMessage); 
        inputField.value = '';  
    }
});

inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});
