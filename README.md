# 🔐 Vaultify - Password Managing Chrome Extension

Vaultify is a password managing Chrome extension. Vaultify encrypts and stores your passwords with the power of AES-128-CBC encryption. Vaultify can also auto-detect the login page of a website and provide you with its password. Vaultify works on any Chromium-based browser.

## 🛠 Setting up Vaultify

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/ShreyBhut/Vaultify.git
    ```

2. **Install Backend Dependencies:**
    ```sh
    pip install Flask bcrypt cryptography
    ```

3. **Load the Extension in Your Browser:**
    1. Open your Chromium-based browser and go to `chrome://extensions/`.
    2. Enable "Developer mode" by clicking the toggle switch in the top right corner.
    3. Click "Load unpacked" and select the folder named `my_extension`.
    4. Pin Vaultify to the toolbar to make it easier to access.

## 🚀 Using Vaultify

1. **Run the Server:**
    ```sh
    python app.py
    ```
    This starts the server on [http://localhost:5678](http://localhost:5678), which handles encryption and decryption requests. (You can change the port in `app.py` if needed.)

2. **Login into Vaultify:**

    Enter the master password to access the password manager.  
    You can change the master password by using the update master password button.  
    *(Initial master password = MasterPasswordVaultify)*

3. **Managing Passwords:**

    After logging into Vaultify, you can:
    1. Add a password for a new site
    2. Update a password for an existing site
    3. View the password of an existing site

4. **Auto-Detecting Websites:**

    Visit any website's sign-in/sign-up page and then click on the Vaultify logo . 

    <img src="https://github.com/user-attachments/assets/f81e20ae-a7b7-48f9-b280-76a42ebea8a3" alt="pslogo" width="100"> 

    It will automatically detect the website.  
    *(If the website is not detected upon opening the sign-in/sign-up page, refresh the page and click on the Vaultify logo again.)*

    <img src="https://github.com/user-attachments/assets/34b96f2b-c0c7-4b15-a415-47dadbc480ca" alt="Screenshot 2025-01-26 070228" width="250">

    After the website is detected, enter the master password of the password manager. After verifying the master password, the password for that website will be fetched from the password manager, and an option to copy the password to the clipboard will appear.

    <img src="https://github.com/user-attachments/assets/ea6bbf02-18e9-4aaf-8f9d-2c2ff86130d3" alt= "Screenshot 2025-01-26 070429" width="250">

## 🌟 Vaultify in the Working

<img src="https://github.com/user-attachments/assets/4de8ddd4-e9f1-46a4-8720-0b1d7802a408" alt= "Screenshot 2025-01-26 072200" width="750">

<br>

<img src="https://github.com/user-attachments/assets/305923f6-0675-4909-820c-773bc71a6e08" alt= "Screenshot 2025-01-26 072030" width="750">

<br>

<img src="https://github.com/user-attachments/assets/b2abbe36-535f-4c26-9663-701c56de55e7" alt= "Screenshot 2025-01-27 000824" width="750">

<br>

<img src="https://github.com/user-attachments/assets/08d71406-ebff-49d7-8597-e7f06694a0e2" alt= "Screenshot 2025-01-26 072555" width="750">

<br>

<img src="https://github.com/user-attachments/assets/c39c3656-cf67-4608-9931-0de27460f631" alt= "Screenshot 2025-01-26 072742" width="750">
