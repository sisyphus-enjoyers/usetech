from typing import Union
from fastapi import FastAPI, Request, HTTPException
import jwt
from pydantic import BaseModel
from config import ALGORITHM, KEYCLOACK_SERVER

import requests


app = FastAPI()

# async def request(client):
#     response = await client.get("https://{KEYCLOCK_SERVER}/auth/realms/master")
#     return response.text


# @app.get('/')
# async def main():
#     request = requests.get('https://localhost:8080/realms/master/protocol/openid-connect/certs')
#     # rsa_public_key = request['access_token']

#     # print(rsa_public_key)
#     print(request)


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
        raise HTTPException(status_code=403, detail="Error blyat")


@app.get("/journal/")
async def journal():
    return {"Response": "It`s work"}


@app.get("/control/")
async def control():
    return {"Response": "It`s work"}
