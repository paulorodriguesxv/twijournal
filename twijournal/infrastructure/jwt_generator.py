import jwt

def generate_jwt(username):
    message = {
        "sub": "1234567890",
        "name": "John Doe",
        "username": username,
        "iat": 1516239022
    }
    signing_key = 'CLIENT_SECRET'

    token = jwt.encode(message, signing_key, algorithm="HS256")

    return token

if __name__ == "__main__":
    generate_jwt("userb")