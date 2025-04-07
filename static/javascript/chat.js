function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (message) {
        const messagesDiv = document.getElementById('messages');
        const messageElement = document.createElement('div');
        messageElement.className = 'message sent';
        messageElement.textContent = message;
        messagesDiv.appendChild(messageElement);
        
        input.value = '';
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

// Handle Enter key
document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});