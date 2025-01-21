from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from send_message.initial_wpp_message import send_whatsapp_message
from send_message.db import save_message, save_waitlist_user
from fastapi.middleware.cors import CORSMiddleware

import logging
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frizbee.site", # recibe api calls el site en vercel o del local host
        "https://landing-frizbee.vercel.app", # recibe api calls el site en vercel o del local host
        "http://localhost:3000"
    ],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WaitlistRequest(BaseModel):
    email: str
    phone: str

@app.post("/api/waitlist")
async def join_waitlist(data: WaitlistRequest):
    logger.info(f"Received request with data: {data}")

    try:
        save_waitlist_user(data.email, data.phone)

        # Send WhatsApp message
        response = send_whatsapp_message(data.phone)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to send WhatsApp message")
        
        # Parse response and save initial message
        response_data = response.json()
        wa_id = response_data["contacts"][0]["wa_id"]
        message_body = "¡Hola! Soy Frisbee, tu ayudante personal de compras en Jumbo 🛒. Te acompañaré a crear tu carrito ideal, personalizado según tus gustos y necesidades. ¿Comenzamos por conocer tus preferencias de compra?" 
        save_message(wa_id, "assistant", message_body, "")
        
        return {"status": "success", "wa_id": wa_id}
        
    except Exception as e:
        logger.error(f"Error in join_waitlist: {str(e)}")

        raise HTTPException(status_code=500, detail=str(e))

# For testing purposes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}