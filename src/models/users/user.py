import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        THis method verifies that an email, password combo is valid or not
        Checks if email exists, and PW associated with email correct
        :param email: The user's email
        :param password: A sha512 hashed pw
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is None:
            # Tell user email doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist!")
        if not Utils.check_hashed_password(password, user_data["password"]):
            raise UserErrors.IncorrectPasswordError("Your password was wrong")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This will register the user
        :param email: string, might be invalid
        :param password: sha512 hash (string)
        :return: True (User registered) False (User does already exist)
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("User already exists!")

        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("Email is invalid!")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, [self.json()])

    @classmethod
    def find_by_email(cls, email):
        user = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user is not None:
            return cls(**user)

    def json(self):
        return {"_id": self._id,
                "email": self.email,
                "password": self.password}


if __name__ == "__main__":

    # Create user DB
    Database.delete_table(UserConstants.COLLECTION)
    Database.create_table(UserConstants.COLLECTION, {"_id": "INTEGER PRIMARY KEY AUTOINCREMENT", "email": "TEXT", "password": "TEXT"})

    user = User("test@text.com", "123")
    user.save_to_db()
