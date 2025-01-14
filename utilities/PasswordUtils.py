import bcrypt

class PasswordUtils:
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    @staticmethod
    def check_password(password, hashed_password):
        """Check a password against its hash."""
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')  # Convert string to bytes
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)