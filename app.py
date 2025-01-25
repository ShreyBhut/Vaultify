from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from manager import PasswordManager
import os
import bcrypt 

app = Flask(__name__)
app.secret_key = 'keytosds_flask_shrey_123098' 

pm = PasswordManager()
key_path = 'key.key'
password_file_path = 'passwords.txt'
master_password_path = 'master_password.txt'

# Loads or creates the encryption key
if os.path.exists(key_path):
    pm.load_key(key_path)
else:
    pm.create_key(key_path)

# Loads or creates the password file
if os.path.exists(password_file_path):
    pm.load_password_file(password_file_path)
else:
    pm.create_password_file(password_file_path)

# Ensures the master password file exists
if not os.path.exists(master_password_path):
    with open(master_password_path, 'wb') as f:  
        f.write(b'') 

# gets the hashed master password
def get_hashed_master_password():
    if not os.path.exists(master_password_path):
        return None
    with open(master_password_path, 'rb') as f:  
        return f.read()

# sets the master password by hashing it
def set_master_password(new_password):
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    with open(master_password_path, 'wb') as f:  
        f.write(hashed)

# domain normalization to remove leading "www."
def normalize_domain(domain):
    return domain.replace("www.", "")

@app.route('/', methods=['GET', 'POST'])
def login():
    hashed_master_password = get_hashed_master_password()
    if request.method == 'POST':
        master = request.form.get('master')
        if not hashed_master_password:
            set_master_password(master)
            session['logged_in'] = True
            flash('Master password set successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            if bcrypt.checkpw(master.encode('utf-8'), hashed_master_password):
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid master password.', 'danger')
    return render_template('login.html', master_password_set=bool(hashed_master_password))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    sites = list(pm.password_dict.keys())
    return render_template('dashboard.html', sites=sites)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/reset_master_password', methods=['POST'])
def reset_master_password():
    """
    POST endpoint to reset the master password.
    The user must provide the current (old) master password, the new password,
    and confirm the new password.
    """
    old_master = request.form.get('old_master')
    new_master = request.form.get('new_master')
    confirm_master = request.form.get('confirm_master')
    stored_hashed_master = get_hashed_master_password()

    if not stored_hashed_master:
        flash("No existing master password found. Please set a master password first.", "danger")
        return redirect(url_for('login'))

    if not bcrypt.checkpw(old_master.encode('utf-8'), stored_hashed_master):
        flash("Current master password is incorrect.", "danger")
        return redirect(url_for('dashboard'))

    if not new_master or new_master != confirm_master:
        flash("New master password and confirmation do not match or are empty.", "danger")
        return redirect(url_for('dashboard'))

    # Updates master password
    set_master_password(new_master)
    flash("Master password updated successfully!", "success")
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_site_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        site = request.form.get('site')
        password = request.form.get('password')
        if not site or not password:
            flash("Site and password are required.", "danger")
        else:
            if not pm.validate_strength(password):
                flash("WARNING: This password is weak. The password must be >8 characters and contain a number, lowercase, uppercase, and special character.", "warning")
                return render_template('add_password.html')  
            if pm.add_password(site, password):
                flash(f"Password for {site} added.", "success")
                return redirect(url_for('dashboard'))
            else:
                flash(f"A password for {site} already exists. Use update instead.", "warning")
    return render_template('add_password.html')

@app.route('/update/<site>', methods=['GET', 'POST'])
def update_site_password(site):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    existing_password = pm.get_password(site)
    if existing_password == "Password not found.":
        flash(f"No password exists for {site}.", "danger")
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        new_password = request.form.get('password')
        if not new_password:
            flash("Password cannot be empty.", "danger")
        else:
            if not pm.validate_strength(new_password):
                flash("WARNING: This new password is weak. The password must be >8 characters and contain a number, lowercase, uppercase, and special character.", "warning")
                return render_template('update_password.html', site=site) 
            if pm.update_password(site, new_password):
                flash(f"Password for {site} updated.", "success")
                return redirect(url_for('dashboard'))
            else:
                flash(f"Failed to update password for {site}.", "danger")
    return render_template('update_password.html', site=site)

@app.route('/delete/<site>', methods=['POST'])
def delete_site_password(site):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    result = pm.delete_password(site)
    if result:
        flash(f"Password for {site} deleted.", "success")
    else:
        flash(f"No password exists for {site}.", "danger")
    return redirect(url_for('dashboard'))

@app.route('/get/<site>')
def get_site_password(site):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    password = pm.get_password(site)
    return render_template('get_password.html', site=site, password=password)

@app.route('/api/get_domain_password', methods=['POST'])
def get_domain_password():
    """
    API endpoint called by popup.js to retrieve the site password
    given a domain and the user's master password.
    """
    data = request.json or {}
    domain = data.get('domain', '').strip()
    user_master_password = data.get('master_password', '').strip()

    if not domain or not user_master_password:
        return {"error": "Missing domain or master_password"}, 400

    hashed_master_password = get_hashed_master_password()

    if not hashed_master_password:
        return {"error": "Master password not set."}, 400

    if not bcrypt.checkpw(user_master_password.encode('utf-8'), hashed_master_password):
        return {"error": "Invalid master password"}, 401

    # Normalizes the domain if storing them without "www."
    domain = normalize_domain(domain)

    # Fetch the site password
    site_password = pm.get_password(domain)
    if site_password == "Password not found.":
        return {"error": "Password not found for this domain"}, 404

    return {"password": site_password}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5678)
