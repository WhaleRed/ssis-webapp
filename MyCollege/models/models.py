from MyCollege.supabase import get_db
from flask_login import UserMixin
import hashlib


class Users(UserMixin):

    def __init__(self, id=None, username=None, password=None, email=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def add(self):
        db = get_db()
        password_hash = hashlib.md5(self.password.encode()).hexdigest()

        db.table("users").insert({
            "username": self.username,
            "user_password": password_hash,
            "email": self.email
        }).execute()

    @classmethod
    def all(cls):
        db = get_db()
        response = db.table("users").select("*").execute()
        users = []
        for row in response.data:
            users.append(cls(
                id=row.get("id"),
                username=row.get("username"),
                email=row.get("email"),
                password=row.get("user_password")
            ))
        return users

    @classmethod
    def delete(cls, id):
        try:
            db = get_db()
            db.table("users").delete().eq("id", id).execute()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    @classmethod
    def update(cls, user_id, username, email, password=None):
        try:
            db = get_db()
            data = {"username": username, "email": email}
            if password:
                password_hash = hashlib.md5(password.encode()).hexdigest()
                data["user_password"] = password_hash

            db.table("users").update(data).eq("id", user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @classmethod
    def get_by_id(cls, user_id):
        db = get_db()
        response = db.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            row = response.data[0]
            return cls(
                id=row.get("id"),
                username=row.get("username"),
                email=row.get("email"),
                password=row.get("user_password")
            )
        return None

    @classmethod
    def get_by_username(cls, username):
        db = get_db()
        response = db.table("users").select("*").eq("username", username).execute()
        if response.data:
            row = response.data[0]
            return cls(
                id=row.get("id"),
                username=row.get("username"),
                email=row.get("email"),
                password=row.get("user_password")
            )
        return None

    def check_password(self, password):
        password_hash = hashlib.md5(password.encode()).hexdigest()
        return self.password == password_hash

    def get_id(self):
        return str(self.id)
