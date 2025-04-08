function showDateTimeSelector(type) {
    // הסתר את כל הסלקטורים
    document.querySelectorAll('.datetime-selector').forEach(el => {
        el.classList.remove('active');
    });
    
    // הצג את הסלקטור המתאים
    const datetimeSelector = document.getElementById(`${type}-datetime`);
    datetimeSelector.classList.add('active');
    
    // הוסף כפתורי ניווט לסלקטור
    const navButtons = `
        <div class="nav-buttons">
            <button class="nav-button" onclick="window.location.href='/'">חזרה למסך הראשי</button>
        </div>
    `;
    
    if (!datetimeSelector.querySelector('.nav-buttons')) {
        datetimeSelector.insertAdjacentHTML('afterbegin', navButtons);
    }
}

function isValidTime(time) {
    // בדיקה שהשעה נבחרה מהתפריט הנפתח
    return time !== "";
}

function scheduleMeeting(type) {
    const dateInput = document.getElementById(`${type}-date`);
    const timeInput = document.getElementById(`${type}-time`);
    
    if (!dateInput.value || !timeInput.value) {
        alert('נא למלא את כל השדות');
        return;
    }
    
    if (!isValidTime(timeInput.value)) {
        alert('נא לבחור שעה מהרשימה');
        return;
    }
    
    // בדיקה אם יש כבר פגישה באותו זמן
    const existingMeetings = document.querySelectorAll('.meeting-card');
    let hasConflict = false;
    
    existingMeetings.forEach(meeting => {
        const meetingDate = meeting.querySelector('p:nth-child(2)').textContent.split(': ')[1];
        const meetingTime = meeting.querySelector('p:nth-child(3)').textContent.split(': ')[1];
        
        if (meetingDate === dateInput.value && meetingTime === timeInput.value) {
            hasConflict = true;
        }
    });
    
    if (hasConflict) {
        alert('יש כבר פגישה מתוכננת בזמן זה. נא לבחור זמן אחר.');
        return;
    }
    
    // Here you would typically send the meeting data to the server
    // For now, we'll just add it to the UI
    const meetingsContainer = document.getElementById('meetings-container');
    const meetingCard = document.createElement('div');
    meetingCard.className = 'meeting-card';
    
    meetingCard.innerHTML = `
        <h3>נקבעה פגישה</h3>
        <p>תאריך: ${dateInput.value}</p>
        <p>שעה: ${timeInput.value}</p>
        <p>סטטוס: מתוכנן</p>
    `;
    
    meetingsContainer.appendChild(meetingCard);
    
    alert('הפגישה נקבעה בהצלחה!');
    hideDateTimeSelectors(type);
}

function hideDateTimeSelectors(type) {
    document.getElementById(`${type}-datetime`).classList.remove('active');
}

// Function to fetch and display meetings
async function fetchMeetings() {
    try {
        const userId = new URLSearchParams(window.location.search).get('user_id');
        console.log("Fetching meetings for user ID:", userId);
        
        // Try to fetch meetings from the API
        const response = await fetch(`/api/meetings/${userId}`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const meetings = await response.json();
        console.log("Fetched meetings:", meetings);
        
        const meetingsContainer = document.getElementById('meetings-container');
        meetingsContainer.innerHTML = '';
        
        if (!meetings || meetings.length === 0) {
            meetingsContainer.innerHTML = '<p>עדיין לא נקבעו פגישות</p>';
            return;
        }
        
        meetings.forEach(meeting => {
            const meetingCard = document.createElement('div');
            meetingCard.className = 'meeting-card';
            
            meetingCard.innerHTML = `
                <h3>נקבעה פגישה</h3>
                <p>תאריך: ${meeting.meeting_date}</p>
                <p>שעה: ${meeting.meeting_time}</p>
                <p>סטטוס: ${meeting.status || 'מתוכנן'}</p>
            `;
            meetingsContainer.appendChild(meetingCard);
        });
    } catch (error) {
        console.error('Error fetching meetings:', error);
        
        // Display a message if there's an error
        const meetingsContainer = document.getElementById('meetings-container');
        meetingsContainer.innerHTML = '<p>עדיין לא נקבעו פגישות</p>';
    }
}

// Fetch meetings when page loads
document.addEventListener('DOMContentLoaded', fetchMeetings);