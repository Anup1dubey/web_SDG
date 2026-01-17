// Dashboard functionality
document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    if (!requireAuth()) return;
    
    // Load user data
    await loadUserProfile();
    await loadDashboardStats();
    
    // Initialize the app (load twins, projects, etc.)
    if (typeof initializeApp === 'function') {
        await initializeApp();
    }
});

// Section Switching
function switchSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all menu items
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Add active class to corresponding menu item
    const menuItem = document.querySelector(`.menu-item[data-section="${sectionName}"]`);
    if (menuItem) {
        menuItem.classList.add('active');
    }
    
    // Load section-specific data if needed
    if (sectionName === 'twins' && typeof loadDigitalTwins === 'function') {
        loadDigitalTwins();
    } else if (sectionName === 'projects' && typeof loadProjects === 'function') {
        loadProjects();
    } else if (sectionName === 'orgs' && typeof loadOrganizations === 'function') {
        loadOrganizations();
    } else if (sectionName === 'simulate' && typeof loadSimulationData === 'function') {
        loadSimulationData();
    }
}

// Load user profile
async function loadUserProfile() {
    try {
        const response = await authFetch(`${API_BASE}/auth/me`);
        if (!response) return;
        
        const user = await response.json();
        
        // Update UI with user data
        const firstName = user.full_name.split(' ')[0];
        document.getElementById('userName').textContent = firstName;
        document.getElementById('userNameDisplay').textContent = firstName;
        document.getElementById('userAvatar').textContent = user.full_name.charAt(0).toUpperCase();
        document.getElementById('userEmail').textContent = user.email;
        document.getElementById('userOrgType').textContent = user.organization_type;
        
        // Display SDG interests
        const sdgBadges = document.getElementById('userSDGBadges');
        if (user.sdg_interests && user.sdg_interests.length > 0) {
            sdgBadges.innerHTML = user.sdg_interests
                .map(sdg => `<span class="sdg-badge">SDG ${sdg}</span>`)
                .join('');
        } else {
            sdgBadges.innerHTML = '<span style="color: #64748b;">No SDG interests selected</span>';
        }
        
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

// Load dashboard statistics
async function loadDashboardStats() {
    try {
        // Load digital twins count
        const twinsResponse = await authFetch(`${API_BASE}/digital-twins`);
        if (twinsResponse) {
            const twins = await twinsResponse.json();
            document.getElementById('twinCount').textContent = twins.length;
        }
        
        // Load projects count
        const projectsResponse = await authFetch(`${API_BASE}/projects`);
        if (projectsResponse) {
            const projects = await projectsResponse.json();
            document.getElementById('projectCount').textContent = projects.length;
        }
        
        // For simulations, we'd need to add an endpoint or filter
        // For now, show placeholder
        document.getElementById('simCount').textContent = '0';
        document.getElementById('impactCount').textContent = '0';
        
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

// Toggle user menu
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-menu')) {
        document.getElementById('userDropdown').classList.remove('show');
    }
});

// Show notifications (placeholder)
function showNotifications() {
    alert('Notifications feature coming soon!');
}
