"""Switchboard app entrypoint

Receives Twilio voice webhooks and respond with TwiML.
For now: a stateless 'hello work' greeter.
"""

from fastapi import FastAPI, Response

app = FastAPI(title="Switchboard", version="0.1.0")

@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. Twilio doesn't hit this; monitoring tools will later"""
    return {"status": "ok"}


@app.post("/voice/incoming")
def voice_incominng() -> Response:
    """Twilio hits this when the number is called.
    
    Returns TwiML: XML instructions telling Twilio what to do with the call.
    <Say> speak text via Twilio's built-in TLS.
    <Hangup> end the call cleanly.
    """

    twiml = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="Polly.Aoife-Neural" language="en-IE"">Hello from Switchboard.</Say>
        <Hangup/>
    </Response>
    """

    return Response(content=twiml, media_type="application/xml")
 
