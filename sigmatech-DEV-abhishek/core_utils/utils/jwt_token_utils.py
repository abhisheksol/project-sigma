import jwt
import datetime
import logging
from core.settings import logger, SECRET_KEY

from typing import Dict, Union

logger = logging.LoggerAdapter(logger, {"app_name": __name__})


class JwtTokenUtils:
    jwt_token: str

    def __init__(self, jwt_token: str):
        self.jwt_token = jwt_token

    def decrypt_jwt_token(self) -> Dict:
        """
        This method will decode the JWT token and return its payload without verifying its signature.
        """
        try:

            decoded_token: Dict = jwt.decode(
                self.jwt_token, SECRET_KEY, algorithms=["HS256"]
            )

            return decoded_token
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return {}
        except jwt.DecodeError:
            logger.error("Invalid token")
            return {}
        except Exception as e:
            logger.error(f"An error occurred while decoding the token: {e}")
            return {}

    def is_token_expired(self) -> bool:
        """
        This method checks if the JWT token is expired.
        Returns True if expired, False otherwise.
        """
        try:
            # Decode the token to get the payload and check its expiration
            decoded_token = self.decrypt_jwt_token()
            exp_timestamp = decoded_token.get("exp")

            if exp_timestamp is None:
                logger.error("Token does not contain an expiration date.")

            # Use timezone-aware datetime objects
            expiration_time: datetime.datetime = datetime.datetime.fromtimestamp(
                exp_timestamp, tz=datetime.timezone.utc
            )
            current_time: datetime.datetime = datetime.datetime.now(
                datetime.timezone.utc
            )
            return current_time > expiration_time

        except jwt.ExpiredSignatureError:
            return True
        except jwt.DecodeError:
            logger.error("Invalid token")
            return True
        except Exception as e:
            logger.error(f"An error occurred while checking expiration: {e}")
            return True


def encode_jwt(user_id: str) -> str:
    """
    Generates a JWT token for the given user ID.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        str: The encoded JWT token.
    """
    payload: Dict = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
    }
    token: bytes = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token if isinstance(token, str) else token.decode()


def decode_jwt(token: str) -> Union[str, dict]:
    """
    Decodes a given JWT token and returns the payload.

    Args:
        token (str): The JWT token to be decoded.

    Returns:
        Union[str, dict]: Returns the decoded payload if successful,
                          otherwise returns an error message.
    """
    try:
        payload: Dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {
            "title": "Authentication Failed",
            "description": "Password reset link has expired.",
            "is_error": True,
        }
    except jwt.InvalidTokenError:
        return {
            "title": "Authentication Failed",
            "description": "Unable to verify the user, please try again.",
            "is_error": True,
        }
    except Exception as e:
        logger.info(f"Error while decoding the token -> {str(e)}")
        return {
            "title": "Something went wrong",
            "description": "Internal Server Error",
            "is_error": True,
        }
