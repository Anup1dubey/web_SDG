// API Configuration
// This will automatically detect the environment and use the correct API URL

// Try to get API_URL from window.ENV (set by build process)
// Otherwise, detect based on current hostname
function getApiUrl() {
    // If API_URL is explicitly set in environment
    if (window.ENV && window.ENV.API_URL) {
        return window.ENV.API_URL;
    }
    
    // Detect environment based on hostname
    const hostname = window.location.hostname;
    
    // Production on Render
    if (hostname.includes('onrender.com')) {
        // Replace 'frontend' with 'backend' in the URL
        return window.location.origin.replace('frontend', 'backend');
    }
    
    // Production (custom domain) - adjust this based on your setup
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
        // Assume backend is at /api or subdomain
        return window.location.origin;
    }
    
    // Local development
    return 'http://localhost:8000';
}

const API_BASE = getApiUrl();

console.log('API Base URL:', API_BASE);
