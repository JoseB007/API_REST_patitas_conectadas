from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.jwt_auth import (
    set_jwt_access_cookie,
    set_jwt_refresh_cookie
)


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Tokens creados en RegisterView.perform_create()
        access = response.data.get("access")
        refresh = response.data.get("refresh")


        # === 1. Colocar tokens en cookies seguras ===
        if access:
            set_jwt_access_cookie(response, access)

        if refresh:
            set_jwt_refresh_cookie(response, refresh)

        # === 2. No devolver tokens en JSON ===
        data = response.data
        data.pop("access", None)
        data.pop("refresh", None)

        return response