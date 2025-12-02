from dj_rest_auth.serializers import LoginSerializer

from allauth.account import app_settings as allauth_settings


class PatitasLoginSerializer(LoginSerializer):

    def get_auth_user_using_allauth(self, username, email, password):
        login_methods = set(allauth_settings.LOGIN_METHODS)

        # Login solo por email
        if login_methods == {"email"}:
            return self._validate_email(email, password)

        # Login solo por username
        if login_methods == {"username"}:
            return self._validate_username(username, password)

        # Login híbrido (username OR email)
        return self._validate_username_email(username, email, password)
