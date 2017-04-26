from passlib.hash import pbkdf2_sha512

from oauth2utils import NebriOSModel


class Oauth2User(NebriOSModel):

    kind = 'oauth2user'

    def __init__(self, username=None, **kwargs):
        super(Oauth2User, self).__init__(**kwargs)
        if username is not None:
            self.username = username

    def set_password(self, password):
        self.password = pbkdf2_sha512.encrypt(password)

    def validate_password(self, password):
        return pbkdf2_sha512.verify(password, self.password)

    def save(self):
        if self.username is None:
            raise Exception('Invalid username')
        if self.password is None:
            raise Exception('Invalid password')
        super(Oauth2User, self).save()


class Oauth2Client(NebriOSModel):

    kind = 'oauth2client'

    def __init__(self, client_key=None, user=None, **kwargs):
        super(Oauth2Client, self).__init__(**kwargs)
        if client_key is not None:
            self.client_id = client_key

    @property
    def user(self):
        return self.__get_reference__(Oauth2User, 'user_id')

    @user.setter
    def set_user(self, value):
        return self.__set_reference__(value, 'user_id')

    def save(self):
        if self.client_id is None:
            raise Exception('Invalid client_id')
        if self.user is None:
            raise Exception('Invalid user')
        super(Oauth2Client, self).save()