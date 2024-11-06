from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    EXPIRATION_TIME_MINUTES = 15

    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp) + str(user.is_active))

    def is_token_expired(self, timestamp):
        expiration_time = datetime.fromtimestamp(timestamp) + timedelta(minutes=self.EXPIRATION_TIME_MINUTES)
        return datetime.now() > expiration_time

    def check_token(self, user, token):
        # Überprüft Token und Ablaufzeit gleichzeitig
        timestamp = self._num_seconds(self._now())
        if self.is_token_expired(timestamp):
            return False
        return super().check_token(user, token)

account_activation_token = AccountActivationTokenGenerator()
