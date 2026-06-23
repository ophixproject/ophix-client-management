import os

TOKEN_WARN_DAYS = int(os.getenv("TOKEN_WARN_DAYS", 30))
TOKEN_REQUIRE_DAYS = int(os.getenv("TOKEN_REQUIRE_DAYS", 90))
TOKEN_LOCKOUT_DAYS = int(os.getenv("TOKEN_LOCKOUT_DAYS", 180))

MIDDLEWARE_INSERT_AFTER = {
    "django.middleware.common.CommonMiddleware": [
        "ophix_client_management.middleware.TokenRotationSignalMiddleware",
    ],
}
