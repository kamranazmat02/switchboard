"""Switchboard app entrypoint

Receives Twilio voice webhooks and respond with TwiML.
For now: a stateless 'hello work' greeter.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Response, HTTPException, Request
from twilio.request_validator import RequestValidator

load_dotenv()

app = FastAPI(title="Switchboard", version="0.1.0")
_validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

async def _verify_twilio_signature(request: Request) -> None:
    """Reject requests that don't have a valid Twilio HMAC signature.
    
    Twilio signs each webhook with SHA1-HMAC over the full URL and POST body, keyed by our auth token.
    If a signature doesn't match, the request didn't come from Twilio (or the auth token is out of sync).
    """

    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    form = await request.form()
    params = dict(form)

    if not _validator.validate(url, params, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio Signature")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.post("/voice/incoming")
async def voice_incoming(request: Request) -> Response:
    """Twilio hits this when the number is called.
    
    Verifies the Twilio signature, then returns TwiML instructing Twilio
    to speak a greeting and hang up.
    """

    await _verify_twilio_signature(request)
    twiml = """<Response>
        <Say voice="Polly.Amy" language="en-GB">Hello from Switchboard.</Say>
        <Hangup/>
    </Response>"""

    return Response(content=twiml, media_type="application/xml")
 
