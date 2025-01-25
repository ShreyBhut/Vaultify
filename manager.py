from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.keyloaded = False

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        self.keyloaded = True

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
        self.keyloaded = True

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        # Create/empty the file
        with open(path, 'w'):
            pass
        if initial_values is not None:
            for site in initial_values:
                self.add_password(site, initial_values[site])

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    site, encrypted = line.split(":", maxsplit=1)
                    try:
                        decrypted = Fernet(self.key).decrypt(encrypted.encode()).decode()
                        self.password_dict[site] = decrypted
                    except Exception as e:
                        print(f"Error decrypting password for {site}: {e}")

    def add_password(self, site, password):
        if site in self.password_dict:
            print(f"Warning: A password for the site '{site}' already exists. Use update instead.")
            return False 
        self.password_dict[site] = password
        self._rewrite_file()
        return True 

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")

    def update_password(self, site, new_password):
        if site not in self.password_dict:
            print(f"No password exists for {site}.")
            return False
        self.password_dict[site] = new_password
        self._rewrite_file()
        return True

    def delete_password(self, site):
        if site in self.password_dict:
            del self.password_dict[site]
            self._rewrite_file()
            return True
        else:
            print(f"No password exists for {site}.")
            return False

    def _rewrite_file(self):
        """Rewrites the entire password file with current data."""
        if self.password_file is None:
            return
        with open(self.password_file, 'w') as f:
            for site, password in self.password_dict.items():
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def validate_strength(self, password):
        #   A strong password should:
        #1)Be longer than 8 characters
        #2)Contain at least one special character !@#$%^&*
        #3)Have both uppercase and lowercase letters
        #4)Contain at least one number
        special_chars = '!@#$%^&*'
        has_good_length = len(password) > 8
        has_special_char = any(ch in special_chars for ch in password)
        has_numeric_characters = any(ch.isdigit() for ch in password)
        has_capital_letters = any(ch.isupper() for ch in password)
        has_small_letters = any(ch.islower() for ch in password)
        return (has_good_length and has_special_char and
                has_numeric_characters and has_capital_letters and has_small_letters)


