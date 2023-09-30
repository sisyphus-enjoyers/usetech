import requests
from fastapi import FastAPI, HTTPException, Header
from jose import jwt

app = FastAPI()


@app.get("/")
async def validate(authorization: str = Header(None)):
    if authorization is None:
        return {"error": "Authorization header is missing"}

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return {"error": "Invalid Authorization header format"}

    token = parts[1]

    response = requests.get("http://localhost:8080/realms/master/").json()
    public_key = response['public_key']

    try:
        jwt.decode(
            token,
            '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----',
            algorithms=["RS256"],
            audience="account"
        )
        return
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid credentials")
