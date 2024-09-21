import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Load JWT_SECRET from environment variables and ensure it's a string
JWT_SECRET = str(os.getenv("JWT_SECRET"))  # Fallback in case JWT_SECRET is missing
JWT_ALGORITHM = "HS256"

# Function to generate a JWT that expires in 5 days
def generate_jwt():
    expiration = datetime.utcnow() + timedelta(days=365)  # Set expiration for 5 days
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45,
        "exp": expiration.timestamp(),  # Expiration time
        "iat": datetime.utcnow().timestamp()  # Issued at time
    }
    
    # Generate the JWT
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Generate a JWT
token = generate_jwt()

# Print the token
print("Generated JWT:", token)
