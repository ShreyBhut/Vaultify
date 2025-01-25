(() => {
    // Checks for password field immediately after DOM loads
    document.addEventListener('DOMContentLoaded', () => {
      detectPasswordField();
    });
  
    //observes changes in the DOM for dynamically added password fields (for eg: facebook)
    const observer = new MutationObserver(mutations => {
      // If password field appears-->sends domain,stop observing.
      if (document.querySelector('input[type="password"]')) {
        sendDomainToBackground();
        observer.disconnect();
      }
    });
  
    // Observe the entire document for added/removed child elements
    observer.observe(document.documentElement, { childList: true, subtree: true });
  
    // Password field check.
    function detectPasswordField() {
      const passwordFields = document.querySelectorAll('input[type="password"]');
      if (passwordFields.length > 0) {
        sendDomainToBackground();
        observer.disconnect();
      }
    }
  
    // send domain info to background script
    function sendDomainToBackground() {
      // normalizes domain
      let domain = window.location.hostname.toLowerCase().replace(/^www\./, '');
      console.log("Detected password field on domain:", domain);
  
      chrome.runtime.sendMessage({
        action: 'LOGIN_PAGE_DETECTED',
        domain
      });
    }
  })();


  
  