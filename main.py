import jwt
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/validate/{jwt_token}")
async def validate(jwt_token):
    response = requests.get("http://localhost:8080/realms/master/").json()
    public_key = response['public_key']

    try:
        decoded_payload = jwt.decode(
            jwt_token,
            '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----',
            algorithms=["RS256"],
            audience="account"
        )
        print(decoded_payload)
        return decoded_payload
    except:
        raise HTTPException(status_code=403, detail="Error")


@app.get("/journal/")
async def journal():
    return {"Response": "It`s work"}


@app.get("/control/")
async def control():
    return {"Response": "It`s work"}
