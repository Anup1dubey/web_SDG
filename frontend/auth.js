// Shared authentication utilities

// API_BASE is now defined in config.js
// This file should be loaded after config.js

// Check if user is authenticated
function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return token !== null;
}

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Logout
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'landing.html';
}

// Get auth headers
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// Protected fetch with auth
async function authFetch(url, options = {}) {
    const headers = {
        ...getAuthHeaders(),
        ...(options.headers || {})
    };
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    // If unauthorized, redirect to login
    if (response.status === 401) {
        logout();
        return null;
    }
    
    return response;
}

// Protect page (redirect to login if not authenticated)
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}
