import re
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


# -----------------------------
#  Email Validator
# -----------------------------
email_validator = EmailValidator(
    message="Enter a valid email address."
)


# -----------------------------
#  Phone Validator
#  Accepts 7–15 digits only
# -----------------------------
phone_validator = RegexValidator(
    regex=r'^[0-9]{7,15}$',
    message="Enter a valid phone number (7–15 digits, numbers only)."
)


# -----------------------------
#  Combined Email OR Phone Validator
# -----------------------------
def email_or_phone_validator(value):
    """
    Validates that the input is either a valid email or a phone number.
    """
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    phone_regex = r"^[0-9]{7,15}$"

    if re.match(email_regex, value):  # valid email
        return value

    if re.match(phone_regex, value):  # valid phone number
        return value

    raise ValidationError(
        "Enter a valid email or phone number."
    )


from django.core.exceptions import ValidationError
import re

def strong_password_validator(password):
    """
    Validate password strength:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    - At least 1 special character
    """

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one digit.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")

    return password
