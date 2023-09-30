from fastapi import FastAPI
import jwt

app = FastAPI()
secret_key = "c7ffd516db32a361859d3cc340b0301fb1a3c8e772f772b0889b837b2d70343c225fb7e374579e0545288b14a19df1e06f2418cf121a4a0d3edba63e19a1b110"
algorithm = "RS256"


@app.get("/new-token")
async def root():
    token = jwt.encode({"message": "Hello World"}, secret_key, algorithm=algorithm)
    return token


@app.get("/validate/{token}")
async def say_hello(token: str):
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded_payload
    except:
        return {"message": "Invalid token"}
