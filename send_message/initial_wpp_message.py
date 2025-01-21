import json
from dotenv import load_dotenv
import os
import requests

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")


# --------------------------------------------------------------
# Send a custom text WhatsApp message
# --------------------------------------------------------------

def send_whatsapp_message(recipient):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {"name": "bienvenida_v2", "language": {"code": "es_AR"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Call the function
#recipient = '5491149276686'
#recipient = '5491167270236'
#response = send_whatsapp_message(recipient)
#print(response)
#print(response.status_code)
#print(response.json())
#response = response.json()
#wa_id = response["contacts"][0]["wa_id"]
#msg_id = response["messages"][0]["id"]

#message_body = "¡Hola! Soy Frisbee, tu asistente para hacer las compras del supermercado. ¿En qué puedo ayudarte hoy?"

#from db import save_message
#save_message(wa_id, "assistant", message_body, "")
