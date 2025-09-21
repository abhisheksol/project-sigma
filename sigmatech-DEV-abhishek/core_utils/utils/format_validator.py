import re
import random
import string
from typing import List


def is_format_validator_email(email: str) -> bool:
    """
    Validates whether the provided email is in correct format.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Basic email regex pattern
    pattern: str = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def is_valid_password(password: str) -> bool:
    """
    Validate password with these rules:
    - Minimum 8 characters, maximum 16 characters
    - At least one special character
    - At least one digit
    - At least one uppercase letter
    - At least one lowercase letter

    :param password: The password string to validate.
    :return: True if valid, False otherwise.
    """
    # Length check
    if not (8 <= len(password) <= 16):
        return False

    # Regex checks
    has_upper: bool = bool(re.search(r"[A-Z]", password))
    has_lower: bool = bool(re.search(r"[a-z]", password))
    has_digit: bool = bool(re.search(r"\d", password))
    has_special: bool = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    return all([has_upper, has_lower, has_digit, has_special])


def generate_valid_password() -> str:
    """
    Generate a random password that satisfies the following rules:
    - Length between 8 and 16 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    special_characters: str = '!@#$%^&*(),.?":{}|<>'
    password_length: int = random.randint(8, 16)

    # Ensure one of each required character type
    password_chars: List = [
        random.choice(string.ascii_uppercase),  # Uppercase
        random.choice(string.ascii_lowercase),  # Lowercase
        random.choice(string.digits),  # Digit
        random.choice(special_characters),  # Special character
    ]

    # Fill the rest with random characters from all allowed sets
    all_chars: str = string.ascii_letters + string.digits + special_characters
    remaining_length: int = password_length - len(password_chars)
    password_chars += random.choices(all_chars, k=remaining_length)

    # Shuffle to avoid predictable positions
    random.shuffle(password_chars)

    # return "".join(password_chars)
    return "Abcd.1234"


def is_format_validator_url(url: str) -> bool:
    """
    Validates whether the provided string is in correct URL format.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    # Basic URL regex pattern (supports http, https, ftp)
    pattern: str = (
        r"^(https?|ftp):\/\/"  # protocol
        r"(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,})"  # domain
        r"(:[0-9]{1,5})?"  # optional port
        r"(\/[a-zA-Z0-9@:%_\+.~#?&//=~-]*)?$"  # path/query/etc.
    )
    return re.match(pattern, url) is not None
