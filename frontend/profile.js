// Profile page functionality
let currentUser = null;

document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    if (!requireAuth()) return;
    
    // Load user profile
    await loadProfile();
    
    // Setup form handlers
    setupFormHandlers();
    setupSDGGrid();
});

async function loadProfile() {
    try {
        const response = await authFetch(`${API_BASE}/auth/me`);
        if (!response) return;
        
        currentUser = await response.json();
        
        // Update UI
        const firstName = currentUser.full_name.charAt(0).toUpperCase();
        document.getElementById('userName').textContent = currentUser.full_name.split(' ')[0];
        document.getElementById('userAvatar').textContent = firstName;
        document.getElementById('profileAvatar').textContent = firstName;
        document.getElementById('profileName').textContent = currentUser.full_name;
        document.getElementById('profileEmail').textContent = currentUser.email;
        
        // Fill form fields
        document.getElementById('fullName').value = currentUser.full_name;
        document.getElementById('email').value = currentUser.email;
        document.getElementById('orgType').value = currentUser.organization_type;
        
        // Set notification toggles
        document.getElementById('emailNotifications').checked = currentUser.email_notifications === 1;
        document.getElementById('allNotifications').checked = currentUser.notifications_enabled === 1;
        
        // Select SDGs
        if (currentUser.sdg_interests) {
            currentUser.sdg_interests.forEach(sdg => {
                const card = document.querySelector(`.sdg-card[data-sdg="${sdg}"]`);
                if (card) card.classList.add('selected');
            });
        }
        
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function setupFormHandlers() {
    // Profile form
    document.getElementById('profileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const fullName = document.getElementById('fullName').value;
        
        try {
            const response = await authFetch(`${API_BASE}/auth/me`, {
                method: 'PUT',
                body: JSON.stringify({ full_name: fullName })
            });
            
            if (response && response.ok) {
                showToast('success', 'Profile updated successfully!');
                await loadProfile();
            } else {
                showToast('error', 'Failed to update profile');
            }
        } catch (error) {
            showToast('error', 'Network error');
        }
    });
    
    // Password form
    document.getElementById('passwordForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (newPassword !== confirmPassword) {
            showToast('error', 'New passwords do not match');
            return;
        }
        
        if (newPassword.length < 8) {
            showToast('error', 'Password must be at least 8 characters');
            return;
        }
        
        try {
            const response = await authFetch(`${API_BASE}/auth/change-password`, {
                method: 'POST',
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });
            
            if (response && response.ok) {
                showToast('success', 'Password changed successfully!');
                document.getElementById('passwordForm').reset();
            } else {
                const data = await response.json();
                showToast('error', data.detail || 'Failed to change password');
            }
        } catch (error) {
            showToast('error', 'Network error');
        }
    });
}

function setupSDGGrid() {
    const sdgNames = {
        1: "No Poverty", 2: "Zero Hunger", 3: "Good Health", 4: "Quality Education",
        5: "Gender Equality", 6: "Clean Water", 7: "Clean Energy", 8: "Decent Work",
        9: "Innovation", 10: "Reduced Inequalities", 11: "Sustainable Cities", 
        12: "Responsible Consumption", 13: "Climate Action", 14: "Life Below Water", 
        15: "Life on Land", 16: "Peace & Justice", 17: "Partnerships"
    };
    
    const sdgGrid = document.getElementById('sdgGrid');
    
    for (let i = 1; i <= 17; i++) {
        const card = document.createElement('div');
        card.className = 'sdg-card';
        card.dataset.sdg = i;
        card.innerHTML = `
            <div class="sdg-number">${i}</div>
            <div class="sdg-name">${sdgNames[i]}</div>
        `;
        card.onclick = () => card.classList.toggle('selected');
        sdgGrid.appendChild(card);
    }
}

async function saveSDGInterests() {
    const selectedSDGs = Array.from(document.querySelectorAll('.sdg-card.selected'))
        .map(card => parseInt(card.dataset.sdg));
    
    try {
        const response = await authFetch(`${API_BASE}/auth/me`, {
            method: 'PUT',
            body: JSON.stringify({ sdg_interests: selectedSDGs })
        });
        
        if (response && response.ok) {
            showToast('success', 'SDG interests updated!');
            await loadProfile();
        } else {
            showToast('error', 'Failed to update SDG interests');
        }
    } catch (error) {
        showToast('error', 'Network error');
    }
}

async function savePreferences() {
    const emailNotifications = document.getElementById('emailNotifications').checked;
    const allNotifications = document.getElementById('allNotifications').checked;
    
    try {
        const response = await authFetch(`${API_BASE}/auth/me`, {
            method: 'PUT',
            body: JSON.stringify({
                email_notifications: emailNotifications,
                notifications_enabled: allNotifications
            })
        });
        
        if (response && response.ok) {
            showToast('success', 'Preferences saved!');
        } else {
            showToast('error', 'Failed to save preferences');
        }
    } catch (error) {
        showToast('error', 'Network error');
    }
}

function confirmDeleteAccount() {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        if (confirm('This will permanently delete all your data. Are you absolutely sure?')) {
            alert('Account deletion feature will be implemented. Contact support for now.');
        }
    }
}

function showToast(type, message) {
    const toastId = type === 'success' ? 'successToast' : 'errorToast';
    const toast = document.getElementById(toastId);
    const messageEl = toast.querySelector('.toast-message');
    messageEl.textContent = message;
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function toggleUserMenu() {
    document.getElementById('userDropdown').classList.toggle('show');
}

// Profile navigation
document.querySelectorAll('.profile-nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active state
        document.querySelectorAll('.profile-nav-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        
        // Scroll to section
        const target = document.querySelector(item.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
