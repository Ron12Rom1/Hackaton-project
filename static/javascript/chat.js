// שמירת סוג המשתמש במשתנה גלובלי
const userType = "{{ user_type }}";
const userId = "{{ user_id }}";

// Load previous messages
async function loadMessages() {
    try {
        const response = await fetch(`/api/messages/${userId}`);
        const data = await response.json();
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = ''; // Clear existing messages
        
        data.messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${message.sender_id == userId ? 'sent' : 'received'}`;
            messageElement.textContent = message.content;
            messagesDiv.appendChild(messageElement);
        });
        
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
            // Save message to database
            const formData = new FormData();
            formData.append('sender_id', userId);
            formData.append('receiver_id', '{{ receiver_id }}');
            formData.append('content', message);
                    
            const response = await fetch('/api/messages', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // Add message to chat
                const messagesDiv = document.getElementById('messages');
                const messageElement = document.createElement('div');
                messageElement.className = 'message sent';
                messageElement.textContent = message;
                messagesDiv.appendChild(messageElement);
                
                input.value = '';
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    }
}

// Handle Enter key
document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});