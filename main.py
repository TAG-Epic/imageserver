from itsdangerous import URLSafeTimedSerializer
from os import environ as env
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from aiohttp import ClientSession

signer = URLSafeTimedSerializer(env["ROOT_KEY"])
session = ClientSession()
app = FastAPI()

allowed_tokens = env["ALLOWED_TOKENS"].split(",")
use_https = env["USE_HTTPS"] == "true"
protocol = "https" if use_https else "http"
url_prefix = env.get("URL_PREFIX", "")

@app.get("/{code}.png")
async def get_image(code: str):
    # Parse image id
    code = code.replace("0000", ".")
    try:
        image_id = signer.loads(code, max_age=60*60*24*30)
    except:
        return JSONResponse({"error": "Image codes must be signed by the root key"}, 400)

    # Download image
    parsed_url = "https://siasky.net/" + image_id
    r = await session.get(parsed_url)
    if r.status != 200:
        return JSONResponse({"error": "Internal server error"}, 500)

    # Deliver to client
    data = await r.read()
    return Response(content=data, headers={"Content-Type": "image/png"})

@app.post("/api/upload")
def upload_image(request: Request, image_id: str):
    # Token
    auth_token = request.headers.get("Authorization")
    if auth_token not in allowed_tokens:
        return JSONResponse({"error": "Unauthorized"}, 403)

    # Signing
    image_code = signer.dumps(image_id)
    image_code = image_code.replace(".", "0000")

    # Output
    origin = request.headers["Host"]
    url = f"{protocol}://{origin}/{url_prefix}/{image_code}.png"
    return {"image": url}
