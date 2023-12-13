from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivatonTokenCenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
        
        # return super()._make_hash_value(user, timestamp)
accout_actvation_token=AccountActivatonTokenCenerator()