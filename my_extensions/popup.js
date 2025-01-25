document.addEventListener('DOMContentLoaded', async () => {
    const domainText = document.getElementById('domainText');
    const masterPasswordInput = document.getElementById('masterPassword');
    const fetchBtn = document.getElementById('fetchBtn');
    const copyBtn = document.getElementById('copyBtn');
    const responseMessage = document.getElementById('responseMessage');
  
    // Retrieves the domain stored by background.js
    const { currentDomain } = await chrome.storage.local.get('currentDomain');
    if (currentDomain) {
      domainText.textContent = `Website detected : ${currentDomain}`;
    } else {
      domainText.textContent = "No domain detected yet.";
    }
  
    let retrievedPassword = null;
  
    fetchBtn.addEventListener('click', async () => {
      const masterPassword = masterPasswordInput.value.trim();
      if (!currentDomain) {
        responseMessage.textContent = "No domain is stored.";
        return;
      }
      if (!masterPassword) {
        responseMessage.textContent = "Please enter your master password.";
        return;
      }
  
      // post request to flask server
      try {
        const response = await fetch('http://localhost:5678/api/get_domain_password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            domain: currentDomain,
            master_password: masterPassword
          })
        });
        const data = await response.json();
  
        if (!response.ok) {
          responseMessage.textContent = `Error: ${data.error || 'Unknown error'}`;
          copyBtn.classList.add('hidden');
          return;
        }
  
        // holds the site password
        retrievedPassword = data.password;
        responseMessage.textContent = `Password retrieved for ${currentDomain}`;
        copyBtn.classList.remove('hidden');
  
      } catch (error) {
        console.error(error);
        responseMessage.textContent = "Error fetching password from server.";
        copyBtn.classList.add('hidden');
      }
    });
  
    copyBtn.addEventListener('click', () => {
      if (retrievedPassword) {
        navigator.clipboard.writeText(retrievedPassword)
          .then(() => {
            responseMessage.textContent = "Password copied to clipboard!";
          })
          .catch(err => {
            console.error('Clipboard error:', err);
            responseMessage.textContent = "Failed to copy to clipboard.";
          });
      }
    });
  });
  