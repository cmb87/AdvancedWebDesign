import re
from passlib.hash import pbkdf2_sha512

class Utils(object):


    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512-> pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Check thats the PW user send matches the one in the database
        DB PW is encrypted more than the user's password at this stage
        :param password:
        :param hashed_password: pbkdf2_sha512 encrypted PW
        :return: True (PW match), False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        pat = re.compile(r'^.+@.+\..+$')
        return True if pat.match(email) else False