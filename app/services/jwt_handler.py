import jwt
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Load JWT_SECRET from environment variables
JWT_SECRET = str(os.getenv("JWT_SECRET"))
JWT_ALGORITHM = "HS256"

def verify_jwt(token: str):
    """Verifies and decodes a JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: Decoded token payload if valid.
        None: If the token is expired or invalid.
    """
    try:
        # Decode the JWT token, allowing a small leeway for clock skew
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], leeway=5)

        # Return the decoded token if valid
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None