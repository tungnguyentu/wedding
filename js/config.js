// Configuration settings for the wedding website

window.WeddingConfig = {
  // API settings
  api: {
    // Base URL for API endpoints - automatically uses appropriate URL for environment
    baseUrl: (function() {
      // Use different base URL based on hostname
      const hostname = window.location.hostname;
      if (hostname === '127.0.0.1' || hostname === 'localhost') {
        return 'http://127.0.0.1:5004'; // Local development with direct API access
      } else {
        return '/api'; // Production - use relative URL for Nginx proxy
      }
    })()
  }
};

console.log('Wedding config loaded, API base URL:', window.WeddingConfig.api.baseUrl);
