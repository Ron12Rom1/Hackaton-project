// Global variables
const userType = "{{ user_type }}";
const userId = "{{ user_id }}";
const receiverId = "{{ receiver_id }}";
console.log(document.getElementById('message-input')); // Should not be null

// Load previous messages
async function loadMessages() {
    try {
        const response = await fetch(`/api/messages/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = ''; // Clear existing messages
        
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';  // All messages are sent by user
                messageElement.textContent = message.content;
                messagesDiv.appendChild(messageElement);
            });
        }
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

// Load messages when page loads
loadMessages();

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (message) {
        try {
            const formData = new FormData();
            formData.append('sender_id', userId.toString());
            formData.append('receiver_id', receiverId.toString());
            formData.append('content', message);
            
            const response = await fetch('/api/messages', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Add user message to chat
            const messagesDiv = document.getElementById('messages');
            const messageElement = document.createElement('div');
            messageElement.className = 'message sent';
            messageElement.textContent = message;
            messagesDiv.appendChild(messageElement);
            
            // Clear input
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        } catch (error) {
            console.error('Error sending message:', error);
            alert('שגיאה בשליחת ההודעה. אנא נסה שוב.');
        }
    }
}

// Handle Enter key
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('message-input');
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
});