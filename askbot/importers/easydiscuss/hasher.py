import hashlib

from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import MD5PasswordHasher

class EasyDiscussMD5PasswordHasher(MD5PasswordHasher):
    algorithm = "ed-md5"

    def encode(self, password, salt):
        assert password
        assert salt and '$' not in salt
        hash = hashlib.md5(force_bytes(password + salt)).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)
