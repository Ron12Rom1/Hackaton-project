function showDateTimeSelector(type) {
    // הסתר את כל הסלקטורים
    document.querySelectorAll('.datetime-selector').forEach(el => {
        el.classList.remove('active');
    });
    
    // הסתר את כל בחירות התפקיד
    document.querySelectorAll('.role-selector').forEach(el => {
        el.classList.remove('active');
    });
    
    // הצג את הסלקטור המתאים
    const datetimeSelector = document.getElementById(`${type}-datetime`);
    datetimeSelector.classList.add('active');
    
    // אם זה פגישה עם חיילים, הצג גם את בחירת התפקיד
    if (type === 'soldiers') {
        const roleSelector = document.getElementById(`${type}-role`);
        roleSelector.classList.add('active');
    }
    
    // הוסף כפתורי ניווט לסלקטור
    const navButtons = `
        <div class="nav-buttons">
            <button class="nav-button" onclick="window.location.href='/options/soldier'">סגור</button>
        </div>
    `;
    
    if (!datetimeSelector.querySelector('.nav-buttons')) {
        datetimeSelector.insertAdjacentHTML('afterbegin', navButtons);
    }
}

function selectRole(element, type) {
    // הסר את הבחירה מכל האפשרויות
    document.querySelectorAll(`#${type}-role .role-option`).forEach(el => {
        el.classList.remove('selected');
    });
    
    // סמן את האפשרות שנבחרה
    element.classList.add('selected');
    
    // מנע את הפעלת האירוע של ההורה
    event.stopPropagation();
}

function isValidTime(time) {
    // בדיקה שהשעה נבחרה מהתפריט הנפתח
    return time !== "";
}

function scheduleMeeting(type) {
    const dateInput = document.getElementById(`${type}-date`);
    const timeInput = document.getElementById(`${type}-time`);
    const roleSelect = document.getElementById(`${type}-role`);
    
    if (!dateInput.value || !timeInput.value) {
        alert('נא למלא את כל השדות');
        return;
    }
    
    if (type === 'psychologist' && !isValidTime(timeInput.value)) {
        alert('פגישות עם פסיכולוג זמינות רק בין השעות 10:00 ל-20:00');
        return;
    }
    
    let role = null;
    if (type === 'soldiers') {
        const selectedRole = document.querySelector(`#${type}-role .role-option.selected`);
        if (!selectedRole) {
            alert('נא לבחור תפקיד');
            return;
        }
        role = selectedRole.textContent;
    }
    
    alert('הפגישה נקבעה בהצלחה!');
    hideDateTimeSelectors(type);
}

function hideDateTimeSelectors(type) {
    document.getElementById(`${type}-datetime`).classList.remove('active');
    if (type === 'soldiers') {
        document.getElementById(`${type}-role`).classList.remove('active');
    }
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

// Also fetch meetings when a new meeting is scheduled
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
    
    const meetingType = type === 'psychologist' ? 'פסיכולוג' : 'מפון אחר';
    meetingCard.innerHTML = `
        <h3>פגישה עם ${meetingType}</h3>
        <p>תאריך: ${dateInput.value}</p>
        <p>שעה: ${timeInput.value}</p>
        <p>סטטוס: מתוכנן</p>
    `;
    
    meetingsContainer.appendChild(meetingCard);
    
    alert('הפגישה נקבעה בהצלחה!');
    hideDateTimeSelectors(type);
}