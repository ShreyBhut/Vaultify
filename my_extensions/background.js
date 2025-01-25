// Listens for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'LOGIN_PAGE_DETECTED') {
      const domain = message.domain;
      chrome.storage.local.set({ currentDomain: domain }, () => {
        console.log('Stored domain:', domain);
      });
    }
  });
  