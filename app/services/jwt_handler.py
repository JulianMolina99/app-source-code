import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants for JWT
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

# Ensure JWT_SECRET is set in environment variables
if not JWT_SECRET:
    raise ValueError("JWT_SECRET is not set in environment variables")

def verify_jwt(token: str):
    """Verifies and decodes a JWT token.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: Decoded token payload if valid.
        None: If the token is expired or invalid.
    """
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Extract expiration timestamp and convert to datetime
        exp_timestamp = decoded_token.get('exp')
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp) if exp_timestamp else None

        # Check if the token has expired
        if exp_datetime and exp_datetime < datetime.utcnow():
            print("Token expired")
            return None

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
