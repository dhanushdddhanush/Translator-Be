import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SUBSCRIPTION_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
REGION = os.getenv("AZURE_TRANSLATOR_REGION")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TranslateRequest(BaseModel):
    text: str
    to_language: str
@app.get("/")
def read_root():
    return {"message": "Welcome to the Azure Translator API!"}

@app.post("/translate/")
def translate_text(request: TranslateRequest):
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-Type": "application/json"
    }

    params = {"api-version": "3.0", "to": request.to_language}
    body = [{"text": request.text}]

    response = requests.post(f"{ENDPOINT}/translate", params=params, headers=headers, json=body)

    result = response.json()
    return {"translated_text": result[0]["translations"][0]["text"]}




@app.get("/languages/")
def get_supported_languages():
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Ocp-Apim-Subscription-Region": REGION,
        "Content-Type": "application/json"
    }
    
    params = {"api-version": "3.0"}

    response = requests.get(f"{ENDPOINT}/languages",params=params, headers=headers)

    result = response.json()
    
    
    return {"supported_languages": result}
    # changed my server to this: uvicorn filename:app --reload-8089
