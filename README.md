# FastAPI Application Documentation

This is a **FastAPI** app that exposes a secure endpoint `/DevOps`. The app uses both an API Key and JWT (JSON Web Token) for authentication to ensure only authorized requests can access the service. Additionally, the app includes proper error handling and validation to manage different types of requests.

---

## Key Features

### 1. Main Endpoint: `/DevOps` (HTTP POST)

This is the main endpoint of the app. It listens for POST requests and expects certain headers and a JSON body.

- **Headers**:
  - `X-Parse-REST-API-Key`: This is the API key used to authenticate the request.
  - `X-JWT-KWY`: This is the JWT token that gets verified to ensure it’s valid.

- **JSON Payload**: The body of the request should include the following fields:
  ```json
  {
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45
  }
  ```

- **Response**: If the API key and JWT are valid, and the payload is complete, you’ll get this response:
  ```json
  {
    "message": "Hello Juan Perez your message will be send"
  }
  ```

- **Error Handling**:

  - If the API key or JWT is invalid, the server will return a 401 Unauthorized error.
  - If the payload is incomplete (i.e., missing fields), the server will return a 400 Bad Request error with the message "Incomplete payload."

### 2. Security: API Key & JWT Authentication

The app ensures only authorized users can interact with it through two layers of security:

- **API Key**: The app checks the API key (stored in the .env file) to ensure it’s correct.
- **JWT Token**: The JWT token is validated using the verify_jwt function. If the token is expired or invalid, the app will reject the request with a 401 Unauthorized error.

### 3. Custom Error Handling

The app has custom error handling for certain cases:

404 Not Found: If you try to access a route that doesn’t exist, the app returns:
```json

{
  "message": "ERROR"
}
```
405 Method Not Allowed: If you try to use an HTTP method other than POST (like GET, PUT, DELETE) on the /DevOps endpoint, the app will return a 405 Method Not Allowed error with the message:
```json

{
  "message": "ERROR"
}
```

### 4. Middleware
The app uses middleware to restrict access to any route that does not start with /DevOps. If a request is made to a different path, it returns a 404 Not Found error with the message:

```json
{
  "message": "ERROR"
}
```

### 5. Testing
The application includes automated tests using pytest:

- **API Key and JWT Validation**: Tests ensure that invalid API keys and JWT tokens return the appropriate 401 Unauthorized errors.
- **Payload Validation**: Tests verify that incomplete payloads return a 400 Bad Request error.
- **Concurrency**: The app is tested for handling multiple concurrent requests using asyncio, ensuring it performs well under load.