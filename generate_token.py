import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Load JWT_SECRET from environment variables
JWT_SECRET = str(os.getenv("JWT_SECRET"))
JWT_ALGORITHM = "HS256"

# Function to generate a JWT that expires
def generate_jwt():
    expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=30)  # Expiration in x time
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45,
        "exp": int(expiration.timestamp()),  # Use integer for 'exp' in UTC
        "iat": int(datetime.now(tz=timezone.utc).timestamp())  # Use integer for 'iat' in UTC
    }
    
    # Generate the JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Generate a JWT
token = generate_jwt()

# Print the token
print("Generated JWT:", token)