from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

from rest_framework import serializers

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


class PatitasRegisterSerializer(RegisterSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        signup_fields = allauth_settings.SIGNUP_FIELDS
        dynamic_fields = {}

        for field in signup_fields:
            required = field.endswith('*')
            clean_name = field.replace('*', '')

            if clean_name == "username":
                dynamic_fields["username"] = serializers.CharField(
                    required=required,
                    allow_blank=not required,
                )
            elif clean_name == "email":
                dynamic_fields["email"] = serializers.EmailField(
                    required=required,
                )
            elif clean_name == "password1":
                dynamic_fields["password1"] = serializers.CharField(
                    write_only=True,
                    required=required,
                )
            elif clean_name == "password2":
                dynamic_fields["password2"] = serializers.CharField(
                    write_only=True,
                    required=required,
                )
            else:
                # Campos extra en tu modelo
                dynamic_fields[clean_name] = serializers.CharField(
                    required=required,
                )

        # Limpiar los campos
        self.fields.clear()
        
        for name, field in dynamic_fields.items():
            self.fields[name] = field

    def get_cleaned_data(self):
        return {
            field: self.validated_data.get(field, '')
            for field in self.fields
        }

