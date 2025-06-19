from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# CORS middleware to allow access from any frontend (optional: restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmailRequest(BaseModel):
    product: str
    audience: str
    tone: str
    cta: str

@app.post("/generate")
def generate_email(req: EmailRequest):
    prompt = f"""Write a cold email for:
Product: {req.product}
Target Audience: {req.audience}
Tone: {req.tone}
CTA: {req.cta}
Keep it short and engaging."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # or gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return {"email": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}