from passlib.hash import bcrypt

class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password
        self.mfa_secret = None
        self.mfa_enabled = False

    @staticmethod
    def create(username, password):
        return User(username, bcrypt.hash(password))

db_users = {}
